#!/usr/bin/env python3
"""
Database connection diagnostic tool for MectoFitness CRM.
This script helps troubleshoot PostgreSQL connection issues on Railway.
"""
import os
import sys
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

def check_environment():
    """Check environment variables."""
    print_header("Environment Variables Check")
    
    database_url = os.environ.get('DATABASE_URL')
    database_public_url = os.environ.get('DATABASE_PUBLIC_URL')
    secret_key = os.environ.get('SECRET_KEY')
    flask_env = os.environ.get('FLASK_ENV', 'development')
    
    print(f"FLASK_ENV: {flask_env}")
    print(f"SECRET_KEY: {'✓ Set' if secret_key else '✗ Not set (will use default)'}")
    
    if database_url:
        # Mask password
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
        print(f"DATABASE_URL: {masked}")
    else:
        print("DATABASE_URL: ✗ Not set (will use SQLite)")
    
    if database_public_url:
        # Mask password
        if '@' in database_public_url and '://' in database_public_url:
            parts = database_public_url.split('@')
            protocol_user = parts[0].split('://')
            if ':' in protocol_user[1]:
                user = protocol_user[1].split(':')[0]
                masked = f"{protocol_user[0]}://{user}:****@{parts[1]}"
            else:
                masked = database_public_url
        else:
            masked = database_public_url
        print(f"DATABASE_PUBLIC_URL: {masked}")
    
    return bool(database_url or database_public_url)

def test_raw_connection():
    """Test raw psycopg2 connection."""
    print_header("Raw PostgreSQL Connection Test")
    
    database_url = os.environ.get('DATABASE_PUBLIC_URL') or os.environ.get('DATABASE_URL')
    
    if not database_url or 'postgresql' not in database_url:
        print("⚠ Skipping (not using PostgreSQL)")
        return True
    
    try:
        import psycopg2
        from urllib.parse import urlparse
        
        # Parse connection string
        url = urlparse(database_url)
        
        print(f"Host: {url.hostname}")
        print(f"Port: {url.port}")
        print(f"Database: {url.path[1:]}")
        print(f"User: {url.username}")
        print("\nAttempting connection...")
        
        start_time = time.time()
        conn = psycopg2.connect(
            host=url.hostname,
            port=url.port,
            database=url.path[1:],
            user=url.username,
            password=url.password,
            connect_timeout=10,
            keepalives=1,
            keepalives_idle=30,
            keepalives_interval=10,
            keepalives_count=5
        )
        
        elapsed = round((time.time() - start_time) * 1000, 2)
        print(f"✓ Connection successful in {elapsed}ms")
        
        # Test query
        cursor = conn.cursor()
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        print(f"✓ PostgreSQL version: {version[:50]}...")
        
        cursor.close()
        conn.close()
        print("✓ Connection closed cleanly")
        return True
        
    except Exception as e:
        print(f"✗ Connection failed: {str(e)}")
        return False

