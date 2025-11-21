from flask import Flask
from config import FLASK_SECRET

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.secret_key = FLASK_SECRET

    # set insecure transport for local testing (http). Remove for production.
    import os
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    with app.app_context():
        from .routes import bp as routes_bp
        app.register_blueprint(routes_bp)
    return app
