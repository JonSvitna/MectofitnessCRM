# MectoFitness CRM

**Professional Personal Trainer Management Software**

MectoFitness CRM is a comprehensive management system designed specifically for personal trainers, fitness coaches, and gym professionals. Built with Flask and SQLite, it provides all the tools you need to manage clients, schedule sessions, create training programs, and integrate with popular calendar services.

## 🎯 Key Features

- **👥 Client Management**: Comprehensive client profiles with fitness goals, medical history, and progress tracking
- **📅 Session Scheduling**: Easy-to-use scheduling system with status tracking and notes
- **🏋️ Training Programs**: Create and manage custom workout programs for your clients
- **🤖 AI-Powered Programs**: Leverage AI to generate personalized training programs (framework ready)
- **📧 Calendar Integration**: Sync with Google Calendar and Outlook for seamless scheduling
- **🔗 Gym Platform APIs**: RESTful API for integration with gym management systems
- **📊 Progress Analytics**: Track client progress and business metrics
- **🎨 Modern UI**: Clean green, white, and black color scheme optimized for fitness professionals

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/JonSvitna/MectofitnessCRM.git
   cd MectofitnessCRM
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Verify setup (recommended)**
   ```bash
   python verify_setup.py
   ```
   This checks your database connection and configuration.

6. **Initialize the database**
   ```bash
   python run.py
   ```
   This will automatically create the database tables.

7. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

> **📖 Documentation**: See the [Complete Manual](docs/) for detailed setup, deployment, features, and API documentation.

### Optional: React Frontend

The application includes an optional modern React interface. The traditional Flask interface is fully functional by default.

To use the React interface:

```bash
# Install Node.js dependencies
npm install

# Build the React app
npm run build

# Access React interface at /app after logging in
```

See [Frontend Setup Guide](docs/01-getting-started/frontend-setup.md) for details.

## 📖 Documentation

**[Complete Manual](docs/)** - Comprehensive documentation including:

- **[Getting Started](docs/01-getting-started/)** - Installation, quickstart, database & frontend setup
- **[Deployment](docs/02-deployment/)** - Deploy to Render, Railway, Vercel, or split stack
- **[Features & Usage](docs/03-features/)** - All features, RBAC, AI programs, roadmap
- **[API Reference](docs/04-api/)** - Complete REST API documentation
- **[Architecture](docs/05-architecture/)** - Technical architecture and design
- **[UI & Theme](docs/06-ui-theme/)** - Theme system and customization

## 📖 Usage

### Getting Started

1. **Register an Account**: Create your personal trainer account at `/auth/register`
2. **Add Clients**: Navigate to Clients > Add New Client to start adding your training clients
3. **Schedule Sessions**: Create training sessions and link them to your clients
4. **Create Programs**: Build custom training programs with exercises
5. **Set Up Calendar Sync**: Connect Google Calendar or Outlook for automatic session syncing

For detailed usage information, see the [Features Guide](docs/03-features/).

### API Integration

The application provides RESTful API endpoints for integration with gym platforms:

- `GET /api/v1/clients` - List all clients
- `GET /api/v1/sessions` - List sessions with filtering
- `GET /api/v1/programs` - List training programs
- `POST /api/v1/webhook/gym-platform` - Webhook for gym platform events

See the complete [API Documentation](docs/04-api/) for details.

## 🎨 Design

### Color Scheme
- **Primary**: Teal blue (#367588)
- **Accent**: Yellow/orange (#FFC107, #FF9500)
- **Professional**: Clean, modern fitness aesthetic

See [Theme Documentation](docs/06-ui-theme/) for customization.

## 🚀 Deployment

Ready for production? Deploy to:
- **Render** (recommended for full features)
- **Railway** (modern with internal networking)
- **Vercel** (frontend only)

See the [Deployment Guide](docs/02-deployment/) for complete instructions.

## 🧪 Development

### Project Structure
```
MectofitnessCRM/
├── app/
│   ├── models/          # Database models
│   ├── routes/          # Application routes/blueprints
│   ├── static/          # CSS, JS, images, React app
│   └── templates/       # HTML templates
├── docs/               # Complete documentation
├── config.py           # Configuration
├── requirements.txt    # Python dependencies
└── run.py             # Application entry point
```

### Running Tests
```bash
# Verify setup
python verify_setup.py

# Test database
python test_db.py
```

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## 🎯 Roadmap

See the complete [Roadmap](docs/03-features/roadmap.md) for planned features and improvements.

---

**Built for Personal Trainers, By Fitness Professionals**

MectoFitness CRM - Empowering fitness professionals to grow their business 💪
