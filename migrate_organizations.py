"""Migration script to add organizations to existing users."""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Organization, User
import re


def slugify(text):
    """Convert text to URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text[:100]


def migrate_users_to_organizations():
    """Create organizations for existing users without one."""
    app = create_app()
    
    with app.app_context():
        # Find users without organizations
        users_without_org = User.query.filter_by(organization_id=None).all()
        
        if not users_without_org:
            print("✅ All users already have organizations assigned")
            return
        
        print(f"Found {len(users_without_org)} users without organizations")
        print("Creating organizations...\n")
        
        migrated_count = 0
        
        for user in users_without_org:
            try:
                # Generate organization name
                if user.first_name and user.last_name:
                    org_name = f"{user.first_name} {user.last_name} Fitness"
                else:
                    org_name = f"{user.username} Training"
                
                # Generate unique slug
                slug = slugify(org_name)
                counter = 1
                original_slug = slug
                while Organization.query.filter_by(slug=slug).first():
                    slug = f"{original_slug}-{counter}"
                    counter += 1
                
                # Create organization
                org = Organization(
                    name=org_name,
                    slug=slug,
                    email=user.email,
                    phone=user.phone,
                    subscription_tier='free',
                    max_trainers=1,
                    max_clients=10
                )
                db.session.add(org)
                db.session.flush()
                
                # Assign user as owner
                user.organization_id = org.id
                user.role = 'owner'
                
                db.session.commit()
                
                print(f"✅ Created organization '{org_name}' for {user.email}")
                print(f"   - Slug: {slug}")
                print(f"   - Role: owner\n")
                
                migrated_count += 1
                
            except Exception as e:
                db.session.rollback()
                print(f"❌ Error creating organization for {user.email}: {e}\n")
        
        print(f"\n{'='*60}")
        print(f"Migration complete!")
        print(f"✅ Successfully migrated {migrated_count} users")
        print(f"{'='*60}\n")


if __name__ == '__main__':
    print("\n" + "="*60)
    print("ORGANIZATION MIGRATION SCRIPT")
    print("="*60 + "\n")
    print("This script will:")
    print("1. Find all users without an organization")
    print("2. Create a new organization for each user")
    print("3. Assign the user as organization owner\n")
    
    response = input("Do you want to continue? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        migrate_users_to_organizations()
    else:
        print("\nMigration cancelled.")
