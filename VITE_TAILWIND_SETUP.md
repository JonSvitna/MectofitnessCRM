# Vite + Tailwind CSS Setup Guide

## Overview

MectoFitness CRM now uses **Vite** as the modern frontend build tool and **Tailwind CSS** as the utility-first CSS framework for enhanced UX/UI design.

### Why Vite + Tailwind?

**Vite Benefits:**
- ⚡ Lightning-fast HMR (Hot Module Replacement)
- 🚀 Optimized production builds
- 📦 Modern ES modules support
- 🔧 Simple configuration
- 💪 Better developer experience

**Tailwind CSS Benefits:**
- 🎨 Utility-first CSS approach
- 📱 Mobile-first responsive design
- 🎭 Consistent design system
- ⚡ Smaller bundle sizes (PurgeCSS built-in)
- 🔌 Rich plugin ecosystem
- 💅 Custom theming with design tokens

## Installation

### 1. Install Node.js Dependencies

```bash
npm install
```

This installs:
- `vite` - Build tool
- `tailwindcss` - CSS framework
- `postcss` - CSS processor
- `autoprefixer` - CSS vendor prefixing
- `@tailwindcss/forms` - Form styling plugin
- `@tailwindcss/typography` - Typography plugin

### 2. Development Mode

Run Vite development server with hot reload:

```bash
npm run dev
```

This starts Vite on `http://localhost:5173` with HMR enabled.

### 3. Production Build

Build optimized assets for production:

```bash
npm run build
```

Output goes to `app/static/dist/` directory.

### 4. Watch Mode (Optional)

Auto-rebuild on file changes without dev server:

```bash
npm run watch
```

## Project Structure

```
MectofitnessCRM/
├── app/
│   └── static/
│       ├── src/                    # Source files (Vite entry)
│       │   ├── main.js            # JavaScript entry point
│       │   └── styles/
│       │       └── main.css       # Tailwind CSS entry point
│       └── dist/                   # Built assets (generated)
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

### tailwind.config.js

Custom color palette inspired by TrueCoach and Trainerize:

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

**Custom Design Tokens:**
- Professional blue/teal palette
- Energetic yellow/orange accents
- Custom shadows and border radius
- Extended spacing scale
- Custom animations

### vite.config.js

- Entry point: `app/static/src/main.js`
- Output: `app/static/dist/`
- Generates manifest for Flask integration
- HMR configured for local development

## Using Tailwind Classes

### Example Component

```html
<div class="bg-white p-8 rounded-card shadow-card hover:shadow-card-hover">
  <h3 class="text-xl font-display font-semibold text-primary-600 mb-3">
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

**Sections:**
- `.hero-section` - Hero banner with gradient
- `.features-section` - Feature grid section
- `.cta-section` - Call-to-action section

**Forms:**
- `.form-input` - Styled form input
- `.form-label` - Form label
- `.form-group` - Form group container

## Flask Integration

### Development (with HMR)

1. Start Flask server:
```bash
python run.py
```

2. Start Vite dev server in another terminal:
```bash
npm run dev
```

Flask serves on `http://localhost:5000`, Vite on `http://localhost:5173` with HMR.

### Production

1. Build assets:
```bash
npm run build
```

2. Run Flask:
```bash
python run.py
```

Flask serves pre-built assets from `app/static/dist/`.

### Template Integration

Update `base.html` to use Vite assets:

**Development:**
```html
<script type="module" src="http://localhost:5173/@vite/client"></script>
<script type="module" src="http://localhost:5173/src/main.js"></script>
```

**Production:**
```html
<link rel="stylesheet" href="{{ url_for('static', filename='dist/assets/main.css') }}">
<script type="module" src="{{ url_for('static', filename='dist/assets/main.js') }}"></script>
```

## Responsive Design

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

## Custom Animations

Defined in Tailwind config:

- `animate-fade-in` - Fade in element
- `animate-slide-up` - Slide up element
- `animate-bounce-in` - Bounce in element

**Usage:**
```html
<div class="animate-fade-in">
  Animated content
</div>
```

## JavaScript Enhancements

`app/static/src/main.js` provides:

- Mobile menu toggle
- Smooth scroll for anchor links
- Scroll-triggered animations
- Alert auto-dismiss (5 seconds)
- Form validation enhancements
- Button loading states
- Dashboard stat counter animations

## Performance Optimization

**Tailwind PurgeCSS:**
- Automatically removes unused CSS
- Production builds are highly optimized
- Only ships CSS actually used in templates

**Vite Optimizations:**
- Code splitting
- Tree shaking
- Asset compression
- Cache busting with hashes

## Deployment

### Vercel

Add build command to `vercel.json`:

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

### Render

Add build command to `render.yaml`:

```yaml
services:
  - type: web
    buildCommand: npm install && npm run build && pip install -r requirements.txt
    startCommand: gunicorn run:app
```

## Troubleshooting

### Issue: Styles not updating

**Solution:** Clear cache and rebuild:
```bash
rm -rf app/static/dist node_modules .vite
npm install
npm run build
```

### Issue: Module not found

**Solution:** Ensure all paths in `vite.config.js` are absolute:
```javascript
import { resolve } from 'path';
// Use resolve(__dirname, 'path/to/file')
```

### Issue: HMR not working

**Solution:** Check Vite dev server is running and ports are correct.

## Resources

- [Vite Documentation](https://vitejs.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [Tailwind UI Components](https://tailwindui.com/)
- [Headless UI](https://headlessui.com/)

## Next Steps

1. ✅ Install dependencies: `npm install`
2. ✅ Build assets: `npm run build`
3. ✅ Update templates to use Tailwind classes
4. ✅ Start development: `npm run dev` + `python run.py`
5. ✅ Deploy to production

---

**Status**: ✅ Vite + Tailwind CSS fully configured and ready for development!
