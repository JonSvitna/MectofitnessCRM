# Client API Documentation

## Base URL
```
https://your-app.railway.app/api/v1/clients
```

## Authentication
All endpoints require authentication. Use your existing login session or implement JWT tokens for API-only access.

---

## Endpoints

### 1. List All Clients
Get a paginated list of clients with filtering and search.

```http
GET /api/v1/clients
```

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | int | 1 | Page number |
| `per_page` | int | 20 | Results per page (max: 100) |
| `search` | string | - | Search by name or email |
| `status` | string | "active" | Filter: "active", "inactive", or "all" |
| `fitness_level` | string | - | Filter by fitness level |
| `sort_by` | string | "last_name" | Sort field |
| `sort_order` | string | "asc" | "asc" or "desc" |

**Example Request:**
```bash
curl -X GET "https://your-app.railway.app/api/v1/clients?page=1&per_page=10&search=john&status=active" \
  -H "Cookie: session=your-session-cookie"
```

**Example Response:**
```json
{
  "success": true,
  "message": "Success",
  "data": {
    "clients": [
      {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "full_name": "John Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
        "is_active": true,
        "created_at": "2025-01-15T10:30:00",
        "updated_at": "2025-01-15T10:30:00"
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 10,
      "total_pages": 3,
      "total_items": 25,
      "has_next": true,
      "has_prev": false
    },
    "filters": {
      "search": "john",
      "status": "active",
      "fitness_level": "",
      "sort_by": "last_name",
      "sort_order": "asc"
    }
  }
}
```

---

### 2. Get Single Client
Get detailed information about a specific client.

```http
GET /api/v1/clients/{id}
```

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `include_sessions` | boolean | false | Include recent sessions |
| `include_programs` | boolean | false | Include assigned programs |

**Example Request:**
```bash
curl -X GET "https://your-app.railway.app/api/v1/clients/1?include_sessions=true&include_programs=true" \
  -H "Cookie: session=your-session-cookie"
```

**Example Response:**
```json
{
  "success": true,
  "message": "Success",
  "data": {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "date_of_birth": "1990-05-15",
    "gender": "Male",
    "address": "123 Main St, City, State 12345",
    "emergency_contact": "Jane Doe",
    "emergency_phone": "+0987654321",
    "fitness_goal": "Weight loss and muscle gain",
    "medical_conditions": "None",
    "fitness_level": "Intermediate",
    "weight": 180.5,
    "height": 72.0,
    "membership_type": "Premium",
    "membership_start": "2025-01-01",
    "membership_end": "2025-12-31",
    "notes": "Prefers morning sessions",
    "is_active": true,
    "created_at": "2025-01-15T10:30:00",
    "updated_at": "2025-01-15T10:30:00",
    "recent_sessions": [
      {
        "id": 10,
        "scheduled_start": "2025-01-20T09:00:00",
        "scheduled_end": "2025-01-20T10:00:00",
        "status": "scheduled",
        "session_type": "personal_training"
      }
    ],
    "programs": [
      {
        "id": 5,
        "name": "Beginner Strength Program",
        "status": "active",
        "start_date": "2025-01-01",
        "end_date": "2025-03-31"
      }
    ]
  }
}
```

---

### 3. Create New Client
Create a new client profile.

```http
POST /api/v1/clients
```

**Request Body:**
```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane@example.com",
  "phone": "+1234567890",
  "date_of_birth": "1995-08-20",
  "gender": "Female",
  "address": "456 Oak Ave, City, State 12345",
  "emergency_contact": "John Smith",
  "emergency_phone": "+0987654321",
  "fitness_goal": "Improve overall fitness",
  "medical_conditions": "None",
  "fitness_level": "Beginner",
  "weight": 140.0,
  "height": 65.0,
  "membership_type": "Basic",
  "membership_start": "2025-01-20",
  "membership_end": "2025-07-20",
  "notes": "New to fitness training"
}
```

**Required Fields:**
- `first_name`
- `last_name`
- `email`

**Example Request:**
```bash
curl -X POST "https://your-app.railway.app/api/v1/clients" \
  -H "Content-Type: application/json" \
  -H "Cookie: session=your-session-cookie" \
  -d '{
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane@example.com",
    "phone": "+1234567890",
    "fitness_goal": "Weight loss",
    "fitness_level": "Beginner"
  }'
```

