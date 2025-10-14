from django.db import models
from django.contrib.auth.models import User
from home.models import GILocation
from adver.models import AdLocation


class TripPlan(models.Model):
    """Model for user trip plans"""
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='trip_plans')
    title = models.CharField(max_length=255)
    start_location_name = models.CharField(max_length=255)
    start_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    start_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    num_days = models.IntegerField(default=1)
    available_hours_per_day = models.IntegerField(default=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Trip Plan'
        verbose_name_plural = 'Trip Plans'
    
    def __str__(self):
        return f"{self.title}"


class TripDay(models.Model):
    """Model for individual days in a trip"""
    
    trip_plan = models.ForeignKey(TripPlan, on_delete=models.CASCADE, related_name='trip_days')
    day_number = models.IntegerField()
    date = models.DateField()
    
    class Meta:
        ordering = ['trip_plan', 'day_number']
        verbose_name = 'Trip Day'
        verbose_name_plural = 'Trip Days'
        unique_together = ['trip_plan', 'day_number']
    
    def __str__(self):
        return f"{self.trip_plan.title} - Day {self.day_number}"


class ScheduleItem(models.Model):
    """Model for schedule items (location visits, travel, breaks, etc.)"""
    
    ITEM_TYPE_CHOICES = [
        ('location', 'Location Visit'),
        ('travel', 'Travel'),
        ('break', 'Break'),
        ('accommodation', 'Accommodation'),
    ]
    
    trip_day = models.ForeignKey(TripDay, on_delete=models.CASCADE, related_name='schedule_items')
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES)
    gi_location = models.ForeignKey(GILocation, on_delete=models.SET_NULL, null=True, blank=True)
    ad_location = models.ForeignKey(AdLocation, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration_minutes = models.IntegerField()
    distance_km = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    order = models.IntegerField()
    
    class Meta:
        ordering = ['trip_day', 'order']
        verbose_name = 'Schedule Item'
        verbose_name_plural = 'Schedule Items'
    
    def __str__(self):
        return f"{self.trip_day} - {self.item_type} (Order: {self.order})"


class SelectedLocation(models.Model):
    """Model to store locations selected for a trip"""
    
    trip_plan = models.ForeignKey(TripPlan, on_delete=models.CASCADE, related_name='selected_locations')
    gi_location = models.ForeignKey(GILocation, on_delete=models.CASCADE, null=True, blank=True)
    ad_location = models.ForeignKey(AdLocation, on_delete=models.CASCADE, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Selected Location'
        verbose_name_plural = 'Selected Locations'
    
    def __str__(self):
        location = self.gi_location if self.gi_location else self.ad_location
        return f"{self.trip_plan.title} - {location.name}"
