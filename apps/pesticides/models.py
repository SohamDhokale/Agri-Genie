from django.db import models

# Create your models here.

class Pesticide(models.Model):
    CATEGORY_CHOICES = [
        ('insecticide', 'Insecticide'),
        ('herbicide', 'Herbicide'),
        ('fungicide', 'Fungicide'),
        ('nematicide', 'Nematicide'),
        ('rodenticide', 'Rodenticide'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    active_ingredient = models.CharField(max_length=200)
    description = models.TextField()
    target_pests = models.TextField()
    application_method = models.TextField()
    dosage = models.CharField(max_length=100)
    safety_precautions = models.TextField()
    manufacturer = models.CharField(max_length=200)
    price_range = models.CharField(max_length=100, blank=True)
    is_organic = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
