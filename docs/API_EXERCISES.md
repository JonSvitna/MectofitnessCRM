# Exercise Library API Documentation

Complete REST API documentation for the MectoFitness CRM Exercise Library system.

**Base URL:** `https://your-domain.com/api/v1/exercises`

**Authentication:** All endpoints require authentication via Flask-Login session cookies or Bearer token.

**Exercise Data Source:** 742+ exercises from WGER Workout Manager (open-source) + custom trainer exercises

---

## Table of Contents

1. [List Exercises](#1-list-exercises)
2. [Get Single Exercise](#2-get-single-exercise)
3. [Create Custom Exercise](#3-create-custom-exercise)
4. [Update Exercise](#4-update-exercise)
5. [Delete Exercise](#5-delete-exercise)
6. [Exercise Statistics](#6-exercise-statistics)
7. [Get Categories](#7-get-categories)
8. [Get Muscle Groups](#8-get-muscle-groups)
9. [Get Equipment](#9-get-equipment)
10. [Seeding Database](#seeding-database)
11. [Data Models](#data-models)
12. [Error Handling](#error-handling)

---

## 1. List Exercises

Browse and search exercises with advanced filtering.

**Endpoint:** `GET /api/v1/exercises`

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | integer | 1 | Page number for pagination |
| `per_page` | integer | 20 | Items per page (max: 100) |
| `search` | string | - | Search in exercise name and description |
| `category` | string | - | Filter by category (strength, cardio, flexibility, balance, mobility) |
| `muscle` | string | - | Filter by muscle group (partial match) |
| `equipment` | string | - | Filter by equipment (partial match) |
| `difficulty` | string | - | Filter by difficulty (beginner, intermediate, advanced) |
| `exercise_type` | string | - | Filter by type (compound, isolation, bodyweight, cardio, plyometric) |
| `custom_only` | boolean | false | Show only trainer's custom exercises |
| `include_usage` | boolean | false | Include usage statistics |
| `sort_by` | string | name | Sort field (name, category, difficulty_level, usage_count, created_at) |
| `sort_order` | string | asc | Sort order (asc or desc) |

**Example Request:**

```bash
# Search for chest exercises
curl -X GET "https://your-domain.com/api/v1/exercises?search=bench%20press&category=strength" \
  -H "Cookie: session=your_session_cookie"

# Get all exercises for specific muscle group
curl -X GET "https://your-domain.com/api/v1/exercises?muscle=chest&per_page=50" \
  -H "Cookie: session=your_session_cookie"

# Get beginner bodyweight exercises
curl -X GET "https://your-domain.com/api/v1/exercises?difficulty=beginner&equipment=bodyweight" \
  -H "Cookie: session=your_session_cookie"
```

**Python Example:**

```python
import requests

# Search for squats
params = {
    "search": "squat",
    "category": "strength",
    "muscle": "quads",
    "per_page": 20
}

response = requests.get(
    "https://your-domain.com/api/v1/exercises",
    params=params,
    cookies={"session": "your_session_cookie"}
)

exercises = response.json()["data"]["exercises"]
for ex in exercises:
    print(f"{ex['name']} - {ex['category']} - {ex['difficulty_level']}")
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "exercises": [
      {
        "id": 145,
        "name": "Barbell Bench Press",
        "description": "Classic compound exercise for chest development",
        "category": "strength",
        "primary_muscle_groups": ["chest", "triceps", "anterior deltoid"],
        "secondary_muscle_groups": ["middle back", "lats"],
        "difficulty_level": "intermediate",
        "equipment_required": ["barbell", "bench"],
        "exercise_type": "compound",
        "setup_instructions": null,
        "execution_steps": [],
        "common_mistakes": [],
        "tips_and_cues": [],
        "image_url": "https://wger.de/media/exercise-images/145.png",
        "video_url": null,
        "animation_url": null,
        "easier_variations": [],
        "harder_variations": [],
        "alternative_exercises": [],
        "contraindications": [],
        "injury_considerations": null,
        "typical_sets": null,
        "typical_reps": null,
        "typical_rest_seconds": null,
        "tags": [],
        "is_custom": false,
        "is_public": true,
        "is_active": true,
        "created_at": "2025-12-09T16:30:00",
        "updated_at": "2025-12-09T16:30:00"
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total_pages": 38,
      "total_items": 742,
      "has_next": true,
      "has_prev": false
    }
  }
}
```

---

## 2. Get Single Exercise

Retrieve detailed information about a specific exercise.

**Endpoint:** `GET /api/v1/exercises/{exercise_id}`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `exercise_id` | integer | The ID of the exercise to retrieve |

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `include_usage` | boolean | false | Include usage statistics |

**Example Request:**

```bash
curl -X GET "https://your-domain.com/api/v1/exercises/145?include_usage=true" \
  -H "Cookie: session=your_session_cookie"
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "id": 145,
    "name": "Barbell Bench Press",
    "description": "Classic compound exercise for chest development. Lie on bench, lower bar to chest, press up.",
    "category": "strength",
    "primary_muscle_groups": ["chest", "triceps", "anterior deltoid"],
    "secondary_muscle_groups": ["middle back", "lats"],
    "difficulty_level": "intermediate",
    "equipment_required": ["barbell", "bench"],
    "exercise_type": "compound",
    "setup_instructions": "Lie flat on bench, feet flat on floor. Grip barbell slightly wider than shoulder width.",
    "execution_steps": [
      "Unrack the bar and hold above chest with arms extended",
      "Lower bar slowly to mid-chest while inhaling",
      "Press bar back up while exhaling",
      "Repeat for desired reps"
    ],
    "common_mistakes": [
      "Bouncing bar off chest",
      "Flaring elbows too wide",
      "Arching back excessively"
    ],
    "tips_and_cues": [
      "Keep shoulder blades retracted",
      "Drive through heels",
      "Maintain wrist alignment"
    ],
    "image_url": "https://wger.de/media/exercise-images/145.png",
    "video_url": null,
    "typical_sets": "3-4",
    "typical_reps": "6-10",
    "typical_rest_seconds": 180,
    "tags": ["push", "chest", "compound", "strength"],
    "is_custom": false,
    "is_public": true,
    "is_active": true,
    "usage_count": 247,
    "average_rating": 4.8
  }
}
```

---

## 3. Create Custom Exercise

Create a new custom exercise specific to your training methods.

**Endpoint:** `POST /api/v1/exercises`

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Exercise name |
| `category` | string | Yes | Category (strength, cardio, flexibility, balance, mobility) |
| `description` | string | No | Exercise description |
| `primary_muscle_groups` | array | No | Array of primary muscles targeted |
| `secondary_muscle_groups` | array | No | Array of secondary muscles |
| `equipment_required` | array | No | Array of equipment needed |
| `difficulty_level` | string | No | Difficulty (beginner, intermediate, advanced) |
| `exercise_type` | string | No | Type (compound, isolation, bodyweight, cardio, plyometric) |
| `setup_instructions` | string | No | Setup instructions |
| `execution_steps` | array | No | Step-by-step execution instructions |
| `common_mistakes` | array | No | Array of common mistakes |
| `tips_and_cues` | array | No | Coaching tips and cues |
| `image_url` | string | No | Image URL |
| `video_url` | string | No | Video URL |
| `contraindications` | array | No | Array of contraindications |
| `injury_considerations` | string | No | Injury considerations |
| `typical_sets` | string | No | Typical sets (e.g., "3-4") |
| `typical_reps` | string | No | Typical reps (e.g., "8-12") |
| `typical_rest_seconds` | integer | No | Rest period in seconds |
| `tags` | array | No | Searchable tags |
| `is_public` | boolean | No | Make visible to other trainers (default: false) |

**Example Request:**

```bash
curl -X POST "https://your-domain.com/api/v1/exercises" \
  -H "Content-Type: application/json" \
  -H "Cookie: session=your_session_cookie" \
  -d '{
    "name": "Single Leg Romanian Deadlift with Rotation",
    "category": "strength",
    "description": "Advanced unilateral hamstring exercise with rotational component for core engagement",
    "primary_muscle_groups": ["hamstrings", "glutes"],
    "secondary_muscle_groups": ["abs", "obliques", "lower back"],
    "equipment_required": ["dumbbell"],
    "difficulty_level": "advanced",
    "exercise_type": "compound",
    "setup_instructions": "Stand on one leg holding dumbbell in opposite hand",
    "execution_steps": [
      "Hinge at hip while extending free leg behind",
      "Rotate torso toward standing leg at bottom",
      "Return to start while maintaining balance",
      "Complete reps then switch sides"
    ],
    "common_mistakes": [
      "Rounding lower back",
      "Losing balance too quickly",
      "Not engaging core during rotation"
    ],
    "tips_and_cues": [
      "Keep hips square throughout movement",
      "Focus on hinging, not squatting",
      "Squeeze glute at top of movement"
    ],
    "typical_sets": "3",
    "typical_reps": "8-10 per leg",
    "typical_rest_seconds": 90,
    "tags": ["unilateral", "balance", "rotation", "functional"],
    "is_public": false
  }'
```

**Python Example:**

```python
import requests

exercise_data = {
    "name": "Banded Pull-Aparts",
    "category": "strength",
    "description": "Excellent rear delt and upper back activation exercise",
    "primary_muscle_groups": ["middle back", "rear deltoid"],
    "secondary_muscle_groups": ["trapezius"],
    "equipment_required": ["resistance band"],
    "difficulty_level": "beginner",
    "exercise_type": "isolation",
    "execution_steps": [
        "Hold resistance band at shoulder height, arms extended",
        "Pull band apart by moving hands away from each other",
        "Squeeze shoulder blades together",
        "Slowly return to start"
    ],
    "typical_sets": "3-4",
    "typical_reps": "15-20",
    "typical_rest_seconds": 45,
    "tags": ["shoulder health", "warm-up", "activation"],
    "is_public": True
}

response = requests.post(
    "https://your-domain.com/api/v1/exercises",
    json=exercise_data,
    cookies={"session": "your_session_cookie"}
)

print(response.json())
```

**Example Response:**

```json
{
  "success": true,
  "message": "Custom exercise created successfully",
  "data": {
    "id": 825,
    "name": "Single Leg Romanian Deadlift with Rotation",
    "category": "strength",
    "difficulty_level": "advanced",
    "is_custom": true,
    "created_by_trainer_id": 1,
    "is_public": false,
    "created_at": "2025-12-09T17:45:00"
  }
}
```

---

## 4. Update Exercise

Update an existing custom exercise. Only the creator can update their custom exercises.

**Endpoint:** `PUT /api/v1/exercises/{exercise_id}` or `PATCH /api/v1/exercises/{exercise_id}`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `exercise_id` | integer | The ID of the exercise to update |

**Request Body:** (All fields optional for PATCH)

Any fields from the create endpoint can be updated.

**Example Request:**

```bash
# Update exercise description and difficulty
curl -X PATCH "https://your-domain.com/api/v1/exercises/825" \
  -H "Content-Type: application/json" \
  -H "Cookie: session=your_session_cookie" \
  -d '{
    "description": "Updated: Advanced unilateral exercise combining hip hinge with anti-rotation",
    "difficulty_level": "advanced",
    "tips_and_cues": [
      "Keep hips square throughout movement",
      "Focus on hinging, not squatting",
      "Squeeze glute at top of movement",
      "Start without rotation if balance is an issue"
    ]
  }'
```

**Example Response:**

```json
{
  "success": true,
  "message": "Exercise updated successfully",
  "data": {
    "id": 825,
    "name": "Single Leg Romanian Deadlift with Rotation",
    "description": "Updated: Advanced unilateral exercise combining hip hinge with anti-rotation",
    "difficulty_level": "advanced",
    "updated_at": "2025-12-09T18:00:00"
  }
}
```

---

## 5. Delete Exercise

Deactivate or permanently delete a custom exercise.

**Endpoint:** `DELETE /api/v1/exercises/{exercise_id}`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `exercise_id` | integer | The ID of the exercise to delete |

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `permanent` | boolean | false | If true, permanently delete. Otherwise deactivate |

**Example Request:**

```bash
# Soft delete (deactivate)
curl -X DELETE "https://your-domain.com/api/v1/exercises/825" \
  -H "Cookie: session=your_session_cookie"

# Permanently delete
curl -X DELETE "https://your-domain.com/api/v1/exercises/825?permanent=true" \
  -H "Cookie: session=your_session_cookie"
```

**Example Response:**

```json
{
  "success": true,
  "message": "Exercise deactivated successfully",
  "data": {
    "id": 825,
    "name": "Single Leg Romanian Deadlift with Rotation",
    "is_active": false
  }
}
```

---

## 6. Exercise Statistics

Get aggregate statistics about the exercise library.

**Endpoint:** `GET /api/v1/exercises/stats`

**Example Request:**

```bash
curl -X GET "https://your-domain.com/api/v1/exercises/stats" \
  -H "Cookie: session=your_session_cookie"
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "total_exercises": 748,
    "standard_exercises": 742,
    "custom_exercises": 6,
    "by_category": {
      "strength": 625,
      "cardio": 78,
      "flexibility": 32,
      "balance": 13
    },
    "by_difficulty": {
      "beginner": 180,
      "intermediate": 425,
      "advanced": 143
    },
    "most_popular": [
      {
        "id": 145,
        "name": "Barbell Bench Press",
        "usage_count": 247,
        "category": "strength"
      },
      {
        "id": 203,
        "name": "Barbell Squat",
        "usage_count": 235,
        "category": "strength"
      }
    ]
  }
}
```

---

## 7. Get Categories

Get all available exercise categories with counts.

**Endpoint:** `GET /api/v1/exercises/categories`

**Example Request:**

```bash
curl -X GET "https://your-domain.com/api/v1/exercises/categories" \
  -H "Cookie: session=your_session_cookie"
```

**Example Response:**

```json
{
  "success": true,
  "data": [
    {
      "name": "strength",
      "count": 625
    },
    {
      "name": "cardio",
      "count": 78
    },
    {
      "name": "flexibility",
      "count": 32
    },
    {
      "name": "balance",
      "count": 13
    }
  ]
}
```

---

## 8. Get Muscle Groups

Get all unique muscle groups available in the library.

**Endpoint:** `GET /api/v1/exercises/muscles`

**Example Request:**

```bash
curl -X GET "https://your-domain.com/api/v1/exercises/muscles" \
  -H "Cookie: session=your_session_cookie"
```

**Example Response:**

```json
{
  "success": true,
  "data": [
    "abs",
    "anterior deltoid",
    "biceps",
    "calves",
    "chest",
    "glutes",
    "hamstrings",
    "lats",
    "middle back",
    "obliques",
    "quads",
    "trapezius",
    "triceps"
  ]
}
```

---

## 9. Get Equipment

Get all unique equipment types in the library.

**Endpoint:** `GET /api/v1/exercises/equipment`

**Example Request:**

```bash
curl -X GET "https://your-domain.com/api/v1/exercises/equipment" \
  -H "Cookie: session=your_session_cookie"
```

**Example Response:**

```json
{
  "success": true,
  "data": [
    "barbell",
    "bench",
    "dumbbell",
    "gym mat",
    "incline bench",
    "kettlebell",
    "none (bodyweight)",
    "pull-up bar",
    "resistance band",
    "swiss ball",
    "sz-bar"
  ]
}
```

---

## Seeding Database

### Initial Setup

Seed your database with 742+ exercises from WGER:

```bash
# Run the seed script
python seed_exercises.py
```

The script will:
1. Fetch exercises from WGER API
2. Transform data to match your schema
3. Populate `exercise_library` table
4. Show statistics and breakdown

**Output:**

```
============================================================
SEEDING EXERCISE LIBRARY FROM WGER API
============================================================

📥 Fetching exercises from WGER API...
This may take a few minutes...

✅ Fetched 742 exercises from WGER

📝 Processing and inserting exercises...
✅ Inserted 50 exercises...
✅ Inserted 100 exercises...
...
✅ Inserted 742 exercises...

============================================================
✅ SEEDING COMPLETE!
============================================================
✅ Successfully inserted: 742 exercises

📊 Total exercises in library: 742
   - Standard exercises: 742
   - Custom exercises: 0

📋 Exercise breakdown by category:
   - strength: 625
   - cardio: 78
   - flexibility: 32
   - balance: 7
```

### Re-seeding

To update the library:

```bash
python seed_exercises.py
# Confirm deletion of existing exercises when prompted
```

---

## Data Models

### Exercise Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique exercise identifier |
| `name` | string | Exercise name |
| `description` | text | Exercise description |
| `category` | string | Category (strength, cardio, flexibility, balance, mobility) |
| `primary_muscle_groups` | array | Primary muscles targeted |
| `secondary_muscle_groups` | array | Secondary muscles engaged |
| `difficulty_level` | string | Difficulty (beginner, intermediate, advanced) |
| `equipment_required` | array | Equipment needed |
| `exercise_type` | string | Type (compound, isolation, bodyweight, cardio, plyometric) |
| `setup_instructions` | text | Setup instructions |
| `execution_steps` | array | Step-by-step instructions |
| `common_mistakes` | array | Common mistakes to avoid |
| `tips_and_cues` | array | Coaching tips |
| `image_url` | string | Image URL |
| `video_url` | string | Video URL |
| `animation_url` | string | Animation/GIF URL |
| `easier_variations` | array | Easier variation IDs |
| `harder_variations` | array | Harder variation IDs |
| `alternative_exercises` | array | Alternative exercise IDs |
| `contraindications` | array | Medical contraindications |
| `injury_considerations` | text | Injury considerations |
| `typical_sets` | string | Typical sets (e.g., "3-4") |
| `typical_reps` | string | Typical reps (e.g., "8-12") |
| `typical_rest_seconds` | integer | Rest period in seconds |
| `tags` | array | Searchable tags |
| `usage_count` | integer | Number of times used |
| `average_rating` | float | Average rating |
| `is_custom` | boolean | Whether exercise is custom |
| `created_by_trainer_id` | integer | Creator trainer ID (if custom) |
| `is_public` | boolean | Whether exercise is public |
| `is_active` | boolean | Whether exercise is active |
| `created_at` | datetime | Creation timestamp |
| `updated_at` | datetime | Last update timestamp |

### Category Values

- `strength` - Strength training exercises
- `cardio` - Cardiovascular exercises
- `flexibility` - Stretching and flexibility
- `balance` - Balance and stability exercises
- `mobility` - Mobility and movement exercises

### Difficulty Levels

- `beginner` - Beginner-friendly
- `intermediate` - Intermediate level
- `advanced` - Advanced/expert level

### Exercise Types

- `compound` - Multi-joint movements
- `isolation` - Single-joint movements
- `bodyweight` - Bodyweight only
- `cardio` - Cardiovascular
- `plyometric` - Explosive/jump training

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
| 409 | Conflict (duplicate name) |
| 500 | Internal server error |

### Common Error Scenarios

**Validation Error:**
```json
{
  "success": false,
  "error": "Validation failed",
  "errors": {
    "name": "Exercise name is required",
    "category": "Invalid category. Must be one of: strength, cardio, flexibility, balance, mobility"
  }
}
```

**Permission Denied:**
```json
{
  "success": false,
  "error": "You do not have permission to update this exercise"
}
```

**Duplicate Exercise:**
```json
{
  "success": false,
  "error": "You already have a custom exercise named \"My Custom Exercise\""
}
```

**Cannot Modify Standard Exercise:**
```json
{
  "success": false,
  "error": "Cannot modify standard exercises from the library"
}
```

---

## Best Practices

1. **Search First:** Use the search and filter endpoints before creating custom exercises
2. **Tag Properly:** Add relevant tags to custom exercises for easy discovery
3. **Document Well:** Include detailed instructions and tips for custom exercises
4. **Share Safely:** Only make exercises public if you want other trainers to use them
5. **Soft Delete:** Prefer deactivating over permanent deletion for record keeping
6. **Use Categories:** Browse by category first, then filter by muscle/equipment
7. **Check Variations:** Look for easier/harder variations before creating custom progressions

---

## Support

For API issues or questions, contact the development team or refer to the main project documentation.

**Data Source:** WGER Workout Manager (https://wger.de)  
**License:** Open source exercise data under AGPLv3+

**Last Updated:** December 9, 2025  
**API Version:** 1.0
