from rest_framework import serializers
from .models import GILocation


class GILocationSerializer(serializers.ModelSerializer):
    """Serializer for GI Location model"""

    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = GILocation
        fields = [
            'id', 'name', 'district', 'latitude', 'longitude',
            'description', 'image', 'image_url', 'opening_time', 'closing_time',
            'typical_visit_duration', 'created_by', 'created_by_username',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            rel_url = obj.image.url
            if request:
                return request.build_absolute_uri(rel_url)
            # fallback: use SITE_URL from settings
            from django.conf import settings
            site_url = getattr(settings, 'SITE_URL', None)
            if site_url:
                return site_url.rstrip('/') + rel_url
            return rel_url
        return None


class GILocationListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing GI locations"""
    
    class Meta:
        model = GILocation
        fields = [
            'id', 'name', 'district', 'latitude', 'longitude',
            'image', 'typical_visit_duration'
        ]


class GILocationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating GI Locations"""
    
    class Meta:
        model = GILocation
        fields = [
            'name', 'district', 'latitude', 'longitude',
            'description', 'image', 'opening_time', 'closing_time',
            'typical_visit_duration'
        ]
    
    def validate(self, data):
        """Validate location data"""
        # Validate latitude
        if not -90 <= data['latitude'] <= 90:
            raise serializers.ValidationError("Latitude must be between -90 and 90")
        
        # Validate longitude
        if not -180 <= data['longitude'] <= 180:
            raise serializers.ValidationError("Longitude must be between -180 and 180")
        
        # Validate typical visit duration
        if data.get('typical_visit_duration', 60) < 15:
            raise serializers.ValidationError("Visit duration must be at least 15 minutes")
        
        return data

