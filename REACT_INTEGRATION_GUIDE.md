# 🚀 React Integration Guide - GI Yatra Backend

## ✅ No Authentication Required!

Your backend APIs are **completely open** - no login, no tokens, no cookies needed!

---

## 📍 Backend URL

```javascript
const API_BASE_URL = 'http://127.0.0.1:8000';
```

---

## 🔧 Setup Your React App

### 1. Install Axios (Recommended)
```bash
npm install axios
```

### 2. Create API Service File

Create `src/services/api.js`:

```javascript
import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
```

---

## 📚 ALL API QUERIES FOR REACT

### 1. GI LOCATIONS APIs

#### Get All GI Locations
```javascript
import api from './services/api';

// Get all locations
export const getAllGILocations = async () => {
  try {
    const response = await api.get('/api/gi-locations/');
    return response.data;
  } catch (error) {
    console.error('Error fetching GI locations:', error);
    throw error;
  }
};

// Usage in component:
const MyComponent = () => {
  const [locations, setLocations] = useState([]);
  
  useEffect(() => {
    getAllGILocations()
      .then(data => setLocations(data.results))
      .catch(err => console.error(err));
  }, []);
};
```

#### Get Single GI Location
```javascript
export const getGILocationById = async (id) => {
  try {
    const response = await api.get(`/api/gi-locations/${id}/`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching location ${id}:`, error);
    throw error;
  }
};

// Usage:
const location = await getGILocationById(1);
```

#### Create GI Location
```javascript
export const createGILocation = async (locationData) => {
  try {
    const response = await api.post('/api/gi-locations/', locationData);
    return response.data;
  } catch (error) {
    console.error('Error creating location:', error);
    throw error;
  }
};

// Usage:
const newLocation = {
  name: 'Mysore Palace',
  district: 'Mysore',
  latitude: '12.3051',
  longitude: '76.6551',
  description: 'Historic palace',
  typical_visit_duration: 120,
  opening_time: '10:00:00',
  closing_time: '18:00:00',
  entry_fee: '100.00'
};

const created = await createGILocation(newLocation);
```

#### Create GI Location with Image
```javascript
export const createGILocationWithImage = async (formData) => {
  try {
    const response = await api.post('/api/gi-locations/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error creating location with image:', error);
    throw error;
  }
};

// Usage in component:
const handleSubmit = async (e) => {
  e.preventDefault();
  
  const formData = new FormData();
  formData.append('name', 'Mysore Palace');
  formData.append('district', 'Mysore');
  formData.append('latitude', '12.3051');
  formData.append('longitude', '76.6551');
  formData.append('description', 'Historic palace');
  formData.append('typical_visit_duration', 120);
  formData.append('image', imageFile); // File from input
  
  const result = await createGILocationWithImage(formData);
};
```

#### Update GI Location
```javascript
export const updateGILocation = async (id, locationData) => {
  try {
    const response = await api.patch(`/api/gi-locations/${id}/`, locationData);
    return response.data;
  } catch (error) {
    console.error(`Error updating location ${id}:`, error);
    throw error;
  }
};

// Usage:
const updated = await updateGILocation(1, {
  description: 'Updated description',
  entry_fee: '150.00'
});
```

#### Delete GI Location
```javascript
export const deleteGILocation = async (id) => {
  try {
    await api.delete(`/api/gi-locations/${id}/`);
    return true;
  } catch (error) {
    console.error(`Error deleting location ${id}:`, error);
    throw error;
  }
};

// Usage:
await deleteGILocation(1);
```

#### Search GI Locations
```javascript
export const searchGILocations = async (searchTerm) => {
  try {
    const response = await api.get('/api/gi-locations/', {
      params: { search: searchTerm }
    });
    return response.data;
  } catch (error) {
    console.error('Error searching locations:', error);
    throw error;
  }
};

// Usage:
const results = await searchGILocations('mysore');
```

#### Filter by District
```javascript
export const filterGILocationsByDistrict = async (district) => {
  try {
    const response = await api.get('/api/gi-locations/', {
      params: { district: district }
    });
    return response.data;
  } catch (error) {
    console.error('Error filtering by district:', error);
    throw error;
  }
};

