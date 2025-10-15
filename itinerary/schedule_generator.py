"""
Schedule Generation Algorithm
Google Maps Directions API is only called when /api/trips/{trip_id}/generate_schedule/ is POSTed (i.e., when 'Select Trip' is pressed in the frontend).
No background or unnecessary invocation occurs.
"""
from datetime import datetime, timedelta, time
from math import radians, cos, sin, asin, sqrt
from typing import List, Dict, Any


## No local distance/route optimization is used. All optimization is via Google Maps Directions API.


def add_minutes_to_time(time_obj: time, minutes: int) -> time:
    """Add minutes to a time object"""
    dt = datetime.combine(datetime.today(), time_obj)
    new_dt = dt + timedelta(minutes=minutes)
    return new_dt.time()


def time_to_minutes(time_obj: time) -> int:
    """Convert time object to minutes since midnight"""
    return time_obj.hour * 60 + time_obj.minute


def minutes_to_time(minutes: int) -> time:
    """Convert minutes since midnight to time object"""
    hours = minutes // 60
    mins = minutes % 60
    return time(hours, mins)


def should_add_lunch_break(current_time: time, lunch_start: str = '13:00') -> bool:
    """Check if lunch break should be added"""
    lunch_time = datetime.strptime(lunch_start, '%H:%M').time()
    current_mins = time_to_minutes(current_time)
    lunch_mins = time_to_minutes(lunch_time)
    
    # Add lunch if current time is between 11:30 and 13:00
    return 690 <= current_mins < lunch_mins  # 690 = 11:30 in minutes


import os
import requests

import logging

def optimize_route(start_point: Dict, locations: List[Dict]) -> List[Dict]:
    """
    Optimize route using Google Maps Directions API with waypoint optimization.
    Returns ordered list of locations with travel info.
    Adds timeout, waypoint limit, and error handling to prevent worker timeouts.
    """
    if not locations:
        return []

    api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    if not api_key:
        raise Exception('Google Maps API key not set in environment variable GOOGLE_MAPS_API_KEY')

    # Google Maps Directions API supports max 23 waypoints
    MAX_WAYPOINTS = 23
    if len(locations) > MAX_WAYPOINTS:
        logging.warning(f"Too many waypoints ({len(locations)}). Limiting to first {MAX_WAYPOINTS}.")
        locations = locations[:MAX_WAYPOINTS]

    waypoints = "|".join([
        f"{loc['latitude']},{loc['longitude']}" for loc in locations
    ])

    url = (
        "https://maps.googleapis.com/maps/api/directions/json?"
        f"origin={start_point['latitude']},{start_point['longitude']}"
        f"&destination={start_point['latitude']},{start_point['longitude']}"  # round trip
        f"&waypoints=optimize:true|{waypoints}"
        f"&mode=driving"
        f"&key={api_key}"
    )

    try:
        response = requests.get(url, timeout=20)  # 20 second timeout
        if response.status_code != 200:
            logging.error(f"Google Maps API error: {response.status_code} {response.text}")
            return locations  # fallback: original order
        data = response.json()
        if data.get('status') != 'OK':
            logging.error(f"Google Maps API error: {data.get('status')} {data.get('error_message')}")
            return locations  # fallback: original order

        waypoint_order = data['routes'][0]['waypoint_order']
        legs = data['routes'][0]['legs']
        polyline = data['routes'][0].get('overview_polyline', {}).get('points')

        ordered = [locations[i] for i in waypoint_order]
        for idx, loc in enumerate(ordered):
            leg = legs[idx]
            loc['travel_distance_m'] = leg['distance']['value']
            loc['travel_duration_s'] = leg['duration']['value']
            loc['travel_distance_text'] = leg['distance']['text']
            loc['travel_duration_text'] = leg['duration']['text']
        if ordered:
            ordered[0]['route_polyline'] = polyline
        return ordered
    except Exception as e:
        logging.error(f"Google Maps API request failed: {e}")
        return locations  # fallback: original order


def split_locations_by_days(locations: List[Dict], num_days: int, available_mins_per_day: int) -> List[List[Dict]]:
    """
    Split locations across multiple days based on time constraints
    """
    if not locations:
        return [[] for _ in range(num_days)]
    
    if num_days == 1:
        return [locations]
    
    # Calculate approximate time per location (visit + travel)
    avg_visit_time = sum(loc.get('typical_visit_duration', 60) for loc in locations) / len(locations)
    avg_travel_time = 30  # Approximate
    avg_time_per_location = avg_visit_time + avg_travel_time
    
    # Calculate locations per day
    locations_per_day = max(1, int(available_mins_per_day / avg_time_per_location))
    
    # Split locations
    days = []
    for i in range(num_days):
        start_idx = i * locations_per_day
        end_idx = start_idx + locations_per_day
        day_locations = locations[start_idx:end_idx]
        if day_locations:
            days.append(day_locations)
        else:
            days.append([])
    
    # If there are remaining locations, distribute them
    remaining = locations[num_days * locations_per_day:]
    for i, loc in enumerate(remaining):
        day_idx = i % num_days
        if day_idx < len(days):
            days[day_idx].append(loc)
    
    return days


