# Frontend Setup Guide

Setup guide for the optional modern React interface with Vite and Tailwind CSS.

## Overview

MectoFitness CRM includes two frontend interfaces:

1. **Traditional Flask Templates** (Default)
   - Server-side rendered
   - Works immediately after installation
   - No build step required
   - Fully functional

2. **Modern React Interface** (Optional)
   - Client-side rendered with React
   - Built with Vite
   - Styled with Tailwind CSS
   - Enhanced UX/UI
   - Requires Node.js and build step

## Do You Need the React Frontend?

**Use Traditional Flask Interface if:**
- You want to get started quickly
- You prefer server-side rendering
- You don't want to manage Node.js dependencies
- You're deploying to a simple hosting environment

**Use React Interface if:**
- You want a modern, app-like experience
- You prefer component-based architecture
- You want to customize the UI extensively
- You're comfortable with Node.js tooling

## Prerequisites

To use the React frontend, you need:
- Node.js 16 or higher
- npm (comes with Node.js)

**Install Node.js:**

**macOS:**
```bash
brew install node
```

**Ubuntu/Debian:**
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**Windows:**
Download from [nodejs.org](https://nodejs.org/)

## Installation

### 1. Install Dependencies

```bash
# Install Node.js dependencies
npm install
```

This installs:
- `vite` - Lightning-fast build tool
- `react` - React library
- `react-dom` - React DOM renderer
- `tailwindcss` - Utility-first CSS framework
- `postcss` - CSS processor
- `autoprefixer` - CSS vendor prefixing
- `@tailwindcss/forms` - Form styling plugin
- `@tailwindcss/typography` - Typography plugin

### 2. Build for Production

```bash
npm run build
```

This creates optimized production assets in `app/static/dist/`.

### 3. Start the Application

```bash
# Start Flask (serves React build)
python run.py
```

Access React interface at: http://localhost:5000/app

## Development Workflow

### Development with Hot Module Replacement (HMR)

For active development with instant updates:

**Terminal 1 - Flask Backend:**
```bash
python run.py
```

**Terminal 2 - Vite Dev Server:**
```bash
npm run dev
```

- Flask runs on: http://localhost:5000
- Vite dev server on: http://localhost:5173
- Changes to React components update instantly

### Watch Mode (Alternative)

Auto-rebuild on file changes without dev server:

```bash
npm run watch
```

Good for when you don't need HMR but want automatic rebuilds.

## Technology Stack

### Vite

**Benefits:**
- ⚡ Lightning-fast HMR (Hot Module Replacement)
- 🚀 Optimized production builds
- 📦 Modern ES modules support
- 🔧 Simple configuration
- 💪 Better developer experience

### Tailwind CSS

**Benefits:**
- 🎨 Utility-first CSS approach
- 📱 Mobile-first responsive design
- 🎭 Consistent design system
- ⚡ Smaller bundle sizes (PurgeCSS built-in)
- 🔌 Rich plugin ecosystem
- 💅 Custom theming with design tokens

## Project Structure

```
MectofitnessCRM/
├── app/
│   └── static/
│       ├── src/                    # Source files (development)
│       │   ├── main.js            # JavaScript entry point
│       │   ├── App.jsx            # Main React component
│       │   ├── pages/             # Page components
│       │   ├── components/        # Reusable components
│       │   └── styles/
│       │       └── main.css       # Tailwind CSS entry
│       └── dist/                   # Built assets (production)
│           ├── assets/
│           │   ├── main-[hash].js
│           │   └── main-[hash].css
│           └── manifest.json
├── tailwind.config.js              # Tailwind configuration
├── postcss.config.js               # PostCSS configuration
├── vite.config.js                  # Vite configuration
└── package.json                    # Node dependencies
```

## Configuration Files

### vite.config.js

Key configuration:
- Entry point: `app/static/src/main.js`
- Output directory: `app/static/dist/`
- Generates manifest for Flask integration
- HMR configured for local development

### tailwind.config.js

Custom design system:
- Professional blue/teal color palette
- Energetic yellow/orange accents
- Custom shadows and border radius
- Extended spacing scale
- Custom animations

**Custom Colors:**
```javascript
colors: {
  primary: {
    400: '#367588',  // Teal blue
    500: '#2E6577',
    600: '#1E566C',
  },
  accent: {
    400: '#FFC107',  // Yellow
    500: '#FFB84D',
    600: '#FF9500',  // Orange
  },
}
```

## Using Tailwind CSS

### Utility Classes

```html
<div class="bg-white p-8 rounded-lg shadow-lg hover:shadow-xl">
  <h3 class="text-xl font-semibold text-primary-600 mb-3">
    Client Management
  </h3>
  <p class="text-gray-600 leading-relaxed">
    Track client profiles and progress.
  </p>
</div>
```

### Custom Component Classes

Defined in `app/static/src/styles/main.css`:

**Buttons:**
- `.btn` - Base button
- `.btn-primary` - Primary action (teal)
- `.btn-secondary` - Secondary action (yellow)
- `.btn-large` - Large button
- `.btn-outline` - Outlined button

**Cards:**
- `.feature-card` - Feature showcase card
- `.stat-card` - Dashboard stat card
- `.client-card` - Client profile card

### Responsive Design

Tailwind mobile-first breakpoints:
- `sm:` - 640px and up
- `md:` - 768px and up
- `lg:` - 1024px and up
- `xl:` - 1280px and up
- `2xl:` - 1536px and up

**Example:**
```html
<div class="text-2xl md:text-4xl lg:text-6xl">
  Responsive Heading
</div>
```

## React Components

### Creating New Components

```jsx
// app/static/src/components/ClientCard.jsx
import React from 'react';

export default function ClientCard({ client }) {
  return (
    <div className="client-card">
      <h3 className="text-lg font-semibold">{client.name}</h3>
      <p className="text-gray-600">{client.email}</p>
    </div>
  );
}
```

### Using in Pages

```jsx
// app/static/src/pages/Clients.jsx
import ClientCard from '../components/ClientCard';

export default function Clients() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {clients.map(client => (
        <ClientCard key={client.id} client={client} />
      ))}
    </div>
  );
}
```

## Performance Optimization

### Tailwind PurgeCSS
- Automatically removes unused CSS
- Production builds are highly optimized
- Only ships CSS actually used in components

### Vite Optimizations
- Code splitting
- Tree shaking
- Asset compression
- Cache busting with hashes

## Deployment

### Build for Production

Always build before deploying:

```bash
npm run build
```

### Deployment Platforms

**Render:**
```yaml
# render.yaml
services:
  - type: web
    buildCommand: npm install && npm run build && pip install -r requirements.txt
    startCommand: gunicorn run:app
```

**Vercel:**
```json
{
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "app/static/dist"
      }
    }
  ]
}
```

See [Deployment Guide](../02-deployment/overview.md) for complete deployment instructions.

## Troubleshooting

### Issue: Styles not updating

**Solution:** Clear cache and rebuild:
```bash
rm -rf app/static/dist node_modules .vite
npm install
npm run build
```

### Issue: Module not found

**Solution:** Check import paths are correct:
```javascript
// Use relative paths from the file
import Component from './Component';
import { utils } from '../utils';
```

### Issue: HMR not working

**Solution:** 
1. Check Vite dev server is running: `npm run dev`
2. Verify port 5173 is not blocked
3. Check browser console for connection errors

### Issue: "Cannot find module 'vite'"

**Solution:** Install dependencies:
```bash
npm install
```

### Issue: Build fails with memory error

**Solution:** Increase Node.js memory:
```bash
NODE_OPTIONS=--max-old-space-size=4096 npm run build
```

## Scripts Reference

Available npm scripts:

- `npm run dev` - Start Vite dev server with HMR
- `npm run build` - Build for production
- `npm run watch` - Watch mode for automatic rebuilds
- `npm run preview` - Preview production build locally

## Accessing the React Interface

After building:

1. Start Flask: `python run.py`
2. Login at: http://localhost:5000/auth/login
3. Access React UI: http://localhost:5000/app

**Note:** The React interface requires authentication. You must login first.

## Traditional Flask Interface

The traditional interface remains fully functional:

- **Homepage**: http://localhost:5000/
- **Dashboard**: http://localhost:5000/dashboard
- **Clients**: http://localhost:5000/clients
- **Sessions**: http://localhost:5000/sessions
- **Programs**: http://localhost:5000/programs

See [Routing Architecture](../05-architecture/routing.md) for details on dual routing.

## Resources

- [Vite Documentation](https://vitejs.dev/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [Tailwind UI Components](https://tailwindui.com/)

## Next Steps

1. ✅ Install Node.js dependencies: `npm install`
2. ✅ Build React assets: `npm run build`
3. ✅ Start Flask: `python run.py`
4. ✅ Access React interface: http://localhost:5000/app
5. ✅ Start developing with `npm run dev` for HMR

For customization, see [Theme & UI documentation](../06-ui-theme/theme-system.md).

---

**React frontend configured!** Enjoy the modern interface. 💪
