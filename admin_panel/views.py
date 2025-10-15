"""
Custom Admin Panel Views
Protected admin interface for managing GI Yatra data
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from functools import wraps
import json
import os

from home.models import GILocation
from adver.models import AdLocation
from itinerary.models import TripPlan


def admin_required(view_func):
    """Decorator to check if admin is authenticated via session"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('admin_authenticated', False):
            messages.warning(request, 'Please login to access the admin panel.')
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper


def ensure_admin_user_exists():
    """Create admin user from environment variables if it doesn't exist - STRICT MODE"""
    admin_username = os.environ.get('ADMIN_USERNAME')
    admin_email = os.environ.get('ADMIN_EMAIL')
    admin_password = os.environ.get('ADMIN_PASSWORD')
    
    # Only create user if ALL environment variables are set
    if not admin_username or not admin_email or not admin_password:
        print("⚠️  Admin environment variables not set - user creation skipped")
        return
    
    if not User.objects.filter(username=admin_username).exists():
        try:
            User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password
            )
            print(f"✅ Admin user '{admin_username}' created successfully!")
        except Exception as e:
            print(f"❌ Error creating admin user: {str(e)}")


def is_admin(user):
    """Check if user is authenticated via session (env-based auth)"""
    # This function is not used anymore with session-based auth
    # Kept for compatibility but sessions are checked directly in views
    return user.is_authenticated and (user.is_superuser or user.is_staff)


def is_admin_session(request):
    """Check if admin is authenticated via session"""
    return request.session.get('admin_authenticated', False)


def validate_env_credentials(username, email, password):
    """Validate all three credentials against environment variables - NO FALLBACKS"""
    env_username = os.environ.get('ADMIN_USERNAME')
    env_email = os.environ.get('ADMIN_EMAIL')
    env_password = os.environ.get('ADMIN_PASSWORD')
    
    # If any environment variable is missing, deny access
    if not env_username or not env_email or not env_password:
        return False
    
    return (username == env_username and 
            email == env_email and 
            password == env_password)


def admin_login_view(request):
    """Admin login page with environment variable validation ONLY"""
    # Check if already logged in via session
    if request.session.get('admin_authenticated'):
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Validate all three credentials against environment variables
        if validate_env_credentials(username, email, password):
            # Set session flag for authenticated admin
            request.session['admin_authenticated'] = True
            request.session['admin_username'] = username
            messages.success(request, f'Welcome back, {username}!')
            return redirect('admin_dashboard')
        else:
            # Check if environment variables are set
            if not os.environ.get('ADMIN_USERNAME') or not os.environ.get('ADMIN_EMAIL') or not os.environ.get('ADMIN_PASSWORD'):
                messages.error(request, 'Server configuration error: Admin environment variables not set.')
            else:
                messages.error(request, 'Access denied. Invalid credentials provided.')
    
    return render(request, 'admin_panel/login.html')


def admin_logout_view(request):
    """Admin logout"""
    # Clear session
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('admin_login')


@admin_required
def admin_dashboard_view(request):
    """Admin dashboard with stats"""
    context = {
        'gi_locations_count': GILocation.objects.count(),
        'ad_locations_count': AdLocation.objects.count(),
        'trips_count': TripPlan.objects.count(),
        'recent_gi_locations': GILocation.objects.order_by('-id')[:5],
        'recent_ad_locations': AdLocation.objects.order_by('-id')[:5],
        'admin_username': request.session.get('admin_username', 'Admin')
    }
    return render(request, 'admin_panel/dashboard.html', context)


@admin_required
def gi_locations_view(request):
    """Manage GI Locations"""
    locations = GILocation.objects.all().order_by('-id')
    paginator = Paginator(locations, 20)  # 20 locations per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'locations': page_obj,
        'total_count': locations.count()
    }
    return render(request, 'admin_panel/gi_locations.html', context)


