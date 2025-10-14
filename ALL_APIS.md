# 🚀 ALL API ENDPOINTS - GI Yatra Backend

## 📍 Base URLs
```
Local:      http://127.0.0.1:8000
Production: https://backend-k4x8.onrender.com
```

## ✅ No Authentication Required!
All APIs are open and can be accessed without login.

---

## 🏛️ GI LOCATIONS APIs

### 4. List All GI Locations
```http
GET /api/gi-locations/
```
**Query Parameters:**
- `search` - Search by name, description, district
- `district` - Filter by district
- `page` - Page number (50 items per page)

**Example:**
```http
GET /api/gi-locations/?search=mysore&district=Mysore&page=1
```

**Response:**
```json
{
  "count": 100,
  "next": "http://127.0.0.1:8000/api/gi-locations/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Mysore Palace",
      "district": "Mysore",
      "latitude": "12.3051",
      "longitude": "76.6551",
      "image": "http://127.0.0.1:8000/media/gi_locations/mysore_palace.jpg",
      "description": "Historical palace in Mysore",
      "typical_visit_duration": 120
    }
  ]
}
```

### 5. Create GI Location
```http
POST /api/gi-locations/
```
**Body (multipart/form-data):**
```json
{
  "name": "Mysore Palace",
  "district": "Mysore",
  "latitude": "12.3051",
  "longitude": "76.6551",
  "description": "Historical palace",
  "image": <file>,
  "typical_visit_duration": 120,
  "opening_time": "10:00:00",
  "closing_time": "18:00:00",
  "entry_fee": "100.00"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Mysore Palace",
  "district": "Mysore",
  "latitude": "12.3051",
  "longitude": "76.6551",
  "image": "http://127.0.0.1:8000/media/gi_locations/mysore_palace.jpg",
  "description": "Historical palace",
  "typical_visit_duration": 120,
  "opening_time": "10:00:00",
  "closing_time": "18:00:00",
  "entry_fee": "100.00",
  "created_by": 1,
  "created_at": "2025-10-14T10:30:00Z",
  "updated_at": "2025-10-14T10:30:00Z"
}
```

### 6. Get Single GI Location
```http
GET /api/gi-locations/{id}/
```
**Example:**
```http
GET /api/gi-locations/1/
```

**Response:**
```json
{
  "id": 1,
  "name": "Mysore Palace",
  "district": "Mysore",
  "latitude": "12.3051",
  "longitude": "76.6551",
  "image": "http://127.0.0.1:8000/media/gi_locations/mysore_palace.jpg",
  "description": "Historical palace in Mysore",
  "typical_visit_duration": 120,
  "opening_time": "10:00:00",
  "closing_time": "18:00:00",
  "entry_fee": "100.00",
  "created_by": 1,
  "created_at": "2025-10-14T10:30:00Z",
  "updated_at": "2025-10-14T10:30:00Z"
}
```

### 7. Update GI Location
```http
PUT /api/gi-locations/{id}/
PATCH /api/gi-locations/{id}/
```
**Example:**
```http
PATCH /api/gi-locations/1/
```
**Body:**
```json
{
  "description": "Updated description",
  "entry_fee": "150.00"
}
```

### 8. Delete GI Location
```http
DELETE /api/gi-locations/{id}/
```
**Example:**
```http
DELETE /api/gi-locations/1/
```
**Response:** `204 No Content`

### 9. Get All Districts
```http
GET /api/gi-locations/districts/
```
**Response:**
```json
{
  "districts": [
    "Mysore",
    "Bangalore",
    "Hampi",
    "Coorg",
    "Mangalore"
  ]
}
```

### 10. Get GI Locations by District
```http
GET /api/gi-locations/by_district/
```
**Response:**
```json
{
  "Mysore": [
    {
      "id": 1,
      "name": "Mysore Palace",
      "latitude": "12.3051",
      "longitude": "76.6551",
      "description": "Historical palace"
    }
  ],
  "Bangalore": [
    {
      "id": 2,
      "name": "Bangalore Palace",
      "latitude": "12.9984",
      "longitude": "77.5920",
      "description": "Royal palace"
    }
  ]
}
```

