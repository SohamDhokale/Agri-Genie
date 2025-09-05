from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any

import numpy as np

from .models import Crop


@dataclass
class YieldInput:
    state: str
    farm_size: float
    soil_ph: float
    temperature: float
    rainfall: float


def predict_yield_for_crops(params: YieldInput) -> List[Dict[str, Any]]:
    """Compute expected yield and profit for suitable crops using simple rules.

    Returns a list of dicts: { crop_id, crop_name, expected_yield_tons, expected_profit }.
    """
    suitable_crops = Crop.objects.filter(suitable_states__icontains=params.state)

    predictions: List[Dict[str, Any]] = []
    for crop in suitable_crops:
        temp_center = (crop.min_temperature + crop.max_temperature) / 2.0
        ph_center = (crop.soil_ph_min + crop.soil_ph_max) / 2.0
        rain_center = (crop.min_rainfall + crop.max_rainfall) / 2.0

        # Normalized Gaussian-like suitability by factor
        temp_sigma = max(1.0, (crop.max_temperature - crop.min_temperature) / 2.0)
        ph_sigma = max(0.3, (crop.soil_ph_max - crop.soil_ph_min) / 2.0)
        rain_sigma = max(5.0, (crop.max_rainfall - crop.min_rainfall) / 2.0)

        temp_factor = np.exp(-((params.temperature - temp_center) ** 2) / (2 * temp_sigma ** 2))
        ph_factor = np.exp(-((params.soil_ph - ph_center) ** 2) / (2 * ph_sigma ** 2))
        rain_factor = np.exp(-((params.rainfall - rain_center) ** 2) / (2 * rain_sigma ** 2))

        suitability = float(0.4 * temp_factor + 0.3 * ph_factor + 0.3 * rain_factor)

        base_yield_per_hectare = float(crop.yield_per_hectare)

        # Simple farm-size efficiency curve
        if params.farm_size < 1:
            efficiency = 0.8
        elif params.farm_size < 5:
            efficiency = 0.9
        else:
            efficiency = 1.0

        expected_yield_tons = round(base_yield_per_hectare * suitability * efficiency * params.farm_size, 2)
        expected_revenue = expected_yield_tons * 1000.0 * float(crop.market_price_per_kg)
        expected_profit = round(expected_revenue * 0.65, 2)  # assume 35% costs

        predictions.append({
            "crop_id": crop.id,
            "crop_name": crop.name,
            "expected_yield_tons": expected_yield_tons,
            "expected_profit": expected_profit,
        })

    predictions.sort(key=lambda x: x["expected_profit"], reverse=True)
    return predictions


def optimize_allocation(params: YieldInput, top_k: int = 5) -> Dict[str, Any]:
    """Greedy continuous allocation of farm_size across top_k crops to maximize profit density.

    Returns dict with allocations and totals.
    """
    predictions = predict_yield_for_crops(params)
    candidates = predictions[:top_k]

    # Profit density per hectare approximation: profit for 1 hectare
    densities = []
    for c in candidates:
        # Recompute per-hectare profit by dividing by farm size used in prediction
        per_hectare_profit = c["expected_profit"] / max(params.farm_size, 1e-6)
        densities.append(per_hectare_profit)

    order = np.argsort(-np.array(densities))  # descending

    remaining = params.farm_size
    allocations: List[Dict[str, Any]] = []
    total_expected_yield = 0.0
    total_expected_profit = 0.0

    for idx in order:
        if remaining <= 0:
            break
        crop_info = candidates[int(idx)]
        # Greedy: allocate as much as possible to highest density first
        allocated_hectares = remaining

        # Estimate per-hectare yield and profit from the candidate aggregate by dividing
        per_hectare_yield = crop_info["expected_yield_tons"] / max(params.farm_size, 1e-6)
        per_hectare_profit = crop_info["expected_profit"] / max(params.farm_size, 1e-6)

        yield_added = per_hectare_yield * allocated_hectares
        profit_added = per_hectare_profit * allocated_hectares

        allocations.append({
            "crop_id": crop_info["crop_id"],
            "crop_name": crop_info["crop_name"],
            "hectares": round(float(allocated_hectares), 2),
            "expected_yield_tons": round(float(yield_added), 2),
            "expected_profit": round(float(profit_added), 2),
        })

        remaining = 0
        total_expected_yield += float(yield_added)
        total_expected_profit += float(profit_added)

    return {
        "allocations": allocations,
        "total_expected_yield_tons": round(total_expected_yield, 2),
        "total_expected_profit": round(total_expected_profit, 2),
    }


