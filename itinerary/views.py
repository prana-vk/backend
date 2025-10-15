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
from home.models import GILocation
from adver.models import AdLocation


class TripPlanViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Trip Plans (without route optimization)
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
