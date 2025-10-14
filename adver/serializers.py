from rest_framework import serializers
from .models import AdLocation


class AdLocationSerializer(serializers.ModelSerializer):
    """Serializer for Ad Location model"""
    
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    service_type_display = serializers.CharField(source='get_service_type_display', read_only=True)
    
    class Meta:
        model = AdLocation
        fields = [
            'id', 'name', 'district', 'latitude', 'longitude',
            'description', 'image', 'service_type', 'service_type_display',
            'opening_time', 'closing_time', 'contact_phone', 'contact_email',
            'website', 'price_range', 'is_active', 'created_by',
            'created_by_username', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']


class AdLocationListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing ad locations"""
    
    service_type_display = serializers.CharField(source='get_service_type_display', read_only=True)
    
    class Meta:
        model = AdLocation
        fields = [
            'id', 'name', 'district', 'latitude', 'longitude',
            'image', 'service_type', 'service_type_display', 'price_range'
        ]


class AdLocationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Ad Locations"""
    
    class Meta:
        model = AdLocation
        fields = [
            'name', 'district', 'latitude', 'longitude',
            'description', 'image', 'service_type',
            'opening_time', 'closing_time', 'contact_phone',
            'contact_email', 'website', 'price_range', 'is_active'
        ]
    
    def validate(self, data):
        """Validate location data"""
        # Validate latitude
        if not -90 <= data['latitude'] <= 90:
            raise serializers.ValidationError("Latitude must be between -90 and 90")
        
        # Validate longitude
        if not -180 <= data['longitude'] <= 180:
            raise serializers.ValidationError("Longitude must be between -180 and 180")
        
        return data

