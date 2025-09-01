from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Crop, CropRecommendation, RecommendedCrop
from .forms import CropRecommendationForm
from .utils import CropRecommendationEngine
import json

@login_required
def crop_recommendation_form(request):
    if request.method == 'POST':
        form = CropRecommendationForm(request.POST)
        if form.is_valid():
            # Manually create CropRecommendation from form data
            recommendation = CropRecommendation.objects.create(
                user=request.user,
                farm_size=1.0,  # Default value, could be added to form
                location=form.cleaned_data.get('state', 'Unknown'),
                state=form.cleaned_data['state'],
                district='Unknown',  # Could be added to form
                soil_ph=form.cleaned_data['ph'],
                temperature=form.cleaned_data['temperature'],
                rainfall=form.cleaned_data['rainfall'],
                nitrogen=form.cleaned_data['nitrogen'],
                phosphorus=form.cleaned_data['phosphorus'],
                potassium=form.cleaned_data['potassium'],
                humidity=form.cleaned_data['humidity']
            )
            
            # Generate recommendations
            engine = CropRecommendationEngine(recommendation)
            recommended_crops = engine.get_recommendations()
            
            # Save recommended crops
            for crop_data in recommended_crops:
                RecommendedCrop.objects.create(
                    recommendation=recommendation,
                    crop=crop_data['crop'],
                    suitability_score=crop_data['score'],
                    expected_yield=crop_data['expected_yield'],
                    expected_profit=crop_data['expected_profit']
                )
            
            messages.success(request, 'Crop recommendations generated successfully!')
            return redirect('crop_recommendation_result', recommendation.id)
    else:
        form = CropRecommendationForm()
    return render(request, 'crops/recommendation_form.html', {'form': form})

@login_required
def crop_recommendation_result(request, recommendation_id):
    try:
        recommendation = CropRecommendation.objects.get(id=recommendation_id, user=request.user)
        recommended_crops = RecommendedCrop.objects.filter(recommendation=recommendation)
        
        # Get price forecasts for each recommended crop
        crops_with_forecasts = []
        for rec_crop in recommended_crops:
            crop = rec_crop.crop
            price_forecasts = crop.price_forecasts.all().order_by('year', 'month')[:6]
            crops_with_forecasts.append({
                'recommendation': rec_crop,
                'forecasts': price_forecasts
            })
        
        return render(request, 'crops/recommendation_result.html', {
            'recommendation': recommendation,
            'recommended_crops': recommended_crops,
            'crops_with_forecasts': crops_with_forecasts
        })
    except CropRecommendation.DoesNotExist:
        messages.error(request, 'Recommendation not found!')
        return redirect('crop_recommendation')

@login_required
def crop_list(request):
    crops = Crop.objects.all().order_by('name')
    return render(request, 'crops/crop_list.html', {'crops': crops})

@login_required
def crop_detail(request, crop_id):
    crop = Crop.objects.get(id=crop_id)
    return render(request, 'crops/crop_detail.html', {'crop': crop})

