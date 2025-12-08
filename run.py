"""Run the MectoFitness CRM application."""
import os
from app import create_app, db
from app.models import User, Client, Session, Program, Exercise, CalendarIntegration

# Create application
app = create_app(os.getenv('FLASK_ENV', 'development'))


@app.shell_context_processor
def make_shell_context():
    """Add models to shell context."""
    return {
        'db': db,
        'User': User,
        'Client': Client,
        'Session': Session,
        'Program': Program,
        'Exercise': Exercise,
        'CalendarIntegration': CalendarIntegration
    }


if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)
