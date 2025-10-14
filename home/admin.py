from django.contrib import admin
from .models import GILocation


@admin.register(GILocation)
class GILocationAdmin(admin.ModelAdmin):
    """Admin interface for GI Locations"""
    
    list_display = ['name', 'district', 'typical_visit_duration', 'created_by', 'created_at']
    list_filter = ['district', 'created_at']
    search_fields = ['name', 'description', 'district']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'district', 'description', 'image')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude')
        }),
        ('Timing', {
            'fields': ('opening_time', 'closing_time', 'typical_visit_duration')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )
