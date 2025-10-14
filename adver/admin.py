from django.contrib import admin
from .models import AdLocation


@admin.register(AdLocation)
class AdLocationAdmin(admin.ModelAdmin):
    """Admin interface for Ad Locations"""
    
    list_display = ['name', 'service_type', 'district', 'is_active', 'created_by', 'created_at']
    list_filter = ['service_type', 'district', 'is_active', 'created_at']
    search_fields = ['name', 'district', 'description', 'contact_phone', 'contact_email']
    ordering = ['district', 'service_type', 'name']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'service_type', 'district', 'description', 'image')
        }),
        ('Location Details', {
            'fields': ('latitude', 'longitude')
        }),
        ('Contact Information', {
            'fields': ('contact_phone', 'contact_email', 'website', 'price_range')
        }),
        ('Timing & Status', {
            'fields': ('opening_time', 'closing_time', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
