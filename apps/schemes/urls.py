from django.urls import path
from . import views

urlpatterns = [
    path('', views.schemes_list, name='schemes_list'),
    path('<int:scheme_id>/', views.scheme_detail, name='scheme_detail'),
    path('<int:scheme_id>/apply/', views.apply_scheme, name='apply_scheme'),
    path('quick-apply/<int:scheme_id>/', views.quick_apply, name='quick_apply'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('application/<int:application_id>/', views.application_detail, name='application_detail'),
    path('withdraw/<int:application_id>/', views.withdraw_application, name='withdraw_application'),
]