// Usage:
const mysoreLocations = await filterGILocationsByDistrict('Mysore');
```

#### Get All Districts
```javascript
export const getAllDistricts = async () => {
  try {
    const response = await api.get('/api/gi-locations/districts/');
    return response.data.districts;
  } catch (error) {
    console.error('Error fetching districts:', error);
    throw error;
  }
};

// Usage:
const districts = await getAllDistricts();
// Returns: ['Mysore', 'Bangalore', 'Hampi', ...]
```

#### Get Locations Grouped by District
```javascript
export const getLocationsByDistrict = async () => {
  try {
    const response = await api.get('/api/gi-locations/by_district/');
    return response.data;
  } catch (error) {
    console.error('Error fetching grouped locations:', error);
    throw error;
  }
};

// Usage:
const grouped = await getLocationsByDistrict();
// Returns: { 'Mysore': [...], 'Bangalore': [...] }
```

---

### 2. ADVERTISEMENT LOCATIONS APIs

#### Get All Ad Locations
```javascript
export const getAllAdLocations = async () => {
  try {
    const response = await api.get('/api/ad-locations/');
    return response.data;
  } catch (error) {
    console.error('Error fetching ad locations:', error);
    throw error;
  }
};
```

#### Get Single Ad Location
```javascript
export const getAdLocationById = async (id) => {
  try {
    const response = await api.get(`/api/ad-locations/${id}/`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching ad location ${id}:`, error);
    throw error;
  }
};
```

#### Create Ad Location
```javascript
export const createAdLocation = async (adData) => {
  try {
    const response = await api.post('/api/ad-locations/', adData);
    return response.data;
  } catch (error) {
    console.error('Error creating ad location:', error);
    throw error;
  }
};

// Usage:
const newAd = {
  name: 'Royal Hotel',
  district: 'Mysore',
  service_type: 'hotel',
  latitude: '12.3051',
  longitude: '76.6551',
  description: 'Luxury hotel near palace',
  contact_phone: '+91-9876543210',
  contact_email: 'info@royalhotel.com',
  website: 'https://royalhotel.com',
  address: 'Palace Road, Mysore',
  price_range: '₹₹₹',
  rating: '4.5',
  is_active: true
};

const created = await createAdLocation(newAd);
```

#### Update Ad Location
```javascript
export const updateAdLocation = async (id, adData) => {
  try {
    const response = await api.patch(`/api/ad-locations/${id}/`, adData);
    return response.data;
  } catch (error) {
    console.error(`Error updating ad location ${id}:`, error);
    throw error;
  }
};
```

#### Delete Ad Location
```javascript
export const deleteAdLocation = async (id) => {
  try {
    await api.delete(`/api/ad-locations/${id}/`);
    return true;
  } catch (error) {
    console.error(`Error deleting ad location ${id}:`, error);
    throw error;
  }
};
```

#### Filter by Service Type
```javascript
export const filterAdLocationsByService = async (serviceType) => {
  try {
    const response = await api.get('/api/ad-locations/', {
      params: { service_type: serviceType }
    });
    return response.data;
  } catch (error) {
    console.error('Error filtering by service type:', error);
    throw error;
  }
};

// Usage:
const hotels = await filterAdLocationsByService('hotel');
```

#### Get All Service Types
```javascript
export const getAllServiceTypes = async () => {
  try {
    const response = await api.get('/api/ad-locations/service_types/');
    return response.data.service_types;
  } catch (error) {
    console.error('Error fetching service types:', error);
    throw error;
  }
};

// Usage:
const serviceTypes = await getAllServiceTypes();
// Returns: [
//   {value: 'hotel', label: 'Hotel'},
//   {value: 'restaurant', label: 'Restaurant'},
//   ...
// ]
```

#### Get Locations Grouped by Service Type
```javascript
export const getLocationsByServiceType = async () => {
  try {
    const response = await api.get('/api/ad-locations/by_service_type/');
    return response.data;
  } catch (error) {
    console.error('Error fetching grouped ad locations:', error);
    throw error;
  }
};

// Returns: { 'hotel': [...], 'restaurant': [...] }
```

---

### 3. TRIP PLANNING APIs

#### Get All Trips
```javascript
export const getAllTrips = async () => {
  try {
    const response = await api.get('/api/trips/');
    return response.data;
  } catch (error) {
    console.error('Error fetching trips:', error);
    throw error;
  }
};
```

#### Get Single Trip
```javascript
export const getTripById = async (id) => {
  try {
    const response = await api.get(`/api/trips/${id}/`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching trip ${id}:`, error);
    throw error;
  }
};
```

#### Create Trip
```javascript
export const createTrip = async (tripData) => {
  try {
    const response = await api.post('/api/trips/', tripData);
    return response.data;
  } catch (error) {
    console.error('Error creating trip:', error);
    throw error;
  }
};

