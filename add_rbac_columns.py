"""Quick fix migration - add RBAC columns to users table."""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app import create_app, db
from sqlalchemy import text


def add_rbac_columns():
    """Add organization_id and role columns to users table."""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*60)
        print("ADDING RBAC COLUMNS TO USERS TABLE")
        print("="*60 + "\n")
        
        try:
            # Check if columns already exist
            print("Checking existing schema...")
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='users' AND column_name IN ('organization_id', 'role')
            """))
            existing_columns = [row[0] for row in result]
            print(f"Existing RBAC columns: {existing_columns}\n")
            
            # Add organization_id column
            if 'organization_id' not in existing_columns:
                print("Adding organization_id column...")
                db.session.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN organization_id INTEGER REFERENCES organizations(id)
                """))
                db.session.commit()
                print("✅ organization_id added\n")
            else:
                print("⏭️  organization_id already exists\n")
            
            # Add role column
            if 'role' not in existing_columns:
                print("Adding role column...")
                db.session.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN role VARCHAR(20) DEFAULT 'trainer'
                """))
                db.session.commit()
                print("✅ role added\n")
            else:
                print("⏭️  role already exists\n")
            
            # Verify columns were added
            print("Verifying schema...")
            result = db.session.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name='users' AND column_name IN ('organization_id', 'role')
                ORDER BY column_name
            """))
            
            print("\nUsers table RBAC columns:")
            print("-" * 60)
            for row in result:
                print(f"  {row[0]:<20} {row[1]:<15} nullable: {row[2]}")
            
            print("\n" + "="*60)
            print("✅ MIGRATION COMPLETE!")
            print("="*60)
            print("\nUsers table now has organization_id and role columns.")
            print("Next: Run migrate_organizations.py to assign users to orgs.\n")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error: {e}\n")
            raise


if __name__ == '__main__':
    add_rbac_columns()
