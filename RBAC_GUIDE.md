# Multi-Tenant RBAC Implementation Guide

## Overview
MectoFitness CRM now supports **multi-tenant architecture** with **role-based access control (RBAC)**. Each trainer or business operates as an independent **Organization** with complete data isolation.

## **Architecture**

### **Organizations**
- Each trainer/business has their own Organization
- Organizations contain multiple users with different roles
- Complete data isolation between organizations
- Subscription tiers control feature access and limits

### **Roles & Permissions**

#### **1. Owner** (Organization Creator)
- **Full access** to everything in the organization
- Can manage organization settings
- Can invite/remove admins and trainers
- Can view all clients, sessions, programs across all trainers
- Can manage billing and subscription

#### **2. Admin**
- Can manage trainers and clients
- Can view all data in the organization
- Cannot modify organization settings
- Cannot change subscription or billing
- Can assign roles to trainers

#### **3. Trainer** (Default for new signups)
- Can manage their own clients
- Can create programs and sessions for their clients
- Can view only their own clients' data
- Cannot see other trainers' clients

#### **4. Client** (Future: Client Portal Access)
- Read-only access to their own data
- Can view their sessions, programs, progress, nutrition plans
- Cannot create or edit data
- Can book sessions online

## **Database Schema Changes**

### **New Table: `organizations`**
```sql
CREATE TABLE organizations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    business_type VARCHAR(50),
    subscription_tier VARCHAR(50) DEFAULT 'free',
    max_trainers INTEGER DEFAULT 1,
    max_clients INTEGER DEFAULT 10,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### **Updated: `users` table**
```sql
ALTER TABLE users 
ADD COLUMN organization_id INTEGER REFERENCES organizations(id),
ADD COLUMN role VARCHAR(20) DEFAULT 'trainer';
```

## **API Endpoints**

### **Organization API** (`/api/v1/organization`)

#### `GET /` - Get Organization Details
- **Auth**: Required (any logged-in user)
- **Returns**: Current user's organization info

#### `POST /` - Create Organization
- **Auth**: Required
- **Body**: `{name, business_type, email, phone, address}`
- **Returns**: New organization + user becomes owner

#### `PUT /` - Update Organization
- **Auth**: Owner only
- **Body**: Organization fields to update

#### `GET /members` - List Organization Members
- **Auth**: Admin or Owner
- **Returns**: All users in organization

#### `PATCH /members/<id>/role` - Update Member Role
- **Auth**: Owner only
- **Body**: `{role: 'admin'|'trainer'|'client'}`

#### `POST /invite` - Invite New Member
- **Auth**: Admin or Owner
- **Body**: `{email, role, first_name, last_name}`
- **Returns**: New user account

#### `GET /stats` - Organization Statistics
- **Auth**: Admin or Owner
- **Returns**: Aggregate stats across all trainers

## **RBAC Decorators**

Use these decorators to protect API endpoints:

```python
from app.utils.rbac import owner_required, admin_required, trainer_required, role_required

@api.route('/endpoint')
@login_required
@owner_required  # Only organization owner
def owner_only():
    pass

@api.route('/endpoint')
@login_required
@admin_required  # Owner or Admin
def admin_only():
    pass

@api.route('/endpoint')
@login_required
@trainer_required  # Owner, Admin, or Trainer
def trainer_access():
    pass

@api.route('/endpoint')
@login_required
@role_required('owner', 'admin')  # Multiple roles
def custom_roles():
    pass
```

## **User Permission Methods**

```python
# Check roles
current_user.is_owner()           # True if owner
current_user.is_admin()           # True if owner or admin
current_user.is_trainer()         # True if owner, admin, or trainer
current_user.is_client_user()     # True if client role

# Check permissions
current_user.can_manage_organization()     # Only owner
current_user.can_manage_users()            # Owner or admin
current_user.can_access_client_data(client_id)  # Check client access
```

## **Migration Steps**

### **1. Run Database Migration**
```bash
flask db migrate -m "Add organizations and RBAC"
flask db upgrade
```

### **2. Create Organizations for Existing Users**
Run this script to migrate existing users:

```python
from app import create_app, db
from app.models import Organization, User

app = create_app()
with app.app_context():
    # Find users without organizations
    users_without_org = User.query.filter_by(organization_id=None).all()
    
    for user in users_without_org:
        # Create organization for each user
        org = Organization(
            name=f"{user.full_name}'s Training Business",
            slug=f"{user.username}-fitness",
            email=user.email,
            subscription_tier='free'
        )
        db.session.add(org)
        db.session.flush()
        
        # Assign user as owner
        user.organization_id = org.id
        user.role = 'owner'
    
    db.session.commit()
    print(f"Migrated {len(users_without_org)} users to organizations")
```

### **3. Test RBAC**
```bash
# Test organization creation
curl -X POST http://localhost:5000/api/v1/organization \
  -H "Content-Type: application/json" \
  -d '{"name": "Elite Fitness"}'

# Test member invitation
curl -X POST http://localhost:5000/api/v1/organization/invite \
  -H "Content-Type: application/json" \
  -d '{"email": "trainer@example.com", "role": "trainer"}'
```

## **Frontend Integration**

### **Login Flow**
1. User logs in → Check `user.organization_id`
2. If no organization → Show "Create Organization" wizard
3. If has organization → Load dashboard based on role

### **Role-Based UI**
```javascript
// Check user role
if (user.role === 'owner') {
  showOrganizationSettings();
  showAllTrainers();
  showAllClients();
}

if (user.role === 'admin') {
  showTrainerManagement();
  showAllClients();
}

if (user.role === 'trainer') {
  showMyClients();
  showMyPrograms();
}

if (user.role === 'client') {
  showMyProfile();
  showMySessions();
}
```

### **API Calls with Organization Context**
```javascript
// All API calls automatically scoped to user's organization
const clients = await fetch('/api/v1/clients', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
// Returns only clients in user's organization
```

## **Subscription Tiers**

### **Free Tier**
- 1 trainer (owner only)
- 10 clients max
- Basic features

### **Basic Tier** ($29/month)
- Up to 3 trainers
- 50 clients max
- All core features

### **Pro Tier** ($99/month)
- Up to 10 trainers
- 200 clients max
- Advanced analytics
- Custom branding

### **Enterprise Tier** (Custom pricing)
- Unlimited trainers
- Unlimited clients
- White-label
- Priority support
- API access

## **Security Considerations**

### **Data Isolation**
- All queries MUST filter by `organization_id`
- Cross-organization data access is forbidden
- Use RBAC decorators on all sensitive endpoints

### **Best Practices**
```python
# ✅ CORRECT: Filter by organization
clients = Client.query.join(User).filter(
    User.organization_id == current_user.organization_id
).all()

# ❌ WRONG: No organization filter
clients = Client.query.all()  # Exposes all organizations' data!
```

## **Next Steps**

1. **Run Migration**: Add organization table and update users
2. **Migrate Existing Data**: Assign organizations to current users
3. **Update Existing APIs**: Add organization filtering to all endpoints
4. **Build Frontend**: Create React/Vue dashboard
5. **Add Client Portal**: Allow clients to log in and view their data
6. **Implement Billing**: Stripe integration for subscriptions

## **API Reference**

Total endpoints: **79+**
- 10 Organization Management endpoints
- 69 existing feature endpoints (now with RBAC)

All APIs use standard authentication and return:
```json
{
  "success": true,
  "data": {},
  "message": "Optional message"
}
```

Errors:
```json
{
  "success": false,
  "error": "Error message"
}
```
