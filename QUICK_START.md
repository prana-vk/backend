# 🚀 Quick Start Guide - GI Yatra Backend

## ⚡ 5-Minute Setup

### Step 1: Activate Virtual Environment
```bash
cd backend
env\Scripts\activate  # Windows
```

### Step 2: Install Dependencies (if not already done)
```bash
pip install -r requirements.txt
```

### Step 3: Run Migrations (if not already done)
```bash
python manage.py migrate
```

### Step 4: Start Server
```bash
python manage.py runserver
```

**✅ Server Running:** http://127.0.0.1:8000/

**✅ No Authentication Required!** All APIs are open and ready to use!

---

## 🎯 Test the Backend in 3 Steps

### 1. Test the API (No Login Needed!)
Open browser or Postman:
```
GET http://127.0.0.1:8000/api/gi-locations/
```

You'll see all locations in JSON format! 🎉

### 2. Create Your First GI Location (via API)
**Method:** POST  
**URL:** http://127.0.0.1:8000/api/gi-locations/  
**Body:**
```json
{
  "name": "Mysore Palace",
  "district": "Mysore",
  "latitude": "12.305200",
  "longitude": "76.655100",
  "description": "Historic royal palace of Mysore",
  "typical_visit_duration": 120
}
```

### 3. View All Locations
```
GET http://127.0.0.1:8000/api/gi-locations/
```

**No authentication needed!** 🎉

---

## 📋 Optional: Use Admin Panel

### Create Superuser (Optional)
```bash
python manage.py createsuperuser
```
Enter username, email, and password when prompted.

### Access Admin Panel
- **URL:** http://127.0.0.1:8000/admin/
- Login with your superuser credentials
- You'll see: GI Locations, Ad Locations, Trip Plans, etc.

### Add Locations via Admin:
1. Admin → GI Locations → Add
2. Fill all fields + upload image
3. Save

---

## 🧪 Test Trip Planning
{
  "username": "traveler1",
  "password": "SecurePass123!"
}
```

Save the session cookie for next requests!

### 3. Create Trip
**Method:** POST  
**URL:** http://127.0.0.1:8000/api/trips/  
**Headers:** Cookie: sessionid=... (from login)  
**Body:**
### 1. Create Trip (No Auth Required!)
**Method:** POST  
**URL:** http://127.0.0.1:8000/api/trips/  
**Body:**
```json
{
  "title": "My Karnataka Tour",
  "start_location_name": "Bangalore",
  "start_location_latitude": "12.971600",
  "start_location_longitude": "77.594600",
  "start_date": "2025-10-25",
  "end_date": "2025-10-27",
  "num_days": 3,
  "preferred_start_time": "09:00:00",
  "preferred_end_time": "18:00:00"
}
```

### 2. Add Locations to Trip
**Method:** POST  
**URL:** http://127.0.0.1:8000/api/trips/1/add_location/  
**Body:**
```json
{
  "gi_location_id": 1,
  "priority": 1
}
```

### 3. Generate Schedule (Magic Happens Here! ✨)
**Method:** POST  
**URL:** http://127.0.0.1:8000/api/trips/1/generate_schedule/

**Response:** Complete day-by-day schedule with time slots!

---

## 📊 Available Endpoints

### Quick Reference (No Auth Required!):
```
GI Locations:
  GET    /api/gi-locations/
  POST   /api/gi-locations/
  GET    /api/gi-locations/{id}/
  PUT    /api/gi-locations/{id}/
  DELETE /api/gi-locations/{id}/
  GET    /api/gi-locations/districts/
  GET    /api/gi-locations/by_district/

Ad Locations:
  GET    /api/ad-locations/
  POST   /api/ad-locations/
  GET    /api/ad-locations/{id}/
  GET    /api/ad-locations/service_types/
  GET    /api/ad-locations/by_service_type/

