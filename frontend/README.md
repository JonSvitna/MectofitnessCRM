# MectoFitness Frontend

Static landing page for MectoFitness CRM built with Vite, Tailwind CSS, and vanilla JavaScript.

## Features

- **Modern Tech Stack**: Vite + Tailwind CSS + Vanilla JS
- **Responsive Design**: Mobile-first approach
- **Dark Orange Theme**: Matches main branch color scheme
- **User Data Capture**: Form for capturing leads
- **API Integration**: Connects to Flask backend

## Tech Stack

- **Build Tool**: Vite 5.0
- **Styling**: Tailwind CSS 3.4
- **HTTP Client**: Axios
- **Fonts**: Inter (Google Fonts)

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:5000/api
```

For production on Railway:
```env
VITE_API_URL=https://your-backend-url.railway.app/api
```

## Project Structure

```
frontend/
├── src/
│   ├── styles/
│   │   └── main.css          # Tailwind CSS and custom styles
│   └── main.js                # Main JavaScript file
├── index.html                 # Main HTML file
├── package.json               # Dependencies
├── vite.config.js             # Vite configuration
├── tailwind.config.js         # Tailwind configuration
└── postcss.config.js          # PostCSS configuration
```

## Color Scheme

The frontend uses a dark orange gradient theme:

- **Primary Orange**: `#F97316` (orange-500)
- **Dark Orange**: `#EA580C` (orange-600)
- **Background**: `#000000` (black)
- **Text**: White and gray shades

## Features

### Landing Page Sections

1. **Hero Section**: Eye-catching introduction with CTA
2. **Features Section**: 6 key features of the platform
3. **Benefits Section**: Why coaches choose MectoFitness
4. **Signup Form**: Captures user data (name, email, phone, business type, message)
5. **Footer**: Simple branding footer

### Form Handling

The signup form captures:
- Full Name (required)
- Email Address (required)
- Phone Number (optional)
- Business Type (required dropdown)
- Message (optional)

Data is sent to the backend API at `/api/leads` endpoint.

## Deployment on Railway

### Build Command
```bash
npm install && npm run build
```

### Start Command
```bash
npx serve -s dist -p $PORT
```

### Environment Variables
Set `VITE_API_URL` to your backend Railway URL.

## Development

```bash
# Run dev server
npm run dev

# The app will be available at http://localhost:3000
# It proxies /api requests to http://localhost:5000
```

## Production Build

```bash
# Build for production
npm run build

# Output will be in dist/ directory
# Serve with any static file server
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

Proprietary - MectoFitness CRM
