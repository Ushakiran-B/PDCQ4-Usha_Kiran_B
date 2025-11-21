import google.auth.transport.requests
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, REDIRECT_URI
SCOPES = [
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email',
    'openid'
]

def _client_config():
    return {
        "web": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "redirect_uris": [REDIRECT_URI]
        }
    }

def create_flow(state=None):
    flow = Flow.from_client_config(
        _client_config(),
        scopes=SCOPES,
        state=state
    )
    flow.redirect_uri = REDIRECT_URI
    return flow

# === UPDATE THIS FUNCTION ===
def verify_id_token(id_token_str):
    """
    Verifies Google ID token and allows 1 minute clock skew to prevent
    'Token used too early' errors.
    """
    request = google.auth.transport.requests.Request()
    id_info = id_token.verify_oauth2_token(
        id_token_str,
        request,
        audience=GOOGLE_CLIENT_ID,
        clock_skew_in_seconds=60  # allow 1 minute of skew
    )
    return id_info
