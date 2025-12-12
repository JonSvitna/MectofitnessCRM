# Mectofitness Next.js Homepage

This directory contains a modern, TrueCoach-style SaaS homepage built with Next.js 14, TypeScript, Tailwind CSS, and Framer Motion.

## 🎨 Features

- **Modern Design**: Linear/Vercel-inspired design with dark backgrounds, orange accents, and glassy card effects
- **Fully Responsive**: Mobile-first design with sm/md/lg breakpoints
- **High Performance**: Optimized for speed and SEO
- **Premium SaaS Look**: Subtle grid backgrounds, blue glows, rounded corners, and soft shadows
- **Smooth Animations**: Framer Motion-powered section fade-ups and hover effects
- **Conversion-Focused**: Copywriting emphasizes Mectofitness as an accountability-first coaching system

## 📁 Structure

```
src/
├── app/
│   ├── layout.tsx          # Root layout with SEO metadata
│   ├── globals.css         # Tailwind + custom styles
│   └── page.tsx            # Homepage composing all sections
├── components/
│   ├── ui/
│   │   ├── Button.tsx      # Primary/secondary/ghost button variants
│   │   └── Card.tsx        # Glassy card component
│   └── sections/
│       ├── Navbar.tsx      # Sticky navbar with CTAs
│       ├── Hero.tsx        # Hero with headline, CTAs, dashboard preview
│       ├── SocialProof.tsx # Icon proof strip
│       ├── Features.tsx    # 6 feature cards
│       ├── Difference.tsx  # Why we're different comparison
│       ├── Pricing.tsx     # 3 pricing tiers
│       ├── FAQ.tsx         # FAQ accordion
│       ├── CTA.tsx         # Email capture form
│       └── Footer.tsx      # Footer with SEO keywords
└── lib/
    └── cn.ts               # className utility helper
```

## 🚀 Running the Homepage

### Important Note about Directory Structure

This repository has a Flask backend with an `app/` directory. Next.js App Router also uses an `app/` directory, which creates a conflict. When Next.js sees a root-level `app/` directory, it checks there first before looking in `src/app/`.

**To run the Next.js homepage:**

1. **Temporarily rename the Flask app directory:**
   ```bash
   mv app flask_app
   ```

2. **Start the Next.js dev server:**
   ```bash
   npm run nextjs:dev
   ```

3. **Visit http://localhost:3000**

4. **When done, restore the Flask app:**
   ```bash
   mv flask_app app
   ```

### Building for Production

```bash
# Rename Flask app
mv app flask_app

# Build Next.js
npm run nextjs:build

# Start production server
npm run nextjs:start

# Restore Flask app
mv flask_app app
```

## 🎯 SEO Keywords

The homepage naturally incorporates these SEO phrases:
- online coaching software
- personal trainer software
- fitness coaching platform
- client workout tracking
- coach messaging and check-ins
- training program delivery
- accountability coaching system

## 🎨 Design System

### Colors
- **Background**: Black (#000000)
- **Primary Accent**: Orange (#FF6B35 - #F97316)
- **Secondary Glow**: Blue (subtle, rgba-based)
- **Text**: White, Gray-300, Gray-400

### Components
- **Buttons**: 3 variants (primary, secondary, ghost)
- **Cards**: Glassy effect with backdrop-blur
- **Rounded Corners**: rounded-2xl (16px)
- **Shadows**: Soft, layered shadows with color tints

### Animations
- Fade-up on scroll (Framer Motion)
- Hover lift effects on cards
- Subtle glow pulse animations
- Smooth transitions (200-300ms)

## 📱 Responsive Breakpoints

- **sm**: 640px
- **md**: 768px
- **lg**: 1024px
- **xl**: 1280px
- **2xl**: 1536px

## 🔧 Tech Stack

- **Next.js 14**: App Router with TypeScript
- **React 18**: Latest features
- **Tailwind CSS**: Utility-first styling
- **Framer Motion**: Smooth animations
- **lucide-react**: Beautiful icons
- **clsx + tailwind-merge**: ClassName management

## 📦 Deployment

For deployment, consider these options:

### Option 1: Separate Deployment (Recommended)
Deploy the Next.js homepage separately from the Flask backend:
- Homepage: Vercel, Netlify, or Railway
- Backend: Railway, Heroku, or dedicated server

### Option 2: Integrated Deployment
1. Build Next.js to a static export: `next build && next export`
2. Serve the exported files from Flask
3. Update Flask routes to serve the Next.js static files

### Option 3: Subdomain/Path
- Homepage: https://mectofitness.com (Next.js)
- App: https://app.mectofitness.com (Flask)

## 🚧 Future Improvements

- Add form submission handling (currently shows alert)
- Connect to backend API for email capture
- Add more interactive demos
- Implement video testimonials
- Add more detailed feature pages
- A/B testing infrastructure

## 📝 License

Part of the Mectofitness CRM project.
