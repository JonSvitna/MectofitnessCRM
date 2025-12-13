/**
 * Theme Manager for MectoFitness CRM
 * Handles light/dark theme switching and persistence
 */

class ThemeManager {
    constructor() {
        this.currentTheme = this.getStoredTheme() || 'dark';
        this.init();
    }

    init() {
        // Apply stored theme immediately
        this.applyTheme(this.currentTheme, false);

        // Setup theme toggle button (either existing or create new)
        this.setupToggleButton();

        // Listen for system theme changes
        this.watchSystemTheme();
    }

    getStoredTheme() {
        // Check localStorage first
        const stored = localStorage.getItem('mecto-theme');
        if (stored) {
            return stored;
        }

        // Check if user has system preference
        if (window.matchMedia) {
            if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
                return 'dark';
            } else if (window.matchMedia('(prefers-color-scheme: light)').matches) {
                return 'light';
            }
        }

        // Default to dark theme
        return 'dark';
    }

    applyTheme(theme, animate = true) {
        const html = document.documentElement;
        
        // Add transition class if animating
        if (animate) {
            html.style.transition = 'background-color 0.3s ease, color 0.3s ease';
        }
        
        // Set theme attribute
        html.setAttribute('data-theme', theme);
        
        // Update toggle button icon
        this.updateToggleIcon(theme);
        
        // Store preference
        localStorage.setItem('mecto-theme', theme);
        this.currentTheme = theme;
        
        // Save to server if user is logged in
        this.saveThemeToServer(theme);
        
        // Remove transition after animation
        if (animate) {
            setTimeout(() => {
                html.style.transition = '';
            }, 300);
        }
    }

    toggleTheme() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.applyTheme(newTheme, true);
    }

    setupToggleButton() {
        // Check if there's an existing theme toggle button in the navbar
        const existingButton = document.getElementById('themeToggle');

        if (existingButton) {
            // Use the existing navbar button
            this.toggleButton = existingButton;
            existingButton.onclick = () => this.toggleTheme();
        } else {
            // Create a floating toggle button (fallback for pages without navbar)
            const button = document.createElement('button');
            button.className = 'theme-toggle';
            button.setAttribute('aria-label', 'Toggle theme');
            button.setAttribute('title', 'Toggle light/dark theme');
            button.onclick = () => this.toggleTheme();

            document.body.appendChild(button);
            this.toggleButton = button;
        }

        this.updateToggleIcon(this.currentTheme);
    }

    updateToggleIcon(theme) {
        if (!this.toggleButton) return;

        // Check if this is the navbar button (has child spans) or floating button
        const lightIcon = this.toggleButton.querySelector('.theme-icon-light');
        const darkIcon = this.toggleButton.querySelector('.theme-icon-dark');

        if (lightIcon && darkIcon) {
            // Navbar button - icons are controlled by CSS based on data-theme attribute
            // No need to update anything here as CSS handles it
            if (theme === 'dark') {
                this.toggleButton.setAttribute('title', 'Switch to light mode');
            } else {
                this.toggleButton.setAttribute('title', 'Switch to dark mode');
            }
        } else {
            // Floating button - update innerHTML directly
            if (theme === 'dark') {
                this.toggleButton.innerHTML = '☀️'; // Sun for light mode
                this.toggleButton.setAttribute('title', 'Switch to light mode');
            } else {
                this.toggleButton.innerHTML = '🌙'; // Moon for dark mode
                this.toggleButton.setAttribute('title', 'Switch to dark mode');
            }
        }
    }

    watchSystemTheme() {
        if (!window.matchMedia) return;
        
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        
        mediaQuery.addEventListener('change', (e) => {
            // Only auto-switch if user hasn't manually set a preference
            const hasManualPreference = localStorage.getItem('mecto-theme') !== null;
            if (!hasManualPreference) {
                const newTheme = e.matches ? 'dark' : 'light';
                this.applyTheme(newTheme, true);
            }
        });
    }

    async saveThemeToServer(theme) {
        try {
            const response = await fetch('/settings/update-theme', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ theme: theme })
            });
            
            if (!response.ok) {
                console.log('Could not save theme preference to server (user may not be logged in)');
            }
        } catch (error) {
            // Silent fail - user might not be logged in
            console.log('Theme preference saved locally only');
        }
    }
}

// Initialize theme manager when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.themeManager = new ThemeManager();
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ThemeManager;
}
