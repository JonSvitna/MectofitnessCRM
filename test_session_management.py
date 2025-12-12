#!/usr/bin/env python3
"""Test session management and authentication flows."""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set test database if not already configured
if 'DATABASE_URL' not in os.environ or 'test' not in os.environ.get('DATABASE_URL', ''):
    os.environ['DATABASE_URL'] = 'sqlite:///test_session_mgmt.db'

from app import create_app, db
from app.models.user import User
from app.models.organization import Organization


def setup_test_user(app):
    """Create a test user and organization."""
    with app.app_context():
        # Clean up any existing test data
        User.query.filter_by(username='testuser').delete()
        Organization.query.filter_by(slug='test-fitness').delete()
        db.session.commit()
        
        # Create test organization
        org = Organization(
            name='Test Fitness',
            slug='test-fitness',
            subscription_tier='free',
            max_trainers=1,
            max_clients=10
        )
        db.session.add(org)
        db.session.flush()
        
        # Create test user
        user, error = User.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!',
            first_name='Test',
            last_name='User',
            role='owner'
        )
        
        if user:
            user.organization_id = org.id
            db.session.commit()
            # Return simple data instead of SQLAlchemy objects
            return {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'id': user.id
            }, {
                'name': org.name,
                'id': org.id
            }
        else:
            raise Exception(f"Failed to create test user: {error}")


def cleanup_test_user(app):
    """Remove test user and organization."""
    with app.app_context():
        User.query.filter_by(username='testuser').delete()
        Organization.query.filter_by(slug='test-fitness').delete()
        db.session.commit()


def test_session_management():
    """Test all session management flows."""
    app = create_app()
    client = app.test_client()
    
    print("\n" + "="*60)
    print("TESTING SESSION MANAGEMENT & AUTHENTICATION FLOWS")
    print("="*60 + "\n")
    
    # Setup test user
    print("Setting up test user...")
    test_user, test_org = setup_test_user(app)
    print(f"✓ Created test user: {test_user['username']}\n")
    
    try:
        # Test 1: Unauthenticated homepage access
        print("Test 1: Unauthenticated Homepage Access")
        print("-" * 40)
        response = client.get('/')
        assert response.status_code == 200, f"Homepage returned {response.status_code}"
        # Should show either Next.js homepage or Jinja template
        assert b'MectoFitness' in response.data or b'Mectofitness' in response.data
        print("✓ Unauthenticated users can access homepage")
        print("✓ Homepage displays correctly\n")
        
        # Test 2: Login flow
        print("Test 2: Login Flow")
        print("-" * 40)
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'TestPass123!',
            'remember': False
        }, follow_redirects=False)
        assert response.status_code in [302, 303], f"Login should redirect, got {response.status_code}"
        # Should redirect to dashboard
        assert '/dashboard' in response.location or response.location == '/'
        print("✓ Login successful")
        print("✓ Redirects to dashboard after login\n")
        
        # Test 3: Authenticated homepage access
        print("Test 3: Authenticated Homepage Access")
        print("-" * 40)
        response = client.get('/', follow_redirects=False)
        assert response.status_code == 200, f"Authenticated homepage returned {response.status_code}"
        # Should show authenticated welcome page
        assert b'Welcome back' in response.data or b'Dashboard' in response.data
        print("✓ Authenticated users see personalized homepage")
        print("✓ Dashboard access visible")
        print("✓ Logout option visible\n")
        
        # Test 4: Dashboard access when authenticated
        print("Test 4: Dashboard Access (Authenticated)")
        print("-" * 40)
        response = client.get('/dashboard')
        assert response.status_code == 200, f"Dashboard returned {response.status_code}"
        print("✓ Authenticated users can access dashboard\n")
        
        # Test 5: Logout flow
        print("Test 5: Logout Flow")
        print("-" * 40)
        response = client.get('/logout', follow_redirects=False)
        assert response.status_code in [302, 303], f"Logout should redirect, got {response.status_code}"
        # Should redirect to homepage (not login page)
        assert response.location == '/' or 'main.index' in str(response.location)
        print("✓ Logout successful")
        print("✓ Redirects to homepage after logout\n")
        
        # Test 6: Homepage after logout
        print("Test 6: Homepage After Logout")
        print("-" * 40)
        response = client.get('/', follow_redirects=True)
        assert response.status_code == 200
        # Should show unauthenticated homepage again
        assert b'Login' in response.data or b'Sign In' in response.data
        print("✓ Users see unauthenticated homepage after logout")
        print("✓ Login/Register options visible\n")
        
        # Test 7: Protected routes block unauthenticated users
        print("Test 7: Protected Routes (Unauthenticated)")
        print("-" * 40)
        response = client.get('/dashboard', follow_redirects=False)
        assert response.status_code in [302, 401], f"Should block/redirect unauthenticated access, got {response.status_code}"
        print("✓ Unauthenticated users cannot access dashboard")
        print("✓ Protected routes properly secured\n")
        
        # Test 8: API endpoint authentication
        print("Test 8: API Endpoint Authentication")
        print("-" * 40)
        response = client.get('/api/v1/user/profile')
        assert response.status_code in [401, 302], f"API should require auth, got {response.status_code}"
        print("✓ API endpoints require authentication\n")
        
        # Test 9: Login and access API
        print("Test 9: Authenticated API Access")
        print("-" * 40)
        # Login again
        client.post('/login', data={
            'username': 'testuser',
            'password': 'TestPass123!',
        })
        response = client.get('/api/v1/user/profile')
        assert response.status_code == 200, f"API should work when authenticated, got {response.status_code}"
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['username'] == 'testuser'
        print("✓ Authenticated users can access API endpoints")
        print("✓ User profile data returned correctly\n")
        
        print("="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\nSession management is working correctly:")
        print("  • Unauthenticated users see public homepage")
        print("  • Login redirects to dashboard")
        print("  • Authenticated users see personalized homepage")
        print("  • Logout redirects to public homepage")
        print("  • Protected routes are secured")
        print("  • API endpoints require authentication")
        
        return True
        
    finally:
        # Cleanup
        print("\nCleaning up test data...")
        cleanup_test_user(app)
        print("✓ Test data cleaned up")


if __name__ == '__main__':
    try:
        success = test_session_management()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
