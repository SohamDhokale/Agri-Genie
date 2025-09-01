from django.urls import path
from . import views

urlpatterns = [
    path('', views.exports_list, name='exports_list'),
    path('detail/<int:item_id>/', views.export_detail, name='export_detail'),
    path('create-sample-data/', views.create_sample_data, name='create_sample_data'),
]
