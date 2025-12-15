# MectoFitness CRM - Rebuild Project

Complete separation of frontend and backend for streamlined development and deployment on Railway.

## 🎯 Project Overview

This is a complete restructure of MectoFitness CRM, separating the frontend marketing site from the backend CRM application. The system is designed to deploy three separate services on Railway:

1. **Frontend** - Static landing page for user acquisition
2. **Backend** - Flask REST API for CRM functionality
3. **Database** - PostgreSQL instance

## 📁 Project Structure

```
MectofitnessCRM/
├── frontend/                 # Static landing page
│   ├── src/
│   │   ├── styles/
│   │   │   └── main.css
│   │   └── main.js
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── railway.toml
│   └── README.md
│
├── backend/                  # Flask REST API
│   ├── app/
│   │   ├── models/
│   │   │   └── __init__.py
│   │   ├── routes/
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── config.py
│   ├── run.py
│   ├── gunicorn_config.py
│   ├── requirements.txt
│   ├── railway.toml
│   └── README.md
│
├── DEPLOYMENT_GUIDE.md      # Railway deployment instructions
└── ROADMAP.md               # Release roadmap with milestones
```

## 🚀 Quick Start

### Frontend Development

```bash
cd frontend
npm install
npm run dev
# Opens at http://localhost:3000
```

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
# API runs at http://localhost:5000
```

## 🛠 Technology Stack

### Frontend
- **Build Tool**: Vite 5.0
- **Styling**: Tailwind CSS 3.4
- **Language**: Vanilla JavaScript
- **HTTP Client**: Axios
- **Deployment**: Railway (static site)

### Backend
- **Framework**: Flask 3.0
- **Database ORM**: SQLAlchemy
- **Migrations**: Flask-Migrate
- **CORS**: Flask-CORS
- **Server**: Gunicorn
- **Deployment**: Railway

### Database
- **Production**: PostgreSQL (Railway)
- **Development**: SQLite

## 🎨 Design System

The project uses a **dark orange color scheme** consistent with the main branch:

- **Primary Orange**: `#F97316` (orange-500)
- **Dark Orange**: `#EA580C` (orange-600)
- **Background**: `#000000` (black)
- **Text**: White and gray shades

## ✨ Key Features

### Frontend
- ✅ Responsive design (mobile-first)
- ✅ Dark theme with orange accents
- ✅ Lead capture form
- ✅ Form validation
- ✅ Error handling
- ✅ Loading states
- ✅ Smooth scrolling
- ✅ SEO optimized

### Backend
- ✅ RESTful API design
- ✅ PostgreSQL database
- ✅ CORS configured
- ✅ Lead management endpoints
- ✅ Email validation
- ✅ Error handling
- ✅ Health check endpoints
- ✅ Production-ready logging

## 🔒 Security Notes

**Authentication is NOT configured** as per requirements. This will be added in a future milestone.

Current security measures:
- CORS configuration
- Email validation
- SQL injection protection (via SQLAlchemy)
- Environment variable management
- Secure secret key handling

## 📊 Database Schema

### Leads Table

| Column        | Type         | Constraints              |
|---------------|--------------|--------------------------|
| id            | INTEGER      | PRIMARY KEY              |
| name          | VARCHAR(255) | NOT NULL                 |
| email         | VARCHAR(255) | UNIQUE, NOT NULL, INDEXED|
| phone         | VARCHAR(50)  | NULLABLE                 |
| business_type | VARCHAR(100) | NOT NULL                 |
| message       | TEXT         | NULLABLE                 |
| source        | VARCHAR(100) | DEFAULT 'landing_page'   |
| status        | VARCHAR(50)  | DEFAULT 'new'            |
| created_at    | DATETIME     | NOT NULL                 |
| updated_at    | DATETIME     | NOT NULL                 |

## 🚢 Deployment

See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for detailed Railway deployment instructions.

### Railway Services

1. **Frontend Service**
   - Root directory: `frontend/`
   - Build: `npm install && npm run build`
   - Start: `npx serve -s dist -p $PORT`

2. **Backend Service**
   - Root directory: `backend/`
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn -c gunicorn_config.py run:app`

3. **PostgreSQL Service**
   - Standard Railway PostgreSQL template
   - Automatically connected via DATABASE_URL

## 📈 Roadmap

See [ROADMAP.md](./ROADMAP.md) for the complete release roadmap with milestone points.

### Upcoming Milestones

- **M1: Core Infrastructure** ✅ (Current)
- **M2: User Authentication** (Next)
- **M3: Trainer Dashboard** (Planned)
- **M4: Client Management** (Planned)
- **M5: Program Builder** (Planned)

## 🧪 Testing

### Frontend Testing
```bash
cd frontend
npm run build  # Test production build
npm run preview  # Preview production build
```

### Backend Testing
```bash
cd backend
python -m pytest  # Run tests (when implemented)
```

### Integration Testing
1. Start backend: `cd backend && python run.py`
2. Start frontend: `cd frontend && npm run dev`
3. Fill out the form at http://localhost:3000
4. Verify lead creation in backend logs

## 📝 API Documentation

### Endpoints

#### Health Check
```
GET /health
GET /api/health
```

#### Create Lead
```
POST /api/leads
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "business_type": "personal_trainer",
  "message": "Optional message"
}
```

#### List Leads
```
GET /api/leads?page=1&per_page=20&status=new
```

#### Get Lead
```
GET /api/leads/<id>
```

#### Update Lead
```
PUT /api/leads/<id>
Content-Type: application/json

{
  "status": "contacted"
}
```

#### Delete Lead
```
DELETE /api/leads/<id>
```

## 🤝 Contributing

1. Create feature branch from `copilot/rebuild-application-frontend-backend`
2. Make changes
3. Test locally
4. Submit pull request

## 📄 License

Proprietary - MectoFitness CRM

## 🆘 Support

For issues or questions:
1. Check the README files in frontend/ and backend/
2. Review DEPLOYMENT_GUIDE.md
3. Check Railway logs for deployment issues
4. Review API error responses

## 🔮 Future Enhancements

- User authentication (OAuth2/JWT)
- Trainer dashboard
- Client management
- Program builder
- Progress tracking
- Messaging system
- Payment integration
- Mobile apps
- Email automation
- Analytics dashboard
