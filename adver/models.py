from django.db import models
from django.contrib.auth.models import User


class AdLocation(models.Model):
    """Model for Advertisement/Service locations (Hotels, Restaurants, etc.)"""
    
    SERVICE_TYPE_CHOICES = [
        ('hotel', 'Hotel'),
        ('restaurant', 'Restaurant'),
        ('transport', 'Transport'),
        ('guide', 'Tour Guide'),
        ('shop', 'Shop'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=255)
    district = models.CharField(max_length=100, db_index=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    description = models.TextField()
    image = models.ImageField(upload_to='ad_locations/', blank=True, null=True)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    price_range = models.CharField(max_length=50, blank=True, help_text="e.g., ₹₹₹")
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['district', 'service_type', 'name']
        verbose_name = 'Ad Location'
        verbose_name_plural = 'Ad Locations'
    
    def __str__(self):
        return f"{self.name} ({self.service_type}) - {self.district}"
