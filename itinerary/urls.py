from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TripPlanViewSet

router = DefaultRouter()
router.register(r'trips', TripPlanViewSet, basename='tripplan')

urlpatterns = [
    path('', include(router.urls)),
]