def test_sqlalchemy_connection():
    """Test SQLAlchemy connection with pool settings."""
    print_header("SQLAlchemy Connection Test")
    
    try:
        from app import create_app, db
        
        # Create app
        env = os.getenv('FLASK_ENV', 'production')
        print(f"Creating app with environment: {env}")
        app = create_app(env)
        
        with app.app_context():
            # Print pool configuration
            print("\nConnection Pool Configuration:")
            pool = db.engine.pool
            print(f"  Class: {pool.__class__.__name__}")
            print(f"  Size: {pool.size()}")
            print(f"  Timeout: {pool._timeout}")
            print(f"  Max Overflow: {pool._max_overflow}")
            
            # Test connection with timing
            print("\nTesting connection...")
            start_time = time.time()
            
            with db.engine.connect() as connection:
                result = connection.execute(db.text("SELECT 1 as test"))
                data = result.fetchone()
                connection.commit()
            
            elapsed = round((time.time() - start_time) * 1000, 2)
            print(f"✓ Connection successful in {elapsed}ms")
            print(f"✓ Query result: {data}")
            
            # Check pool stats
            print(f"\nPool stats after connection:")
            print(f"  Size: {pool.size()}")
            print(f"  Checked out: {pool.checked_out_connections}")
            
            return True
            
    except Exception as e:
        print(f"✗ Connection failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_table_existence():
    """Test if tables exist."""
    print_header("Database Tables Check")
    
    try:
        from app import create_app, db
        from sqlalchemy import inspect
        
        env = os.getenv('FLASK_ENV', 'production')
        app = create_app(env)
        
        with app.app_context():
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if tables:
                print(f"✓ Found {len(tables)} tables:")
                for i, table in enumerate(sorted(tables), 1):
                    print(f"  {i}. {table}")
            else:
                print("⚠ No tables found - database may need initialization")
                print("  Run: python init_db.py")
            
            # Check for critical tables
            critical_tables = ['users', 'clients', 'sessions', 'programs']
            missing = [t for t in critical_tables if t not in tables]
            
            if missing:
                print(f"\n⚠ Missing critical tables: {', '.join(missing)}")
                return False
            else:
                print(f"\n✓ All critical tables exist")
                return True
                
    except Exception as e:
        print(f"✗ Table check failed: {str(e)}")
        return False

def test_query_performance():
    """Test query performance."""
    print_header("Query Performance Test")
    
    try:
        from app import create_app, db
        from app.models.user import User
        
        env = os.getenv('FLASK_ENV', 'production')
        app = create_app(env)
        
        with app.app_context():
            # Test simple query
            print("Testing User.query.count()...")
            start_time = time.time()
            count = User.query.count()
            elapsed = round((time.time() - start_time) * 1000, 2)
            print(f"✓ Found {count} users in {elapsed}ms")
            
            # Test with limit
            print("\nTesting User.query.limit(5).all()...")
            start_time = time.time()
            users = User.query.limit(5).all()
            elapsed = round((time.time() - start_time) * 1000, 2)
            print(f"✓ Retrieved {len(users)} users in {elapsed}ms")
            
            if elapsed > 1000:
                print("⚠ Query took over 1 second - may indicate connection issues")
            
            return True
            
    except Exception as e:
        print(f"✗ Query test failed: {str(e)}")
        return False

def test_connection_retry():
    """Test connection with retry logic."""
    print_header("Connection Retry Test")
    
    try:
        from app import create_app, db
        
        env = os.getenv('FLASK_ENV', 'production')
        app = create_app(env)
        
        max_retries = 3
        print(f"Testing retry logic with {max_retries} attempts...")
        
        for attempt in range(1, max_retries + 1):
            try:
                with app.app_context():
                    print(f"\nAttempt {attempt}/{max_retries}:")
                    
                    # Dispose pool before retry
                    if attempt > 1:
                        print("  Disposing connection pool...")
                        db.engine.dispose()
                    
                    start_time = time.time()
                    with db.engine.connect() as connection:
                        result = connection.execute(db.text("SELECT 1"))
                        result.fetchone()
                        connection.commit()
                    
                    elapsed = round((time.time() - start_time) * 1000, 2)
                    print(f"  ✓ Connected in {elapsed}ms")
                    
                    if attempt == 1:
                        print("\n✓ Connection successful on first attempt (no retry needed)")
                    else:
                        print(f"\n✓ Connection successful after {attempt} attempts")
                    
                    return True
                    
            except Exception as e:
                if attempt < max_retries:
                    delay = 2 ** (attempt - 1)
                    print(f"  ✗ Failed: {str(e)}")
                    print(f"  Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    print(f"  ✗ Failed after {max_retries} attempts: {str(e)}")
                    return False
        
        return False
        
    except Exception as e:
        print(f"✗ Retry test failed: {str(e)}")
        return False

def run_diagnostics():
    """Run all diagnostic tests."""
    print_header("MectoFitness CRM - Database Diagnostics")
    print("This tool helps diagnose PostgreSQL connection issues")
    print()
    
    results = {
        'environment': False,
        'raw_connection': False,
        'sqlalchemy': False,
        'tables': False,
        'performance': False,
        'retry': False
    }
    
    # Run tests
    results['environment'] = check_environment()
    
    if results['environment']:
        results['raw_connection'] = test_raw_connection()
        results['sqlalchemy'] = test_sqlalchemy_connection()
        
        if results['sqlalchemy']:
            results['tables'] = test_table_existence()
            results['performance'] = test_query_performance()
            results['retry'] = test_connection_retry()
    
    # Summary
    print_header("Diagnostic Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test.replace('_', ' ').title()}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All diagnostics passed! Database connection is healthy.")
        return 0
    else:
        print("\n⚠ Some diagnostics failed. Check errors above for details.")
        print("\nTroubleshooting steps:")
        print("1. Verify DATABASE_URL is set correctly in Railway")
        print("2. Check PostgreSQL service is running in Railway dashboard")
        print("3. Review RAILWAY_DB_TROUBLESHOOTING.md for detailed guidance")
        print("4. Try running: python init_db.py")
        return 1

if __name__ == '__main__':
    try:
        exit_code = run_diagnostics()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nDiagnostics interrupted by user")
        sys.exit(1)
