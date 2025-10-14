"""
Script to load sample data into GI Yatra database
Run this on Render Shell or locally with production database
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'giyatra_project.settings')
django.setup()

from home.models import GILocation
from adver.models import AdLocation

def load_gi_locations():
    """Load sample GI locations"""
    
    gi_locations = [
        {
            'name': 'Mysore Palace',
            'description': 'Historic royal palace with Indo-Saracenic architecture',
            'district': 'Mysore',
            'latitude': 12.3052,
            'longitude': 76.6551,
            'opening_time': '10:00:00',
            'closing_time': '17:30:00',
            'entry_fee': 70,
            'image': None
        },
        {
            'name': 'Hampi Ruins',
            'description': 'UNESCO World Heritage Site with ancient temples',
            'district': 'Ballari',
            'latitude': 15.3350,
            'longitude': 76.4600,
            'opening_time': '06:00:00',
            'closing_time': '18:00:00',
            'entry_fee': 40,
            'image': None
        },
        {
            'name': 'Jog Falls',
            'description': 'Second highest plunge waterfall in India',
            'district': 'Shimoga',
            'latitude': 14.2291,
            'longitude': 74.8127,
            'opening_time': '06:00:00',
            'closing_time': '18:00:00',
            'entry_fee': 20,
            'image': None
        },
        {
            'name': 'Gokarna Beach',
            'description': 'Pristine beaches and ancient temples',
            'district': 'Uttara Kannada',
            'latitude': 14.5479,
            'longitude': 74.3188,
            'opening_time': '00:00:00',
            'closing_time': '23:59:00',
            'entry_fee': 0,
            'image': None
        },
        {
            'name': 'Bandipur National Park',
            'description': 'Wildlife sanctuary with tigers and elephants',
            'district': 'Chamarajanagar',
            'latitude': 11.6906,
            'longitude': 76.5783,
            'opening_time': '06:30:00',
            'closing_time': '18:00:00',
            'entry_fee': 300,
            'image': None
        },
        {
            'name': 'Coorg Coffee Plantations',
            'description': 'Scenic coffee estates in Western Ghats',
            'district': 'Kodagu',
            'latitude': 12.4244,
            'longitude': 75.7382,
            'opening_time': '07:00:00',
            'closing_time': '18:00:00',
            'entry_fee': 0,
            'image': None
        },
        {
            'name': 'Belur Chennakeshava Temple',
            'description': 'Hoysala architecture masterpiece',
            'district': 'Hassan',
            'latitude': 13.1657,
            'longitude': 75.8650,
            'opening_time': '07:30:00',
            'closing_time': '19:30:00',
            'entry_fee': 25,
            'image': None
        },
        {
            'name': 'Nandi Hills',
            'description': 'Hill station with sunrise views near Bangalore',
            'district': 'Chikkaballapur',
            'latitude': 13.3703,
            'longitude': 77.6838,
            'opening_time': '06:00:00',
            'closing_time': '22:00:00',
            'entry_fee': 30,
            'image': None
        },
        {
            'name': 'Badami Cave Temples',
            'description': 'Rock-cut temples from 6th century',
            'district': 'Bagalkot',
            'latitude': 15.9150,
            'longitude': 75.6765,
            'opening_time': '09:00:00',
            'closing_time': '18:00:00',
            'entry_fee': 40,
            'image': None
        },
        {
            'name': 'Udupi Krishna Temple',
            'description': 'Famous pilgrimage site with unique rituals',
            'district': 'Udupi',
            'latitude': 13.3409,
            'longitude': 74.7421,
            'opening_time': '05:30:00',
            'closing_time': '21:00:00',
            'entry_fee': 0,
            'image': None
        }
    ]
    
    created_count = 0
    for location_data in gi_locations:
        location, created = GILocation.objects.get_or_create(
            name=location_data['name'],
            defaults=location_data
        )
        if created:
            created_count += 1
            print(f"✅ Created: {location.name}")
        else:
            print(f"⏭️  Already exists: {location.name}")
    
    print(f"\n🎉 Created {created_count} new GI locations!")


def load_ad_locations():
    """Load sample advertisement locations"""
    
    ad_locations = [
        {
            'name': 'The Grand Hotel Mysore',
            'ad_type': 'Hotel',
            'description': '5-star luxury hotel near Mysore Palace',
            'contact_info': '+91-821-2512345, bookings@grandmysore.com',
            'latitude': 12.3015,
            'longitude': 76.6553
        },
        {
            'name': 'Coorg Homestay',
            'ad_type': 'Hotel',
            'description': 'Traditional homestay in coffee plantations',
            'contact_info': '+91-8272-234567, stay@coorgh omestay.com',
            'latitude': 12.4200,
            'longitude': 75.7400
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
            'name': 'Hampi Heritage Tours',
            'ad_type': 'Guide',
            'description': 'Expert guides for Hampi historical sites',
            'contact_info': '+91-8394-234123, info@hampitours.com',
            'latitude': 15.3340,
            'longitude': 76.4610
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
            'name': 'Gokarna Beach Resort',
            'ad_type': 'Hotel',
            'description': 'Beachfront resort with sea view rooms',
            'contact_info': '+91-8386-256789, resort@gokarna.com',
            'latitude': 14.5450,
            'longitude': 74.3200
        },
        {
            'name': 'Coastal Kitchen Udupi',
            'ad_type': 'Restaurant',
            'description': 'Famous for Udupi cuisine and seafood',
            'contact_info': '+91-820-2567890',
            'latitude': 13.3380,
            'longitude': 74.7450
        },
        {
            'name': 'Nandi Hills Adventure Guide',
            'ad_type': 'Guide',
            'description': 'Trekking and cycling tours',
            'contact_info': '+91-9876-543210, adventure@nandihills.com',
            'latitude': 13.3700,
            'longitude': 77.6840
        }
    ]
    
    created_count = 0
    for ad_data in ad_locations:
        ad, created = AdLocation.objects.get_or_create(
            name=ad_data['name'],
            defaults=ad_data
        )
        if created:
            created_count += 1
            print(f"✅ Created: {ad.name}")
        else:
            print(f"⏭️  Already exists: {ad.name}")
    
    print(f"\n🎉 Created {created_count} new advertisement locations!")


if __name__ == '__main__':
    print("🚀 Loading sample data into GI Yatra database...\n")
    print("=" * 50)
    print("Loading GI Locations...")
    print("=" * 50)
    load_gi_locations()
    
    print("\n" + "=" * 50)
    print("Loading Advertisement Locations...")
    print("=" * 50)
    load_ad_locations()
    
    print("\n✅ All done! Check your database.")
    print(f"📊 Total GI Locations: {GILocation.objects.count()}")
    print(f"📊 Total Ad Locations: {AdLocation.objects.count()}")