def generate_optimized_schedule(trip_plan, selected_locations: List[Dict]) -> Dict[str, Any]:
    """
    Main function to generate optimized schedule
    Returns schedule dictionary with day-by-day itinerary
    """
    # Constants
    AVERAGE_SPEED_KMH = 40
    BUFFER_TIME_MINS = 15
    LUNCH_BREAK_START = '13:00'
    LUNCH_BREAK_DURATION = 60
    
    schedule = {
        'trip_id': trip_plan.id,
        'title': trip_plan.title,
        'days': []
    }
    
    # Get start location
    start_point = {
        'latitude': float(trip_plan.start_latitude),
        'longitude': float(trip_plan.start_longitude),
        'name': trip_plan.start_location_name
    }
    
    # Calculate available time per day
    start_time_mins = time_to_minutes(trip_plan.start_time)
    end_time_mins = time_to_minutes(trip_plan.end_time)
    available_minutes_per_day = end_time_mins - start_time_mins
    
    # Optimize route
    ordered_locations = optimize_route(start_point, selected_locations)
    
    # Split locations by days
    locations_per_day = split_locations_by_days(
        ordered_locations,
        trip_plan.num_days,
        available_minutes_per_day
    )
    
    # Generate schedule for each day
    for day_num in range(1, trip_plan.num_days + 1):
        day_date = trip_plan.start_date + timedelta(days=day_num - 1)
        current_time = trip_plan.start_time
        current_location = start_point if day_num == 1 else locations_per_day[day_num - 2][-1] if day_num > 1 and locations_per_day[day_num - 2] else start_point
        
        day_schedule = {
            'day_number': day_num,
            'date': day_date.isoformat(),
            'items': []
        }
        
        day_locations = locations_per_day[day_num - 1] if day_num <= len(locations_per_day) else []
        
        for location in day_locations:
            # Calculate travel time
            distance_km = calculate_distance(
                current_location['latitude'], current_location['longitude'],
                location['latitude'], location['longitude']
            )
            travel_time_mins = max(5, int((distance_km / AVERAGE_SPEED_KMH) * 60))
            
            # Add travel segment
            if travel_time_mins > 0 and distance_km > 0.5:  # Only add if > 0.5 km
                travel_end_time = add_minutes_to_time(current_time, travel_time_mins)
                
                # Check if travel exceeds day end time
                if time_to_minutes(travel_end_time) > end_time_mins:
                    break
                
                day_schedule['items'].append({
                    'type': 'travel',
                    'start_time': current_time.isoformat(),
                    'end_time': travel_end_time.isoformat(),
                    'duration': travel_time_mins,
                    'distance': round(distance_km, 2)
                })
                current_time = travel_end_time
            
            # Add buffer time
            current_time = add_minutes_to_time(current_time, BUFFER_TIME_MINS)
            
            # Check for lunch break
            if should_add_lunch_break(current_time, LUNCH_BREAK_START):
                lunch_time = datetime.strptime(LUNCH_BREAK_START, '%H:%M').time()
                lunch_end = add_minutes_to_time(lunch_time, LUNCH_BREAK_DURATION)
                day_schedule['items'].append({
                    'type': 'break',
                    'name': 'Lunch Break',
                    'start_time': LUNCH_BREAK_START,
                    'end_time': lunch_end.isoformat(),
                    'duration': LUNCH_BREAK_DURATION
                })
                current_time = lunch_end
            
            # Check if we have time for this location
            visit_duration = location.get('typical_visit_duration', 60)
            visit_end_time = add_minutes_to_time(current_time, visit_duration)
            
            if time_to_minutes(visit_end_time) > end_time_mins:
                # Not enough time, skip this location or move to next day
                break
            
            # Add location visit
            day_schedule['items'].append({
                'type': 'location',
                'location': location,
                'location_id': location.get('id'),
                'location_type': location.get('type'),  # 'gi' or 'ad'
                'start_time': current_time.isoformat(),
                'end_time': visit_end_time.isoformat(),
                'duration': visit_duration
            })
            
            current_time = visit_end_time
            current_location = location
        
        schedule['days'].append(day_schedule)
    
    return schedule
