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
   python scripts/verify_setup.py
   ```
   This checks your database connection and configuration.

6. **Initialize the database**
   ```bash
   python run.py
   ```
   This will automatically create the database tables.

7. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

> **Note**: For PostgreSQL setup, see [docs/setup/POSTGRESQL_SETUP.md](docs/setup/POSTGRESQL_SETUP.md). For troubleshooting, see [docs/QUICKSTART.md](docs/QUICKSTART.md).

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

See [docs/ROUTING_ARCHITECTURE.md](docs/ROUTING_ARCHITECTURE.md) for details on the dual routing system.

### Next.js Marketing Homepage

A modern, TrueCoach-style marketing homepage built with Next.js 14 is available in the `src/` directory. This provides a premium SaaS landing page with:

- Modern Linear/Vercel-inspired design
- Dark theme with orange accents
- Fully responsive (mobile-first)
- SEO-optimized
- Framer Motion animations

**To run the Next.js homepage:**

```bash
# Quick start with helper script
./run-nextjs-homepage.sh

# Or manually:
mv app flask_app          # Temporarily rename Flask app
npm run nextjs:dev        # Start Next.js dev server
# Visit http://localhost:3000
mv flask_app app          # Restore Flask app when done
```

See [docs/setup/NEXT_JS_HOMEPAGE_README.md](docs/setup/NEXT_JS_HOMEPAGE_README.md) for full documentation.

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

1. **Set up OpenAI API**: Add your `OPENAI_API_KEY` to the `.env` file
2. **Prepare Your Knowledge Base**: Add your training expertise and program templates
3. **Train the Model**: Use scikit-learn to train on your knowledge base
4. **Integrate**: The AI model will generate personalized programs based on client goals and fitness level

Example model training structure is included in the codebase.

## 💬 AI Chatbot Assistant

MectoFitness includes an AI-powered chatbot assistant that helps with:
- Workout program recommendations
- Exercise form tips
- Nutrition guidance
- Client management best practices
- Platform feature guidance

**Keyboard Shortcuts:**
- `Ctrl+/` (Windows/Linux) or `Cmd+/` (Mac): Toggle chatbot
- `Escape`: Close chatbot

The chatbot is integrated in both Flask and React interfaces and automatically adjusts its position based on your layout.

## 💳 Payment Processing with Stripe

Integrated Stripe payment processing for accepting client payments. Features include:
- One-time payments
- Recurring subscriptions
- Multiple payment methods (cards, digital wallets, bank transfers)
- Automated invoicing and receipts
- Webhook integration for real-time updates

See [docs/setup/STRIPE_SETUP.md](docs/setup/STRIPE_SETUP.md) for detailed setup instructions.

## 🎥 Video Conferencing with Zoom

Integrated Zoom video conferencing for virtual training sessions. Features include:
- Auto-scheduled meetings linked to training sessions
- Automatic cloud recording
- Secure waiting rooms
- Session recordings available after meetings
- Webhook integration for meeting status updates

See [docs/setup/ZOOM_SETUP.md](docs/setup/ZOOM_SETUP.md) for detailed setup instructions.

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
│   ├── static/          # CSS, JS, images, React app
│   └── templates/       # HTML templates
├── docs/                # Documentation
│   ├── setup/          # Setup guides
│   ├── deployment/     # Deployment documentation
│   └── archive/        # Historical documentation
├── scripts/            # Utility and test scripts
├── src/                # Next.js homepage source
├── credentials/        # API credentials
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

# Run specific test scripts
python scripts/test_api_endpoints.py
python scripts/test_db.py
```

## 📚 Documentation

Comprehensive documentation is available in the `/docs` directory:

### Getting Started
- **[docs/QUICKSTART.md](docs/QUICKSTART.md)** - Quick start guide
- **[docs/SETUP.md](docs/SETUP.md)** - Detailed setup instructions
- **[docs/setup/DATABASE_INITIALIZATION.md](docs/setup/DATABASE_INITIALIZATION.md)** - Database setup

### Features & Integration
- **[docs/API.md](docs/API.md)** - API documentation overview
- **[docs/FEATURES.md](docs/FEATURES.md)** - Complete feature list
- **[docs/setup/AI_CHATBOT_SETUP.md](docs/setup/AI_CHATBOT_SETUP.md)** - AI chatbot configuration
- **[docs/setup/STRIPE_SETUP.md](docs/setup/STRIPE_SETUP.md)** - Stripe payment integration
- **[docs/setup/ZOOM_SETUP.md](docs/setup/ZOOM_SETUP.md)** - Zoom integration

### Deployment
- **[docs/deployment/](docs/deployment/)** - Deployment guides for various platforms
- **[CLEANUP_RECOMMENDATIONS.md](CLEANUP_RECOMMENDATIONS.md)** - Code quality and maintenance recommendations

### Architecture
- **[docs/ROUTING_ARCHITECTURE.md](docs/ROUTING_ARCHITECTURE.md)** - Application routing
- **[docs/RBAC_GUIDE.md](docs/RBAC_GUIDE.md)** - Role-based access control
- **[docs/THEME_SYSTEM.md](docs/THEME_SYSTEM.md)** - Theme system documentation

See **[docs/README.md](docs/README.md)** for complete documentation index.

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## 🎯 Roadmap

See **[docs/ROADMAP.md](docs/ROADMAP.md)** for the complete product roadmap.

### Recent Improvements
- [x] Google Calendar integration framework
- [x] Outlook Calendar integration framework
- [x] AI model training interface
- [x] Stripe payment processing integration
- [x] Zoom video conferencing integration
- [x] AI chatbot assistant
- [x] Documentation organization and cleanup
- [x] Centralized logging utility

### Upcoming Features
- [ ] Mobile app development
- [ ] Advanced analytics dashboard
- [ ] Multi-trainer/gym support
- [ ] Client mobile app for viewing programs
- [ ] Apple Pay / Google Pay support
- [ ] Advanced reporting and insights

---

**Built for Personal Trainers, By Fitness Professionals**

MectoFitness CRM - Empowering fitness professionals to grow their business 💪