---

## 🏨 ADVERTISEMENT LOCATIONS APIs

### 11. List All Ad Locations
```http
GET /api/ad-locations/
```
**Query Parameters:**
- `search` - Search by name, description
- `district` - Filter by district
- `service_type` - Filter by service type
- `page` - Page number

**Example:**
```http
GET /api/ad-locations/?service_type=hotel&district=Mysore&page=1
```

**Response:**
```json
{
  "count": 50,
  "next": "http://127.0.0.1:8000/api/ad-locations/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Royal Hotel",
      "service_type": "hotel",
      "district": "Mysore",
      "latitude": "12.3051",
      "longitude": "76.6551",
      "contact_phone": "+91-9876543210",
      "price_range": "₹₹₹",
      "is_active": true
    }
  ]
}
```

### 12. Create Ad Location
```http
POST /api/ad-locations/
```
**Body (multipart/form-data):**
```json
{
  "name": "Royal Hotel",
  "service_type": "hotel",
  "district": "Mysore",
  "latitude": "12.3051",
  "longitude": "76.6551",
  "description": "Luxury hotel near palace",
  "contact_phone": "+91-9876543210",
  "contact_email": "info@royalhotel.com",
  "website": "https://royalhotel.com",
  "address": "Palace Road, Mysore",
  "image": <file>,
  "price_range": "₹₹₹",
  "rating": "4.5",
  "is_active": true
}
```

**Service Types:**
- `hotel` - Hotel
- `restaurant` - Restaurant
- `transport` - Transport Service
- `guide` - Tour Guide
- `shop` - Shop
- `other` - Other Service

**Response:**
```json
{
  "id": 1,
  "name": "Royal Hotel",
  "service_type": "hotel",
  "district": "Mysore",
  "latitude": "12.3051",
  "longitude": "76.6551",
  "description": "Luxury hotel near palace",
  "contact_phone": "+91-9876543210",
  "contact_email": "info@royalhotel.com",
  "website": "https://royalhotel.com",
  "address": "Palace Road, Mysore",
  "image": "http://127.0.0.1:8000/media/ad_locations/royal_hotel.jpg",
  "price_range": "₹₹₹",
  "rating": "4.5",
  "is_active": true,
  "created_by": 1,
  "created_at": "2025-10-14T10:30:00Z",
  "updated_at": "2025-10-14T10:30:00Z"
}
```

### 13. Get Single Ad Location
```http
GET /api/ad-locations/{id}/
```

### 14. Update Ad Location
```http
PUT /api/ad-locations/{id}/
PATCH /api/ad-locations/{id}/
```

### 15. Delete Ad Location
```http
DELETE /api/ad-locations/{id}/
```

### 16. Get All Service Types
```http
GET /api/ad-locations/service_types/
```
**Response:**
```json
{
  "service_types": [
    {"value": "hotel", "label": "Hotel"},
    {"value": "restaurant", "label": "Restaurant"},
    {"value": "transport", "label": "Transport Service"},
    {"value": "guide", "label": "Tour Guide"},
    {"value": "shop", "label": "Shop"},
    {"value": "other", "label": "Other Service"}
  ]
}
```

### 17. Get Ad Locations by Service Type
```http
GET /api/ad-locations/by_service_type/
```
**Response:**
```json
{
  "hotel": [
    {
      "id": 1,
      "name": "Royal Hotel",
      "district": "Mysore",
      "contact_phone": "+91-9876543210",
      "price_range": "₹₹₹"
    }
  ],
  "restaurant": [
    {
      "id": 2,
      "name": "Spice Garden",
      "district": "Mysore",
      "contact_phone": "+91-9876543211"
    }
  ]
}
```

### 18. Get My Ad Locations
```http
GET /api/ad-locations/my_locations/
```
**Response:**
```json
[
  {
    "id": 1,
    "name": "Royal Hotel",
    "service_type": "hotel",
    "is_active": true
  }
]
```