Trip Planning:
  GET    /api/trips/
  POST   /api/trips/
  POST   /api/trips/{id}/add_location/
  POST   /api/trips/{id}/generate_schedule/  ⭐
  GET    /api/trips/{id}/schedule/
```

**Total: 26 Open APIs** - See **ALL_APIS.md** for complete reference

---

## 🎨 Admin Panel Features

### What You Can Do:
- ✅ Add/Edit/Delete GI Locations
- ✅ Upload images for locations
- ✅ Manage service advertisements
- ✅ View all user trips
- ✅ See generated schedules
- ✅ Manage users
- ✅ Search and filter everything

---

## 🔧 Common Commands

```bash
# Start server
python manage.py runserver

# Create superuser
python manage.py createsuperuser

# Make migrations (after model changes)
python manage.py makemigrations
python manage.py migrate

# Open Django shell
python manage.py shell

# Create new app
python manage.py startapp appname
```

---

## 🌐 CORS Settings

Frontend URLs already configured:
- http://localhost:3000 (React default)
- http://localhost:5173 (Vite default)

To add more, edit `giyatra_project/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://your-frontend-url",  # Add here
]
```

---

## 📦 File Upload

Images are saved to `/media/` directory:
- GI location images: `/media/gi_locations/`
- Ad location images: `/media/ad_locations/`

Access via: `http://127.0.0.1:8000/media/gi_locations/image.jpg`

---

## 🐛 Troubleshooting

### Server won't start?
```bash
# Check if migrations are done
python manage.py migrate

# Check for errors
python manage.py check
```

### Can't login to admin?
```bash
# Create/reset superuser
python manage.py createsuperuser
```

### API returns 401 Unauthorized?
- Make sure you're logged in (use /api/auth/login/)
- Include session cookie in requests
- Or use Django admin session

### CORS errors from frontend?
- Check `CORS_ALLOWED_ORIGINS` in settings.py
- Make sure `corsheaders` is in `INSTALLED_APPS`
- Verify middleware order

---

## 📱 Testing Tools

### Recommended:
1. **Postman** - GUI for API testing
2. **Thunder Client** - VS Code extension
3. **cURL** - Command line
4. **Browser** - For GET requests

### Browser Extensions:
- JSON Viewer
- ModHeader (for cookies)

---

## 🎯 Next Steps

1. ✅ **Add Sample Data** - Create 5-10 GI locations
2. ✅ **Test All APIs** - Use Postman
3. ✅ **Generate a Schedule** - Test the algorithm
4. ✅ **Share API Docs** - With frontend team
5. ✅ **Start Frontend Development** - Connect to APIs

---

## 📚 Documentation

- **README.md** - Full setup guide
- **API_DOCUMENTATION.md** - Complete API reference
- **PROJECT_COMPLETION_SUMMARY.md** - What's been built
- **This File** - Quick start guide

---

## ✅ Checklist for Success

- [ ] Server running (python manage.py runserver)
- [ ] Superuser created
- [ ] Admin panel accessible
- [ ] Added at least 3 GI locations
- [ ] Added at least 2 service locations
- [ ] Tested user registration
- [ ] Created a trip via API
- [ ] Generated schedule successfully
- [ ] Frontend team has API documentation

---

## 🎉 You're All Set!

The backend is **fully operational** and ready for:
- ✅ Adding locations via admin
- ✅ API integration with frontend
- ✅ Creating and managing trips
- ✅ Generating smart schedules

**Happy Building! 🚀**

---

## 💡 Pro Tips

1. **Use Admin Panel** for quick data entry
2. **Test APIs** with Postman before frontend integration
3. **Check logs** in terminal if something fails
4. **Read API_DOCUMENTATION.md** for request/response formats
5. **Generate schedules** with different trip configurations to test algorithm

---

**Need Help?**
- Check README.md for detailed information
- See API_DOCUMENTATION.md for endpoint details
- Review PROJECT_COMPLETION_SUMMARY.md for overview

**Everything is documented and ready to use!** 📖✨