@admin_required
def add_gi_location_view(request):
    """Add new GI Location"""
    if request.method == 'POST':
        try:
            location = GILocation.objects.create(
                name=request.POST.get('name'),
                description=request.POST.get('description', ''),
                district=request.POST.get('district'),
                latitude=float(request.POST.get('latitude', 0)),
                longitude=float(request.POST.get('longitude', 0)),
                opening_time=request.POST.get('opening_time') or '09:00:00',
                closing_time=request.POST.get('closing_time') or '18:00:00',
                image=request.FILES.get('image')
            )
            messages.success(request, f'GI Location "{location.name}" added successfully!')
            return redirect('gi_locations')
        except Exception as e:
            messages.error(request, f'Error adding location: {str(e)}')
    
    return render(request, 'admin_panel/add_gi_location.html')


@admin_required
def edit_gi_location_view(request, location_id):
    """Edit GI Location"""
    location = get_object_or_404(GILocation, id=location_id)
    
    if request.method == 'POST':
        try:
            location.name = request.POST.get('name')
            location.description = request.POST.get('description', '')
            location.district = request.POST.get('district')
            location.latitude = float(request.POST.get('latitude', 0))
            location.longitude = float(request.POST.get('longitude', 0))
            location.opening_time = request.POST.get('opening_time') or '09:00:00'
            location.closing_time = request.POST.get('closing_time') or '18:00:00'
            
            if request.FILES.get('image'):
                location.image = request.FILES.get('image')
            
            location.save()
            messages.success(request, f'GI Location "{location.name}" updated successfully!')
            return redirect('gi_locations')
        except Exception as e:
            messages.error(request, f'Error updating location: {str(e)}')
    
    context = {'location': location}
    return render(request, 'admin_panel/edit_gi_location.html', context)


@admin_required
def delete_gi_location_view(request, location_id):
    """Delete GI Location"""
    location = get_object_or_404(GILocation, id=location_id)
    
    if request.method == 'POST':
        name = location.name
        location.delete()
        messages.success(request, f'GI Location "{name}" deleted successfully!')
        return redirect('gi_locations')
    
    context = {'location': location}
    return render(request, 'admin_panel/delete_gi_location.html', context)


@admin_required
def ad_locations_view(request):
    """Manage Ad Locations"""
    locations = AdLocation.objects.all().order_by('-id')
    paginator = Paginator(locations, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'locations': page_obj,
        'total_count': locations.count()
    }
    return render(request, 'admin_panel/ad_locations.html', context)


@admin_required
def add_ad_location_view(request):
    """Add new Ad Location"""
    if request.method == 'POST':
        try:
            location = AdLocation.objects.create(
                name=request.POST.get('name'),
                ad_type=request.POST.get('ad_type'),
                description=request.POST.get('description', ''),
                contact_info=request.POST.get('contact_info', ''),
                latitude=float(request.POST.get('latitude', 0)),
                longitude=float(request.POST.get('longitude', 0))
            )
            messages.success(request, f'Ad Location "{location.name}" added successfully!')
            return redirect('ad_locations')
        except Exception as e:
            messages.error(request, f'Error adding ad location: {str(e)}')
    
    context = {
        'ad_types': ['Hotel', 'Restaurant', 'Guide', 'Transport']
    }
    return render(request, 'admin_panel/add_ad_location.html', context)


@admin_required
def edit_ad_location_view(request, location_id):
    """Edit Ad Location"""
    location = get_object_or_404(AdLocation, id=location_id)
    
    if request.method == 'POST':
        try:
            location.name = request.POST.get('name')
            location.ad_type = request.POST.get('ad_type')
            location.description = request.POST.get('description', '')
            location.contact_info = request.POST.get('contact_info', '')
            location.latitude = float(request.POST.get('latitude', 0))
            location.longitude = float(request.POST.get('longitude', 0))
            location.save()
            
            messages.success(request, f'Ad Location "{location.name}" updated successfully!')
            return redirect('ad_locations')
        except Exception as e:
            messages.error(request, f'Error updating ad location: {str(e)}')
    
    context = {
        'location': location,
        'ad_types': ['Hotel', 'Restaurant', 'Guide', 'Transport']
    }
    return render(request, 'admin_panel/edit_ad_location.html', context)


