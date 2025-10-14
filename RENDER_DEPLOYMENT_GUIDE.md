# 🚀 Deploy GI Yatra Backend to Render

Complete guide to deploy your Django backend to Render.

---

## ✅ Pre-Deployment Checklist

All files are ready:
- ✅ `Procfile` - Gunicorn configuration
- ✅ `build.sh` - Build script for Render
- ✅ `requirements.txt` - Updated with production dependencies
- ✅ `settings.py` - Configured for production
- ✅ Code pushed to GitHub

---

## 🔧 Step 1: Create Render Account

1. Go to: https://render.com/
2. Click **"Get Started for Free"**
3. Sign up with your GitHub account
4. Authorize Render to access your repositories

---

## 🗄️ Step 2: Create PostgreSQL Database

1. From Render Dashboard, click **"New +"**
2. Select **"PostgreSQL"**
3. Fill in details:
   - **Name:** `giyatra-db`
   - **Database:** `giyatra`
   - **User:** `giyatra_user` (auto-filled)
   - **Region:** Choose closest to your users
   - **Plan:** Free
4. Click **"Create Database"**
5. **Wait for database to be created** (takes 1-2 minutes)
6. Once ready, **copy the Internal Database URL** (starts with `postgres://`)

---

## 🌐 Step 3: Create Web Service

1. From Render Dashboard, click **"New +"**
2. Select **"Web Service"**
3. Connect your GitHub repository:
   - Click **"Connect account"** if needed
   - Search for: `prana-vk/backend`
   - Click **"Connect"**

### Configure Web Service:

#### **Basic Settings:**
- **Name:** `giyatra-backend`
- **Region:** Same as your database
- **Branch:** `main`
- **Root Directory:** (leave blank)
- **Runtime:** `Python 3`
- **Build Command:** `./build.sh`
- **Start Command:** `gunicorn giyatra_project.wsgi:application`

#### **Plan:**
- Select **"Free"**

---

## ⚙️ Step 4: Environment Variables

Click **"Advanced"** and add these environment variables:

### Required Variables:

```
SECRET_KEY
django-insecure-CHANGE-THIS-TO-RANDOM-STRING-IN-PRODUCTION

DEBUG
False

ALLOWED_HOSTS
giyatra-backend.onrender.com,localhost,127.0.0.1

DATABASE_URL
postgres://giyatra_user:password@dpg-xxx.oregon-postgres.render.com/giyatra
(Paste the Internal Database URL from Step 2)

PYTHON_VERSION
3.12.0

CORS_ALLOWED_ORIGINS
https://your-frontend-domain.com,http://localhost:3000,http://localhost:5173
```

### Optional Variables:

```
DISABLE_COLLECTSTATIC
0
```

---

## 🔑 Step 5: Generate Secret Key

You need a secure SECRET_KEY for production. Generate one:

### Method 1: Python
```python
import secrets
print(secrets.token_urlsafe(50))
```

### Method 2: Online
Visit: https://djecrety.ir/

Copy the generated key and use it for `SECRET_KEY` environment variable.

---

## 🚀 Step 6: Deploy

1. Click **"Create Web Service"**
2. Render will:
   - Clone your repository
   - Install dependencies
   - Run migrations
   - Collect static files
   - Start your app
3. Wait for deployment (5-10 minutes for first deployment)
4. Once deployed, you'll see **"Your service is live 🎉"**

---

## 🧪 Step 7: Test Your API

Your API will be available at: `https://giyatra-backend.onrender.com`

### Test Endpoints:

```bash
# Test home endpoint
curl https://giyatra-backend.onrender.com/api/gi-locations/

# Test in browser
https://giyatra-backend.onrender.com/api/gi-locations/
```

---

## 📝 Step 8: Create Superuser (Optional)

To access Django admin:

1. Go to Render Dashboard
2. Click on your `giyatra-backend` service
3. Click **"Shell"** tab
4. Run:
```bash
python manage.py createsuperuser
```
5. Follow prompts to create admin user
6. Access admin at: `https://giyatra-backend.onrender.com/admin/`

---

## 🔄 Future Updates

When you make changes to your code:

```bash
# 1. Commit changes
git add .
git commit -m "Your update message"

# 2. Push to GitHub
git push origin main

# 3. Render auto-deploys!
# Watch deployment in Render Dashboard
```

