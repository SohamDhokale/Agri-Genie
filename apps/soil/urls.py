from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.soil_test_form, name='soil_test'),
    path('report/<int:test_id>/', views.soil_report, name='soil_report'),
    path('history/', views.soil_history, name='soil_history'),
    path('pdf-tools/', views.pdf_tools, name='soil_pdf_tools'),
    path('pdf-tools/grid/', views.generate_grid, name='soil_pdf_grid'),
    path('pdf-tools/fill/', views.fill_pdf, name='soil_pdf_fill'),
    path('pdf-tools/ocr/', views.extract_text_from_pdf, name='soil_pdf_ocr'),
]
