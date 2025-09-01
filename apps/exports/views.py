from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from .models import ExportService
import json

@login_required
def exports_list(request):
    exports = ExportService.objects.all()
    
    # Prepare data for chart (export volumes by country)
    # Generate random colors for each country
    import random
    
    # Create a list of visually distinct colors
    colors = [
        'rgba(75, 192, 192, 1)',   # Teal
        'rgba(255, 99, 132, 1)',    # Red
        'rgba(54, 162, 235, 1)',    # Blue
        'rgba(255, 206, 86, 1)',    # Yellow
        'rgba(153, 102, 255, 1)',   # Purple
        'rgba(255, 159, 64, 1)',    # Orange
        'rgba(46, 204, 113, 1)',    # Green
        'rgba(52, 73, 94, 1)'       # Dark Blue
    ]
    
    # Sort exports by volume for better visualization
    sorted_exports = sorted(exports, key=lambda x: x.export_volume, reverse=True)
    
    # Ensure we have data to display
    if not sorted_exports:
        # Create sample data if no exports exist
        create_sample_data(request)
        # Refresh the exports list
        exports = ExportService.objects.all()
        sorted_exports = sorted(exports, key=lambda x: x.export_volume, reverse=True)
    
    # Prepare colors for each country
    background_colors = []
    border_colors = []
    
    for i in range(len(sorted_exports)):
        color_index = i % len(colors)
        border_colors.append(colors[color_index])
        background_colors.append(colors[color_index].replace('1)', '0.6)'))
    
    line_chart_data = {
        'labels': [export.country for export in sorted_exports],
        'datasets': [{
            'label': 'Export Volume (tons)',
            'data': [export.export_volume for export in sorted_exports],
            'borderColor': border_colors,
            'backgroundColor': background_colors,
            'borderWidth': 2,
            'pointRadius': 6,
            'pointHoverRadius': 8,
            'hoverBackgroundColor': border_colors
        }]
    }
    
    context = {
        'exports': exports,
        'line_chart_data': json.dumps(line_chart_data),
    }
    return render(request, 'exports/list.html', context)


@login_required
def export_detail(request, item_id: int):
    item = get_object_or_404(ExportService, id=item_id)
    
    # Prepare data for Venn diagram with improved sizing
    # Scale the values to make the visualization more meaningful
    market_share_size = max(50, int(item.market_share * 150))
    growth_potential_size = max(50, int(item.potential_growth * 150))
    
    # Calculate intersection size based on the relationship between market share and growth potential
    # The intersection should be proportional to both values but not too small
    intersection_size = max(25, int((item.market_share * item.potential_growth) * 200))
    
    # Format percentages for labels
    market_share_pct = int(item.market_share * 100)
    growth_potential_pct = int(item.potential_growth * 100)
    
    venn_data = [
        {'sets': ['Market Share'], 'size': market_share_size, 'label': f'Market Share\n{market_share_pct}%'},
        {'sets': ['Growth Potential'], 'size': growth_potential_size, 'label': f'Growth Potential\n{growth_potential_pct}%'},
        {'sets': ['Market Share', 'Growth Potential'], 'size': intersection_size, 'label': 'Opportunity\nZone'}
    ]
    
    # Get related products (same country)
    related_products = ExportService.objects.filter(country=item.country).exclude(id=item.id)
    
    context = {
        'item': item,
        'venn_data': json.dumps(venn_data),
        'related_products': related_products
    }
    return render(request, 'exports/detail.html', context)


