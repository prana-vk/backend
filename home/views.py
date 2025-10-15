    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Q
from .models import GILocation
from .serializers import GILocationSerializer, GILocationCreateSerializer


class GILocationViewSet(viewsets.ModelViewSet):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    """
    ViewSet for GI Locations
    Supports: list, retrieve, create, update, delete
    Filtering: by district, search by name/description
    """
    queryset = GILocation.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'district']
    ordering_fields = ['name', 'district', 'created_at']
    ordering = ['district', 'name']
    
    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.action in ['create', 'update', 'partial_update']:
            return GILocationCreateSerializer
        return GILocationSerializer
    
    def get_queryset(self):
        """Filter queryset based on query parameters"""
        queryset = GILocation.objects.all()
        
        # Filter by district
        district = self.request.query_params.get('district', None)
        if district:
            queryset = queryset.filter(district__iexact=district)
        
        return queryset
    
    def perform_create(self, serializer):
        """Set the created_by field to the current user"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def districts(self, request):
        """Get list of all districts with GI locations"""
        districts = GILocation.objects.values_list('district', flat=True).distinct().order_by('district')
        return Response({'districts': list(districts)})
    
    @action(detail=False, methods=['get'])
    def by_district(self, request):
        """Get GI locations grouped by district"""
        districts = GILocation.objects.values_list('district', flat=True).distinct()
        result = {}
        
        for district in districts:
            locations = GILocation.objects.filter(district=district)
            result[district] = GILocationSerializer(locations, many=True).data
        
        return Response(result)
