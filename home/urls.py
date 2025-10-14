from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GILocationViewSet

router = DefaultRouter()
router.register(r'gi-locations', GILocationViewSet, basename='gi-location')

urlpatterns = [
    path('', include(router.urls)),
]
