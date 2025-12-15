# Backend Code Location

⚠️ **Important:** The backend code for MectoFitness CRM is located in the `/app` directory, not here.

## Architecture Overview

This project uses a **monolithic Flask architecture** where all backend code is integrated into the `app/` directory. The old separate `backend/` folder structure was removed in December 2024 as part of a codebase reorganization.

## Backend Code Structure

All backend functionality can be found in the following locations:

```
app/
├── models/          # Database models (SQLAlchemy)
├── routes/          # API endpoints and view routes (Flask blueprints)
│   ├── api_*.py    # RESTful API endpoints
│   ├── auth.py     # Authentication routes
│   └── main.py     # Main application routes
├── services/        # Business logic and service layer
├── utils/           # Utility functions and helpers
├── static/          # Frontend assets (React app, CSS, images)
└── templates/       # Jinja2 HTML templates
```

## Key Backend Components

### API Routes (`app/routes/`)
- **Authentication**: `auth.py`
- **Client Management**: `api_clients.py`
- **Session Management**: `api_sessions.py`
- **Exercise Library**: `api_exercises.py`
- **Program Builder**: `api_programs.py`
- **Progress Tracking**: `api_progress.py`
- **Nutrition Plans**: `api_nutrition.py`
- **Booking System**: `api_booking.py`
- **Payment Processing**: `api_payments.py`
- **Dashboard Analytics**: `api_dashboard.py`
- **Organization Settings**: `api_organization.py`
- **User Management**: `api_user.py`

### Database Models (`app/models/`)
- User, Organization, Client models
- Session, Exercise, Program models
- Progress tracking models
- Payment and booking models

### Business Logic (`app/services/`)
- Service layer for complex business operations
- Integration with external APIs (Stripe, Zoom, etc.)

## Configuration

- **Main Config**: `config.py` (in project root)
- **Application Factory**: `app/__init__.py`
- **Entry Point**: `run.py` (in project root)

## Database Management

Database scripts are in the `/scripts` directory:
- `init_db.py` - Initialize database
- `diagnose_db.py` - Database diagnostics
- `migrate_organizations.py` - Migration scripts

## Running the Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python scripts/init_db.py

# Run development server
python run.py
```

## Documentation

For more information, see:
- `/docs/API.md` - API documentation
- `/docs/SETUP.md` - Setup guide
- `/docs/FEATURES.md` - Feature overview
- `/README.md` - Main project README

## Why This Structure?

The monolithic architecture was adopted to:
- Simplify deployment
- Reduce configuration complexity
- Improve code organization
- Enable better integration between frontend and backend
- Streamline development workflow

---

**Note:** This README exists to help developers who might be looking for a `backend/` folder. All backend code is in `/app`.
