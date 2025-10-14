from django.contrib import admin
from .models import TripPlan, TripDay, ScheduleItem, SelectedLocation


class TripDayInline(admin.TabularInline):
    model = TripDay
    extra = 0
    readonly_fields = ['day_number', 'date']


class SelectedLocationInline(admin.TabularInline):
    model = SelectedLocation
    extra = 0
    readonly_fields = ['added_at']


@admin.register(TripPlan)
class TripPlanAdmin(admin.ModelAdmin):
    """Admin interface for Trip Plans"""
    
    list_display = ['title', 'user', 'start_date', 'num_days', 'created_at']
    list_filter = ['start_date', 'num_days', 'created_at']
    search_fields = ['title', 'user__username', 'start_location_name']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [SelectedLocationInline, TripDayInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'title')
        }),
        ('Start Location', {
            'fields': ('start_location_name', 'start_latitude', 'start_longitude')
        }),
        ('Schedule', {
            'fields': ('start_date', 'start_time', 'end_time', 'num_days', 'available_hours_per_day')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class ScheduleItemInline(admin.TabularInline):
    model = ScheduleItem
    extra = 0
    readonly_fields = ['order']


@admin.register(TripDay)
class TripDayAdmin(admin.ModelAdmin):
    """Admin interface for Trip Days"""
    
    list_display = ['trip_plan', 'day_number', 'date']
    list_filter = ['date']
    search_fields = ['trip_plan__title']
    inlines = [ScheduleItemInline]


@admin.register(ScheduleItem)
class ScheduleItemAdmin(admin.ModelAdmin):
    """Admin interface for Schedule Items"""
    
    list_display = ['trip_day', 'item_type', 'start_time', 'end_time', 'duration_minutes', 'order']
    list_filter = ['item_type', 'trip_day__date']
    search_fields = ['trip_day__trip_plan__title', 'notes']
    ordering = ['trip_day', 'order']


@admin.register(SelectedLocation)
class SelectedLocationAdmin(admin.ModelAdmin):
    """Admin interface for Selected Locations"""
    
    list_display = ['trip_plan', 'get_location_name', 'added_at']
    list_filter = ['added_at']
    search_fields = ['trip_plan__title']
    
    def get_location_name(self, obj):
        if obj.gi_location:
            return f"GI: {obj.gi_location.name}"
        elif obj.ad_location:
            return f"Ad: {obj.ad_location.name}"
        return "Unknown"
    get_location_name.short_description = 'Location'
