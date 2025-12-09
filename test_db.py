#!/usr/bin/env python3
"""Test database connection for Railway deployment."""
import os
import sys

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
        return False
    
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
        
        app = create_app(os.getenv('FLASK_ENV', 'production'))
        
        with app.app_context():
            # Try to connect
            db.engine.connect()
            print("✓ Database connection successful!")
            
            # Check if tables exist
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if tables:
                print(f"✓ Found {len(tables)} tables: {', '.join(tables[:5])}")
                if len(tables) > 5:
                    print(f"   ... and {len(tables) - 5} more")
            else:
                print("⚠ No tables found - will be created on first startup")
            
            return True
            
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False

if __name__ == '__main__':
    success = test_database_connection()
    print("=" * 60)
    sys.exit(0 if success else 1)
