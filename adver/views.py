from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import AdLocation
from .serializers import AdLocationSerializer, AdLocationListSerializer


class AdLocationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Ad Location CRUD operations
    """
    queryset = AdLocation.objects.filter(is_active=True)
    serializer_class = AdLocationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'district', 'description', 'service_type']
    ordering_fields = ['name', 'district', 'service_type', 'created_at']
    ordering = ['district', 'service_type', 'name']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AdLocationListSerializer
        return AdLocationSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on query parameters
        """
        queryset = AdLocation.objects.filter(is_active=True)
        
        # Filter by district
        district = self.request.query_params.get('district', None)
        if district:
            queryset = queryset.filter(district__iexact=district)
        
        # Filter by service type
        service_type = self.request.query_params.get('service_type', None)
        if service_type:
            queryset = queryset.filter(service_type=service_type)
        
        # Filter by multiple service types
        service_types = self.request.query_params.get('service_types', None)
        if service_types:
            type_list = service_types.split(',')
            queryset = queryset.filter(service_type__in=type_list)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def service_types(self, request):
        """
        Get list of all service types
        """
        service_types = [
            {'value': choice[0], 'label': choice[1]}
            for choice in AdLocation.SERVICE_TYPE_CHOICES
        ]
        return Response({'service_types': service_types})
    
    @action(detail=False, methods=['get'])
    def by_service_type(self, request):
        """
        Get ad locations grouped by service type
        """
        result = {}
        
        for service_type, label in AdLocation.SERVICE_TYPE_CHOICES:
            locations = AdLocation.objects.filter(service_type=service_type, is_active=True)
            serializer = AdLocationListSerializer(locations, many=True)
            result[service_type] = {
                'label': label,
                'locations': serializer.data
            }
        
        return Response(result)
    
    @action(detail=False, methods=['get'])
    def my_locations(self, request):
        """
        Get locations created by the current user
        """
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        locations = AdLocation.objects.filter(created_by=request.user)
        serializer = AdLocationSerializer(locations, many=True)
        return Response(serializer.data)
