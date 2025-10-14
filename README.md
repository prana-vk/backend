# GI Yatra Backend

Django REST API for Karnataka travel planning with smart itinerary generation.

**🌐 Live API:** https://backend-k4x8.onrender.com

---

## 🚀 Quick Start

### Local Development:
```bash
cd backend
python manage.py runserver
```

**Local Server:** http://127.0.0.1:8000  
**Production API:** https://backend-k4x8.onrender.com  
**✅ No authentication required** - All 26 APIs are open!

---

## 📖 Documentation

### **For React Developers:**
→ **REACT_INTEGRATION_GUIDE.md** ⭐
- All 26 API queries as functions
- 5 ready-to-use React components
- Complete integration guide

### **For API Reference:**
→ **ALL_APIS.md**
- Complete list of 26 endpoints
- Request/response examples
- cURL commands

### **For Setup:**
→ **QUICK_START.md**
- 5-minute setup guide
- Testing instructions

---

## 🎯 Features

### GI Locations (10 APIs)
- CRUD operations
- Search & filter by district
- Image upload support
- Get all districts
- Group by district

### Advertisement Locations (8 APIs)
- Hotels, restaurants, guides, transport
- Filter by service type
- Contact information
- Price range & ratings

### Trip Planning (8 APIs)
- Create multi-day trips
- Add/remove locations
- **Smart schedule generation** ⭐
- Route optimization
- Time slot management

---

## 🔧 Tech Stack

- Django 5.0.7
- Django REST Framework 3.14.0
- SQLite (development)
- CORS enabled for React
- Image upload support
- No authentication (open APIs)

---

## 📊 API Endpoints

```
Base URL: http://127.0.0.1:8000

GI Locations:
  GET    /api/gi-locations/
  POST   /api/gi-locations/
  GET    /api/gi-locations/{id}/
  GET    /api/gi-locations/districts/
  ...and 6 more

Ad Locations:
  GET    /api/ad-locations/
  POST   /api/ad-locations/
  GET    /api/ad-locations/service_types/
  ...and 5 more

Trip Planning:
  GET    /api/trips/
  POST   /api/trips/
  POST   /api/trips/{id}/generate_schedule/  ⭐
  ...and 5 more
```

See **ALL_APIS.md** for complete list.

---

## 💻 React Integration

### Install Axios
```bash
npm install axios
```

### Copy API Service
Copy the complete service from **REACT_INTEGRATION_GUIDE.md** to your React app:
```javascript
import { getAllGILocations, createTrip } from './services/giyatraApi';

// Use anywhere!
const locations = await getAllGILocations();
const trip = await createTrip(tripData);
```

**No authentication setup needed!**

---

## 🗂️ Project Structure

```
backend/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── .env
│
├── giyatra_project/        # Settings & URLs
├── home/                   # GI Locations
├── adver/                  # Advertisements
└── itinerary/              # Trip Planning
    └── schedule_generator.py  # Smart algorithm
```

---

## 🔑 Key Algorithms

### Route Optimization
- **Haversine formula** for distance calculation
- **Nearest neighbor algorithm** for optimal route
- **Time slot management** with buffers
- **Automatic scheduling** across multiple days

### Smart Features
- Travel time calculation (40 km/h average)
- Lunch break insertion at 13:00
- Visit duration management
- Multi-day distribution

---

## 🧪 Test APIs

### Browser
```
http://127.0.0.1:8000/api/gi-locations/
```

### cURL
```bash
curl http://127.0.0.1:8000/api/gi-locations/
```

### React
```javascript
fetch('http://127.0.0.1:8000/api/gi-locations/')
  .then(res => res.json())
  .then(data => console.log(data));
```

---

## 🎨 Admin Panel (Optional)

Create superuser to access Django admin at `/admin/`:

```bash
python manage.py createsuperuser
```

Then visit: http://127.0.0.1:8000/admin/

---

## 📝 Environment Variables

Copy `.env.example` to `.env` and configure:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

---

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up static files (Whitenoise/AWS S3)
- [ ] Configure CORS for production domains
- [ ] Add rate limiting (optional)
- [ ] Add authentication (optional)

---

## 📚 API Documentation

All documentation is in the `backend/` folder:

1. **REACT_INTEGRATION_GUIDE.md** - Complete React integration
2. **ALL_APIS.md** - 26 API endpoints reference  
3. **QUICK_START.md** - Quick setup guide

---

## ✅ Summary

- ✅ 26 open APIs (no auth required)
- ✅ Smart scheduling algorithm
- ✅ React-ready with CORS
- ✅ Image upload support
- ✅ Complete documentation
- ✅ Admin panel for data management

**Ready to use!** Start with **REACT_INTEGRATION_GUIDE.md** for frontend integration.

---

**Built with Django & Django REST Framework** 🚀