---

## 🌍 Update Frontend CORS

After deployment, update your frontend to use the production API:

### In your React app:

```javascript
// Change from:
const API_BASE_URL = 'http://127.0.0.1:8000';

// To:
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://giyatra-backend.onrender.com';
```

### Update CORS in Render:

Add your frontend domain to `CORS_ALLOWED_ORIGINS` environment variable:
```
CORS_ALLOWED_ORIGINS=https://your-react-app.com,http://localhost:3000
```

---

## 🔍 Troubleshooting

### Deployment Failed?

**Check Logs:**
1. Go to Render Dashboard
2. Click your service
3. Click **"Logs"** tab
4. Look for error messages

**Common Issues:**

#### Issue: Build failed
**Solution:** Check `build.sh` permissions
```bash
# Run locally:
chmod +x build.sh
git add build.sh
git commit -m "Fix build.sh permissions"
git push
```

#### Issue: Database connection failed
**Solution:** 
- Verify `DATABASE_URL` in environment variables
- Ensure it's the **Internal Database URL** from PostgreSQL service

#### Issue: Static files not loading
**Solution:**
- Check `STATIC_ROOT` in settings.py
- Verify `whitenoise` is installed
- Run `python manage.py collectstatic` manually in Shell

#### Issue: Module not found
**Solution:**
- Check `requirements.txt` includes all dependencies
- Verify Python version matches

---

## 📊 Monitor Your Service

### Check Service Health:

- **Dashboard:** https://dashboard.render.com/
- **Metrics:** CPU, Memory usage
- **Logs:** Real-time application logs
- **Events:** Deployment history

### Free Plan Limitations:

- ⚠️ Service **sleeps after 15 minutes** of inactivity
- First request after sleep takes **~1 minute** to wake up
- 750 hours/month free (enough for 1 service)
- Upgrade to paid plan for always-on service

---

## 🎯 Production Checklist

Before going live:

- [ ] Set `DEBUG=False`
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up PostgreSQL database
- [ ] Configure CORS for production frontend
- [ ] Test all API endpoints
- [ ] Create superuser for admin
- [ ] Set up monitoring/logging
- [ ] Consider upgrading from free plan

---

## 📦 Your Deployment URLs

After deployment, you'll have:

- **API Base:** `https://giyatra-backend.onrender.com`
- **Admin:** `https://giyatra-backend.onrender.com/admin/`
- **API Docs:** Share updated API URLs with frontend team

### All Endpoints:

```
GI Locations:
  https://giyatra-backend.onrender.com/api/gi-locations/

Ad Locations:
  https://giyatra-backend.onrender.com/api/ad-locations/

Trips:
  https://giyatra-backend.onrender.com/api/trips/
```

---

## 🔐 Security Notes

### Protect Your Keys:

- ✅ Never commit `.env` file
- ✅ Use environment variables in Render
- ✅ Generate strong SECRET_KEY
- ✅ Keep DEBUG=False in production
- ✅ Configure ALLOWED_HOSTS properly

### GitHub Security:

Your repo is public, but:
- ✅ `.gitignore` excludes `.env`
- ✅ Secrets are in Render environment variables
- ✅ Database credentials not in code

---

## 💡 Pro Tips

### 1. Custom Domain (Optional)
- Buy domain from Namecheap/GoDaddy
- Add to Render: Settings → Custom Domain
- Update DNS records

### 2. SSL Certificate
- ✅ Automatically provided by Render
- Your API will be served over HTTPS

### 3. Monitoring
- Set up Render notification webhooks
- Use external monitoring (UptimeRobot, etc.)

### 4. Backups
- Render Free plan: No automatic backups
- Paid plan: Daily automatic backups
- Manual: Use `pg_dump` to backup database

---

## 🎉 Success!

Your Django backend is now live on Render! 🚀

**Next Steps:**
1. Test all APIs
2. Share URL with frontend team
3. Update React app API base URL
4. Deploy frontend

**Your API:** `https://giyatra-backend.onrender.com`

---

## 📚 Resources

- **Render Docs:** https://render.com/docs
- **Django Deployment:** https://docs.djangoproject.com/en/5.0/howto/deployment/
- **Render Support:** https://render.com/support

---

**Happy Deploying!** 🎊
