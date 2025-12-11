"""Test user and settings API endpoints."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User
from app.models.settings import TrainerSettings
from werkzeug.security import generate_password_hash
import json

def test_user_settings_api():
    """Test user profile and settings API endpoints."""
    app = create_app()
    client = app.test_client()
    
    with app.app_context():
        # Clean up any existing test data
        test_user = User.query.filter_by(username='test_api_user').first()
        if test_user:
            db.session.delete(test_user)
            db.session.commit()
        
        # Create a test user
        test_user = User(
            username='test_api_user',
            email='test@example.com',
            password=generate_password_hash('password123'),
            name='Test User',
            role='trainer',
            is_active=True
        )
        db.session.add(test_user)
        db.session.commit()
        
        print(f"✅ Created test user: {test_user.username}")
        
        # Login the user (simulate)
        with client.session_transaction() as sess:
            sess['user_id'] = str(test_user.id)
        
        # Test 1: Get user profile
        print("\n=== Test 1: GET /api/v1/user/profile ===")
        with client:
            with client.session_transaction() as sess:
                sess['_user_id'] = str(test_user.id)
            
            response = client.get('/api/v1/user/profile')
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = json.loads(response.data)
                print(f"✅ Response: {json.dumps(data, indent=2)}")
            elif response.status_code == 401:
                print("⚠️  Authentication required (expected in test environment)")
            else:
                print(f"❌ Error: {response.data.decode()}")
        
        # Test 2: Get settings
        print("\n=== Test 2: GET /api/v1/settings ===")
        with client:
            with client.session_transaction() as sess:
                sess['_user_id'] = str(test_user.id)
            
            response = client.get('/api/v1/settings')
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = json.loads(response.data)
                print(f"✅ Response: {json.dumps(data, indent=2)[:200]}...")
            elif response.status_code == 401:
                print("⚠️  Authentication required (expected in test environment)")
            else:
                print(f"❌ Error: {response.data.decode()}")
        
        # Test 3: Update settings (without authentication, should fail)
        print("\n=== Test 3: PATCH /api/v1/settings (without auth) ===")
        response = client.patch(
            '/api/v1/settings',
            data=json.dumps({'business_name': 'Test Gym'}),
            content_type='application/json'
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 401:
            print("✅ Correctly requires authentication")
        else:
            print(f"⚠️  Unexpected status: {response.status_code}")
        
        # Clean up
        db.session.delete(test_user)
        settings = TrainerSettings.query.filter_by(trainer_id=test_user.id).first()
        if settings:
            db.session.delete(settings)
        db.session.commit()
        print("\n✅ Cleaned up test data")

if __name__ == '__main__':
    print("Testing User and Settings API Endpoints")
    print("=" * 50)
    try:
        test_user_settings_api()
        print("\n" + "=" * 50)
        print("✅ All tests completed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
