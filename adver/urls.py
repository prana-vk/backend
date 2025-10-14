from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdLocationViewSet

router = DefaultRouter()
router.register(r'ad-locations', AdLocationViewSet, basename='adlocation')

urlpatterns = [
    path('', include(router.urls)),
]
