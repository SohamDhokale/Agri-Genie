
from django.contrib import admin
from .models import ExportService

@admin.register(ExportService)
class ExportServiceAdmin(admin.ModelAdmin):
    list_display = ('country', 'product', 'demand_level', 'contact_name', 'updated_at')
    list_filter = ('country', 'demand_level')
    search_fields = ('country', 'product', 'contact_name')
    date_hierarchy = 'updated_at'