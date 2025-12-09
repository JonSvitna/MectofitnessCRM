"""Run the MectoFitness CRM application."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app import create_app, db
from app.models import (User, Client, Session, Program, Exercise, CalendarIntegration,
                       ClientIntake, EmailTemplate, SMSTemplate, MarketingCampaign,
                       WorkflowTemplate, WorkflowExecution, AutomationRule,
                       ExerciseLibrary, ProgramTemplate, TrainerSettings)

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
        'CalendarIntegration': CalendarIntegration,
        'ClientIntake': ClientIntake,
        'EmailTemplate': EmailTemplate,
        'SMSTemplate': SMSTemplate,
        'MarketingCampaign': MarketingCampaign,
        'WorkflowTemplate': WorkflowTemplate,
        'WorkflowExecution': WorkflowExecution,
        'AutomationRule': AutomationRule,
        'ExerciseLibrary': ExerciseLibrary,
        'ProgramTemplate': ProgramTemplate,
        'TrainerSettings': TrainerSettings
    }


if __name__ == '__main__':
    # Create database tables if they don't exist with retry logic
    from app.utils.db_helpers import init_db_with_retry
    
    if init_db_with_retry(app, max_retries=5, retry_delay=2):
        print("Database tables created successfully!")
    else:
        print("Warning: Database initialization failed. Application may not work correctly.")
        print("Please check DATABASE_URL and database connectivity.")
    
    # Run the application
    # Debug mode is controlled by FLASK_ENV environment variable
    # Set FLASK_ENV=production in production to disable debug mode
    debug_mode = os.getenv('FLASK_ENV', 'development') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
