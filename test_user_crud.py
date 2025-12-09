#!/usr/bin/env python3
"""Test User CRUD methods."""
import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app, db
from app.models.user import User

def test_user_crud_methods():
    """Test all User CRUD methods."""
    print("=" * 60)
    print("Testing User CRUD Methods")
    print("=" * 60)
    
    app = create_app('development')
    
    with app.app_context():
        # Clean up any existing test users
        test_user = User.query.filter_by(username='test_crud_user').first()
        if test_user:
            db.session.delete(test_user)
            db.session.commit()
        
        # Test 1: Create User
        print("\n1. Testing User.create_user()...")
        user, error = User.create_user(
            username='test_crud_user',
            email='test_crud@example.com',
            password='TestPassword123!',
            first_name='Test',
            last_name='CRUD'
        )
        
        if user:
            print(f"   ✓ User created: {user.username} (ID: {user.id})")
        else:
            print(f"   ❌ Failed to create user: {error}")
            return False
        
        # Test 2: Get by ID
        print("\n2. Testing User.get_by_id()...")
        fetched_user = User.get_by_id(user.id)
        if fetched_user and fetched_user.id == user.id:
            print(f"   ✓ User fetched by ID: {fetched_user.username}")
        else:
            print("   ❌ Failed to fetch user by ID")
            return False
        
        # Test 3: Get by username
        print("\n3. Testing User.get_by_username()...")
        username_user = User.get_by_username('test_crud_user')
        if username_user and username_user.username == 'test_crud_user':
            print(f"   ✓ User fetched by username: {username_user.username}")
        else:
            print("   ❌ Failed to fetch user by username")
            return False
        
        # Test 4: Get by email
        print("\n4. Testing User.get_by_email()...")
        email_user = User.get_by_email('test_crud@example.com')
        if email_user and email_user.email == 'test_crud@example.com':
            print(f"   ✓ User fetched by email: {email_user.email}")
        else:
            print("   ❌ Failed to fetch user by email")
            return False
        
        # Test 5: Authenticate
        print("\n5. Testing User.authenticate()...")
        auth_user, auth_error = User.authenticate('test_crud_user', 'TestPassword123!')
        if auth_user:
            print(f"   ✓ User authenticated: {auth_user.username}")
        else:
            print(f"   ❌ Authentication failed: {auth_error}")
            return False
        
        # Test 6: Authenticate with wrong password
        print("\n6. Testing authentication with wrong password...")
        wrong_user, wrong_error = User.authenticate('test_crud_user', 'WrongPassword')
        if not wrong_user and wrong_error:
            print(f"   ✓ Correctly rejected wrong password: {wrong_error}")
        else:
            print("   ❌ Should have rejected wrong password")
            return False
        
        # Test 7: Update profile
        print("\n7. Testing user.update_profile()...")
        success, update_error = user.update_profile(
            first_name='Updated',
            last_name='Name',
            phone='555-1234'
        )
        if success:
            updated_user = User.get_by_id(user.id)
            if updated_user.first_name == 'Updated' and updated_user.phone == '555-1234':
                print(f"   ✓ Profile updated: {updated_user.full_name}, {updated_user.phone}")
            else:
                print("   ❌ Profile not updated correctly")
                return False
        else:
            print(f"   ❌ Profile update failed: {update_error}")
            return False
        
        # Test 8: Change password
        print("\n8. Testing user.change_password()...")
        success, pwd_error = user.change_password('TestPassword123!', 'NewPassword456!')
        if success:
            # Verify new password works
            auth_user, _ = User.authenticate('test_crud_user', 'NewPassword456!')
            if auth_user:
                print("   ✓ Password changed successfully")
            else:
                print("   ❌ New password doesn't work")
                return False
        else:
            print(f"   ❌ Password change failed: {pwd_error}")
            return False
        
        # Test 9: Duplicate username
        print("\n9. Testing duplicate username prevention...")
        dup_user, dup_error = User.create_user(
            username='test_crud_user',
            email='different@example.com',
            password='Password123!'
        )
        if not dup_user and 'already exists' in dup_error.lower():
            print(f"   ✓ Correctly prevented duplicate username: {dup_error}")
        else:
            print("   ❌ Should have prevented duplicate username")
            return False
        
        # Test 10: Duplicate email
        print("\n10. Testing duplicate email prevention...")
        dup_user, dup_error = User.create_user(
            username='different_user',
            email='test_crud@example.com',
            password='Password123!'
        )
        if not dup_user and 'already registered' in dup_error.lower():
            print(f"   ✓ Correctly prevented duplicate email: {dup_error}")
        else:
            print("   ❌ Should have prevented duplicate email")
            return False
        
        # Test 11: Delete user
        print("\n11. Testing user.delete_user()...")
        success, del_error = user.delete_user()
        if success:
            deleted = User.get_by_id(user.id)
            if not deleted:
                print("   ✓ User deleted successfully")
            else:
                print("   ❌ User still exists after deletion")
                return False
        else:
            print(f"   ❌ User deletion failed: {del_error}")
            return False
        
        print("\n" + "=" * 60)
        print("✓ All User CRUD tests passed!")
        print("=" * 60)
        return True

if __name__ == '__main__':
    success = test_user_crud_methods()
    exit(0 if success else 1)
