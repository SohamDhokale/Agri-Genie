from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Pesticide

# Create your views here.

@login_required
def pesticides_list(request):
    category = request.GET.get('category')
    if category:
        # Get organic pesticides first, then non-organic ones
        organic_pesticides = Pesticide.objects.filter(category=category, is_organic=True)
        non_organic_pesticides = Pesticide.objects.filter(category=category, is_organic=False)
        # Combine the querysets
        pesticides = list(organic_pesticides) + list(non_organic_pesticides)
    else:
        # Get organic pesticides first, then non-organic ones
        organic_pesticides = Pesticide.objects.filter(is_organic=True)
        non_organic_pesticides = Pesticide.objects.filter(is_organic=False)
        # Combine the querysets
        pesticides = list(organic_pesticides) + list(non_organic_pesticides)
    
    categories = Pesticide.CATEGORY_CHOICES
    selected_category = category
    
    context = {
        'pesticides': pesticides,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'pesticides/list.html', context)

@login_required
def pesticide_detail(request, pesticide_id):
    pesticide = get_object_or_404(Pesticide, id=pesticide_id)
    return render(request, 'pesticides/detail.html', {'pesticide': pesticide})
