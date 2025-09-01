from django.urls import path
from . import views

urlpatterns = [
    path('', views.pesticides_list, name='pesticides_list'),
    path('<int:pesticide_id>/', views.pesticide_detail, name='pesticide_detail'),
]
