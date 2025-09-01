from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SoilTest(models.Model):
    QUALITY_CHOICES = [
        ('poor', 'Poor'),
        ('slightly_poor', 'Slightly Poor'),
        ('moderate', 'Moderate'),
        ('good', 'Good'),
        ('excellent', 'Excellent'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ph_value = models.FloatField()
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    moisture = models.FloatField()
    humidity = models.FloatField()
    organic_matter = models.FloatField()
    quality_index = models.FloatField()
    quality_rating = models.CharField(max_length=20, choices=QUALITY_CHOICES)
    recommendations = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Soil Test - {self.user.username} - {self.created_at}"
    
    def calculate_quality_index(self):
        # Soil Quality Index calculation based on various parameters
        ph_score = self.get_ph_score()
        npk_score = self.get_npk_score()
        moisture_score = self.get_moisture_score()
        organic_score = self.get_organic_score()
        
        total_score = (ph_score + npk_score + moisture_score + organic_score) / 4
        self.quality_index = round(total_score, 2)
        
        if total_score >= 90:
            self.quality_rating = 'excellent'
        elif total_score >= 75:
            self.quality_rating = 'good'
        elif total_score >= 60:
            self.quality_rating = 'moderate'
        elif total_score >= 40:
            self.quality_rating = 'slightly_poor'
        else:
            self.quality_rating = 'poor'
    
    def get_ph_score(self):
        if 6.0 <= self.ph_value <= 7.5:
            return 100
        elif 5.5 <= self.ph_value < 6.0 or 7.5 < self.ph_value <= 8.0:
            return 80
        elif 5.0 <= self.ph_value < 5.5 or 8.0 < self.ph_value <= 8.5:
            return 60
        else:
            return 30
    
    def get_npk_score(self):
        n_score = min(self.nitrogen / 40 * 100, 100) if self.nitrogen <= 40 else 100
        p_score = min(self.phosphorus / 25 * 100, 100) if self.phosphorus <= 25 else 100
        k_score = min(self.potassium / 300 * 100, 100) if self.potassium <= 300 else 100
        return (n_score + p_score + k_score) / 3
    
    def get_moisture_score(self):
        if 40 <= self.moisture <= 60:
            return 100
        elif 30 <= self.moisture < 40 or 60 < self.moisture <= 70:
            return 80
        else:
            return 50
    
    def get_organic_score(self):
        if self.organic_matter >= 3:
            return 100
        elif self.organic_matter >= 2:
            return 80
        elif self.organic_matter >= 1:
            return 60
        else:
            return 40
