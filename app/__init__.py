"""Initialize Flask application."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from config import config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app(config_name='default'):
    """Create and configure Flask application."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    CORS(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Register blueprints
    from app.routes import (auth, main, clients, sessions, programs, calendar_sync, api,
                           intake, marketing, workflow, settings, exercise_library)
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(clients.bp)
    app.register_blueprint(sessions.bp)
    app.register_blueprint(programs.bp)
    app.register_blueprint(calendar_sync.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(intake.bp)
    app.register_blueprint(marketing.bp)
    app.register_blueprint(workflow.bp)
    app.register_blueprint(settings.bp)
    app.register_blueprint(exercise_library.bp)
    
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
    
    return app
