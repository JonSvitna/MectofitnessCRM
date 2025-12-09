#!/usr/bin/env python3
"""
Robust database initialization script for MectoFitness CRM.
This script ensures all tables are created with proper error handling and retry logic.
"""
import os
import sys
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def wait_for_db(app, db, max_retries=5, delay=2):
    """
    Wait for database to be available with retry logic and exponential backoff.
    
    Args:
        app: Flask application instance
        db: SQLAlchemy database instance
        max_retries: Maximum number of connection attempts
        delay: Initial delay in seconds between retries (will increase exponentially)
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    print("Waiting for database to be ready...")
    
    for attempt in range(1, max_retries + 1):
        try:
            with app.app_context():
                # Dispose of any stale connections before attempting
                try:
                    db.engine.dispose()
                except Exception:
                    pass
                
                # Try to connect to the database
                with db.engine.connect() as connection:
                    result = connection.execute(db.text("SELECT 1"))
                    result.fetchone()
                    connection.commit()
                    print(f"✓ Database connection successful (attempt {attempt}/{max_retries})")
                    return True
        except Exception as e:
            error_msg = str(e)
            print(f"⚠ Database connection attempt {attempt}/{max_retries} failed: {error_msg}")
            
            # Dispose of connection pool on failure
            try:
                db.engine.dispose()
            except Exception:
                pass
            
            if attempt < max_retries:
                # Exponential backoff
                current_delay = delay * (2 ** (attempt - 1))
                print(f"  Retrying in {current_delay} seconds...")
                time.sleep(current_delay)
            else:
                print(f"❌ Failed to connect to database after {max_retries} attempts")
                print(f"   Last error: {error_msg}")
                return False
    
    return False


def create_tables(app, db):
    """
    Create all database tables with error handling.
    
    Args:
        app: Flask application instance
        db: SQLAlchemy database instance
    
    Returns:
        bool: True if tables created successfully, False otherwise
    """
    print("\nCreating database tables...")
    
    try:
        with app.app_context():
            # Import all models to ensure they're registered
            from app.models import (
                User, Client, Session, Program, Exercise, CalendarIntegration,
                ClientIntake, EmailTemplate, SMSTemplate, MarketingCampaign,
                CommunicationLog, WorkflowTemplate, WorkflowExecution,
                AutomationRule, ExerciseLibrary, ProgramTemplate,
                TrainerSettings, SystemSettings, Message, MessageNotification,
                ProgressPhoto, CustomMetric, ProgressEntry, NutritionPlan,
                FoodLog, Habit, HabitLog, PaymentPlan, Subscription, Payment,
                Invoice, BookingAvailability, BookingException, OnlineBooking,
                BookingSettings, Integration, VideoConference, WebhookEndpoint,
                AppCustomization
            )
            
            # Create all tables
            db.create_all()
            
            # Verify tables were created
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if tables:
                # Core tables that are critical for the application
                CORE_TABLES = ['users', 'clients', 'sessions', 'programs', 'exercises']
                core_tables_found = [t for t in tables if t in CORE_TABLES]
                print(f"✓ Successfully created {len(tables)} tables")
                print(f"  Core tables: {', '.join(core_tables_found)}")
                return True
            else:
                print("⚠ No tables were created")
                return False
                
    except Exception as e:
        print(f"❌ Error creating tables: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def verify_user_table(app, db):
    """
    Verify that the users table exists and has the correct structure.
    
    Args:
        app: Flask application instance
        db: SQLAlchemy database instance
    
    Returns:
        bool: True if verification successful, False otherwise
    """
    print("\nVerifying users table...")
    
    try:
        with app.app_context():
            from sqlalchemy import inspect
            from app.models.user import User
            
            inspector = inspect(db.engine)
            
            # Check if users table exists
            if 'users' not in inspector.get_table_names():
                print("❌ Users table does not exist")
                return False
            
            # Get column information
            columns = inspector.get_columns('users')
            column_names = [col['name'] for col in columns]
            
            # Verify required columns exist
            required_columns = ['id', 'username', 'email', 'password_hash']
            missing_columns = [col for col in required_columns if col not in column_names]
            
            if missing_columns:
                print(f"❌ Missing required columns: {', '.join(missing_columns)}")
                return False
            
            print(f"✓ Users table verified with {len(columns)} columns")
            print(f"  Columns: {', '.join(column_names[:8])}")
            if len(column_names) > 8:
                print(f"           ... and {len(column_names) - 8} more")
            
            # Test query capability
            try:
                user_count = User.query.count()
                print(f"✓ Users table is queryable (current count: {user_count})")
                return True
            except Exception as e:
                print(f"⚠ Users table exists but query failed: {str(e)}")
                return False
                
    except Exception as e:
        print(f"❌ Error verifying users table: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_user_crud(app, db):
    """
    Test CRUD operations on User model.
    
    Args:
        app: Flask application instance
        db: SQLAlchemy database instance
    
    Returns:
        bool: True if all CRUD operations successful, False otherwise
    """
    print("\nTesting User CRUD operations...")
    
    try:
        with app.app_context():
            from app.models.user import User
            
            test_username = "_test_user_init_db"
            
            # CREATE - Test user creation
            print("  Testing CREATE...")
            test_user = User(
                username=test_username,
                email="test_init@example.com",
                first_name="Test",
                last_name="User"
            )
            test_user.set_password("TestPassword123!")
            
            db.session.add(test_user)
            db.session.commit()
            print("  ✓ User created successfully")
            
            # READ - Test user retrieval
            print("  Testing READ...")
            retrieved_user = User.query.filter_by(username=test_username).first()
            if not retrieved_user:
                print("  ❌ Failed to retrieve created user")
                return False
            
            if retrieved_user.username != test_username:
                print("  ❌ Retrieved user has incorrect data")
                return False
            
            print(f"  ✓ User retrieved successfully (ID: {retrieved_user.id})")
            
            # Test password verification
            if not retrieved_user.check_password("TestPassword123!"):
                print("  ❌ Password verification failed")
                return False
            print("  ✓ Password verification works")
            
            # UPDATE - Test user modification
            print("  Testing UPDATE...")
            retrieved_user.first_name = "Updated"
            db.session.commit()
            
            updated_user = User.query.filter_by(username=test_username).first()
            if updated_user.first_name != "Updated":
                print("  ❌ User update failed")
                return False
            print("  ✓ User updated successfully")
            
            # DELETE - Test user deletion
            print("  Testing DELETE...")
            user_id = updated_user.id
            db.session.delete(updated_user)
            db.session.commit()
            
            deleted_user = db.session.get(User, user_id)
            if deleted_user:
                print("  ❌ User deletion failed")
                return False
            print("  ✓ User deleted successfully")
            
            print("✓ All CRUD operations passed")
            return True
            
    except Exception as e:
        print(f"❌ CRUD operations failed: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Attempt cleanup
        try:
            with app.app_context():
                from app.models.user import User
                cleanup_user = User.query.filter_by(username=test_username).first()
                if cleanup_user:
                    db.session.delete(cleanup_user)
                    db.session.commit()
                    print("  ✓ Test user cleaned up")
        except Exception:
            # Cleanup failure is not critical
            pass
        
        return False


def initialize_database():
    """
    Main function to initialize the database with all necessary tables.
    
    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    print("=" * 70)
    print("MectoFitness CRM - Database Initialization")
    print("=" * 70)
    print()
    
    # Check DATABASE_URL
    database_url = os.environ.get('DATABASE_URL') or os.environ.get('DATABASE_PUBLIC_URL')
    if database_url:
        # Mask password for display
        if '@' in database_url and '://' in database_url:
            parts = database_url.split('@')
            protocol_user = parts[0].split('://')
            if ':' in protocol_user[1]:
                user = protocol_user[1].split(':')[0]
                masked = f"{protocol_user[0]}://{user}:****@{parts[1]}"
            else:
                masked = database_url
        else:
            masked = database_url
        print(f"Database: {masked}")
    else:
        print("Database: Using SQLite (default)")
    print()
    
    try:
        # Import Flask app
        from app import create_app, db
        
        # Create application instance
        env = os.getenv('FLASK_ENV', 'production')
        print(f"Environment: {env}")
        app = create_app(env)
        
        # Step 1: Wait for database to be available
        if not wait_for_db(app, db, max_retries=5, delay=3):
            print("\n❌ Database initialization failed: Could not connect to database")
            return 1
        
        # Step 2: Create all tables
        if not create_tables(app, db):
            print("\n❌ Database initialization failed: Could not create tables")
            return 1
        
        # Step 3: Verify users table
        if not verify_user_table(app, db):
            print("\n❌ Database initialization failed: Users table verification failed")
            return 1
        
        # Step 4: Test CRUD operations
        if not test_user_crud(app, db):
            print("\n❌ Database initialization failed: CRUD operations test failed")
            return 1
        
        print("\n" + "=" * 70)
        print("✓ Database initialization completed successfully!")
        print("=" * 70)
        return 0
        
    except Exception as e:
        print(f"\n❌ Database initialization failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit_code = initialize_database()
    sys.exit(exit_code)
