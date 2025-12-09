#!/usr/bin/env python3
"""Test database connection for Railway deployment."""
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def test_database_connection():
    """Test if database is properly configured and accessible."""
    print("=" * 60)
    print("Database Connection Test")
    print("=" * 60)
    
    # Check for DATABASE_URL
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL environment variable not set!")
        print("   Using fallback SQLite database")
        database_url = "sqlite:///mectofitness.db"
    
    print(f"✓ DATABASE_URL found")
    
    # Mask password in URL for display
    if '@' in database_url:
        parts = database_url.split('@')
        if '://' in parts[0]:
            protocol_user = parts[0].split('://')
            if ':' in protocol_user[1]:
                user = protocol_user[1].split(':')[0]
                masked = f"{protocol_user[0]}://{user}:****@{parts[1]}"
            else:
                masked = database_url
        else:
            masked = database_url
    else:
        masked = database_url
    
    print(f"   Connection: {masked}")
    
    # Test actual connection
    try:
        from app import create_app, db
        from app.models.user import User
        
        app = create_app(os.getenv('FLASK_ENV', 'development'))
        
        with app.app_context():
            # Try to connect
            connection = db.engine.connect()
            print("✓ Database connection successful!")
            connection.close()
            
            # Check if tables exist
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if tables:
                print(f"✓ Found {len(tables)} tables: {', '.join(tables[:5])}")
                if len(tables) > 5:
                    print(f"   ... and {len(tables) - 5} more")
                
                # Check if users table exists
                if 'users' in tables:
                    print("✓ Users table exists")
                    
                    # Test query
                    try:
                        user_count = User.query.count()
                        print(f"✓ Can query users table - found {user_count} users")
                    except Exception as e:
                        print(f"⚠ Error querying users table: {str(e)}")
                else:
                    print("⚠ Users table not found")
            else:
                print("⚠ No tables found - will be created on first startup")
                print("   Run 'python run.py' to create tables")
            
            return True
            
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_account_creation():
    """Test creating a test account."""
    print("\n" + "=" * 60)
    print("Account Creation Test")
    print("=" * 60)
    
    try:
        from app import create_app, db
        from app.models.user import User
        
        app = create_app(os.getenv('FLASK_ENV', 'development'))
        
        with app.app_context():
            # Create tables if they don't exist
            print("Creating database tables...")
            db.create_all()
            print("✓ Database tables created/verified")
            
            # Check if test user already exists
            test_username = "test_user_db_check"
            existing_user = User.query.filter_by(username=test_username).first()
            
            if existing_user:
                print(f"✓ Test user '{test_username}' already exists")
                # Clean up
                db.session.delete(existing_user)
                db.session.commit()
                print("  Cleaned up for fresh test")
            
            # Create a test user
            print(f"Creating test user '{test_username}'...")
            test_user = User(
                username=test_username,
                email="test@example.com",
                first_name="Test",
                last_name="User"
            )
            test_user.set_password("TestPassword123!")
            
            db.session.add(test_user)
            db.session.commit()
            print("✓ Test user created successfully!")
            
            # Verify user was created
            created_user = User.query.filter_by(username=test_username).first()
            if created_user:
                print(f"✓ User verified in database (ID: {created_user.id})")
                print(f"  Username: {created_user.username}")
                print(f"  Email: {created_user.email}")
                print(f"  Name: {created_user.full_name}")
                
                # Test password checking
                if created_user.check_password("TestPassword123!"):
                    print("✓ Password verification works")
                else:
                    print("⚠ Password verification failed")
                
                # Clean up test user
                db.session.delete(created_user)
                db.session.commit()
                print("✓ Test user cleaned up")
                
                return True
            else:
                print("❌ User not found after creation")
                return False
                
    except Exception as e:
        print(f"❌ Account creation test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success1 = test_database_connection()
    success2 = test_account_creation() if success1 else False
    print("=" * 60)
    
    if success1 and success2:
        print("✓ All tests passed!")
    else:
        print("❌ Some tests failed")
    
    print("=" * 60)
    sys.exit(0 if (success1 and success2) else 1)
