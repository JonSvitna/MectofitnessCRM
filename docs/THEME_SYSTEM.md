# Theme System Implementation

## Overview
This document describes the light/dark theme system implemented for MectoFitness CRM.

## Features

### 1. Light & Dark Themes
- **Light Theme**: Bright, clear interface with high contrast
- **Dark Theme**: Easy on the eyes with darker colors
- **Auto Mode**: Automatically matches system preference

### 2. User Preferences
- Theme preference is saved per user in the database
- Preference persists across sessions
- Can be changed via Settings → Branding

### 3. Theme Toggle Button
- Fixed position button in bottom-right corner
- Quick switch between light and dark modes
- Visual feedback on hover and click

## Files Modified/Created

### CSS Files
- `app/static/css/theme.css` - Complete theme system with CSS variables
  - Light mode variables
  - Dark mode variables
  - Form control theming
  - Card and table theming
  - Chatbot theming

### JavaScript Files
- `app/static/js/theme.js` - Theme management logic
  - Loads saved theme preference
  - Handles theme switching
  - Syncs with system preferences
  - Saves to server

### Python Files
- `app/models/settings.py` - Added `theme_preference` field
- `app/routes/settings.py` - Added theme update endpoint

### Templates
- `app/templates/base.html` - Includes theme CSS/JS and loads user preference
- `app/templates/auth/login.html` - Fixed white-on-white text issue
- `app/templates/settings/branding.html` - Added theme preference selector

### Database
- `migrations/add_theme_preference.sql` - Migration to add theme_preference column

## Usage

### For Users
1. Log in to your account
2. Go to Settings → Branding
3. Select your preferred theme:
   - **Light**: Bright interface
   - **Dark**: Dark interface
   - **Auto**: Follows system preference
4. Save changes

Alternatively, use the floating theme toggle button in the bottom-right corner for quick switching.

### For Developers

#### CSS Variables
All theme colors are defined as CSS variables in `:root` and `[data-theme="dark"]`:

```css
/* Light mode */
:root {
    --theme-bg-primary: #FFFFFF;
    --theme-text-primary: #1A1A2E;
    --theme-input-bg: #FFFFFF;
    /* ... */
}

/* Dark mode */
[data-theme="dark"] {
    --theme-bg-primary: #0F172A;
    --theme-text-primary: #F1F5F9;
    --theme-input-bg: #1E293B;
    /* ... */
}
```

#### Using Theme Variables
Always use theme variables for colors that should change with theme:

```css
/* Good */
.my-element {
    background: var(--theme-bg-primary);
    color: var(--theme-text-primary);
}

/* Avoid */
.my-element {
    background: #FFFFFF;
    color: #000000;
}
```

#### JavaScript API
```javascript
// Get current theme
const theme = window.themeManager.currentTheme;

// Switch theme
window.themeManager.toggleTheme();

// Apply specific theme
window.themeManager.applyTheme('dark');
```

## Theme Variables Reference

### Background Colors
- `--theme-bg-primary`: Primary background (pages, cards)
- `--theme-bg-secondary`: Secondary background (page background)
- `--theme-bg-tertiary`: Tertiary background (hover states)
- `--theme-bg-elevated`: Elevated surfaces (modals, dropdowns)

### Text Colors
- `--theme-text-primary`: Primary text
- `--theme-text-secondary`: Secondary text (labels, captions)
- `--theme-text-tertiary`: Tertiary text (placeholders, hints)
- `--theme-text-inverse`: Inverse text (on dark backgrounds)

### Input Colors
- `--theme-input-bg`: Input background
- `--theme-input-text`: Input text
- `--theme-input-border`: Input border
- `--theme-input-border-focus`: Input border when focused
- `--theme-input-placeholder`: Placeholder text

### Border Colors
- `--theme-border-light`: Light borders
- `--theme-border-medium`: Medium borders
- `--theme-border-strong`: Strong borders

### Brand Colors (Constant)
These remain the same across themes:
- `--brand-primary`: #FF6B35 (Orange)
- `--brand-secondary`: #004E89 (Blue)
- `--brand-accent`: #1AE5BE (Mint)
- `--brand-dark`: #1A1A2E (Black)
- `--brand-gold`: #FFD700 (Gold)

## Browser Support
- Modern browsers with CSS variables support
- Graceful degradation to light theme on older browsers
- System preference detection via `prefers-color-scheme`

## Performance
- Theme switching is instant with CSS variables
- No page reload required
- Smooth transitions for theme changes

## Accessibility
- High contrast maintained in both themes
- WCAG AA compliant color combinations
- Clear focus states
- Keyboard accessible theme toggle

## Troubleshooting

### Theme not persisting
- Check browser localStorage is enabled
- Verify user is logged in for server-side persistence
- Check database migration was run

### Flash of wrong theme
- Theme is applied in `<head>` before body renders
- Saved preference is loaded immediately

### Chatbot not visible
- Chatbot only shows for authenticated users
- Check `chatbot.js` is loaded in base.html
- Verify `/api/chatbot/` endpoint is accessible

## Future Enhancements
- Additional theme options (e.g., high contrast, colorblind modes)
- Custom color schemes
- Theme preview before applying
- Import/export theme settings
