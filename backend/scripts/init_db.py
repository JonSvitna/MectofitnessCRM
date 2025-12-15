#!/usr/bin/env python3
"""Initialize database tables for MectoFitness CRM."""
import os
import sys

# Ensure we can import from app - add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db

print("🔄 Initializing database...")
print(f"Environment: {os.getenv('FLASK_ENV', 'production')}")

# Create Flask app
app = create_app(os.getenv('FLASK_ENV', 'production'))

with app.app_context():
    try:
        print("\n📊 Creating all database tables...")
        
        # Import all models to ensure they're registered
        from app.models import (
            User, Client, Session, Program, Exercise, 
            CalendarIntegration, ClientIntake, EmailTemplate, 
            SMSTemplate, MarketingCampaign, WorkflowTemplate, 
            WorkflowExecution, AutomationRule, ExerciseLibrary, 
            ProgramTemplate, TrainerSettings
        )
        
        # Create all tables
        db.create_all()
        
        print("✅ Database tables created successfully!")
        
        # List all tables
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"\n✅ Created {len(tables)} tables:")
        for table in sorted(tables):
            print(f"  ✓ {table}")
        
        print("\n🎉 Database initialization complete!")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ Error creating tables: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
