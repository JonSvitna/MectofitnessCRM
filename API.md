# API Documentation - MectoFitness CRM

## Overview

MectoFitness CRM provides a RESTful API for integration with gym management platforms and other fitness software. All API endpoints require authentication via Flask-Login session cookies.

## Base URL

```
http://localhost:5000/api/v1
```

For production, replace with your domain:
```
https://your-domain.com/api/v1
```

## Authentication

API requests require an authenticated session. First, authenticate via the web interface or use session cookies from a logged-in user.

### Login (Web Interface)
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=trainer&password=password123
```

## API Endpoints

### Clients

#### List All Clients

Get a list of all active clients for the authenticated trainer.

```http
GET /api/v1/clients
```

**Response:**
```json
{
  "clients": [
    {
      "id": 1,
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com",
      "phone": "+1-555-0100",
      "fitness_goal": "Weight loss"
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success
- `401 Unauthorized`: Not authenticated

---

### Sessions

#### List Sessions

Get training sessions with optional filtering.

```http
GET /api/v1/sessions?start_date=2024-01-01&end_date=2024-12-31
```

**Query Parameters:**
- `start_date` (optional): ISO 8601 date (e.g., "2024-01-01")
- `end_date` (optional): ISO 8601 date

**Response:**
```json
{
  "sessions": [
    {
      "id": 1,
      "title": "Upper Body Workout",
      "client_id": 1,
      "scheduled_start": "2024-12-08T10:00:00",
      "scheduled_end": "2024-12-08T11:00:00",
      "status": "scheduled",
      "location": "Main Gym"
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success
- `401 Unauthorized`: Not authenticated
- `400 Bad Request`: Invalid date format

---

### Programs

#### List Programs

Get training programs with optional client filtering.

```http
GET /api/v1/programs?client_id=1
```

**Query Parameters:**
- `client_id` (optional): Filter by specific client

**Response:**
```json
{
  "programs": [
    {
      "id": 1,
      "name": "12-Week Strength Building",
      "client_id": 1,
      "goal": "Build muscle mass",
      "duration_weeks": 12,
      "status": "active",
      "is_ai_generated": false
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Success
- `401 Unauthorized`: Not authenticated

---

### Webhooks

#### Gym Platform Webhook

Receive events from gym management platforms.

```http
POST /api/v1/webhook/gym-platform
Content-Type: application/json

{
  "event": "member_checkin",
  "member_id": "12345",
  "timestamp": "2024-12-08T10:00:00Z",
  "location": "Main Gym"
}
```

**Response:**
```json
{
  "status": "received"
}
```

**Status Codes:**
- `200 OK`: Webhook received and processed
- `400 Bad Request`: Invalid payload

## Integration Examples

### Python Example

```python
import requests

# Login
session = requests.Session()
session.post(
    'http://localhost:5000/auth/login',
    data={'username': 'trainer', 'password': 'password123'}
)

# Get clients
response = session.get('http://localhost:5000/api/v1/clients')
clients = response.json()['clients']

# Get sessions for today
from datetime import datetime
today = datetime.now().date().isoformat()
response = session.get(
    f'http://localhost:5000/api/v1/sessions',
    params={'start_date': today, 'end_date': today}
)
sessions = response.json()['sessions']
```

### JavaScript Example

```javascript
// Using fetch API
async function getClients() {
  const response = await fetch('/api/v1/clients', {
    credentials: 'include' // Include session cookies
  });
  const data = await response.json();
  return data.clients;
}

// Get sessions
async function getSessions(startDate, endDate) {
  const params = new URLSearchParams({
    start_date: startDate,
    end_date: endDate
  });
  
  const response = await fetch(`/api/v1/sessions?${params}`, {
    credentials: 'include'
  });
  const data = await response.json();
  return data.sessions;
}
```

### cURL Examples

```bash
# Login and save cookies
curl -c cookies.txt -X POST http://localhost:5000/auth/login \
  -d "username=trainer&password=password123"

# Get clients
curl -b cookies.txt http://localhost:5000/api/v1/clients

# Get sessions with date filter
curl -b cookies.txt "http://localhost:5000/api/v1/sessions?start_date=2024-01-01&end_date=2024-12-31"

# Get programs for specific client
curl -b cookies.txt "http://localhost:5000/api/v1/programs?client_id=1"
```

## Gym Platform Integration

### Supported Events

The webhook endpoint can receive various events from gym management systems:

- `member_checkin`: Member checks in at gym
- `membership_created`: New membership created
- `membership_expired`: Membership expired
- `class_booked`: Member books a class
- `class_cancelled`: Member cancels a class

### Example Integration Flow

1. **Gym Platform** → Webhook Event → **MectoFitness CRM**
2. CRM processes event and updates relevant data
3. Optionally sync back to gym platform via their API

### Configuration

To set up webhook integration:

1. Get your webhook URL: `https://your-domain.com/api/v1/webhook/gym-platform`
2. Configure in your gym platform's settings
3. Add API key to `.env` if required by gym platform
4. Test with sample payload

## Rate Limiting

Currently, no rate limiting is implemented. For production use, consider:

- Implementing Flask-Limiter
- Setting reasonable limits (e.g., 100 requests per minute)
- Returning `429 Too Many Requests` when exceeded

## Error Handling

All endpoints return appropriate HTTP status codes and JSON error messages:

```json
{
  "error": "Resource not found",
  "message": "The requested client does not exist"
}
```

**Common Status Codes:**
- `200 OK`: Success
- `400 Bad Request`: Invalid parameters
- `401 Unauthorized`: Not authenticated
- `404 Not Found`: Resource doesn't exist
- `500 Internal Server Error`: Server error

## Future API Endpoints

Planned additions:

- `POST /api/v1/clients` - Create new client
- `PUT /api/v1/clients/:id` - Update client
- `POST /api/v1/sessions` - Create session
- `PUT /api/v1/sessions/:id` - Update session
- `POST /api/v1/programs` - Create program
- `GET /api/v1/analytics` - Get business analytics

## Support

For API support or integration assistance:
- Open an issue on GitHub
- Check the main [README.md](README.md)
- Review [SETUP.md](SETUP.md) for configuration help

---

**API Version:** 1.0  
**Last Updated:** December 2024
