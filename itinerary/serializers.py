from rest_framework import serializers
from .models import TripPlan, TripDay, ScheduleItem, SelectedLocation
from home.serializers import GILocationListSerializer
from adver.serializers import AdLocationListSerializer


class ScheduleItemSerializer(serializers.ModelSerializer):
    """Serializer for Schedule Items"""
    
    gi_location = GILocationListSerializer(read_only=True)
    ad_location = AdLocationListSerializer(read_only=True)
    item_type_display = serializers.CharField(source='get_item_type_display', read_only=True)
    
    class Meta:
        model = ScheduleItem
        fields = [
            'id', 'item_type', 'item_type_display', 'gi_location', 'ad_location',
            'start_time', 'end_time', 'duration_minutes', 'distance_km',
            'notes', 'order'
        ]


class TripDaySerializer(serializers.ModelSerializer):
    """Serializer for Trip Days"""
    
    schedule_items = ScheduleItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = TripDay
        fields = ['id', 'day_number', 'date', 'schedule_items']


class SelectedLocationSerializer(serializers.ModelSerializer):
    """Serializer for Selected Locations"""
    
    gi_location = GILocationListSerializer(read_only=True)
    ad_location = AdLocationListSerializer(read_only=True)
    gi_location_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    ad_location_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = SelectedLocation
        fields = ['id', 'gi_location', 'ad_location', 'gi_location_id', 'ad_location_id', 'added_at']


class TripPlanSerializer(serializers.ModelSerializer):
    """Serializer for Trip Plans"""
    
    username = serializers.CharField(source='user.username', read_only=True)
    trip_days = TripDaySerializer(many=True, read_only=True)
    selected_locations = SelectedLocationSerializer(many=True, read_only=True)
    
    class Meta:
        model = TripPlan
        fields = [
            'id', 'user', 'username', 'title', 'start_location_name',
            'start_latitude', 'start_longitude', 'start_date', 'start_time',
            'end_time', 'num_days', 'available_hours_per_day',
            'created_at', 'updated_at', 'trip_days', 'selected_locations'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)


class TripPlanCreateSerializer(serializers.ModelSerializer):
    """Lightweight serializer for creating trip plans"""
    
    selected_gi_locations = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    selected_ad_locations = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = TripPlan
        fields = [
            'id', 'title', 'start_location_name', 'start_latitude',
            'start_longitude', 'start_date', 'start_time', 'end_time',
            'num_days', 'available_hours_per_day',
            'selected_gi_locations', 'selected_ad_locations'
        ]
    
    def create(self, validated_data):
        selected_gi = validated_data.pop('selected_gi_locations', [])
        selected_ad = validated_data.pop('selected_ad_locations', [])
        
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        
        trip_plan = super().create(validated_data)
        
        # Add selected GI locations
        from home.models import GILocation
        for gi_id in selected_gi:
            try:
                gi_location = GILocation.objects.get(id=gi_id)
                SelectedLocation.objects.create(
                    trip_plan=trip_plan,
                    gi_location=gi_location
                )
            except GILocation.DoesNotExist:
                pass
        
        # Add selected Ad locations
        from adver.models import AdLocation
        for ad_id in selected_ad:
            try:
                ad_location = AdLocation.objects.get(id=ad_id)
                SelectedLocation.objects.create(
                    trip_plan=trip_plan,
                    ad_location=ad_location
                )
            except AdLocation.DoesNotExist:
                pass
        
        return trip_plan
