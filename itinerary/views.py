from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from .models import TripPlan, TripDay, ScheduleItem, SelectedLocation
from .serializers import (
    TripPlanSerializer, TripPlanCreateSerializer,
    TripDaySerializer, ScheduleItemSerializer, SelectedLocationSerializer
)
from .schedule_generator import generate_optimized_schedule
from home.models import GILocation
from adver.models import AdLocation


class TripPlanViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Trip Plans
    """
    serializer_class = TripPlanSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return trips for current user only"""
        return TripPlan.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TripPlanCreateSerializer
        return TripPlanSerializer
    
    @action(detail=True, methods=['post'])
    def generate_schedule(self, request, pk=None):
        """
        Generate optimized schedule for the trip
        """
        import logging
        import time as pytime
        logging.warning(f"[generate_schedule] Start for trip_id={pk}")
        start_time = pytime.time()
        trip_plan = self.get_object()
        
        # Get selected locations
        selected_locations_qs = SelectedLocation.objects.filter(trip_plan=trip_plan)
        
        # Prepare location data
        locations = []
        for sel_loc in selected_locations_qs:
            if sel_loc.gi_location:
                loc = sel_loc.gi_location
                locations.append({
                    'id': loc.id,
                    'type': 'gi',
                    'name': loc.name,
                    'latitude': float(loc.latitude),
                    'longitude': float(loc.longitude),
                    'typical_visit_duration': loc.typical_visit_duration,
                    'description': loc.description,
                    'image': loc.image.url if loc.image else None,
                })
            elif sel_loc.ad_location:
                loc = sel_loc.ad_location
                locations.append({
                    'id': loc.id,
                    'type': 'ad',
                    'name': loc.name,
                    'latitude': float(loc.latitude),
                    'longitude': float(loc.longitude),
                    'typical_visit_duration': 60,  # Default for ad locations
                    'description': loc.description,
                    'image': loc.image.url if loc.image else None,
                    'service_type': loc.service_type,
                })
        
        logging.warning(f"[generate_schedule] {len(locations)} locations to optimize")
        if len(locations) > 23:
            logging.error("[generate_schedule] Too many locations for Google Maps API (max 23 waypoints). Returning error.")
            return Response({'error': 'Too many locations selected. Google Maps API supports a maximum of 23 waypoints.'}, status=status.HTTP_400_BAD_REQUEST)
        if not locations:
            return Response(
                {'error': 'No locations selected for this trip'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate schedule
        try:
            schedule = generate_optimized_schedule(trip_plan, locations)
        except Exception as e:
            logging.error(f"[generate_schedule] Exception during schedule generation: {e}")
            return Response({'error': f'Schedule generation failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        elapsed = pytime.time() - start_time
        logging.warning(f"[generate_schedule] Finished in {elapsed:.2f} seconds for trip_id={pk}")
        # Clear existing schedule
        TripDay.objects.filter(trip_plan=trip_plan).delete()
        
        # Save schedule to database
        for day_data in schedule['days']:
            trip_day = TripDay.objects.create(
                trip_plan=trip_plan,
                day_number=day_data['day_number'],
                date=day_data['date']
            )
            
            for order, item_data in enumerate(day_data['items'], start=1):
                item_type = item_data['type']
                
                schedule_item = ScheduleItem(
                    trip_day=trip_day,
                    item_type=item_type,
                    start_time=item_data['start_time'],
                    end_time=item_data['end_time'],
                    duration_minutes=item_data['duration'],
                    order=order
                )
                
                if item_type == 'travel':
                    schedule_item.distance_km = item_data.get('distance')
                    schedule_item.notes = f"Travel: {item_data.get('distance')} km"
                
                elif item_type == 'location':
                    location = item_data.get('location')
                    if location:
                        location_id = location.get('id')
                        location_type = location.get('type')
                        
                        if location_type == 'gi':
                            schedule_item.gi_location = GILocation.objects.get(id=location_id)
                        elif location_type == 'ad':
                            schedule_item.ad_location = AdLocation.objects.get(id=location_id)
                
                elif item_type == 'break':
                    schedule_item.notes = item_data.get('name', 'Break')
                
                schedule_item.save()
        
        # Return generated schedule
        trip_plan.refresh_from_db()
        serializer = TripPlanSerializer(trip_plan)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def schedule(self, request, pk=None):
        """
        Get the generated schedule for a trip
        """
        trip_plan = self.get_object()
        serializer = TripPlanSerializer(trip_plan)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_location(self, request, pk=None):
        """
        Add a location to the trip
        """
        trip_plan = self.get_object()
        gi_location_id = request.data.get('gi_location_id')
        ad_location_id = request.data.get('ad_location_id')
        
        if gi_location_id:
            try:
                gi_location = GILocation.objects.get(id=gi_location_id)
                SelectedLocation.objects.create(
                    trip_plan=trip_plan,
                    gi_location=gi_location
                )
                return Response({'message': 'GI Location added successfully'})
            except GILocation.DoesNotExist:
                return Response(
                    {'error': 'GI Location not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        elif ad_location_id:
            try:
                ad_location = AdLocation.objects.get(id=ad_location_id)
                SelectedLocation.objects.create(
                    trip_plan=trip_plan,
                    ad_location=ad_location
                )
                return Response({'message': 'Ad Location added successfully'})
            except AdLocation.DoesNotExist:
                return Response(
                    {'error': 'Ad Location not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(
            {'error': 'Please provide either gi_location_id or ad_location_id'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['delete'])
    def remove_location(self, request, pk=None):
        """
        Remove a location from the trip
        """
        trip_plan = self.get_object()
        selected_location_id = request.data.get('selected_location_id')
        
        try:
            selected_location = SelectedLocation.objects.get(
                id=selected_location_id,
                trip_plan=trip_plan
            )
            selected_location.delete()
            return Response({'message': 'Location removed successfully'})
        except SelectedLocation.DoesNotExist:
            return Response(
                {'error': 'Selected location not found'},
                status=status.HTTP_404_NOT_FOUND
            )
