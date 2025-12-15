"""Initialize Flask application for MectoFitness Backend API."""
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name='default'):
    """Create and configure Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Log configuration (without credentials)
    logger.info(f"Starting MectoFitness API in {config_name} mode")
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    if db_uri and 'postgresql://' in db_uri:
        masked_uri = db_uri.split('@')[1] if '@' in db_uri else 'configured'
        logger.info(f"Database: {masked_uri}")
    else:
        logger.info("Database: SQLite (local development)")
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": False
        }
    })
    
    # Test database connection
    with app.app_context():
        try:
            connection = db.engine.connect()
            connection.close()
            logger.info("Database connection successful")
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
    
    # Register blueprints
    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'service': 'MectoFitness API'}, 200
    
    # Root endpoint
    @app.route('/')
    def index():
        return {
            'service': 'MectoFitness API',
            'version': app.config['API_VERSION'],
            'status': 'running'
        }, 200
    
    return app
