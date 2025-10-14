"""
Create superuser script for production deployment
Run this on Render Shell to create admin user
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'giyatra_project.settings')
django.setup()

from django.contrib.auth.models import User

def create_superuser():
    """Create superuser if it doesn't exist"""
    
    # Default admin credentials (change these!)
    username = 'admin'
    email = 'admin@giyatra.com'
    password = 'GiYatra2025Admin!'  # Change this to a strong password
    
    if User.objects.filter(username=username).exists():
        print(f"✅ Superuser '{username}' already exists!")
        user = User.objects.get(username=username)
        print(f"📧 Email: {user.email}")
        print(f"🔑 Admin Status: {'Yes' if user.is_superuser else 'No'}")
        print(f"👤 Staff Status: {'Yes' if user.is_staff else 'No'}")
        print(f"📅 Last Login: {user.last_login or 'Never'}")
        return user
    
    try:
        # Create superuser
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"🎉 Superuser '{username}' created successfully!")
        print(f"📧 Email: {email}")
        print(f"🔑 Password: {password}")
        print(f"🌐 Login URL: https://backend-k4x8.onrender.com/admin-panel/")
        print("\n⚠️  IMPORTANT: Change the password after first login!")
        return user
        
    except Exception as e:
        print(f"❌ Error creating superuser: {str(e)}")
        return None

if __name__ == '__main__':
    print("🚀 Creating superuser for GI Yatra Admin Panel...\n")
    print("=" * 50)
    create_superuser()
    print("=" * 50)
    print("✅ Done!")