---

## 🗺️ TRIP PLANNING APIs

### 19. List All Trips
```http
GET /api/trips/
```
**Response:**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Mysore Weekend Trip",
      "start_date": "2025-10-20",
      "end_date": "2025-10-22",
      "num_days": 3,
      "start_location_name": "Bangalore",
      "total_locations": 5,
      "created_at": "2025-10-14T10:30:00Z"
    }
  ]
}
```

### 20. Create Trip
```http
POST /api/trips/
```
**Body:**
```json
{
  "title": "Mysore Weekend Trip",
  "start_date": "2025-10-20",
  "end_date": "2025-10-22",
  "num_days": 3,
  "start_location_name": "Bangalore",
  "start_location_latitude": "12.9716",
  "start_location_longitude": "77.5946",
  "preferred_start_time": "09:00:00",
  "preferred_end_time": "18:00:00"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Mysore Weekend Trip",
  "start_date": "2025-10-20",
  "end_date": "2025-10-22",
  "num_days": 3,
  "start_location_name": "Bangalore",
  "start_location_latitude": "12.9716",
  "start_location_longitude": "77.5946",
  "preferred_start_time": "09:00:00",
  "preferred_end_time": "18:00:00",
  "is_scheduled": false,
  "created_by": 1,
  "created_at": "2025-10-14T10:30:00Z",
  "updated_at": "2025-10-14T10:30:00Z"
}
```

### 21. Get Single Trip
```http
GET /api/trips/{id}/
```

### 22. Update Trip
```http
PUT /api/trips/{id}/
PATCH /api/trips/{id}/
```

### 23. Delete Trip
```http
DELETE /api/trips/{id}/
```

### 24. Add Location to Trip
```http
POST /api/trips/{trip_id}/add_location/
```
**Body:**
```json
{
  "gi_location_id": 1,
  "priority": 1
}
```
**Response:**
```json
{
  "message": "Location added to trip",
  "selected_location": {
    "id": 1,
    "gi_location": {
      "id": 1,
      "name": "Mysore Palace",
      "district": "Mysore"
    },
    "priority": 1
  }
}
```

### 25. Remove Location from Trip
```http
POST /api/trips/{trip_id}/remove_location/
```
**Body:**
```json
{
  "selected_location_id": 1
}
```
**Response:**
```json
{
  "message": "Location removed from trip"
}
```

### 26. Generate Trip Schedule (SMART ALGORITHM)
```http
POST /api/trips/{trip_id}/generate_schedule/
```
**This is the MAIN API - Generates optimized itinerary!**

**Response:**
```json
{
  "message": "Schedule generated successfully",
  "schedule": {
    "trip_id": 1,
    "title": "Mysore Weekend Trip",
    "start_date": "2025-10-20",
    "end_date": "2025-10-22",
    "total_days": 3,
    "days": [
      {
        "day_number": 1,
        "date": "2025-10-20",
        "items": [
          {
            "order": 1,
            "item_type": "location",
            "start_time": "09:00:00",
            "end_time": "11:00:00",
            "location": {
              "id": 1,
              "name": "Mysore Palace",
              "district": "Mysore",
              "latitude": "12.3051",
              "longitude": "76.6551"
            },
            "duration_minutes": 120
          },
          {
            "order": 2,
            "item_type": "travel",
            "start_time": "11:00:00",
            "end_time": "11:30:00",
            "from_location": "Mysore Palace",
            "to_location": "Chamundi Hills",
            "distance_km": 15.2,
            "duration_minutes": 30
          },
          {
            "order": 3,
            "item_type": "location",
            "start_time": "11:30:00",
            "end_time": "13:00:00",
            "location": {
              "id": 2,
              "name": "Chamundi Hills",
              "district": "Mysore"
            },
            "duration_minutes": 90
          },
          {
            "order": 4,
            "item_type": "break",
            "start_time": "13:00:00",
            "end_time": "14:00:00",
            "description": "Lunch break",
            "duration_minutes": 60
          }
        ]
      },
      {
        "day_number": 2,
        "date": "2025-10-21",
        "items": [...]
      }
    ]
  }
}
```

### 27. Get Trip Schedule
```http
GET /api/trips/{trip_id}/schedule/
```
**Returns the saved schedule for a trip**

**Response:**
```json
{
  "schedule": {
    "trip_id": 1,
    "days": [...]
  }
}
```

### 28. Get Trip Days
```http
GET /api/trips/{trip_id}/days/
```
**Response:**
```json
[
  {
    "id": 1,
    "day_number": 1,
    "date": "2025-10-20",
    "notes": "First day - Mysore city tour"
  },
  {
    "id": 2,
    "day_number": 2,
    "date": "2025-10-21",
    "notes": "Second day - Nearby attractions"
  }
]
```

### 29. Get Selected Locations for Trip
```http
GET /api/trips/{trip_id}/selected_locations/
```
**Response:**
```json
[
  {
    "id": 1,
    "gi_location": {
      "id": 1,
      "name": "Mysore Palace",
      "district": "Mysore",
      "latitude": "12.3051",
      "longitude": "76.6551"
    },
    "priority": 1,
    "added_at": "2025-10-14T10:30:00Z"
  }
]
```

---

## 📊 API SUMMARY

### Total Endpoints: **26 APIs**

#### By Category:
- **GI Locations:** 10 APIs
- **Ad Locations:** 8 APIs
- **Trip Planning:** 8 APIs

#### By HTTP Method:
- **GET:** 15 APIs
- **POST:** 10 APIs
- **PUT/PATCH:** 3 APIs
- **DELETE:** 1 API

---

## 🧪 TESTING APIs

### Using cURL:

#### 1. Get GI Locations
```bash
curl -X GET http://127.0.0.1:8000/api/gi-locations/
```

#### 2. Create Trip
```bash
curl -X POST http://127.0.0.1:8000/api/trips/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Trip",
    "start_date": "2025-10-20",
    "end_date": "2025-10-22",
    "num_days": 3,
    "start_location_name": "Bangalore",
    "start_location_latitude": "12.9716",
    "start_location_longitude": "77.5946"
  }'