**Example Response:**
```json
{
  "success": true,
  "message": "Client created successfully",
  "data": {
    "id": 2,
    "first_name": "Jane",
    "last_name": "Smith",
    "full_name": "Jane Smith",
    "email": "jane@example.com",
    "phone": "+1234567890",
    "fitness_goal": "Weight loss",
    "fitness_level": "Beginner",
    "is_active": true,
    "created_at": "2025-01-20T14:30:00",
    "updated_at": "2025-01-20T14:30:00"
  }
}
```

---

### 4. Update Client
Update an existing client's information.

```http
PUT /api/v1/clients/{id}
PATCH /api/v1/clients/{id}
```

**Request Body:**
```json
{
  "phone": "+1111111111",
  "fitness_level": "Intermediate",
  "weight": 145.0,
  "notes": "Making great progress!"
}
```

**Example Request:**
```bash
curl -X PUT "https://your-app.railway.app/api/v1/clients/2" \
  -H "Content-Type: application/json" \
  -H "Cookie: session=your-session-cookie" \
  -d '{
    "fitness_level": "Intermediate",
    "weight": 145.0
  }'
```

**Example Response:**
```json
{
  "success": true,
  "message": "Client updated successfully",
  "data": {
    "id": 2,
    "first_name": "Jane",
    "last_name": "Smith",
    "weight": 145.0,
    "fitness_level": "Intermediate",
    "updated_at": "2025-02-01T10:15:00"
  }
}
```

---

### 5. Delete Client
Soft delete (deactivate) or permanently delete a client.

```http
DELETE /api/v1/clients/{id}
```

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `permanent` | boolean | false | If true, permanently delete |

**Example Request (Soft Delete):**
```bash
curl -X DELETE "https://your-app.railway.app/api/v1/clients/2" \
  -H "Cookie: session=your-session-cookie"
```

**Example Request (Permanent Delete):**
```bash
curl -X DELETE "https://your-app.railway.app/api/v1/clients/2?permanent=true" \
  -H "Cookie: session=your-session-cookie"
```

**Example Response:**
```json
{
  "success": true,
  "message": "Client deactivated successfully",
  "data": {
    "client_id": 2
  }
}
```

---

### 6. Get Client Statistics
Get aggregate statistics about your clients.

```http
GET /api/v1/clients/stats
```

**Example Request:**
```bash
curl -X GET "https://your-app.railway.app/api/v1/clients/stats" \
  -H "Cookie: session=your-session-cookie"
```

**Example Response:**
```json
{
  "success": true,
  "message": "Success",
  "data": {
    "total_clients": 45,
    "active_clients": 42,
    "inactive_clients": 3,
    "recent_clients_30_days": 5,
    "by_fitness_level": {
      "Beginner": 15,
      "Intermediate": 20,
      "Advanced": 7,
      "Not Set": 3
    }
  }
}
```

---

## Error Responses

All endpoints return consistent error responses:

```json
{
  "success": false,
  "error": "Error message describing what went wrong"
}
```

**Common Error Codes:**
- `400` - Bad Request (invalid data, validation error)
- `404` - Not Found (client doesn't exist)
- `409` - Conflict (duplicate email)
- `500` - Server Error

**Example Error Response:**
```json
{
  "success": false,
  "error": "Missing required field: email"
}
```

---

## Testing the API

### Using curl:
```bash
# Login first to get session cookie
curl -X POST "https://your-app.railway.app/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=yourpassword" \
  -c cookies.txt

# Then use the saved cookie
curl -X GET "https://your-app.railway.app/api/v1/clients" \
  -b cookies.txt
```

### Using Python:
```python
import requests

# Login
session = requests.Session()
session.post('https://your-app.railway.app/auth/login', data={
    'username': 'admin',
    'password': 'yourpassword'
})

# Get clients
response = session.get('https://your-app.railway.app/api/v1/clients')
print(response.json())

# Create client
new_client = {
    'first_name': 'Test',
    'last_name': 'Client',
    'email': 'test@example.com',
    'fitness_level': 'Beginner'
}
response = session.post('https://your-app.railway.app/api/v1/clients', json=new_client)
print(response.json())
```

### Using Postman:
1. Import the endpoints
2. Set base URL as environment variable
3. Login to get session cookie
4. Use cookie for subsequent requests

---

## Next Steps

1. ✅ Test each endpoint with your Railway URL
2. ✅ Verify pagination works correctly
3. ✅ Test search and filter functionality
4. ✅ Create a few test clients
5. ✅ Test update and delete operations
6. 📋 Move on to Sessions API next

Ready to build the Sessions API next!
