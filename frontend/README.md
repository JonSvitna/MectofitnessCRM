# MectoFitness CRM - Frontend

Next.js-based static marketing website for MectoFitness CRM.

## Overview

This directory contains the frontend Next.js application for the MectoFitness CRM marketing website. This is a modern, SEO-optimized landing page separate from the backend dashboard.

## Structure

```
frontend/
├── src/                   # Next.js application
│   ├── app/              # App directory (Next.js 14)
│   │   ├── page.tsx     # Homepage
│   │   └── layout.tsx   # Root layout
│   ├── components/       # React components
│   ├── styles/           # CSS and styling
│   └── lib/              # Utility functions
├── public/               # Static assets
├── next.config.mjs       # Next.js configuration
├── package.json          # Node.js dependencies
├── tailwind.config.js    # Tailwind CSS configuration
├── postcss.config.js     # PostCSS configuration
└── tsconfig.json         # TypeScript configuration
```

## Features

- **Modern Design**: TrueCoach/Linear-inspired design system
- **Dark Theme**: Black background with orange accents
- **Fully Responsive**: Mobile-first design
- **SEO Optimized**: Next.js 14 with app directory
- **Animations**: Framer Motion for smooth transitions
- **TypeScript**: Full type safety
- **Fast Performance**: Optimized builds and code splitting

## Quick Start

### Prerequisites
- Node.js 18+ or 20+
- npm or yarn

### Installation

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Set up environment variables (if needed):**
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your configuration
   ```

### Development

**Start development server:**
```bash
npm run dev
```

The site will be available at `http://localhost:3000`

### Building for Production

**Build the site:**
```bash
npm run build
```

**Preview production build:**
```bash
npm run start
```

**Export static site:**
```bash
npm run export
```

## Deployment

The frontend can be deployed to:
- **Vercel** (recommended for Next.js)
- **Netlify**
- **CloudFlare Pages**
- Any static hosting service

### Vercel Deployment

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

Or connect your GitHub repository to Vercel for automatic deployments.

### Static Export

For static hosting without server-side features:

```bash
npm run build
npm run export
```

Output will be in the `out/` directory.

## Configuration

### Environment Variables

Create `.env.local` for local development:

```env
# Optional: Analytics
NEXT_PUBLIC_GA_ID=your-google-analytics-id

# Optional: Contact form endpoint
NEXT_PUBLIC_CONTACT_API=https://your-backend/api/contact
```

### Next.js Config

Edit `next.config.mjs` to customize:
- Image optimization
- Redirects and rewrites
- Headers
- Environment variables

### Tailwind Config

Edit `tailwind.config.js` to customize:
- Colors and theme
- Fonts
- Breakpoints
- Plugins

## Development Guidelines

### Component Structure

```tsx
// src/components/MyComponent.tsx
import React from 'react';

interface MyComponentProps {
  title: string;
  description?: string;
}

export default function MyComponent({ title, description }: MyComponentProps) {
  return (
    <div className="container mx-auto">
      <h2>{title}</h2>
      {description && <p>{description}</p>}
    </div>
  );
}
```

### Styling

Use Tailwind CSS utility classes:
```tsx
<div className="bg-black text-white p-8 rounded-lg shadow-lg">
  <h1 className="text-4xl font-bold text-orange-500">Title</h1>
</div>
```

### Dark Mode

The site uses dark mode by default with the color scheme:
- **Background**: Black (`#000000`)
- **Primary**: Orange (`#F97316`)
- **Text**: White with varying opacity
- **Accents**: Gray tones

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Icons**: Heroicons / Lucide React
- **Fonts**: Inter (from next/font)

## Scripts

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
npm run export       # Export static site
```

## Pages

### Homepage (`src/app/page.tsx`)
- Hero section with CTA
- Features showcase
- Pricing (if applicable)
- Testimonials
- Call-to-action sections

### Future Pages
- `/about` - About the company
- `/pricing` - Pricing plans
- `/contact` - Contact form
- `/blog` - Blog posts (if needed)

## SEO

The site includes:
- Meta tags for social sharing
- Open Graph tags
- Twitter Card tags
- Sitemap generation
- Robots.txt
- Schema.org markup

## Performance

- **Lighthouse Score**: 90+ on all metrics
- **Core Web Vitals**: Optimized
- **Image Optimization**: Next.js automatic image optimization
- **Code Splitting**: Automatic route-based splitting
- **Font Optimization**: next/font for optimal font loading

## Support

For issues and questions:
- Check `/docs/` directory in project root
- Review Next.js documentation: https://nextjs.org/docs
- Open an issue on GitHub

## Related

- **Backend**: See `/backend/README.md` for API documentation
- **Main Docs**: See `/docs/` for complete project documentation
