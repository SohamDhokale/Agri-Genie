from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import GovernmentScheme, SchemeApplication
from .forms import SchemeApplicationForm
import json

@login_required
def schemes_list(request):
    category = request.GET.get('category', '')
    schemes = GovernmentScheme.objects.filter(is_active=True)
    
    if category:
        schemes = schemes.filter(category=category)
    
    # Get user's applications for status display
    user_applications = []
    if request.user.is_authenticated:
        applications = SchemeApplication.objects.filter(user=request.user)
        user_applications = [app.scheme.id for app in applications]
    
    categories = GovernmentScheme.CATEGORY_CHOICES
    
    return render(request, 'schemes/list.html', {
        'schemes': schemes,
        'categories': categories,
        'selected_category': category,
        'user_applications': user_applications
    })

@login_required
def scheme_detail(request, scheme_id):
    scheme = get_object_or_404(GovernmentScheme, id=scheme_id, is_active=True)
    
    # Check if user has already applied
    user_application = None
    if request.user.is_authenticated:
        try:
            user_application = SchemeApplication.objects.get(user=request.user, scheme=scheme)
        except SchemeApplication.DoesNotExist:
            pass
    
    return render(request, 'schemes/detail.html', {
        'scheme': scheme,
        'user_application': user_application
    })

@login_required
def apply_scheme(request, scheme_id):
    scheme = get_object_or_404(GovernmentScheme, id=scheme_id, is_active=True)
    
    # Check if user has already applied
    try:
        existing_application = SchemeApplication.objects.get(user=request.user, scheme=scheme)
        messages.warning(request, f'You have already applied for {scheme.name}.')
        return redirect('scheme_detail', scheme_id=scheme_id)
    except SchemeApplication.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = SchemeApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.scheme = scheme
            application.status = 'submitted'
            application.save()
            
            messages.success(request, f'Your application for {scheme.name} has been submitted successfully!')
            return redirect('my_applications')
    else:
        # Pre-fill form with user data
        initial_data = {
            'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'email': request.user.email,
        }
        form = SchemeApplicationForm(initial=initial_data)
    
    return render(request, 'schemes/apply.html', {
        'scheme': scheme,
        'form': form
    })

@login_required
def my_applications(request):
    applications = SchemeApplication.objects.filter(user=request.user).order_by('-application_date')
    
    return render(request, 'schemes/my_applications.html', {
        'applications': applications
    })

@login_required
def application_detail(request, application_id):
    application = get_object_or_404(SchemeApplication, id=application_id, user=request.user)
    
    return render(request, 'schemes/application_detail.html', {
        'application': application
    })

@require_POST
@csrf_exempt
def quick_apply(request, scheme_id):
    """Quick apply functionality via AJAX"""
    try:
        scheme = get_object_or_404(GovernmentScheme, id=scheme_id, is_active=True)
        
        # Check if user has already applied
        if SchemeApplication.objects.filter(user=request.user, scheme=scheme).exists():
            return JsonResponse({
                'success': False,
                'message': 'You have already applied for this scheme.'
            })
        
        # Create a basic application
        application = SchemeApplication.objects.create(
            user=request.user,
            scheme=scheme,
            status='pending',
            full_name=f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            email=request.user.email,
            phone_number='',  # Will be filled later
            address=''  # Will be filled later
        )
        
        return JsonResponse({
            'success': True,
            'message': f'Application started for {scheme.name}. Please complete your details.',
            'application_id': application.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred while processing your application.'
        })

@login_required
def withdraw_application(request, application_id):
    """Withdraw an application"""
    application = get_object_or_404(SchemeApplication, id=application_id, user=request.user)
    
    if application.status in ['pending', 'submitted']:
        application.delete()
        messages.success(request, 'Application withdrawn successfully.')
    else:
        messages.error(request, 'Cannot withdraw application at this stage.')
    
    return redirect('my_applications')

