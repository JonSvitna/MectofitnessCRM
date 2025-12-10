"""Initialize Flask application."""
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from config import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app(config_name='default'):
    """Create and configure Flask application."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Log database configuration (without credentials)
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    if db_uri and 'postgresql://' in db_uri:
        # Mask credentials in log
        masked_uri = db_uri.split('@')[1] if '@' in db_uri else 'configured'
        logger.info(f"Database configured: {masked_uri}")
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    CORS(app)
    
    # Test database connection and create tables on startup
    with app.app_context():
        try:
            # Test connection
            connection = db.engine.connect()
            connection.close()
            logger.info("Database connection successful")
            
            # Import all models to ensure they're registered
            from app.models import (
                Organization, User, Client, Session, Program, Exercise, 
                CalendarIntegration, ClientIntake, EmailTemplate, 
                SMSTemplate, MarketingCampaign, WorkflowTemplate, 
                WorkflowExecution, AutomationRule, ExerciseLibrary, 
                ProgramTemplate, TrainerSettings
            )
            
            # Create tables if they don't exist (silently ignore if they already exist)
            try:
                logger.info("Checking database tables...")
                db.create_all()
                
                # Verify tables exist
                from sqlalchemy import inspect
                inspector = inspect(db.engine)
                tables = inspector.get_table_names()
                logger.info(f"✅ Database ready with {len(tables)} tables")
            except Exception as table_error:
                # Tables might already exist, check if we can query
                try:
                    db.session.execute(db.text('SELECT 1 FROM users LIMIT 1'))
                    logger.info("✅ Database tables already exist and are accessible")
                except:
                    logger.error(f"Table creation issue: {table_error}")
                    raise
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            logger.warning("App will continue, but database operations may fail")
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Register blueprints
    from app.routes import (auth, main, clients, sessions, programs, calendar_sync, api,
                           intake, marketing, workflow, settings, exercise_library, api_chatbot)
    from app.routes import (api_clients_bp, api_sessions_bp, api_exercises_bp, api_programs_bp,
                           api_progress_bp, api_nutrition_bp, api_booking_bp, api_payments_bp,
                           api_dashboard_bp, api_organization_bp)
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(clients.bp)
    app.register_blueprint(sessions.bp)
    app.register_blueprint(programs.bp)
    app.register_blueprint(calendar_sync.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(api_clients_bp)  # RESTful client API
    app.register_blueprint(api_sessions_bp)  # RESTful sessions API
    app.register_blueprint(api_exercises_bp)  # RESTful exercise library API
    app.register_blueprint(api_programs_bp)  # RESTful programs API
    app.register_blueprint(api_progress_bp)  # RESTful progress tracking API
    app.register_blueprint(api_nutrition_bp)  # RESTful nutrition API
    app.register_blueprint(api_booking_bp)  # RESTful booking API
    app.register_blueprint(api_payments_bp)  # RESTful payments API
    app.register_blueprint(api_dashboard_bp)  # RESTful dashboard API
    app.register_blueprint(api_organization_bp)  # RESTful organization API
    app.register_blueprint(intake.bp)
    app.register_blueprint(marketing.bp)
    app.register_blueprint(workflow.bp)
    app.register_blueprint(settings.bp)
    app.register_blueprint(exercise_library.bp)
    app.register_blueprint(api_chatbot.bp)  # AI Chatbot API
    app.register_blueprint(api_chatbot.bp)  # AI Chatbot API
    app.register_blueprint(api_chatbot.bp)  # AI Chatbot API
    
    # User loader
    from app.models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(User, int(user_id))
        except Exception:
            return None
    
    # Register error handlers
    from sqlalchemy.exc import OperationalError
    
    @app.errorhandler(OperationalError)
    def handle_db_error(error):
        """Handle database connection errors."""
        from flask import render_template, jsonify, request
        import logging
        
        logger = logging.getLogger(__name__)
        logger.error(f"Database connection error: {str(error)}")
        
        # Rollback session
        db.session.rollback()
        
        # Return JSON for API requests
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Database connection error',
                'message': 'Unable to connect to database. Please try again later.'
            }), 503
        
        # Return HTML for regular requests
        return render_template(
            'error.html',
            error_title='Database Connection Error',
            error_message='Unable to connect to the database. Please try again in a moment.'
        ), 503
    
    @app.errorhandler(500)
    def handle_server_error(error):
        """Handle internal server errors."""
        from flask import render_template, jsonify, request
        import logging
        
        logger = logging.getLogger(__name__)
        logger.error(f"Internal server error: {str(error)}", exc_info=True)
        
        # Rollback session
        db.session.rollback()
        
        # Return JSON for API requests
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Internal server error',
                'message': 'An unexpected error occurred. Please try again later.'
            }), 500
        
        # Return HTML for regular requests
        return render_template(
            'error.html',
            error_title='Internal Server Error',
            error_message='An unexpected error occurred. Please try again later.'
        ), 500
    
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        """
        Clean up database session after each request.
        This ensures connections are returned to the pool properly.
        """
        if exception:
            db.session.rollback()
        db.session.remove()
    
    # Add context processor for Vite manifest
    @app.context_processor
    def inject_vite_manifest():
        """Load Vite manifest for production builds."""
        import json
        import os
        
        def load_vite_manifest():
            manifest_path = os.path.join(app.static_folder, 'dist', '.vite', 'manifest.json')
            if os.path.exists(manifest_path):
                with open(manifest_path, 'r') as f:
                    return json.load(f)
            return {}
        
        return dict(load_vite_manifest=load_vite_manifest)
    
    return app
