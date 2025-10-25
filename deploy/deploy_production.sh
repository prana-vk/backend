#!/usr/bin/env bash
# Minimal production deployment helper (Ubuntu/Debian)
# This script is a template and performs these actions:
# - creates a python virtualenv
# - installs requirements
# - runs migrations and collectstatic
# - creates a systemd service file for gunicorn (template)
# - outputs the nginx site config path to copy/enable

set -euo pipefail
APP_DIR=$(cd "$(dirname "$0")/.." && pwd)
VENV_DIR="$APP_DIR/.venv"
USER=www-data
GROUP=www-data
SERVICE_NAME=giyatra
GUNICORN_SOCKET=/run/gunicorn-${SERVICE_NAME}.sock

echo "Deploying to $APP_DIR"

if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip
pip install -r "$APP_DIR/requirements.txt"

# Apply migrations and collectstatic
cd "$APP_DIR"
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Create systemd service file
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
cat <<'EOF' | sudo tee "$SERVICE_FILE"
[Unit]
Description=gunicorn daemon for Giyatra
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=${APP_DIR}
ExecStart=${APP_DIR}/.venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:${GUNICORN_SOCKET} giyatra_project.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now ${SERVICE_NAME}

# Nginx config template location
NGINX_SITE="/etc/nginx/sites-available/giyatra"
cat <<'EOF' > "$APP_DIR/deploy/nginx_giyatra.conf"
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    location /static/ {
        alias ${APP_DIR}/staticfiles/;
    }

    location /media/ {
        alias ${APP_DIR}/media/;
    }

    location / {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://unix:${GUNICORN_SOCKET};
    }
}
EOF

sudo mv "$APP_DIR/deploy/nginx_giyatra.conf" /etc/nginx/sites-available/giyatra
sudo ln -sf /etc/nginx/sites-available/giyatra /etc/nginx/sites-enabled/giyatra
sudo nginx -t
sudo systemctl restart nginx

echo "Deployment template finished. If you have a public domain, run certbot to obtain TLS certs."

echo "Example: sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com"

echo "If you need rollback, stop the systemd service: sudo systemctl stop ${SERVICE_NAME}"