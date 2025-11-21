import os

# Load from environment variables. For local development you can create a .env file
# and load these values into your environment.
# Required:
#   - GOOGLE_CLIENT_ID
#   - GOOGLE_CLIENT_SECRET
#   - FLASK_SECRET (a random string for Flask session)
#
# Redirect URI set in Google Cloud Console should be: http://localhost:5000/callback