```

#### 3. Generate Schedule
```bash
curl -X POST http://127.0.0.1:8000/api/trips/1/generate_schedule/
```

### Using Postman:

1. **Import Collection:**
   - Create new collection: "GI Yatra APIs"
   - Add base URL: `http://127.0.0.1:8000`

2. **Setup:**
   - Create new collection: "GI Yatra APIs"
   - Add base URL: `http://127.0.0.1:8000`
   - No authentication needed!

3. **Test All Endpoints:**
   - Copy endpoints from this document
   - Test each one

---

## 🔥 MOST IMPORTANT APIs

### Top 5 Must-Use APIs:

1. **POST /api/trips/generate_schedule/**
   - The SMART algorithm!
   - Generates optimized itinerary
   - Uses route optimization
   - Calculates travel time

2. **GET /api/gi-locations/**
   - Get all GI locations
   - Search and filter
   - Pagination support

3. **POST /api/trips/**
   - Create new trip
   - Set dates and preferences
   - Define start location

4. **POST /api/trips/{id}/add_location/**
   - Add locations to trip
   - Set priority
   - Multiple locations

5. **GET /api/ad-locations/**
   - Find hotels, restaurants
   - Filter by service type
   - Get contact information

---

## 🌟 SPECIAL FEATURES

### 1. Smart Schedule Generation
- **Haversine Formula** for distance calculation
- **Nearest Neighbor Algorithm** for route optimization
- **Time Slot Management** for realistic scheduling
- **Lunch Break Insertion** at 13:00
- **Multi-day Support** with proper distribution

### 2. Image Upload
- GI locations can have images
- Ad locations can have images
- Stored in `/media/` folder
- URLs returned in API response

### 3. Search & Filter
- Full-text search on name, description
- Filter by district
- Filter by service type
- Sort by various fields

### 4. Pagination
- 50 items per page
- Next/previous links
- Total count included

### 5. User-specific Data
- `/api/ad-locations/my_locations/` - Get your ads
- Trip plans linked to user
- Created_by tracking

---

## 📱 API WORKFLOW EXAMPLES

### Example 1: Plan a Trip

```http
# Step 1: Get available GI locations
GET /api/gi-locations/?district=Mysore

# Step 2: Create trip
POST /api/trips/
Body: {
  "title": "Mysore Trip",
  "start_date": "2025-10-20",
  "end_date": "2025-10-22",
  "num_days": 3,
  "start_location_name": "Bangalore",
  "start_location_latitude": "12.9716",
  "start_location_longitude": "77.5946"
}

# Step 3: Add locations to trip
POST /api/trips/1/add_location/
Body: {"gi_location_id": 1, "priority": 1}

POST /api/trips/1/add_location/
Body: {"gi_location_id": 2, "priority": 2}

# Step 4: Generate optimized schedule
POST /api/trips/1/generate_schedule/

# Step 5: Get the schedule
GET /api/trips/1/schedule/
```

### Example 2: Find Hotels Near Location

```http
# Step 1: Get GI location
GET /api/gi-locations/1/

# Step 2: Find nearby hotels
GET /api/ad-locations/?service_type=hotel&district=Mysore

# Step 3: Get hotel details
GET /api/ad-locations/5/
```

### Example 3: Add New GI Location

```http
# Step 1: Create GI location
POST /api/gi-locations/
Body (form-data): {
  "name": "New Location",
  "district": "Mysore",
  "latitude": "12.3051",
  "longitude": "76.6551",
  "description": "Description",
  "image": <file>,
  "typical_visit_duration": 90
}

# Step 2: Verify creation
GET /api/gi-locations/
```

---

## ⚙️ API CONFIGURATION

### Base Settings:
- **Host:** http://127.0.0.1:8000
- **Protocol:** HTTP (HTTPS in production)
- **Format:** JSON
- **Authentication:** None (Open APIs)
- **Pagination:** 50 items per page
- **CORS:** Enabled for localhost:3000, localhost:5173

### Headers:
```http
Content-Type: application/json
Accept: application/json
```

### For File Upload:
```http
Content-Type: multipart/form-data
```

---

## 🎯 QUICK REFERENCE

### GI Locations:
```
GET    /api/gi-locations/              - List all
POST   /api/gi-locations/              - Create
GET    /api/gi-locations/{id}/         - Get one
PATCH  /api/gi-locations/{id}/         - Update
DELETE /api/gi-locations/{id}/         - Delete
GET    /api/gi-locations/districts/    - Get districts
GET    /api/gi-locations/by_district/  - Group by district
```

### Ad Locations:
```
GET   /api/ad-locations/                  - List all
POST  /api/ad-locations/                  - Create
GET   /api/ad-locations/{id}/             - Get one
PATCH /api/ad-locations/{id}/             - Update
DELETE /api/ad-locations/{id}/            - Delete
GET   /api/ad-locations/service_types/    - Get service types
GET   /api/ad-locations/by_service_type/  - Group by type
GET   /api/ad-locations/my_locations/     - My ads
```

### Trips:
```
GET  /api/trips/                            - List all
POST /api/trips/                            - Create
GET  /api/trips/{id}/                       - Get one
POST /api/trips/{id}/add_location/          - Add location
POST /api/trips/{id}/remove_location/       - Remove location
POST /api/trips/{id}/generate_schedule/     - Generate schedule ⭐
GET  /api/trips/{id}/schedule/              - Get schedule
GET  /api/trips/{id}/days/                  - Get days
GET  /api/trips/{id}/selected_locations/    - Get selected locations
```

---

## 🚀 READY TO USE!

All **26 APIs** are working and ready to use!

**No authentication required - all APIs are open!**

Start testing with:
```bash
cd backend
python manage.py runserver
```

Then open: http://127.0.0.1:8000/api/

Happy coding! 🎉