# Add a new view to create initial data for testing
def create_sample_data(request):
    # Only create if no data exists
    if ExportService.objects.count() == 0:
        sample_data = [
            {
                'country': 'United Arab Emirates',
                'product': 'Basmati Rice',
                'demand_level': 'High',
                'notes': 'Strong demand in retail and hospitality sectors.',
                'contact_name': 'Ahmed Al-Mansour',
                'contact_email': 'ahmed@uaeimports.com',
                'contact_phone': '+971-50-123-4567',
                'contact_website': 'https://uaeimports.com',
                'export_volume': 5000,
                'market_share': 0.35,
                'potential_growth': 0.25
            },
            {
                'country': 'United Kingdom',
                'product': 'Mango (Alphonso)',
                'demand_level': 'Medium',
                'notes': 'Seasonal spike during summer; follow phytosanitary norms.',
                'contact_name': 'Emma Thompson',
                'contact_email': 'emma@ukfruits.co.uk',
                'contact_phone': '+44-20-7946-0384',
                'contact_website': 'https://ukfruits.co.uk',
                'export_volume': 2500,
                'market_share': 0.20,
                'potential_growth': 0.15
            },
            {
                'country': 'Netherlands',
                'product': 'Cut Flowers',
                'demand_level': 'High',
                'notes': 'Consider cold-chain logistics for freshness.',
                'contact_name': 'Jan van der Meer',
                'contact_email': 'jan@dutchflowers.nl',
                'contact_phone': '+31-20-123-4567',
                'contact_website': 'https://dutchflowers.nl',
                'export_volume': 8000,
                'market_share': 0.45,
                'potential_growth': 0.30
            },
            {
                'country': 'Singapore',
                'product': 'Spices (Turmeric, Cardamom)',
                'demand_level': 'Medium',
                'notes': 'Prefer organic-certified consignments.',
                'contact_name': 'Li Wei Chen',
                'contact_email': 'liwei@sgspices.com.sg',
                'contact_phone': '+65-6123-4567',
                'contact_website': 'https://sgspices.com.sg',
                'export_volume': 1500,
                'market_share': 0.15,
                'potential_growth': 0.40
            },
            {
                'country': 'Japan',
                'product': 'Organic Tea',
                'demand_level': 'High',
                'notes': 'Strong preference for certified organic products with detailed origin information.',
                'contact_name': 'Takashi Yamamoto',
                'contact_email': 'takashi@japantea.co.jp',
                'contact_phone': '+81-3-1234-5678',
                'contact_website': 'https://japantea.co.jp',
                'export_volume': 3000,
                'market_share': 0.25,
                'potential_growth': 0.35
            },
            {
                'country': 'Germany',
                'product': 'Organic Honey',
                'demand_level': 'Medium',
                'notes': 'Must meet EU organic standards and sustainability certifications.',
                'contact_name': 'Klaus Schmidt',
                'contact_email': 'klaus@deutschehoney.de',
                'contact_phone': '+49-30-1234-5678',
                'contact_website': 'https://deutschehoney.de',
                'export_volume': 1800,
                'market_share': 0.18,
                'potential_growth': 0.22
            },
            {
                'country': 'United States',
                'product': 'Handcrafted Textiles',
                'demand_level': 'Medium',
                'notes': 'Focus on fair trade certification and artisan stories.',
                'contact_name': 'Sarah Johnson',
                'contact_email': 'sarah@usimports.com',
                'contact_phone': '+1-212-555-6789',
                'contact_website': 'https://usimports.com',
                'export_volume': 2200,
                'market_share': 0.12,
                'potential_growth': 0.28
            },
            {
                'country': 'Australia',
                'product': 'Cashew Nuts',
                'demand_level': 'High',
                'notes': 'Strong demand for premium quality, organic preferred.',
                'contact_name': 'Michael Wilson',
                'contact_email': 'michael@ausnuts.com.au',
                'contact_phone': '+61-2-9876-5432',
                'contact_website': 'https://ausnuts.com.au',
                'export_volume': 4500,
                'market_share': 0.30,
                'potential_growth': 0.20
            }
        ]
        
        for data in sample_data:
            ExportService.objects.create(**data)
        
        return JsonResponse({'status': 'success', 'message': 'Sample data created successfully'})
    
    return JsonResponse({'status': 'error', 'message': 'Data already exists'})
