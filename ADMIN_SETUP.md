# 🔐 Admin Panel Setup Instructions

Your GI Yatra backend now has a **3-Factor Authentication system** that requires username, email, and password to match environment variables.

---

## 🚀 **Quick Setup on Render:**

### **Step 1: Set Environment Variables**

Go to your Render service → **Environment** → Add these **3 variables**:

```
ADMIN_USERNAME = admin
ADMIN_EMAIL = admin@giyatra.com
ADMIN_PASSWORD = YourSecurePassword123!
```

### **Step 2: Access Admin Panel**

1. **URL:** https://backend-k4x8.onrender.com/admin-panel/
2. **Enter ALL 3 credentials:** Username, Email, AND Password
3. **All must match exactly** - 3-factor authentication
4. **Start adding locations!**

---

## 🔒 **Security Features:**

✅ **3-Factor Authentication** - Username, Email, AND Password must all match  
✅ **Environment-Based Auth** - Credentials stored securely in environment variables  
✅ **Auto User Creation** - Admin user created automatically if it doesn't exist  
✅ **Triple Validation** - Checks all three credentials + Django auth  
✅ **No Database Dependencies** - Works even with empty database  

---

## 📱 **Admin Panel Features:**

- **Dashboard** - Stats and quick actions
- **GI Locations** - Add tourist spots with images, timings, coordinates
- **Ad Locations** - Add hotels, restaurants, guides, transport services
- **Bulk Add Data** - Instantly populate with 9 sample locations
- **Mobile Responsive** - Works on all devices

---

## 🎯 **How It Works:**

1. **Login Page** asks for Username, Email, AND Password
2. **Validates ALL THREE** against environment variables
3. **If all match**, creates Django user automatically (if doesn't exist)
4. **Authenticates** and grants access to admin panel
5. **All operations** are secured and logged

---

## 🛡️ **Security Notes:**

- **3-Factor Authentication**: Username + Email + Password must ALL match
- Only users with ALL correct environment credentials can access
- Admin user is automatically created with superuser permissions
- All forms protected with CSRF tokens
- Session management for secure logout

---

**Your admin panel is ready to use!** 🎉

Visit: https://backend-k4x8.onrender.com/admin-panel/