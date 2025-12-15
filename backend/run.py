"""Run the Flask application."""
import os
from app import create_app, db

# Get environment
env = os.environ.get('FLASK_ENV', 'development')

# Create app
app = create_app(env)

if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
    
    # Run app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=(env == 'development'))
