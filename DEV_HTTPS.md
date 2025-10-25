Local HTTPS options for the Giyatra Django development server

This file summarizes easy ways to run your Django dev server over HTTPS on Windows (PowerShell). Pick one option.

1) Quick option: ngrok (no code changes)
- Pros: Easiest, provides a public HTTPS URL that tunnels to your local HTTP server. Works immediately.
- Cons: External tunnel, ephemeral public URL (unless you have paid plan), requires ngrok installed.

Steps:
1. Run your Django dev server normally (HTTP):

```powershell
# from project backend folder
python -m pip install -r requirements.txt
python manage.py runserver 0.0.0.0:8000
```

2. In a separate terminal, start ngrok (install from https://ngrok.com):

```powershell
# Forward local port 8000 to an HTTPS public URL
ngrok http 8000
```

3. ngrok will print an https:// URL you can use from your frontend (or directly in the browser). This avoids dealing with certificates locally.

---

2) Self-signed cert + django-sslserver (local HTTPS on your machine)
- Pros: Fully local, you keep the hostname as `localhost` or `0.0.0.0` and use HTTPS. Good for testing cookie/CSRF behavior.
- Cons: Browser will warn about the certificate (unless you import it/trust it). Using `mkcert` avoids warnings.

Steps (basic self-signed cert):

1. Install packages:

```powershell
python -m pip install -r requirements.txt
```

2. Generate a self-signed certificate and key (PowerShell / OpenSSL). If you have OpenSSL installed:

```powershell
# create cert and key
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout dev.key -out dev.crt -subj "/C=IN/ST=State/L=City/O=Dev/CN=localhost"
# Combine into a PEM if needed
type dev.key,dev.crt > dev.pem
```

3. Run the HTTPS dev server using django-sslserver's management command. Adjust paths to the generated cert/key.

```powershell
python manage.py runsslserver 0.0.0.0:8000 --certificate dev.crt --key dev.key
```

Notes:
- If your django-sslserver version accepts a single PEM file, pass the combined file (e.g. `--certificate dev.pem`).
- Browsers will show a warning for the self-signed cert. To avoid warnings use `mkcert` (see next section).

---

3) mkcert (trusted local cert) + django-sslserver (recommended for local trust)
- Pros: Trusted cert for `localhost` and development hostnames. No browser warnings after you install mkcert.
- Cons: Requires installing mkcert and nss/CA tools on Windows.

Steps:

1. Install mkcert (https://github.com/FiloSottile/mkcert#installation). On Windows the easiest is via Chocolatey:

```powershell
choco install mkcert
mkcert -install
```

2. Create cert for localhost (and other hostnames you need):

```powershell
mkcert localhost 127.0.0.1 ::1
# mkcert will produce files like localhost+2.pem and localhost+2-key.pem
```

3. Run django-sslserver with the generated cert and key:

```powershell
python manage.py runsslserver 0.0.0.0:8000 --certificate localhost+2.pem --key localhost+2-key.pem
```

Your browser should now trust the cert for `https://localhost:8000`.

---

4) Configuration reminders
- `DEBUG=True` is fine for local HTTPS testing. Your `settings.py` already sets `SESSION_COOKIE_SECURE` and `CSRF_COOKIE_SECURE` to False in DEBUG mode so cookies work over HTTP; if you switch to HTTPS locally and want to test secure cookie behavior set `DEBUG=False` and configure the environment variables accordingly.
- To test secure-cookie behavior locally over HTTPS you can export environment variables in PowerShell before running Django:

```powershell
$env:DEBUG="False";
$env:SESSION_COOKIE_SECURE="True";
$env:CSRF_COOKIE_SECURE="True";
python manage.py runsslserver 0.0.0.0:8000 --certificate dev.crt --key dev.key
```

- If you use ngrok, you can keep `DEBUG=True` locally and use the ngrok HTTPS URL for frontend callbacks.

---

5) Final notes and troubleshooting
- If the dev server prints "You're accessing the development server over HTTPS, but it only supports HTTP" it means you're attempting to use Django's regular `runserver` over HTTPS. Use `runsslserver` (or a proxy) instead.
- If you see CSRF issues after switching to HTTPS, ensure the frontend uses the HTTPS host that matches the certificate CN (e.g. `localhost`). Also ensure cookies are sent (use `fetch` with `credentials: 'include'`).

If you want, I can:
- Add a small `make` / PowerShell script to automate cert creation and start the HTTPS server.
- Apply a settings toggle to allow forcing `SESSION_COOKIE_SECURE`/`CSRF_COOKIE_SECURE` via an environment variable like `FORCE_SECURE_COOKIES`.

Tell me which option you prefer and I'll implement the small automation step (script or env toggle) for you.
