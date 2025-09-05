from django.urls import path
from . import views

urlpatterns = [
    path('', views.crop_list, name='crop_list'),
    path('recommend/', views.crop_recommendation_form, name='crop_recommendation'),
    path('recommend/result/<int:recommendation_id>/', views.crop_recommendation_result, name='crop_recommendation_result'),
    path('crop/<int:crop_id>/', views.crop_detail, name='crop_detail'),
    path('api/predict-yield/', views.api_predict_yield, name='api_predict_yield'),
    path('api/optimize-allocation/', views.api_optimize_allocation, name='api_optimize_allocation'),
]
