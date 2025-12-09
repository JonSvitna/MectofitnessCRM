#!/usr/bin/env python3
"""Verification script to check MectoFitness CRM setup."""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)

def check_environment():
    """Check environment configuration."""
    print_header("ENVIRONMENT CHECK")
    
    flask_env = os.getenv('FLASK_ENV', 'development')
    print(f"✓ FLASK_ENV: {flask_env}")
    
    secret_key = os.getenv('SECRET_KEY', 'NOT SET')
    if secret_key == 'your-secret-key-here-change-in-production':
        print("⚠ SECRET_KEY: Using default (change for production)")
    elif secret_key == 'NOT SET':
        print("⚠ SECRET_KEY: Not set (will use config default)")
    else:
        print("✓ SECRET_KEY: Custom key set")
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("⚠ DATABASE_URL: Not set (will use SQLite)")
        return 'sqlite'
    elif database_url.startswith('postgresql://') or database_url.startswith('postgres://'):
        print("✓ DATABASE_URL: PostgreSQL configured")
        return 'postgresql'
    elif database_url.startswith('sqlite:'):
        print("✓ DATABASE_URL: SQLite configured")
        return 'sqlite'
    else:
        print(f"⚠ DATABASE_URL: Unknown type ({database_url.split(':')[0]})")
        return 'unknown'

def test_database_connection(db_type):
    """Test database connection."""
    print_header("DATABASE CONNECTION TEST")
    
    try:
        from app import create_app, db
        from app.models.user import User
        
        app = create_app(os.getenv('FLASK_ENV', 'development'))
        
        with app.app_context():
            # Test connection
            with db.engine.connect() as connection:
                print("✓ Database connection successful")
            
            # Check tables
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if not tables:
                print("ℹ No tables found - creating...")
                db.create_all()
                print("✓ Database tables created")
                tables = inspector.get_table_names()
            
            print(f"✓ Found {len(tables)} tables")
            
            # Check users table
            if 'users' in tables:
                user_count = User.query.count()
                print(f"✓ Users table exists with {user_count} users")
            
            return True
            
    except Exception as e:
        # Log error without exposing sensitive details
        error_type = type(e).__name__
        print(f"❌ Database connection failed: {error_type}")
        if db_type == 'postgresql':
            print("\nPostgreSQL Troubleshooting Tips:")
            print("1. Verify DATABASE_URL format: postgresql://user:password@host:port/database")
            print("2. Check PostgreSQL server is running")
            print("3. Verify database credentials")
            print("4. Ensure database exists")
            print("5. Check firewall/network settings")
            print("\nFor detailed error information, check application logs")
        return False

def test_user_operations():
    """Test user creation and operations."""
    print_header("USER OPERATIONS TEST")
    
    try:
        from app import create_app, db
        from app.models.user import User
        
        app = create_app(os.getenv('FLASK_ENV', 'development'))
        
        with app.app_context():
            # Try to create a test user
            test_username = "verify_test_user"
            
            # Clean up if exists
            existing = User.query.filter_by(username=test_username).first()
            if existing:
                db.session.delete(existing)
                db.session.commit()
                print("ℹ Cleaned up existing test user")
            
            # Create test user
            test_user = User(
                username=test_username,
                email="verify@test.com",
                first_name="Verify",
                last_name="Test"
            )
            test_user.set_password("VerifyPassword123!")
            
            db.session.add(test_user)
            db.session.commit()
            print("✓ Test user created successfully")
            
            # Verify user
            created = User.query.filter_by(username=test_username).first()
            if created:
                print(f"✓ User verified (ID: {created.id})")
                
                # Test password
                if created.check_password("VerifyPassword123!"):
                    print("✓ Password verification works")
                else:
                    print("❌ Password verification failed")
                
                # Clean up
                db.session.delete(created)
                db.session.commit()
                print("✓ Test user cleaned up")
                
                return True
            else:
                print("❌ User not found after creation")
                return False
                
    except Exception as e:
        print(f"❌ User operations failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def print_summary(all_passed):
    """Print final summary."""
    print_header("SUMMARY")
    
    if all_passed:
        print("✅ All checks passed!")
        print("\nYour MectoFitness CRM is properly configured.")
        print("\nNext steps:")
        print("1. Start the application: python run.py")
        print("2. Open browser: http://localhost:5000")
        print("3. Register an account: /auth/register")
        print("4. Login and start using the CRM")
    else:
        print("❌ Some checks failed")
        print("\nPlease review the errors above and:")
        print("1. Check POSTGRESQL_SETUP.md for configuration guide")
        print("2. Verify your .env file settings")
        print("3. Ensure database is accessible")
        print("4. Run this script again after fixing issues")
    
    print("=" * 60)

def main():
    """Main verification flow."""
    print("\n🏋️  MectoFitness CRM Setup Verification")
    
    # Run checks
    db_type = check_environment()
    db_ok = test_database_connection(db_type)
    user_ok = test_user_operations() if db_ok else False
    
    all_passed = db_ok and user_ok
    
    # Print summary
    print_summary(all_passed)
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
