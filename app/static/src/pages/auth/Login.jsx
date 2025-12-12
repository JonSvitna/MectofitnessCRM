import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import { useThemeStore } from '../../store/themeStore';
import { SunIcon, MoonIcon } from '@heroicons/react/24/outline';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { setAuth } = useAuthStore();
  const { theme, toggleTheme } = useThemeStore();

  // Initialize theme on mount
  useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [theme]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // For now, simulate login - replace with actual API call
      const mockUser = {
        id: 1,
        name: 'Sean Murrill',
        email: email,
        role: 'owner',
      };
      const mockOrg = {
        id: 1,
        name: 'SEAN MURRILL Fitness',
        subscription_tier: 'professional',
      };

      setAuth(mockUser, mockOrg);
      navigate('/dashboard');
    } catch (err) {
      setError('Invalid email or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 dark:from-black dark:to-gray-900 px-4 sm:px-6 lg:px-8 relative">
      {/* Grid background for dark mode */}
      <div className="absolute inset-0 dark:block hidden">
        <div className="absolute inset-0" style={{
          backgroundImage: 'linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px), linear-gradient(to bottom, rgba(255, 255, 255, 0.03) 1px, transparent 1px)',
          backgroundSize: '64px 64px'
        }} />
        {/* Glow effects */}
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-orange-500/10 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl" />
      </div>

      {/* Theme Toggle Button */}
      <button
        onClick={toggleTheme}
        className="absolute top-4 right-4 p-3 rounded-lg bg-white dark:bg-white/5 border border-gray-200 dark:border-white/10 hover:bg-gray-50 dark:hover:bg-white/10 transition-colors backdrop-blur-sm z-10"
        aria-label="Toggle theme"
      >
        {theme === 'dark' ? (
          <SunIcon className="h-5 w-5 text-gray-700 dark:text-gray-300" />
        ) : (
          <MoonIcon className="h-5 w-5 text-gray-700 dark:text-gray-300" />
        )}
      </button>

      <div className="max-w-md w-full space-y-8 relative z-10">
        <div className="text-center">
          <h2 className="text-5xl font-bold bg-gradient-to-r from-primary-600 to-teal-500 dark:from-orange-500 dark:to-orange-600 bg-clip-text text-transparent mb-3">
            MectoFitness
          </h2>
          <p className="text-lg text-gray-700 dark:text-gray-200 font-medium">
            Welcome back
          </p>
          <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
            Sign in to access your training dashboard
          </p>
        </div>
        <div className="bg-white dark:bg-white/5 rounded-2xl shadow-xl border border-gray-200 dark:border-white/10 p-8 sm:p-10 backdrop-blur-sm">
          <form className="space-y-5" onSubmit={handleSubmit}>
            {error && (
              <div className="rounded-lg bg-danger-50 dark:bg-danger-900/30 border border-danger-200 dark:border-danger-500/50 p-4">
                <p className="text-sm text-danger-700 dark:text-danger-400 font-medium">{error}</p>
              </div>
            )}

            <div>
              <label htmlFor="email" className="block text-sm font-semibold text-gray-700 dark:text-gray-200 mb-2">
                Email address
              </label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="block w-full px-4 py-3 border border-gray-300 dark:border-white/10 rounded-lg shadow-sm placeholder-gray-600 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 dark:focus:ring-orange-500 focus:border-primary-500 dark:focus:border-orange-500 transition-colors text-base min-h-[44px] bg-white dark:bg-white/5 text-gray-900 dark:text-white"
                placeholder="you@example.com"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-semibold text-gray-700 dark:text-gray-200 mb-2">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="block w-full px-4 py-3 border border-gray-300 dark:border-white/10 rounded-lg shadow-sm placeholder-gray-600 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 dark:focus:ring-orange-500 focus:border-primary-500 dark:focus:border-orange-500 transition-colors text-base min-h-[44px] bg-white dark:bg-white/5 text-gray-900 dark:text-white"
                placeholder="••••••••"
              />
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <input
                  id="remember-me"
                  name="remember-me"
                  type="checkbox"
                  className="h-4 w-4 text-primary-600 dark:text-orange-500 focus:ring-primary-500 dark:focus:ring-orange-500 border-gray-300 dark:border-white/10 rounded bg-white dark:bg-white/5"
                />
                <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-700 dark:text-gray-300 font-medium">
                  Remember me
                </label>
              </div>

              <div className="text-sm">
                <a href="#" className="font-medium text-primary-600 dark:text-orange-500 hover:text-primary-700 dark:hover:text-orange-400 transition-colors">
                  Forgot password?
                </a>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full flex justify-center py-3.5 px-4 border border-transparent rounded-lg shadow-sm text-base font-semibold text-white bg-gradient-to-r from-primary-600 to-primary-500 dark:from-orange-500 dark:to-orange-600 hover:from-primary-700 hover:to-primary-600 dark:hover:from-orange-600 dark:hover:to-orange-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 dark:focus:ring-orange-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 min-h-[48px]"
            >
              {loading ? 'Signing in...' : 'Sign in'}
            </button>
          </form>

          <div className="mt-6 pt-6 border-t border-gray-200 dark:border-white/10">
            <p className="text-center text-sm text-gray-700 dark:text-gray-300">
              Don't have an account?{' '}
              <Link to="/register" className="font-semibold text-primary-600 dark:text-orange-500 hover:text-primary-700 dark:hover:text-orange-400 transition-colors">
                Create account
              </Link>
            </p>
          </div>
        </div>

        <p className="text-center text-xs text-gray-600 dark:text-gray-400">
          © 2025 MectoFitness. All rights reserved.
        </p>
      </div>
    </div>
  );
}
