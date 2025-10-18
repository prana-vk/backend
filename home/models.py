from django.db import models
from django.contrib.auth.models import User


class GILocation(models.Model):
    """Model for Geographical Indication (GI) locations in Karnataka"""
    
    name = models.CharField(max_length=255)
    district = models.CharField(max_length=100, db_index=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    description = models.TextField()
    image = models.ImageField(upload_to='gi_locations/', blank=True, null=True)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    typical_visit_duration = models.IntegerField(default=60, help_text="Duration in minutes")
    sellable_quantity = models.IntegerField(
        null=True, 
        blank=True, 
        help_text="Available quantity for sale (optional, leave empty if not sellable)"
    )
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['district', 'name']
        verbose_name = 'GI Location'
        verbose_name_plural = 'GI Locations'
    
    def __str__(self):
        return f"{self.name} - {self.district}"
