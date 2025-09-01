from django.db import models
from django.utils import timezone

class ExportService(models.Model):
    DEMAND_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    
    country = models.CharField(max_length=100)
    product = models.CharField(max_length=100)
    demand_level = models.CharField(max_length=10, choices=DEMAND_CHOICES)
    notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(default=timezone.now)
    
    # Contact information
    contact_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    contact_website = models.URLField(blank=True)
    
    # Statistics for charts
    export_volume = models.IntegerField(default=0)  # For line chart
    market_share = models.FloatField(default=0.0)   # For Venn diagram
    potential_growth = models.FloatField(default=0.0)  # For Venn diagram
    
    def __str__(self):
        return f"{self.country} - {self.product}"
