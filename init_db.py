"""Initialize database tables for MectoFitness CRM."""
import os
from app import create_app, db

# Create Flask app
app = create_app(os.getenv('FLASK_ENV', 'production'))

with app.app_context():
    print("Creating all database tables...")
    db.create_all()
    print("✅ Database tables created successfully!")
    
    # List all tables
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"\n📊 Created {len(tables)} tables:")
    for table in tables:
        print(f"  - {table}")
