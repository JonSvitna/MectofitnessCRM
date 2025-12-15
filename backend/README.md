# MectoFitness Backend API

Flask REST API for MectoFitness CRM. Handles user data capture and CRM functionality for trainers and clients.

## Features

- **RESTful API**: Clean, well-documented API endpoints
- **PostgreSQL Database**: Production-ready with SQLAlchemy ORM
- **CORS Enabled**: Secure cross-origin requests
- **Lead Management**: Capture and manage leads from landing page
- **Health Checks**: Built-in health monitoring
- **Production Ready**: Configured with Gunicorn for Railway deployment

## Tech Stack

- **Framework**: Flask 3.0
- **Database**: PostgreSQL (with SQLAlchemy ORM)
- **Migrations**: Flask-Migrate
- **CORS**: Flask-CORS
- **Server**: Gunicorn
- **Validation**: email-validator

## Project Structure

```
backend/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models/
│   │   └── __init__.py       # Database models
│   └── routes/
│       └── __init__.py       # API routes
├── config.py                 # Configuration
├── run.py                    # Application entry point
├── gunicorn_config.py        # Gunicorn configuration
├── requirements.txt          # Python dependencies
├── railway.toml              # Railway deployment config
└── README.md                 # This file
```

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL (for production) or SQLite (for development)

### Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the backend directory:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///mectofitness.db
CORS_ORIGINS=http://localhost:3000
PORT=5000
```

For production on Railway:
```env
FLASK_ENV=production
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://...  # Automatically set by Railway
CORS_ORIGINS=https://your-frontend-url.railway.app
```

### Database Setup

```bash
# Initialize database (creates tables)
python run.py

# Or use Flask-Migrate for migrations:
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Running the Application

### Development

```bash
# Run with Flask development server
python run.py

# Or with Flask CLI
flask run

# The API will be available at http://localhost:5000
```

### Production

```bash
# Run with Gunicorn
gunicorn -c gunicorn_config.py run:app

# The API will bind to the PORT environment variable
```

## API Endpoints

### Health Check

```
GET /health
GET /api/health
```

Returns API health status.

### Lead Management

#### Create Lead
```
POST /api/leads
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "business_type": "personal_trainer",
  "message": "I want to learn more"
}
```

**Response (201 Created):**
```json
{
  "message": "Lead created successfully",
  "lead": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "business_type": "personal_trainer",
    "message": "I want to learn more",
    "source": "landing_page",
    "status": "new",
    "created_at": "2024-12-15T10:00:00",
    "updated_at": "2024-12-15T10:00:00"
  }
}
```

#### Get All Leads
```
GET /api/leads?page=1&per_page=20&status=new
```

**Response (200 OK):**
```json
{
  "leads": [...],
  "total": 100,
  "page": 1,
  "per_page": 20,
  "pages": 5
}
```

#### Get Single Lead
```
GET /api/leads/<lead_id>
```

#### Update Lead
```
PUT /api/leads/<lead_id>
Content-Type: application/json

{
  "status": "contacted"
}
```

#### Delete Lead
```
DELETE /api/leads/<lead_id>
```

## Database Models

### Lead Model

| Field         | Type     | Required | Description                    |
|---------------|----------|----------|--------------------------------|
| id            | Integer  | Yes      | Primary key                    |
| name          | String   | Yes      | Full name                      |
| email         | String   | Yes      | Email address (unique)         |
| phone         | String   | No       | Phone number                   |
| business_type | String   | Yes      | Type of business               |
| message       | Text     | No       | Additional message             |
| source        | String   | No       | Lead source (default: landing_page) |
| status        | String   | No       | Lead status (default: new)     |
| created_at    | DateTime | Yes      | Creation timestamp             |
| updated_at    | DateTime | Yes      | Last update timestamp          |

## Deployment on Railway

### Prerequisites
1. Railway account
2. PostgreSQL service created in Railway
3. Backend service created in Railway

### Configuration

1. **Create PostgreSQL Service**:
   - In Railway, create a new PostgreSQL service
   - Note the connection string (automatically set as DATABASE_URL)

2. **Create Backend Service**:
   - Connect your GitHub repository
   - Set root directory to `backend/`
   - Railway will detect the `railway.toml` configuration

3. **Environment Variables**:
   Set these in Railway dashboard:
   ```
   FLASK_ENV=production
   SECRET_KEY=<generate-secure-key>
   CORS_ORIGINS=https://your-frontend-url.railway.app
   ```

4. **Deploy**:
   - Push to your repository
   - Railway will automatically deploy

### Build Command
Railway automatically uses:
```bash
pip install -r requirements.txt
```

### Start Command
Defined in `railway.toml`:
```bash
gunicorn -c gunicorn_config.py run:app
```

## Development Tips

### Database Migrations

```bash
# Create a migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback
flask db downgrade
```

### Testing

```bash
# Run with test configuration
FLASK_ENV=testing python run.py
```

### Debugging

Enable debug mode in development:
```python
# config.py already has DEBUG=True for development
```

View logs:
```bash
# In development
tail -f logs/app.log

# In Railway
# Use Railway dashboard logs viewer
```

## Security Considerations

1. **SECRET_KEY**: Always use a strong, random secret key in production
2. **CORS**: Set specific origins, not `*` in production
3. **Database**: Use PostgreSQL in production, not SQLite
4. **HTTPS**: Railway provides HTTPS automatically
5. **Environment Variables**: Never commit `.env` file

## Troubleshooting

### Database Connection Issues

```python
# Check DATABASE_URL format
# Correct: postgresql://user:pass@host:port/db
# Wrong: postgres://user:pass@host:port/db
```

### CORS Issues

```python
# Make sure CORS_ORIGINS includes your frontend URL
# Check preflight OPTIONS requests are allowed
```

### Port Issues

```python
# Railway sets PORT automatically
# Make sure your app binds to 0.0.0.0, not 127.0.0.1
```

## Future Enhancements

- [ ] Add authentication (OAuth2, JWT)
- [ ] Add rate limiting
- [ ] Add request validation with marshmallow
- [ ] Add caching with Redis
- [ ] Add file upload support
- [ ] Add email notifications
- [ ] Add webhooks
- [ ] Add API documentation with Swagger/OpenAPI

## License

Proprietary - MectoFitness CRM
