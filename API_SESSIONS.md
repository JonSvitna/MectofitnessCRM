# Sessions API Documentation

Complete REST API documentation for the MectoFitness CRM Session Management system.

**Base URL:** `https://your-domain.com/api/v1/sessions`

**Authentication:** All endpoints require authentication via Flask-Login session cookies or Bearer token.

---

## Table of Contents

1. [List Sessions](#1-list-sessions)
2. [Get Single Session](#2-get-single-session)
3. [Create Session](#3-create-session)
4. [Update Session](#4-update-session)
5. [Delete Session](#5-delete-session)
6. [Session Statistics](#6-session-statistics)
7. [Check Availability](#7-check-availability)
8. [Data Models](#data-models)
9. [Error Handling](#error-handling)

---

## 1. List Sessions

Get a paginated list of sessions with filtering, searching, and sorting.

**Endpoint:** `GET /api/v1/sessions`

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | integer | 1 | Page number for pagination |
| `per_page` | integer | 20 | Items per page (max: 100) |
| `client_id` | integer | - | Filter by client ID |
| `status` | string | - | Filter by status (scheduled, completed, cancelled, no-show) |
| `session_type` | string | - | Filter by type (personal, group, online, assessment) |
| `start_date` | string | - | Filter sessions from this date (ISO format) |
| `end_date` | string | - | Filter sessions up to this date (ISO format) |
| `include_client` | boolean | false | Include full client details |
| `include_trainer` | boolean | false | Include full trainer details |
| `sort_by` | string | scheduled_start | Sort field (scheduled_start, scheduled_end, created_at, updated_at, status, title) |
| `sort_order` | string | desc | Sort order (asc or desc) |

**Example Request:**

```bash
# Get upcoming sessions for this week
curl -X GET "https://your-domain.com/api/v1/sessions?start_date=2025-12-09T00:00:00&end_date=2025-12-15T23:59:59&status=scheduled&include_client=true" \
  -H "Cookie: session=your_session_cookie"

# Get all sessions for a specific client
curl -X GET "https://your-domain.com/api/v1/sessions?client_id=5&per_page=50&sort_by=scheduled_start&sort_order=desc" \
  -H "Cookie: session=your_session_cookie"
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "sessions": [
      {
        "id": 1,
        "title": "Personal Training Session",
        "description": "Full body workout focusing on strength",
        "session_type": "personal",
        "location": "Main Gym - Studio A",
        "scheduled_start": "2025-12-10T14:00:00",
        "scheduled_end": "2025-12-10T15:00:00",
        "actual_start": null,
        "actual_end": null,
        "status": "scheduled",
        "exercises_performed": null,
        "notes": "Client wants to focus on upper body",
        "client_feedback": null,
        "trainer_notes": "Remember client has shoulder sensitivity",
        "google_event_id": null,
        "outlook_event_id": null,
        "created_at": "2025-12-09T10:30:00",
        "updated_at": "2025-12-09T10:30:00",
        "trainer_id": 1,
        "client_id": 5,
        "client": {
          "id": 5,
          "name": "John Doe",
          "email": "john@example.com",
          "phone": "+1-555-0123",
          "status": "active"
        }
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total_pages": 3,
      "total_items": 48,
      "has_next": true,
      "has_prev": false
    }
  }
}
```

---

## 2. Get Single Session

Retrieve detailed information about a specific session.

**Endpoint:** `GET /api/v1/sessions/{session_id}`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `session_id` | integer | The ID of the session to retrieve |

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `include_client` | boolean | false | Include full client details |
| `include_trainer` | boolean | false | Include full trainer details |

**Example Request:**

```bash
curl -X GET "https://your-domain.com/api/v1/sessions/15?include_client=true&include_trainer=true" \
  -H "Cookie: session=your_session_cookie"
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "id": 15,
    "title": "HIIT Training",
    "description": "High intensity interval training session",
    "session_type": "personal",
    "location": "Outdoor Track",
    "scheduled_start": "2025-12-10T09:00:00",
    "scheduled_end": "2025-12-10T10:00:00",
    "actual_start": "2025-12-10T09:05:00",
    "actual_end": "2025-12-10T10:02:00",
    "status": "completed",
    "exercises_performed": "Sprints, burpees, mountain climbers, box jumps",
    "notes": "Great energy today",
    "client_feedback": "Tough but felt amazing after!",
    "trainer_notes": "Client showed significant improvement in stamina",
    "google_event_id": "abc123xyz",
    "outlook_event_id": null,
    "created_at": "2025-12-05T14:20:00",
    "updated_at": "2025-12-10T10:05:00",
    "trainer_id": 1,
    "client_id": 8,
    "client": {
      "id": 8,
      "name": "Sarah Johnson",
      "email": "sarah@example.com",
      "phone": "+1-555-0456",
      "status": "active"
    },
    "trainer": {
      "id": 1,
      "username": "trainer_mike",
      "email": "mike@mectofitness.com",
      "full_name": "Mike Thompson"
    }
  }
}
```

---

## 3. Create Session

Schedule a new training session.

**Endpoint:** `POST /api/v1/sessions`

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `client_id` | integer | Yes | ID of the client |
| `title` | string | Yes | Session title |
| `scheduled_start` | string | Yes | Start datetime (ISO format) |
| `scheduled_end` | string | Yes | End datetime (ISO format) |
| `description` | string | No | Session description |
| `session_type` | string | No | Type (personal, group, online, assessment, consultation) |
| `location` | string | No | Session location |
| `notes` | string | No | General session notes |
| `trainer_notes` | string | No | Private trainer notes |

**Example Request:**

```bash
curl -X POST "https://your-domain.com/api/v1/sessions" \
  -H "Content-Type: application/json" \
  -H "Cookie: session=your_session_cookie" \
  -d '{
    "client_id": 5,
    "title": "Initial Fitness Assessment",
    "description": "Comprehensive fitness evaluation and goal setting",
    "session_type": "assessment",
    "location": "Main Gym - Assessment Area",
    "scheduled_start": "2025-12-11T10:00:00",
    "scheduled_end": "2025-12-11T11:30:00",
    "notes": "Bring body composition analysis equipment",
    "trainer_notes": "Client mentioned previous knee injury"
  }'
```

**Python Example:**

```python
import requests
from datetime import datetime, timedelta

# Calculate session time
start_time = datetime.now() + timedelta(days=2)
end_time = start_time + timedelta(hours=1)

session_data = {
    "client_id": 5,
    "title": "Strength Training - Lower Body",
    "description": "Focus on squats, deadlifts, and leg press",
    "session_type": "personal",
    "location": "Main Gym - Weight Room",
    "scheduled_start": start_time.isoformat(),
    "scheduled_end": end_time.isoformat(),
    "notes": "Client prefers morning sessions",
    "trainer_notes": "Progressive overload - increase weight by 5lbs"
}

response = requests.post(
    "https://your-domain.com/api/v1/sessions",
    json=session_data,
    cookies={"session": "your_session_cookie"}
)

print(response.json())
```

**Example Response:**

```json
{
  "success": true,
  "message": "Session created successfully",
  "data": {
    "id": 25,
    "title": "Initial Fitness Assessment",
    "description": "Comprehensive fitness evaluation and goal setting",
    "session_type": "assessment",
    "location": "Main Gym - Assessment Area",
    "scheduled_start": "2025-12-11T10:00:00",
    "scheduled_end": "2025-12-11T11:30:00",
    "actual_start": null,
    "actual_end": null,
    "status": "scheduled",
    "exercises_performed": null,
    "notes": "Bring body composition analysis equipment",
    "client_feedback": null,
    "trainer_notes": "Client mentioned previous knee injury",
    "google_event_id": null,
    "outlook_event_id": null,
    "created_at": "2025-12-09T15:20:00",
    "updated_at": "2025-12-09T15:20:00",
    "trainer_id": 1,
    "client_id": 5,
    "client": {
      "id": 5,
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1-555-0123",
      "status": "active"
    }
  }
}
```

**Validation & Conflict Detection:**

The API automatically:
- Validates datetime formats (must be ISO 8601)
- Ensures end time is after start time
- Checks for scheduling conflicts with existing sessions
- Verifies client exists and belongs to the trainer

**Error Response (Conflict):**

```json
{
  "success": false,
  "error": "Scheduling conflict detected with session \"Personal Training Session\" at 2025-12-11T10:30:00"
}
```

---

## 4. Update Session

Update an existing session (supports partial updates).

**Endpoint:** `PUT /api/v1/sessions/{session_id}` or `PATCH /api/v1/sessions/{session_id}`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `session_id` | integer | The ID of the session to update |

**Request Body:** (All fields optional for PATCH)

Any session fields from the create endpoint can be updated.

**Example Request:**

```bash
# Update session status to completed and add notes
curl -X PATCH "https://your-domain.com/api/v1/sessions/25" \
  -H "Content-Type: application/json" \
  -H "Cookie: session=your_session_cookie" \
  -d '{
    "status": "completed",
    "actual_start": "2025-12-11T10:05:00",
    "actual_end": "2025-12-11T11:35:00",
    "exercises_performed": "Body composition scan, flexibility tests, strength assessments, cardiovascular evaluation",
    "trainer_notes": "Client showed good baseline fitness. Needs work on core strength and flexibility.",
    "client_feedback": "Really helpful assessment. Excited to start training!"
  }'

# Reschedule a session
curl -X PATCH "https://your-domain.com/api/v1/sessions/15" \
  -H "Content-Type: application/json" \
  -H "Cookie: session=your_session_cookie" \
  -d '{
    "scheduled_start": "2025-12-12T14:00:00",
    "scheduled_end": "2025-12-12T15:00:00"
  }'
```

**Python Example:**

```python
import requests

# Mark session as completed with details
update_data = {
    "status": "completed",
    "actual_start": "2025-12-10T09:05:00",
    "actual_end": "2025-12-10T10:02:00",
    "exercises_performed": "Bench press 3x10, Squats 4x8, Deadlifts 3x6",
    "trainer_notes": "Client hit new PR on deadlift!",
    "client_feedback": "Best workout yet!"
}

response = requests.patch(
    "https://your-domain.com/api/v1/sessions/20",
    json=update_data,
    cookies={"session": "your_session_cookie"}
)

print(response.json())
```

**Example Response:**

```json
{
  "success": true,
  "message": "Session updated successfully",
  "data": {
    "id": 25,
    "title": "Initial Fitness Assessment",
    "status": "completed",
    "actual_start": "2025-12-11T10:05:00",
    "actual_end": "2025-12-11T11:35:00",
    "exercises_performed": "Body composition scan, flexibility tests, strength assessments, cardiovascular evaluation",
    "trainer_notes": "Client showed good baseline fitness. Needs work on core strength and flexibility.",
    "client_feedback": "Really helpful assessment. Excited to start training!",
    "updated_at": "2025-12-11T11:40:00"
  }
}
```

---

## 5. Delete Session

Cancel or permanently delete a session.

**Endpoint:** `DELETE /api/v1/sessions/{session_id}`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `session_id` | integer | The ID of the session to delete |

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `permanent` | boolean | false | If true, permanently delete. Otherwise just cancel (soft delete) |

**Example Request:**

```bash
# Soft delete (cancel session)
curl -X DELETE "https://your-domain.com/api/v1/sessions/30" \
  -H "Cookie: session=your_session_cookie"

# Permanently delete
curl -X DELETE "https://your-domain.com/api/v1/sessions/30?permanent=true" \
  -H "Cookie: session=your_session_cookie"
```

**Example Response (Soft Delete):**

```json
{
  "success": true,
  "message": "Session cancelled successfully",
  "data": {
    "id": 30,
    "title": "Personal Training Session",
    "status": "cancelled",
    "updated_at": "2025-12-09T16:45:00"
  }
}
```

**Example Response (Permanent Delete):**

```json
{
  "success": true,
  "message": "Session permanently deleted"
}
```

---

## 6. Session Statistics

Get aggregate statistics about sessions.

**Endpoint:** `GET /api/v1/sessions/stats`

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `start_date` | string | Start date for stats (ISO format) |
| `end_date` | string | End date for stats (ISO format) |
| `client_id` | integer | Filter stats by specific client |

**Example Request:**

```bash
# Get stats for the current month
curl -X GET "https://your-domain.com/api/v1/sessions/stats?start_date=2025-12-01T00:00:00&end_date=2025-12-31T23:59:59" \
  -H "Cookie: session=your_session_cookie"

# Get stats for a specific client
curl -X GET "https://your-domain.com/api/v1/sessions/stats?client_id=5" \
  -H "Cookie: session=your_session_cookie"
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "total_sessions": 48,
    "by_status": {
      "completed": 32,
      "scheduled": 12,
      "cancelled": 3,
      "no-show": 1
    },
    "by_type": {
      "personal": 38,
      "group": 6,
      "online": 3,
      "assessment": 1
    },
    "upcoming_sessions": 8
  }
}
```

**Python Example:**

```python
import requests
from datetime import datetime, timedelta

# Get stats for last 30 days
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

params = {
    "start_date": start_date.isoformat(),
    "end_date": end_date.isoformat()
}

response = requests.get(
    "https://your-domain.com/api/v1/sessions/stats",
    params=params,
    cookies={"session": "your_session_cookie"}
)

stats = response.json()["data"]
print(f"Total sessions: {stats['total_sessions']}")
print(f"Completion rate: {stats['by_status']['completed'] / stats['total_sessions'] * 100:.1f}%")
```

---

## 7. Check Availability

Check trainer availability for scheduling new sessions.

**Endpoint:** `GET /api/v1/sessions/availability`

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `date` | string | today | Date to check (ISO format) |
| `duration` | integer | 60 | Desired session duration in minutes |

**Example Request:**

```bash
# Check availability for tomorrow with 90-minute session
curl -X GET "https://your-domain.com/api/v1/sessions/availability?date=2025-12-10&duration=90" \
  -H "Cookie: session=your_session_cookie"
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "date": "2025-12-10",
    "requested_duration": 90,
    "available_slots": [
      {
        "start": "2025-12-10T08:00:00",
        "end": "2025-12-10T10:00:00",
        "duration_minutes": 120
      },
      {
        "start": "2025-12-10T11:00:00",
        "end": "2025-12-10T14:00:00",
        "duration_minutes": 180
      },
      {
        "start": "2025-12-10T15:30:00",
        "end": "2025-12-10T20:00:00",
        "duration_minutes": 270
      }
    ],
    "booked_sessions": [
      {
        "start": "2025-12-10T10:00:00",
        "end": "2025-12-10T11:00:00",
        "title": "Personal Training - John Doe"
      },
      {
        "start": "2025-12-10T14:00:00",
        "end": "2025-12-10T15:30:00",
        "title": "Group Class - HIIT"
      }
    ]
  }
}
```

**Python Example:**

```python
import requests
from datetime import datetime, timedelta

def find_available_slot(date, duration=60):
    """Find available time slots for a session."""
    params = {
        "date": date.isoformat(),
        "duration": duration
    }
    
    response = requests.get(
        "https://your-domain.com/api/v1/sessions/availability",
        params=params,
        cookies={"session": "your_session_cookie"}
    )
    
    data = response.json()["data"]
    
    if data["available_slots"]:
        print(f"Available slots for {date.date()}:")
        for slot in data["available_slots"]:
            print(f"  {slot['start']} - {slot['end']} ({slot['duration_minutes']} min)")
    else:
        print(f"No availability on {date.date()}")
    
    return data

# Check next 7 days for availability
for i in range(7):
    check_date = datetime.now() + timedelta(days=i)
    find_available_slot(check_date, duration=60)
```

---

## Data Models

### Session Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique session identifier |
| `trainer_id` | integer | ID of the trainer |
| `client_id` | integer | ID of the client |
| `title` | string | Session title |
| `description` | string | Detailed session description |
| `session_type` | string | Type (personal, group, online, assessment, consultation) |
| `location` | string | Physical or virtual location |
| `scheduled_start` | datetime | Scheduled start time (ISO format) |
| `scheduled_end` | datetime | Scheduled end time (ISO format) |
| `actual_start` | datetime | Actual start time (ISO format) |
| `actual_end` | datetime | Actual end time (ISO format) |
| `status` | string | Status (scheduled, completed, cancelled, no-show) |
| `exercises_performed` | text | List or description of exercises |
| `notes` | text | General session notes |
| `client_feedback` | text | Client's feedback |
| `trainer_notes` | text | Private trainer notes |
| `google_event_id` | string | Google Calendar event ID |
| `outlook_event_id` | string | Outlook Calendar event ID |
| `created_at` | datetime | Record creation timestamp |
| `updated_at` | datetime | Last update timestamp |

### Session Status Values

- `scheduled` - Session is scheduled and pending
- `completed` - Session was completed successfully
- `cancelled` - Session was cancelled
- `no-show` - Client did not show up

### Session Type Values

- `personal` - One-on-one personal training
- `group` - Group training session
- `online` - Virtual/online session
- `assessment` - Fitness assessment or evaluation
- `consultation` - Consultation meeting

---

## Error Handling

All error responses follow this format:

```json
{
  "success": false,
  "error": "Error message description",
  "errors": {
    "field_name": "Specific field error message"
  }
}
```

### Common HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created successfully |
| 400 | Bad request (validation error) |
| 401 | Unauthorized (not logged in) |
| 403 | Forbidden (no permission) |
| 404 | Resource not found |
| 409 | Conflict (scheduling conflict) |
| 500 | Internal server error |

### Common Error Scenarios

**Validation Error:**
```json
{
  "success": false,
  "error": "Validation failed",
  "errors": {
    "scheduled_start": "Scheduled start time is required",
    "scheduled_end": "Scheduled end time must be after start time"
  }
}
```

**Permission Denied:**
```json
{
  "success": false,
  "error": "You do not have permission to view this session"
}
```

**Scheduling Conflict:**
```json
{
  "success": false,
  "error": "Scheduling conflict detected with session \"Personal Training Session\" at 2025-12-10T14:00:00"
}
```

**Not Found:**
```json
{
  "success": false,
  "error": "Session not found"
}
```

---

## Testing with Postman

### Environment Variables

Create a Postman environment with:

```
BASE_URL: https://your-domain.com
SESSION_COOKIE: your_session_cookie_value
```

### Collection Structure

1. **Authentication** → Login to get session cookie
2. **Sessions** → CRUD operations
   - List Sessions
   - Get Session
   - Create Session
   - Update Session
   - Delete Session
   - Session Stats
   - Check Availability

### Pre-request Script (for authenticated requests)

```javascript
pm.request.headers.add({
    key: 'Cookie',
    value: 'session=' + pm.environment.get('SESSION_COOKIE')
});
```

---

## Rate Limiting & Best Practices

1. **Pagination:** Always use pagination for list endpoints to avoid large responses
2. **Date Filters:** Use date ranges when querying sessions to improve performance
3. **Include Parameters:** Only request related data (client/trainer) when needed
4. **Soft Delete:** Prefer canceling sessions over permanent deletion for record keeping
5. **Conflict Checking:** Use the availability endpoint before creating sessions
6. **Datetime Format:** Always use ISO 8601 format (YYYY-MM-DDTHH:MM:SS)

---

## Support

For API issues or questions, contact the development team or refer to the main project documentation.

**Last Updated:** December 9, 2025  
**API Version:** 1.0
