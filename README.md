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

> **Note**: For PostgreSQL setup, see [POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md). For troubleshooting, see [QUICKSTART.md](QUICKSTART.md).

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

See [ROUTING_ARCHITECTURE.md](ROUTING_ARCHITECTURE.md) for details on the dual routing system.

## 📖 Usage

### Getting Started

1. **Register an Account**: Create your personal trainer account at `/auth/register`
2. **Add Clients**: Navigate to Clients > Add New Client to start adding your training clients
3. **Schedule Sessions**: Create training sessions and link them to your clients
4. **Create Programs**: Build custom training programs with exercises
5. **Set Up Calendar Sync**: Connect Google Calendar or Outlook for automatic session syncing

### API Integration

The application provides RESTful API endpoints for integration with gym platforms:

- `GET /api/v1/clients` - List all clients
- `GET /api/v1/sessions` - List sessions with filtering
- `GET /api/v1/programs` - List training programs
- `POST /api/v1/webhook/gym-platform` - Webhook for gym platform events

API authentication is handled through Flask-Login sessions.

## 🎨 Design & SEO

### Color Scheme
- **Primary Green**: `#2ECC71` - Main brand color
- **Dark Green**: `#27AE60` - Hover states and accents
- **Black**: `#1C1C1C` - Text and headers
- **White**: `#FFFFFF` - Backgrounds and contrast

### SEO Optimization
The application is optimized for fitness industry keywords:
- Personal trainer software
- Fitness CRM
- Gym management
- Client tracking
- Workout programs
- Trainer scheduling
- Fitness coaching

## 🤖 AI Training Program Generation

The application includes a framework for AI-powered training program generation. To implement:

1. **Prepare Your Knowledge Base**: Add your training expertise and program templates
2. **Train the Model**: Use scikit-learn to train on your knowledge base
3. **Integrate**: The AI model will generate personalized programs based on client goals and fitness level

Example model training structure is included in the codebase.

## 📅 Calendar Integration

### Google Calendar Setup

1. Create a Google Cloud Project
2. Enable Google Calendar API
3. Create OAuth 2.0 credentials
4. Download credentials JSON and place in `credentials/google_credentials.json`
5. Add credentials to `.env` file

### Outlook Calendar Setup

1. Register app in Azure Portal
2. Configure Microsoft Graph API permissions
3. Add Client ID and Secret to `.env` file

## 🗄️ Database Schema

The application uses SQLite with the following main tables:

- **users**: Personal trainers/coaches
- **clients**: Training clients
- **sessions**: Training sessions
- **programs**: Training programs
- **exercises**: Individual exercises in programs
- **calendar_integrations**: Calendar sync settings

## 🔧 Configuration

Edit `config.py` to customize:
- Database connection
- Secret keys
- Session settings
- API credentials
- Upload limits

## 🧪 Development

### Project Structure
```
MectofitnessCRM/
├── app/
│   ├── models/          # Database models
│   ├── routes/          # Application routes/blueprints
│   ├── static/          # CSS, JS, images
│   └── templates/       # HTML templates
├── credentials/         # API credentials
├── models/             # AI model files
├── config.py           # Configuration
├── requirements.txt    # Python dependencies
└── run.py             # Application entry point
```

### Running Tests
```bash
# Set up test environment
export FLASK_ENV=testing
python -m pytest tests/
```

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## 🎯 Roadmap

- [ ] Complete Google Calendar integration
- [ ] Complete Outlook Calendar integration
- [ ] Implement AI model training interface
- [ ] Add payment processing integration
- [ ] Mobile app development
- [ ] Advanced analytics dashboard
- [ ] Multi-trainer/gym support
- [ ] Client mobile app for viewing programs

---

**Built for Personal Trainers, By Fitness Professionals**

MectoFitness CRM - Empowering fitness professionals to grow their business 💪
