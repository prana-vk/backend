#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🔧 Installing dependencies..."
pip install -r requirements.txt

echo "🗄️ Checking database connection..."
python manage.py check --database default

echo "📋 Making migrations..."
python manage.py makemigrations

echo "🔄 Running migrations..."
python manage.py migrate --verbosity=2

echo "📦 Collecting static files..."
python manage.py collectstatic --no-input

echo "✅ Build completed successfully!"