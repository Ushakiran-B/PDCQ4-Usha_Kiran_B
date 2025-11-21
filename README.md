# Flask Google OAuth (Structured Project)

## What this is
A small Flask application demonstrating Sign in with Google (OAuth) with a clean file structure.
After signing in, the app shows the user's name, email, a sign-out link, and the current Indian time (Asia/Kolkata).

## Setup (Local)

1. Create OAuth credentials at https://console.cloud.google.com/apis/credentials
   - Application type: Web application
   - Add redirect URI: `http://localhost:5000/callback`
   - Copy **Client ID** and **Client Secret**

2. Create a `.env` file (or set env variables in your shell):
   ```env
   GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-client-secret
   FLASK_SECRET=a-random-secret
   REDIRECT_URI=http://localhost:5000/callback
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   python run.py
   ```

5. Open `http://localhost:5000` in your browser and click "Sign in with Google".

## Files
- `run.py` - entrypoint
- `config.py` - config using environment variables
- `app/` - Flask application package
  - `__init__.py` - app factory
  - `routes.py` - route handlers
  - `oauth.py` - Google OAuth flow helpers
  - `templates/` - HTML templates
  - `static/` - CSS

## Notes
- For local development we set `OAUTHLIB_INSECURE_TRANSPORT=1` to allow http redirect on localhost.
- Do NOT keep production client secrets in code. Use secrets manager/env vars.
