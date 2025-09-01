from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from apps.authentication.views import dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard_view, name='dashboard'),
    path('authentication/', include('apps.authentication.urls')),
    path('weather/', include('apps.weather.urls')),
    path('voice/', include('apps.voice.urls')),
    path('soil/', include('apps.soil.urls')),
    path('schemes/', include('apps.schemes.urls')),
    path('exports/', include('apps.exports.urls')),
    path('crops/', include('apps.crops.urls')),
    path('pesticides/', include('apps.pesticides.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
