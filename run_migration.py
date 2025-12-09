"""Manual migration script to add organizations and RBAC to production database."""
import sys
import os
from sqlalchemy import text

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app import create_app, db


def run_migration():
    """Run the migration to add organizations and RBAC."""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*60)
        print("RUNNING RBAC MIGRATION")
        print("="*60 + "\n")
        
        try:
            # Step 1: Create organizations table
            print("1. Creating organizations table...")
            db.session.execute(text("""
                CREATE TABLE IF NOT EXISTS organizations (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(200) NOT NULL,
                    slug VARCHAR(100) UNIQUE NOT NULL,
                    business_type VARCHAR(50),
                    website VARCHAR(200),
                    phone VARCHAR(20),
                    email VARCHAR(120),
                    address_line1 VARCHAR(200),
                    address_line2 VARCHAR(200),
                    city VARCHAR(100),
                    state VARCHAR(50),
                    zip_code VARCHAR(20),
                    country VARCHAR(100) DEFAULT 'USA',
                    subscription_tier VARCHAR(50) DEFAULT 'free',
                    max_trainers INTEGER DEFAULT 1,
                    max_clients INTEGER DEFAULT 10,
                    logo_url VARCHAR(500),
                    primary_color VARCHAR(7),
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                )
            """))
            db.session.commit()
            print("✅ Organizations table created\n")
            
            # Step 2: Check if columns already exist
            print("2. Checking existing users table schema...")
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='users' AND column_name IN ('organization_id', 'role')
            """))
            existing_columns = [row[0] for row in result]
            
            # Step 3: Add organization_id column if it doesn't exist
            if 'organization_id' not in existing_columns:
                print("3. Adding organization_id to users table...")
                db.session.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN organization_id INTEGER REFERENCES organizations(id)
                """))
                db.session.commit()
                print("✅ organization_id column added\n")
            else:
                print("3. ⏭️  organization_id column already exists\n")
            
            # Step 4: Add role column if it doesn't exist
            if 'role' not in existing_columns:
                print("4. Adding role to users table...")
                db.session.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN role VARCHAR(20) DEFAULT 'trainer'
                """))
                db.session.commit()
                print("✅ role column added\n")
            else:
                print("4. ⏭️  role column already exists\n")
            
            # Step 5: Count users without organizations
            print("5. Checking users without organizations...")
            result = db.session.execute(text("""
                SELECT COUNT(*) FROM users WHERE organization_id IS NULL
            """))
            count = result.scalar()
            print(f"   Found {count} users without organizations\n")
            
            print("="*60)
            print("MIGRATION COMPLETE!")
            print("="*60)
            print("\nNext step: Run migrate_organizations.py to assign organizations to users\n")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error during migration: {e}\n")
            raise


if __name__ == '__main__':
    print("\n⚠️  WARNING: This will modify the production database schema!\n")
    response = input("Do you want to continue? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        run_migration()
    else:
        print("\nMigration cancelled.")
