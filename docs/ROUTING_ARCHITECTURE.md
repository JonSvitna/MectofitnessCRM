# Routing Architecture

## Overview

MectoFitness CRM supports **dual routing** to provide flexibility during the transition from traditional Flask templates to a modern React SPA.

## Routes

### Public Routes
- `/` - Landing page (redirects to `/dashboard` if authenticated)
- `/auth/login` - Login page
- `/auth/register` - Registration page
- `/about` - About page
- `/health` - Health check endpoint

### Protected Routes (Traditional Flask)
- `/dashboard` - Main dashboard (default for authenticated users)
- `/clients/*` - Client management pages
- `/sessions/*` - Session management pages
- `/programs/*` - Program management pages
- `/settings/*` - Settings pages
- And other traditional Flask routes...

### Protected Routes (React SPA - Optional)
- `/app` - React SPA entry point
- `/app/*` - All React SPA routes (handled client-side)

## Default Behavior

**Authenticated users are directed to `/dashboard` by default**, ensuring the traditional Flask interface is always available and functional.

## React SPA Usage

The React SPA at `/app` is **optional** and requires building:

```bash
# Install dependencies
npm install

# Build for production
npm run build

# Or build and watch for changes during development
npm run watch
```

### When React App is Not Built

If users navigate to `/app` without building the React app first, they will see a helpful message with:
- Instructions on how to build the React app
- A button to return to the traditional dashboard

This ensures users are never stuck and can always access the working backend functionality.

## Benefits of Dual Routing

1. **Backward Compatibility** - Traditional Flask routes continue to work
2. **Gradual Migration** - Can transition to React gradually
3. **Development Flexibility** - Developers can work on React without breaking production
4. **Resilience** - System remains functional even if React build fails
5. **User Choice** - Users can choose between traditional or modern interface

## Migration Path

As the React SPA matures:
1. **Phase 1 (Current)**: Traditional Flask is default, React is optional
2. **Phase 2**: React becomes default for new features, traditional remains for core functions
3. **Phase 3**: React becomes primary interface, traditional available as fallback
4. **Phase 4**: React-only (if desired), with traditional routes deprecated

## For Developers

### Adding New Features

- **Traditional route**: Add to appropriate blueprint in `app/routes/`
- **React route**: Add to `app/static/src/App.jsx` and create component
- **API endpoint**: Add to appropriate `api_*.py` file for React to consume

### Testing Routes

```bash
# Test traditional routes
# Start the Flask app and navigate to routes directly

# Test React routes
# Build React app first, then navigate to /app
npm run build
```

## API Endpoints

Both traditional and React interfaces share the same REST API endpoints under `/api/v1/`:
- `/api/v1/clients`
- `/api/v1/sessions`
- `/api/v1/programs`
- `/api/v1/exercises`
- And more...

These API endpoints ensure consistent backend functionality regardless of which frontend is used.
