from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.admin_login_view, name='admin_login'),
    path('logout/', views.admin_logout_view, name='admin_logout'),
    
    # Dashboard
    path('', views.admin_dashboard_view, name='admin_dashboard'),
    
    # GI Locations Management
    path('gi-locations/', views.gi_locations_view, name='gi_locations'),
    path('gi-locations/add/', views.add_gi_location_view, name='add_gi_location'),
    path('gi-locations/<int:location_id>/edit/', views.edit_gi_location_view, name='edit_gi_location'),
    path('gi-locations/<int:location_id>/delete/', views.delete_gi_location_view, name='delete_gi_location'),
    
    # Ad Locations Management
    path('ad-locations/', views.ad_locations_view, name='ad_locations'),
    path('ad-locations/add/', views.add_ad_location_view, name='add_ad_location'),
    path('ad-locations/<int:location_id>/edit/', views.edit_ad_location_view, name='edit_ad_location'),
    path('ad-locations/<int:location_id>/delete/', views.delete_ad_location_view, name='delete_ad_location'),
    
    # Bulk Operations
    path('bulk-add-data/', views.bulk_add_data_view, name='bulk_add_data'),
]