@admin_required
def delete_ad_location_view(request, location_id):
    """Delete Ad Location"""
    location = get_object_or_404(AdLocation, id=location_id)
    
    if request.method == 'POST':
        name = location.name
        location.delete()
        messages.success(request, f'Ad Location "{name}" deleted successfully!')
        return redirect('ad_locations')
    
    context = {'location': location}
    return render(request, 'admin_panel/delete_ad_location.html', context)


@admin_required
@csrf_exempt
def bulk_add_data_view(request):
    """Bulk add sample data"""
    if request.method == 'POST':
        try:
            data_type = request.POST.get('data_type')
            
            if data_type == 'gi_locations':
                # Add sample GI locations
                sample_gi_data = [
                    {
                        'name': 'Mysore Palace',
                        'description': 'Historic royal palace with Indo-Saracenic architecture',
                        'district': 'Mysore',
                        'latitude': 12.3052,
                        'longitude': 76.6551,
                        'opening_time': '10:00:00',
                        'closing_time': '17:30:00'
                    },
                    {
                        'name': 'Hampi Ruins',
                        'description': 'UNESCO World Heritage Site with ancient temples',
                        'district': 'Ballari',
                        'latitude': 15.3350,
                        'longitude': 76.4600,
                        'opening_time': '06:00:00',
                        'closing_time': '18:00:00'
                    },
                    {
                        'name': 'Jog Falls',
                        'description': 'Second highest plunge waterfall in India',
                        'district': 'Shimoga',
                        'latitude': 14.2291,
                        'longitude': 74.8127,
                        'opening_time': '06:00:00',
                        'closing_time': '18:00:00'
                    },
                    {
                        'name': 'Gokarna Beach',
                        'description': 'Pristine beaches and ancient temples',
                        'district': 'Uttara Kannada',
                        'latitude': 14.5479,
                        'longitude': 74.3188,
                        'opening_time': '00:00:00',
                        'closing_time': '23:59:00'
                    },
                    {
                        'name': 'Coorg Coffee Plantations',
                        'description': 'Scenic coffee estates in Western Ghats',
                        'district': 'Kodagu',
                        'latitude': 12.4244,
                        'longitude': 75.7382,
                        'opening_time': '07:00:00',
                        'closing_time': '18:00:00'
                    }
                ]
                
                created_count = 0
                for location_data in sample_gi_data:
                    location, created = GILocation.objects.get_or_create(
                        name=location_data['name'],
                        defaults=location_data
                    )
                    if created:
                        created_count += 1
                
                messages.success(request, f'Added {created_count} new GI locations!')
            
            elif data_type == 'ad_locations':
                # Add sample Ad locations
                sample_ad_data = [
                    {
                        'name': 'The Grand Hotel Mysore',
                        'ad_type': 'Hotel',
                        'description': '5-star luxury hotel near Mysore Palace',
                        'contact_info': '+91-821-2512345, bookings@grandmysore.com',
                        'latitude': 12.3015,
                        'longitude': 76.6553
                    },
                    {
                        'name': 'RRR Restaurant',
                        'ad_type': 'Restaurant',
                        'description': 'Authentic Karnataka cuisine',
                        'contact_info': '+91-821-2456789',
                        'latitude': 12.3100,
                        'longitude': 76.6500
                    },
                    {
                        'name': 'Karnataka Travels',
                        'ad_type': 'Transport',
                        'description': 'AC buses and car rentals across Karnataka',
                        'contact_info': '+91-80-2345-6789, bookings@karnatravels.com',
                        'latitude': 12.9716,
                        'longitude': 77.5946
                    },
                    {
                        'name': 'Hampi Heritage Tours',
                        'ad_type': 'Guide',
                        'description': 'Expert guides for Hampi historical sites',
                        'contact_info': '+91-8394-234123, info@hampitours.com',
                        'latitude': 15.3340,
                        'longitude': 76.4610
                    }
                ]
                
                created_count = 0
                for ad_data in sample_ad_data:
                    location, created = AdLocation.objects.get_or_create(
                        name=ad_data['name'],
                        defaults=ad_data
                    )
                    if created:
                        created_count += 1
                
                messages.success(request, f'Added {created_count} new ad locations!')
            
            return JsonResponse({'success': True, 'message': 'Data added successfully!'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return render(request, 'admin_panel/bulk_add_data.html')
