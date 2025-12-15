# MectoFitness CRM - Backend

Flask-based backend application providing the CRM tools and dashboard functionality.

## Overview

This directory contains the backend Flask application for MectoFitness CRM, including:
- RESTful API endpoints
- Database models and migrations
- Business logic and services
- Authentication and authorization
- React-based dashboard (built with Vite)

## Structure

```
backend/
├── app/                    # Main Flask application
│   ├── models/            # SQLAlchemy database models
│   ├── routes/            # API endpoints and view routes
│   │   ├── api_*.py      # RESTful API endpoints
│   │   ├── auth.py       # Authentication routes
│   │   └── main.py       # Main application routes
│   ├── services/          # Business logic layer
│   ├── utils/             # Utility functions
│   ├── static/            # Static assets and React dashboard
│   │   ├── dist/         # Built React app (generated)
│   │   └── src/          # React dashboard source
│   └── templates/         # Jinja2 templates
├── migrations/            # Database migration scripts
├── scripts/               # Utility scripts
│   ├── init_db.py        # Initialize database
│   ├── test_*.py         # Test scripts
│   └── ...
├── config.py              # Application configuration
├── run.py                 # Application entry point
├── requirements.txt       # Python dependencies
├── gunicorn_config.py     # Gunicorn configuration
└── vite.config.js         # Vite build config for React dashboard
```

## Quick Start

### Prerequisites
- Python 3.8+
- pip
- Node.js 16+ (for building React dashboard)

### Installation

1. **Install Python dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Initialize database:**
   ```bash
   python scripts/init_db.py
   ```

4. **(Optional) Build React dashboard:**
   ```bash
   cd ..  # Go to project root
   npm install
   npm run build
   ```

### Running the Application

**Development mode:**
```bash
python run.py
```

**Production mode:**
```bash
gunicorn -c gunicorn_config.py run:app
```

The application will be available at `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `GET /auth/logout` - User logout

### Client Management
- `GET /api/clients` - List all clients
- `POST /api/clients` - Create new client
- `GET /api/clients/<id>` - Get client details
- `PUT /api/clients/<id>` - Update client
- `DELETE /api/clients/<id>` - Delete client

### Session Management
- `GET /api/sessions` - List sessions
- `POST /api/sessions` - Create session
- `GET /api/sessions/<id>` - Get session details
- `PUT /api/sessions/<id>` - Update session
- `DELETE /api/sessions/<id>` - Delete session

### Other APIs
- Exercise Library: `/api/exercises/*`
- Program Builder: `/api/programs/*`
- Progress Tracking: `/api/progress/*`
- Nutrition Plans: `/api/nutrition/*`
- Booking System: `/api/booking/*`
- Payment Processing: `/api/payments/*`
- Dashboard Analytics: `/api/dashboard/*`

See `/docs/API.md` for complete API documentation.

## Database

The application uses SQLAlchemy ORM with support for:
- **Development**: SQLite (default)
- **Production**: PostgreSQL (recommended)

### Database Scripts

Located in `scripts/` directory:
- `init_db.py` - Initialize database schema
- `diagnose_db.py` - Database diagnostics
- `migrate_organizations.py` - Run migrations
- `test_db.py` - Test database connectivity

## Configuration

Configuration is managed through `config.py` and environment variables:

### Required Environment Variables
- `SECRET_KEY` - Flask secret key
- `DATABASE_URL` - Database connection string (optional, defaults to SQLite)

### Optional Environment Variables
- `FLASK_ENV` - Environment (development/production)
- `CORS_ORIGINS` - Allowed CORS origins
- `OPENAI_API_KEY` - OpenAI API key for chatbot
- `STRIPE_SECRET_KEY` - Stripe API key for payments
- `ZOOM_CLIENT_ID` - Zoom API credentials
- See `.env.example` for complete list

## Development

### Running Tests
```bash
# Set test environment
export FLASK_ENV=testing

# Run all tests
python -m pytest

# Run specific test scripts
python scripts/test_api_endpoints.py
python scripts/test_db.py
```

### React Dashboard Development
The React dashboard source is in `app/static/src/`. To develop:

```bash
# From project root
npm install
npm run dev  # Start Vite dev server with hot reload
```

Build for production:
```bash
npm run build  # Outputs to app/static/dist/
```

## Deployment

The backend can be deployed to various platforms:
- Railway
- Render
- Heroku
- Vercel (with adaptations)

See `/docs/deployment/` for platform-specific guides.

## Documentation

- **API Documentation**: `/docs/API.md`
- **Setup Guide**: `/docs/SETUP.md`
- **Features**: `/docs/FEATURES.md`
- **RBAC Guide**: `/docs/RBAC_GUIDE.md`
- **Deployment**: `/docs/deployment/`

## Tech Stack

- **Framework**: Flask 3.0+
- **Database**: SQLAlchemy 2.0+, PostgreSQL/SQLite
- **Authentication**: Flask-Login
- **API**: RESTful JSON APIs
- **Frontend Build**: Vite 5.0+
- **Dashboard**: React 18+, Tailwind CSS
- **Server**: Gunicorn (production)

## Support

For issues and questions:
- Check `/docs/` directory
- Open an issue on GitHub
- Contact maintainers
