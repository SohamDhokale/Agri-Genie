from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class GovernmentScheme(models.Model):
    CATEGORY_CHOICES = [
        ('subsidy', 'Subsidy'),
        ('loan', 'Loan'),
        ('insurance', 'Insurance'),
        ('training', 'Training'),
        ('equipment', 'Equipment'),
        ('technology', 'Technology'),
    ]
    
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    eligibility = models.TextField()
    benefits = models.TextField()
    application_process = models.TextField()
    documents_required = models.TextField()
    contact_info = models.TextField()
    website_url = models.URLField(blank=True)
    application_form_url = models.URLField(blank=True, help_text="Direct link to application form")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class SchemeApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scheme_applications')
    scheme = models.ForeignKey(GovernmentScheme, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    application_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, help_text="Additional notes or comments")
    
    # Application details
    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    farm_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Farm size in hectares")
    crop_type = models.CharField(max_length=100, blank=True)
    annual_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Document uploads (optional - can be added later)
    documents_uploaded = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.scheme.name}"
    
    class Meta:
        ordering = ['-application_date']
        unique_together = ['user', 'scheme']  # One application per user per scheme