// Usage:
const newTrip = {
  title: 'Mysore Weekend Trip',
  start_date: '2025-10-20',
  end_date: '2025-10-22',
  num_days: 3,
  start_location_name: 'Bangalore',
  start_location_latitude: '12.9716',
  start_location_longitude: '77.5946',
  preferred_start_time: '09:00:00',
  preferred_end_time: '18:00:00'
};

const trip = await createTrip(newTrip);
```

#### Update Trip
```javascript
export const updateTrip = async (id, tripData) => {
  try {
    const response = await api.patch(`/api/trips/${id}/`, tripData);
    return response.data;
  } catch (error) {
    console.error(`Error updating trip ${id}:`, error);
    throw error;
  }
};
```

#### Delete Trip
```javascript
export const deleteTrip = async (id) => {
  try {
    await api.delete(`/api/trips/${id}/`);
    return true;
  } catch (error) {
    console.error(`Error deleting trip ${id}:`, error);
    throw error;
  }
};
```

#### Add Location to Trip
```javascript
export const addLocationToTrip = async (tripId, locationId, priority = 1) => {
  try {
    const response = await api.post(`/api/trips/${tripId}/add_location/`, {
      gi_location_id: locationId,
      priority: priority
    });
    return response.data;
  } catch (error) {
    console.error('Error adding location to trip:', error);
    throw error;
  }
};

// Usage:
await addLocationToTrip(1, 5, 1); // tripId=1, locationId=5, priority=1
```

#### Remove Location from Trip
```javascript
export const removeLocationFromTrip = async (tripId, selectedLocationId) => {
  try {
    const response = await api.post(`/api/trips/${tripId}/remove_location/`, {
      selected_location_id: selectedLocationId
    });
    return response.data;
  } catch (error) {
    console.error('Error removing location from trip:', error);
    throw error;
  }
};
```

#### Generate Trip Schedule (SMART ALGORITHM! ⭐)
```javascript
export const generateTripSchedule = async (tripId) => {
  try {
    const response = await api.post(`/api/trips/${tripId}/generate_schedule/`);
    return response.data;
  } catch (error) {
    console.error('Error generating schedule:', error);
    throw error;
  }
};

