#!/usr/bin/env python3
"""Test unauthenticated homepage access and navigation."""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set test database if not already configured
if 'DATABASE_URL' not in os.environ or 'test' not in os.environ.get('DATABASE_URL', ''):
    os.environ['DATABASE_URL'] = 'sqlite:///test_homepage.db'

from app import create_app


def test_homepage_access():
    """Test that unauthenticated users can access the homepage."""
    app = create_app()
    client = app.test_client()
    
    print("Testing unauthenticated homepage access...")
    
    # Test 1: Homepage accessible without authentication
    response = client.get('/')
    assert response.status_code == 200, f"Homepage returned {response.status_code}"
    assert b'All-in-One Software' in response.data or b'MectoFitness' in response.data
    print("✓ Homepage accessible to unauthenticated users")
    
    # Test 2: Features visible on homepage
    assert b'Client Management' in response.data or b'Program Builder' in response.data
    print("✓ Product features visible on homepage")
    
    # Test 3: Login button present
    assert b'/auth/login' in response.data or b'Login' in response.data
    print("✓ Login button/link present")
    
    # Test 4: Signup/Register button present
    assert b'/auth/register' in response.data or b'Sign' in response.data or b'Trial' in response.data
    print("✓ Signup/trial button present")
    
    # Test 5: Login page accessible
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Login' in response.data or b'login' in response.data
    print("✓ Login page accessible")
    
    # Test 6: Registration page accessible
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert b'Register' in response.data or b'Sign' in response.data or b'Create' in response.data
    print("✓ Registration page accessible")
    
    # Test 7: Protected routes redirect unauthenticated users
    response = client.get('/dashboard', follow_redirects=False)
    assert response.status_code in [302, 401], f"Dashboard should redirect/block unauthenticated, got {response.status_code}"
    print("✓ Protected routes properly secured")
    
    print("\n✅ All tests passed! Unauthenticated access works correctly.")
    return True


if __name__ == '__main__':
    try:
        success = test_homepage_access()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
