<#
Start HTTPS Test Server (Windows PowerShell)

This script helps run the Django app locally on a Windows test server in HTTPS/production-like
mode using mkcert and django-sslserver. It does the following:

Usage:
  # From the repository root (backend folder)
  powershell -ExecutionPolicy Bypass -File .\scripts\start_https_test_server.ps1

Notes:
    choco install mkcert
    mkcert -install

  It does not edit your .env file.
#>

param(
    [switch]$SkipInstall  # If passed, script will not run pip install -r requirements.txt
)

function Write-Info($msg){ Write-Host "[INFO] $msg" -ForegroundColor Cyan }
function Write-Warn($msg){ Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Write-ErrorAndExit($msg){ Write-Host "[ERROR] $msg" -ForegroundColor Red; exit 1 }

Set-Location -Path (Split-Path -Path $MyInvocation.MyCommand.Definition -Parent)\..\

Write-Info "Working directory: $(Get-Location)"

# Check for python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-ErrorAndExit "Python not found in PATH. Please install Python 3.10+ and ensure 'python' is on PATH."
}

# Check for mkcert
$mkcertCmd = Get-Command mkcert -ErrorAction SilentlyContinue
if (-not $mkcertCmd) {
    Write-Warn "mkcert not found. To create trusted local certs install mkcert (recommended):"
    Write-Host "  choco install mkcert" -ForegroundColor Yellow
    Write-Host "  mkcert -install" -ForegroundColor Yellow
    Write-Host "After installing mkcert, re-run this script. Alternatively create a self-signed cert manually and run runsslserver with --certificate/--key." -ForegroundColor Yellow
    Read-Host -Prompt "Press Enter to continue and attempt to run without mkcert (you will likely see browser warnings), or Ctrl+C to abort"
}

# Generate certs (if mkcert available)
$certFile = "localhost+2.pem"
$keyFile = "localhost+2-key.pem"
if (Get-Command mkcert -ErrorAction SilentlyContinue) {
    Write-Info "Generating/refreshing mkcert certificate for localhost and 127.0.0.1"
    & mkcert -install | Out-Null
    & mkcert localhost 127.0.0.1 ::1 | Out-Null
    # mkcert names files like localhost+2.pem and localhost+2-key.pem in current folder
    if (-not (Test-Path $certFile) -or -not (Test-Path $keyFile)) {
        Write-Warn "Expected mkcert output files not found. Listing directory:"
        Get-ChildItem -File | Format-Table Name,Length
    }
} else {
    Write-Warn "mkcert not available — you can still use a self-signed cert, but your browser will warn."
    if (-not (Test-Path $certFile) -or -not (Test-Path $keyFile)) {
        Write-Warn "No cert found at $certFile and $keyFile. You may create them manually or install mkcert."
    }
}

# Optionally install Python requirements
if (-not $SkipInstall) {
    Write-Info "Installing Python requirements (may take a minute)..."
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
}

# Set environment variables for this session only
Write-Info "Setting environment variables for HTTPS test run (temporary)"
$env:DEBUG = "False"
$env:ALLOWED_HOSTS = "localhost,127.0.0.1"
$env:SITE_URL = "https://localhost:8000"
$env:FRONTEND_URL = "https://localhost:3000"
$env:SESSION_COOKIE_SECURE = "True"
$env:CSRF_COOKIE_SECURE = "True"
$env:SECURE_SSL_REDIRECT = "True"
$env:EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

Write-Info "Collecting static files (if required)"
python manage.py collectstatic --noinput

if (-not (Test-Path $certFile) -or -not (Test-Path $keyFile)) {
    Write-Warn "Certificate or key file not found. The server will start but browsers will warn about the certificate."
}

Write-Info "Starting HTTPS dev server on https://0.0.0.0:8000"
python manage.py runsslserver 0.0.0.0:8000 --certificate $certFile --key $keyFile
