# Migration and Testing Instructions

## ✅ **What's Ready**

All code for RBAC and Organizations has been committed to GitHub and will be deployed to Railway automatically:

1. ✅ Organization model created
2. ✅ User model updated with `organization_id` and `role` fields
3. ✅ Organization API with 10 endpoints
4. ✅ RBAC decorators for permission control
5. ✅ Migration scripts ready

## 🚀 **Deployment to Railway**

### **Automatic Migration on Railway**

When the code is deployed to Railway, the database tables will be created automatically because:

1. **Flask-SQLAlchemy's `db.create_all()`** runs on startup (see `app/__init__.py`)
2. Railway PostgreSQL connection is configured
3. All models are imported and registered

### **Verify Deployment**

1. **Check Railway Logs**
```
railway logs
```

Look for:
- ✅ Database connection successful
- ✅ Database ready with X tables
- ✅ Organizations table created

2. **Check Tables Were Created**

Connect to Railway PostgreSQL:
```bash
railway connect
```

Then run:
```sql
-- Check if organizations table exists
\dt organizations

-- Check if user columns were added
\d users

-- View organizations
SELECT * FROM organizations;

-- View users with roles
SELECT id, username, email, role, organization_id FROM users;
```

## 🔧 **Manual Migration (If Needed)**

If tables aren't created automatically, run the migration script on Railway:

```bash
# SSH into Railway instance or use Railway CLI
railway run python run_migration.py
```

Then run the user migration:
```bash
railway run python migrate_organizations.py
```

## 📋 **Testing the RBAC System**

### **1. Test Organization Creation**

```bash
# Create a test organization
curl -X POST https://your-app.railway.app/api/v1/organization \
  -H "Content-Type: application/json" \
  -H "Cookie: session=YOUR_SESSION_COOKIE" \
  -d '{
    "name": "Elite Fitness Training",
    "business_type": "personal_trainer",
    "email": "owner@elitefitness.com",
    "phone": "+1234567890",
    "city": "New York",
    "state": "NY"
  }'
```

Expected response:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Elite Fitness Training",
    "slug": "elite-fitness-training",
    "role": "owner"
  },
  "message": "Organization created successfully"
}
```

### **2. Test Member Invitation**

```bash
# Invite a trainer (as owner)
curl -X POST https://your-app.railway.app/api/v1/organization/invite \
  -H "Content-Type: application/json" \
  -H "Cookie: session=OWNER_SESSION" \
  -d '{
    "email": "trainer@elitefitness.com",
    "role": "trainer",
    "first_name": "John",
    "last_name": "Trainer",
    "temporary_password": "ChangeMe123!"
  }'
```

### **3. Test Role-Based Access**

```bash
# As Trainer: Try to access organization settings (should fail)
curl -X PUT https://your-app.railway.app/api/v1/organization \
  -H "Content-Type: application/json" \
  -H "Cookie: session=TRAINER_SESSION" \
  -d '{"name": "New Name"}'
```

Expected:
```json
{
  "success": false,
  "error": "Owner access required"
}
```

### **4. Test Organization Stats**

```bash
# As Owner/Admin: Get organization statistics
curl https://your-app.railway.app/api/v1/organization/stats \
  -H "Cookie: session=OWNER_SESSION"
```

Expected:
```json
{
  "success": true,
  "data": {
    "organization": {
      "name": "Elite Fitness Training",
      "subscription_tier": "free"
    },
    "members": {
      "total_trainers": 2,
      "max_trainers": 1
    },
    "clients": {
      "total": 15,
      "active": 12,
      "max_clients": 10
    }
  }
}
```

## 🧪 **Complete API Test Suite**

### **Organization Endpoints**

| Method | Endpoint | Role Required | Test |
|--------|----------|--------------|------|
| GET | `/api/v1/organization` | Any | View org details |
| POST | `/api/v1/organization` | None | Create organization |
| PUT | `/api/v1/organization` | Owner | Update org |
| GET | `/api/v1/organization/members` | Admin+ | List members |
| PATCH | `/api/v1/organization/members/<id>/role` | Owner | Change role |
| POST | `/api/v1/organization/invite` | Admin+ | Invite member |
| GET | `/api/v1/organization/stats` | Admin+ | View stats |

### **Permission Tests**

| User Role | Can Do | Cannot Do |
|-----------|--------|-----------|
| **Owner** | Everything | - |
| **Admin** | Manage trainers, view all clients | Change org settings, billing |
| **Trainer** | Manage own clients, create programs | View other trainers' clients |
| **Client** | View own data | Create/edit anything |

## 🔍 **Debugging**

### **Check User Role**

```python
# In Python console on Railway
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    user = User.query.filter_by(email='your@email.com').first()
    print(f"Role: {user.role}")
    print(f"Org ID: {user.organization_id}")
    print(f"Is Owner: {user.is_owner()}")
    print(f"Is Admin: {user.is_admin()}")
```

### **Check Organization**

```python
from app.models import Organization

with app.app_context():
    org = Organization.query.get(1)
    print(f"Name: {org.name}")
    print(f"Trainers: {org.trainer_count}")
    print(f"Clients: {org.client_count}")
```

### **Fix Common Issues**

**Issue**: User has no organization
```python
# Assign user to organization
user.organization_id = 1
user.role = 'owner'
db.session.commit()
```

**Issue**: Multiple owners in organization
```python
# Only one owner allowed per org
# Change extra owners to admin
extra_owner = User.query.filter_by(organization_id=1, role='owner').offset(1).first()
extra_owner.role = 'admin'
db.session.commit()
```

## 📊 **Expected Database State After Migration**

### **organizations table**
```
id | name                  | slug                | subscription_tier | max_trainers | max_clients
---|-----------------------|---------------------|-------------------|--------------|------------
1  | John's Fitness        | johns-fitness       | free              | 1            | 10
2  | Elite Training Co     | elite-training-co   | free              | 1            | 10
```

### **users table**
```
id | username | email           | role    | organization_id
---|----------|-----------------|---------|----------------
1  | john     | john@email.com  | owner   | 1
2  | jane     | jane@email.com  | owner   | 2
3  | coach1   | coach@email.com | trainer | 1
```

## ✅ **Success Criteria**

- [x] Organizations table exists in Railway PostgreSQL
- [ ] All existing users have been assigned to organizations
- [ ] All users have roles assigned (default: owner for existing users)
- [ ] Organization API endpoints are accessible
- [ ] RBAC decorators block unauthorized access
- [ ] Owner can invite new members
- [ ] Trainers can only see their own clients
- [ ] Admins can see all organization data

## 🎯 **Next Steps After Migration**

1. **Test all endpoints** using the test suite above
2. **Verify data isolation** between organizations
3. **Build frontend** authentication and org management UI
4. **Implement client portal** (role: 'client')
5. **Add Stripe integration** for subscription billing

## 📞 **Support**

If you encounter issues:

1. Check Railway logs: `railway logs`
2. Verify database connection in logs
3. Run migration scripts manually if needed
4. Review RBAC_GUIDE.md for detailed documentation

---

**Last Updated**: December 9, 2025  
**Status**: Ready for Railway deployment
