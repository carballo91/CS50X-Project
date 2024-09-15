from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel, format_datetime
from flask_cors import CORS
from flask_session import Session
from flask_socketio import SocketIO
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from dotenv import load_dotenv
from app.models import User

from .helpers import generate_nonce
import pytz
import logging
import os

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('flask-limiter')

session = Session()
babel = Babel()
csrf = CSRFProtect()

migrate = Migrate()
socketio = SocketIO(async_mode='eventlet' ,cors_allowed_origins="*")
talisman = Talisman()

#Change config_name to 'development' when you are ready to use if for development
def create_app(config_name='production'):
    app = Flask(__name__)
    
    #check if config_name is None
    if config_name is None:
        config_name = os.getenv('FLASK_ENV','default')
    #Loads configutarion
    from config import config
    app.config.from_object(config[config_name])

    from .models import db, login_manager
    db.init_app(app)
    login_manager.init_app(app)
    
    from app.blueprints.login.routes import limiter
    limiter.init_app(app)

    session.init_app(app)
    babel.init_app(app)
    csrf.init_app(app)
    CORS(app,origins=[f"http://{{ip_where_server_is_running}}"])
    migrate.init_app(app, db)
    socketio.init_app(app)

    # Content Security Policy (CSP) Header
    csp = {
        
        'default-src' : ["'self'"],
        'script-src' : ["'self'", 
                        'https://code.jquery.com', 
                        'https://cdnjs.cloudflare.com',
                        'https://cdn.jsdelivr.net'],
        'style-src' : ["'self'","'unsafe-inline'",'https://cdn.jsdelivr.net'],
        'img-src' : ["'self'",'data:'],
        'font-src' : ["'self'", 'https://fonts.googleapis.com', 'https://fonts.gstatic.com'],
        'connect-src': ["'self'","http://127.0.0.1", "http://127.0.0.1:8000", "http://localhost", "ws://localhost","http://127.0.0.1:5000"],
        'object-src': ["'none'"],
        'media-src': ["'self'"],
        'frame-src': ["'self'"],
        'base-uri': ["'self'"],
        'form-action': ["'self'"],
        'frame-ancestors': ["'self'"],
        'worker-src': ["'self'"]
    }
    
    nonce_list = ['default-src', 'script-src', 'style-src']
    
    talisman = Talisman(app, content_security_policy=csp, content_security_policy_nonce_in=nonce_list)

    # Enforce HTTPS and other headers
    talisman.force_https = False
    talisman.session_cookie_secure = True
    talisman.strict_transport_security = True
    talisman.strict_transport_security_max_age = 31536000
    talisman.strict_transport_security_include_subdomains = True

    
    from app.models import admin
    admin.init_app(app)

    # Register blueprints
    from .blueprints.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .blueprints.patient import patient as patient_blueprint
    app.register_blueprint(patient_blueprint)

    from .blueprints.consultation import consultation as consultation_blueprint
    app.register_blueprint(consultation_blueprint)

    from .blueprints.reports import reports as reports_blueprint
    app.register_blueprint(reports_blueprint)

    from .blueprints.login import login as login_blueprint
    app.register_blueprint(login_blueprint)
    

    @app.after_request
    def apply_caching(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response


    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        db.session.rollback()
        return render_template('500.html'), 500

    # Register a custom Jinja filter to convert time from Datetime
    @app.template_filter('localize_datetime')
    def localize_datetime_filter(value, timezone='UTC', format='medium'):
        time = pytz.utc.localize(value)
        tz = pytz.timezone(timezone)
        converted_datetime = time.astimezone(tz)
        formatted_datetime = format_datetime(converted_datetime, format=format)
        return formatted_datetime

    with app.app_context():
        from config import Config
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                role='admin'
            )
            
            admin.set_password(Config.ADMIN_PASSWORD)
            
            db.session.add(admin)
            db.session.commit()
    return app