// Usage:
const schedule = await generateTripSchedule(1);
// Returns optimized day-by-day itinerary!
```

#### Get Trip Schedule
```javascript
export const getTripSchedule = async (tripId) => {
  try {
    const response = await api.get(`/api/trips/${tripId}/schedule/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching schedule:', error);
    throw error;
  }
};
```

#### Get Trip Days
```javascript
export const getTripDays = async (tripId) => {
  try {
    const response = await api.get(`/api/trips/${tripId}/days/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching trip days:', error);
    throw error;
  }
};
```

#### Get Selected Locations for Trip
```javascript
export const getSelectedLocations = async (tripId) => {
  try {
    const response = await api.get(`/api/trips/${tripId}/selected_locations/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching selected locations:', error);
    throw error;
  }
};
```

---

## 📦 Complete API Service File

Create `src/services/giyatraApi.js`:

```javascript
import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ========== GI LOCATIONS ==========

export const getAllGILocations = async (params = {}) => {
  const response = await api.get('/api/gi-locations/', { params });
  return response.data;
};

export const getGILocationById = async (id) => {
  const response = await api.get(`/api/gi-locations/${id}/`);
  return response.data;
};

export const createGILocation = async (data) => {
  const response = await api.post('/api/gi-locations/', data);
  return response.data;
};

export const createGILocationWithImage = async (formData) => {
  const response = await api.post('/api/gi-locations/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const updateGILocation = async (id, data) => {
  const response = await api.patch(`/api/gi-locations/${id}/`, data);
  return response.data;
};

export const deleteGILocation = async (id) => {
  await api.delete(`/api/gi-locations/${id}/`);
};

export const searchGILocations = async (searchTerm) => {
  const response = await api.get('/api/gi-locations/', {
    params: { search: searchTerm }
  });
  return response.data;
};

export const filterGILocationsByDistrict = async (district) => {
  const response = await api.get('/api/gi-locations/', {
    params: { district }
  });
  return response.data;
};

export const getAllDistricts = async () => {
  const response = await api.get('/api/gi-locations/districts/');
  return response.data.districts;
};

export const getLocationsByDistrict = async () => {
  const response = await api.get('/api/gi-locations/by_district/');
  return response.data;
};

// ========== AD LOCATIONS ==========

export const getAllAdLocations = async (params = {}) => {
  const response = await api.get('/api/ad-locations/', { params });
  return response.data;
};

export const getAdLocationById = async (id) => {
  const response = await api.get(`/api/ad-locations/${id}/`);
  return response.data;
};

export const createAdLocation = async (data) => {
  const response = await api.post('/api/ad-locations/', data);
  return response.data;
};

export const updateAdLocation = async (id, data) => {
  const response = await api.patch(`/api/ad-locations/${id}/`, data);
  return response.data;
};

export const deleteAdLocation = async (id) => {
  await api.delete(`/api/ad-locations/${id}/`);
};

export const filterAdLocationsByService = async (serviceType) => {
  const response = await api.get('/api/ad-locations/', {
    params: { service_type: serviceType }
  });
  return response.data;
};

export const getAllServiceTypes = async () => {
  const response = await api.get('/api/ad-locations/service_types/');
  return response.data.service_types;
};

export const getLocationsByServiceType = async () => {
  const response = await api.get('/api/ad-locations/by_service_type/');
  return response.data;
};

// ========== TRIP PLANNING ==========

export const getAllTrips = async () => {
  const response = await api.get('/api/trips/');
  return response.data;
};

export const getTripById = async (id) => {
  const response = await api.get(`/api/trips/${id}/`);
  return response.data;
};

export const createTrip = async (data) => {
  const response = await api.post('/api/trips/', data);
  return response.data;
};

export const updateTrip = async (id, data) => {
  const response = await api.patch(`/api/trips/${id}/`, data);
  return response.data;
};

export const deleteTrip = async (id) => {
  await api.delete(`/api/trips/${id}/`);
};

export const addLocationToTrip = async (tripId, locationId, priority = 1) => {
  const response = await api.post(`/api/trips/${tripId}/add_location/`, {
    gi_location_id: locationId,
    priority
  });
  return response.data;
};

export const removeLocationFromTrip = async (tripId, selectedLocationId) => {
  const response = await api.post(`/api/trips/${tripId}/remove_location/`, {
    selected_location_id: selectedLocationId
  });
  return response.data;
};

export const generateTripSchedule = async (tripId) => {
  const response = await api.post(`/api/trips/${tripId}/generate_schedule/`);
  return response.data;
};

export const getTripSchedule = async (tripId) => {
  const response = await api.get(`/api/trips/${tripId}/schedule/`);
  return response.data;
};

export const getTripDays = async (tripId) => {
  const response = await api.get(`/api/trips/${tripId}/days/`);
  return response.data;
};

export const getSelectedLocations = async (tripId) => {
  const response = await api.get(`/api/trips/${tripId}/selected_locations/`);
  return response.data;
};

export default api;
```

---

## 🎯 Example React Components

### 1. Display GI Locations

```javascript
import React, { useState, useEffect } from 'react';
import { getAllGILocations } from './services/giyatraApi';

function GILocationsList() {
  const [locations, setLocations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLocations();
  }, []);

  const fetchLocations = async () => {
    try {
      setLoading(true);
      const data = await getAllGILocations();
      setLocations(data.results);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h1>GI Locations</h1>
      <div className="grid">
        {locations.map(location => (
          <div key={location.id} className="card">
            {location.image && <img src={location.image} alt={location.name} />}
            <h3>{location.name}</h3>
            <p>{location.district}</p>
            <p>{location.description}</p>
            <p>Visit Duration: {location.typical_visit_duration} mins</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default GILocationsList;
```

### 2. Create GI Location Form

```javascript
import React, { useState } from 'react';
import { createGILocationWithImage } from './services/giyatraApi';

function CreateGILocation() {
  const [formData, setFormData] = useState({
    name: '',
    district: '',
    latitude: '',
    longitude: '',
    description: '',
    typical_visit_duration: 60,
  });
  const [image, setImage] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const data = new FormData();
    Object.keys(formData).forEach(key => {
      data.append(key, formData[key]);
    });
    if (image) {
      data.append('image', image);
    }

    try {
      const result = await createGILocationWithImage(data);
      alert('Location created successfully!');
      console.log(result);
    } catch (error) {
      alert('Error creating location');
      console.error(error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Add New GI Location</h2>
      
      <input
        name="name"
        placeholder="Name"
        value={formData.name}
        onChange={handleChange}
        required
      />
      
      <input
        name="district"
        placeholder="District"
        value={formData.district}
        onChange={handleChange}
        required
      />
      
      <input
        name="latitude"
        placeholder="Latitude"
        value={formData.latitude}
        onChange={handleChange}
        required
      />
      
      <input
        name="longitude"
        placeholder="Longitude"
        value={formData.longitude}
        onChange={handleChange}
        required
      />
      
      <textarea
        name="description"
        placeholder="Description"
        value={formData.description}
        onChange={handleChange}
        required
      />
      
      <input
        name="typical_visit_duration"
        type="number"
        placeholder="Visit Duration (minutes)"
        value={formData.typical_visit_duration}
        onChange={handleChange}
      />
      
      <input
        type="file"
        accept="image/*"
        onChange={handleImageChange}
      />
      
      <button type="submit">Create Location</button>
    </form>
  );
}

export default CreateGILocation;
```

### 3. Trip Planner Component

```javascript
import React, { useState, useEffect } from 'react';
import {
  getAllGILocations,
  createTrip,
  addLocationToTrip,
  generateTripSchedule
} from './services/giyatraApi';

function TripPlanner() {
  const [locations, setLocations] = useState([]);
  const [selectedLocations, setSelectedLocations] = useState([]);
  const [tripData, setTripData] = useState({
    title: '',
    start_date: '',
    end_date: '',
    num_days: 3,
    start_location_name: 'Bangalore',
    start_location_latitude: '12.9716',
    start_location_longitude: '77.5946',
    preferred_start_time: '09:00:00',
    preferred_end_time: '18:00:00'
  });
  const [schedule, setSchedule] = useState(null);

  useEffect(() => {
    fetchLocations();
  }, []);

  const fetchLocations = async () => {
    const data = await getAllGILocations();
    setLocations(data.results);
  };

  const handleLocationSelect = (locationId) => {
    if (selectedLocations.includes(locationId)) {
      setSelectedLocations(selectedLocations.filter(id => id !== locationId));
    } else {
      setSelectedLocations([...selectedLocations, locationId]);
    }
  };

  const handleCreateTrip = async () => {
    try {
      // 1. Create trip
      const trip = await createTrip(tripData);
      console.log('Trip created:', trip);

      // 2. Add selected locations
      for (let i = 0; i < selectedLocations.length; i++) {
        await addLocationToTrip(trip.id, selectedLocations[i], i + 1);
      }

      // 3. Generate schedule
      const scheduleData = await generateTripSchedule(trip.id);
      setSchedule(scheduleData.schedule);
      
      alert('Trip created and schedule generated!');
    } catch (error) {
      console.error('Error:', error);
      alert('Error creating trip');
    }
  };

  return (
    <div>
      <h1>Plan Your Trip</h1>
      
      {/* Trip Details Form */}
      <div>
        <input
          placeholder="Trip Title"
          value={tripData.title}
          onChange={(e) => setTripData({...tripData, title: e.target.value})}
        />
        <input
          type="date"
          value={tripData.start_date}
          onChange={(e) => setTripData({...tripData, start_date: e.target.value})}
        />
        <input
          type="date"
          value={tripData.end_date}
          onChange={(e) => setTripData({...tripData, end_date: e.target.value})}
        />
      </div>

      {/* Location Selection */}
      <div>
        <h2>Select Locations</h2>
        {locations.map(location => (
          <div key={location.id}>
            <input
              type="checkbox"
              checked={selectedLocations.includes(location.id)}
              onChange={() => handleLocationSelect(location.id)}
            />
            <label>{location.name} - {location.district}</label>
          </div>
        ))}
      </div>

      <button onClick={handleCreateTrip}>
        Create Trip & Generate Schedule
      </button>

      {/* Display Schedule */}
      {schedule && (
        <div>
          <h2>Your Optimized Schedule</h2>
          {schedule.days.map(day => (
            <div key={day.day_number}>
              <h3>Day {day.day_number} - {day.date}</h3>
              {day.items.map((item, idx) => (
                <div key={idx}>
                  <p>
                    {item.start_time} - {item.end_time}: {' '}
                    {item.item_type === 'location' && item.location.name}
                    {item.item_type === 'travel' && `Travel to ${item.to_location}`}
                    {item.item_type === 'break' && item.description}
                  </p>
                </div>
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default TripPlanner;
```

### 4. Search Component

```javascript
import React, { useState } from 'react';
import { searchGILocations } from './services/giyatraApi';

function SearchLocations() {
  const [searchTerm, setSearchTerm] = useState('');
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    const data = await searchGILocations(searchTerm);
    setResults(data.results);
  };

  return (
    <div>
      <input
        placeholder="Search locations..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <button onClick={handleSearch}>Search</button>

      <div>
        {results.map(location => (
          <div key={location.id}>
            <h3>{location.name}</h3>
            <p>{location.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default SearchLocations;
```

### 5. Hotels/Services Component

```javascript
import React, { useState, useEffect } from 'react';
import { getAllAdLocations, getAllServiceTypes } from './services/giyatraApi';

function ServicesPage() {
  const [services, setServices] = useState([]);
  const [serviceTypes, setServiceTypes] = useState([]);
  const [selectedType, setSelectedType] = useState('all');

  useEffect(() => {
    fetchServiceTypes();
    fetchServices();
  }, []);

  const fetchServiceTypes = async () => {
    const types = await getAllServiceTypes();
    setServiceTypes(types);
  };

  const fetchServices = async () => {
    const params = selectedType !== 'all' ? { service_type: selectedType } : {};
    const data = await getAllAdLocations(params);
    setServices(data.results);
  };

  useEffect(() => {
    fetchServices();
  }, [selectedType]);

  return (
    <div>
      <h1>Services</h1>
      
      {/* Filter by type */}
      <select value={selectedType} onChange={(e) => setSelectedType(e.target.value)}>
        <option value="all">All Services</option>
        {serviceTypes.map(type => (
          <option key={type.value} value={type.value}>
            {type.label}
          </option>
        ))}
      </select>

      {/* Display services */}
      <div className="grid">
        {services.map(service => (
          <div key={service.id} className="card">
            {service.image && <img src={service.image} alt={service.name} />}
            <h3>{service.name}</h3>
            <p>{service.service_type}</p>
            <p>{service.description}</p>
            <p>📞 {service.contact_phone}</p>
            <p>📧 {service.contact_email}</p>
            {service.website && (
              <a href={service.website} target="_blank" rel="noopener noreferrer">
                Visit Website
              </a>
            )}
            <p>Price: {service.price_range}</p>
            <p>Rating: {service.rating} ⭐</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ServicesPage;
```

---

## 🚀 Quick Start

### 1. Install in Your React App
```bash
npm install axios
```

### 2. Copy the API Service
Copy the complete `giyatraApi.js` file to your `src/services/` folder.

### 3. Import and Use
```javascript
import { getAllGILocations, createTrip } from './services/giyatraApi';

// In your component
const locations = await getAllGILocations();
```

### 4. Make Sure Backend is Running
```bash
cd backend
python manage.py runserver
```

---

## ⚙️ Configuration

### Update API Base URL
When deploying to production, update the base URL:

```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';
```

Add to `.env`:
```
REACT_APP_API_URL=https://your-backend-url.com
```

---

## 🎉 Summary

### ✅ What You Have:
- **26 Open APIs** - No authentication required
- **Complete React integration** - All API queries ready
- **Example components** - Copy-paste and use
- **No setup needed** - Just import and call

### 🚀 Ready to Use:
1. Backend is running at `http://127.0.0.1:8000`
2. All APIs are open (no auth)
3. Copy API service to your React app
4. Start building!

**Happy coding!** 🎨💻✨
