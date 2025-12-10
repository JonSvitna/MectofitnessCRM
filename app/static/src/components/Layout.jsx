import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import {
  HomeIcon,
  UsersIcon,
  CalendarIcon,
  DocumentTextIcon,
  Cog6ToothIcon,
  ArrowRightOnRectangleIcon,
  Bars3Icon,
  XMarkIcon,
} from '@heroicons/react/24/outline';
import { useState, useEffect } from 'react';

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
  { name: 'Clients', href: '/clients', icon: UsersIcon },
  { name: 'Sessions', href: '/sessions', icon: CalendarIcon },
  { name: 'Programs', href: '/programs', icon: DocumentTextIcon },
  { name: 'Settings', href: '/settings', icon: Cog6ToothIcon },
];

export default function Layout() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, organization, logout } = useAuthStore();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Prevent body scroll when mobile menu is open
  useEffect(() => {
    if (mobileMenuOpen) {
      document.body.classList.add('overflow-hidden');
      document.body.style.touchAction = 'none';
    } else {
      document.body.classList.remove('overflow-hidden');
      document.body.style.touchAction = 'auto';
    }

    // Cleanup on unmount
    return () => {
      document.body.classList.remove('overflow-hidden');
      document.body.style.touchAction = 'auto';
    };
  }, [mobileMenuOpen]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar for desktop */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-64 lg:flex-col">
        <div className="flex min-h-0 flex-1 flex-col bg-gradient-to-b from-orange-600 to-orange-700">
          <div className="flex flex-1 flex-col overflow-y-auto pt-5 pb-4">
            {/* Logo */}
            <div className="flex flex-shrink-0 items-center px-4">
              <h1 className="text-2xl font-bold text-white">MectoFitness</h1>
            </div>

            {/* Navigation */}
            <nav className="mt-8 flex-1 space-y-1 px-3">
              {navigation.map((item) => {
                const isActive = location.pathname.startsWith(item.href);
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`
                      group flex items-center px-3 py-3 text-sm font-medium rounded-lg transition-colors
                      min-h-[44px] tap-highlight-none
                      ${
                        isActive
                          ? 'bg-orange-800 text-white'
                          : 'text-orange-100 hover:bg-orange-800/50 hover:text-white'
                      }
                    `}
                  >
                    <item.icon className="mr-3 h-6 w-6 flex-shrink-0" aria-hidden="true" />
                    {item.name}
                  </Link>
                );
              })}
            </nav>
          </div>

          {/* User section */}
          <div className="flex flex-shrink-0 border-t border-orange-800 p-4">
            <div className="w-full">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="h-10 w-10 rounded-full bg-orange-800 flex items-center justify-center text-white font-semibold">
                    {user?.name?.charAt(0) || 'U'}
                  </div>
                </div>
                <div className="ml-3 flex-1">
                  <p className="text-sm font-medium text-white">{user?.name}</p>
                  <p className="text-xs text-orange-200 capitalize">{user?.role}</p>
                </div>
                <button
                  onClick={handleLogout}
                  className="ml-auto flex-shrink-0 text-orange-200 hover:text-white transition-colors p-2 -mr-2 min-h-[44px] min-w-[44px] flex items-center justify-center tap-highlight-none"
                  title="Logout"
                  aria-label="Logout"
                >
                  <ArrowRightOnRectangleIcon className="h-6 w-6" />
                </button>
              </div>
              {organization && (
                <div className="mt-2 px-2 py-1 bg-orange-800/30 rounded text-xs text-orange-100">
                  {organization.name}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      <div className="lg:hidden safe-area-inset-top">
        <div className="flex items-center justify-between bg-orange-600 px-4 py-3 sm:px-6">
          <h1 className="text-xl font-bold text-white xs:text-2xl">MectoFitness</h1>
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="text-white hover:text-orange-100 p-2 -mr-2 min-h-[44px] min-w-[44px] flex items-center justify-center tap-highlight-none"
            aria-label={mobileMenuOpen ? "Close menu" : "Open menu"}
            aria-expanded={mobileMenuOpen}
          >
            {mobileMenuOpen ? (
              <XMarkIcon className="h-7 w-7" />
            ) : (
              <Bars3Icon className="h-7 w-7" />
            )}
          </button>
        </div>

        {/* Mobile menu panel */}
        {mobileMenuOpen && (
          <div
            className="fixed inset-0 z-40 bg-gray-900 bg-opacity-75 lg:hidden"
            onClick={() => setMobileMenuOpen(false)}
          >
            <div
              className="fixed inset-y-0 left-0 flex w-full max-w-xs xs:max-w-sm flex-col bg-gradient-to-b from-orange-600 to-orange-700 safe-area-inset-top safe-area-inset-bottom"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex flex-1 flex-col overflow-y-auto smooth-scroll pt-5 pb-4">
                <div className="flex items-center justify-between px-4">
                  <h1 className="text-2xl font-bold text-white">MectoFitness</h1>
                  <button
                    onClick={() => setMobileMenuOpen(false)}
                    className="text-white hover:text-orange-100 p-2 -mr-2 min-h-[44px] min-w-[44px] flex items-center justify-center tap-highlight-none"
                    aria-label="Close menu"
                  >
                    <XMarkIcon className="h-7 w-7" />
                  </button>
                </div>

                <nav className="mt-8 flex-1 space-y-2 px-3">
                  {navigation.map((item) => {
                    const isActive = location.pathname.startsWith(item.href);
                    return (
                      <Link
                        key={item.name}
                        to={item.href}
                        onClick={() => setMobileMenuOpen(false)}
                        className={`
                          group flex items-center px-4 py-3.5 text-base font-medium rounded-lg transition-colors
                          min-h-[48px] tap-highlight-none
                          ${
                            isActive
                              ? 'bg-orange-800 text-white'
                              : 'text-orange-100 hover:bg-orange-800/50 hover:text-white active:bg-orange-800/70'
                          }
                        `}
                      >
                        <item.icon className="mr-4 h-6 w-6 flex-shrink-0" />
                        {item.name}
                      </Link>
                    );
                  })}
                </nav>
              </div>

              <div className="flex flex-shrink-0 border-t border-orange-800 p-4">
                <div className="w-full">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <div className="h-12 w-12 rounded-full bg-orange-800 flex items-center justify-center text-white font-semibold text-lg">
                        {user?.name?.charAt(0) || 'U'}
                      </div>
                    </div>
                    <div className="ml-3 flex-1">
                      <p className="text-base font-medium text-white">{user?.name}</p>
                      <p className="text-sm text-orange-200 capitalize">{user?.role}</p>
                    </div>
                    <button
                      onClick={handleLogout}
                      className="ml-auto flex-shrink-0 text-orange-200 hover:text-white transition-colors p-2 -mr-2 min-h-[44px] min-w-[44px] flex items-center justify-center tap-highlight-none"
                      aria-label="Logout"
                      title="Logout"
                    >
                      <ArrowRightOnRectangleIcon className="h-6 w-6" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Main content */}
      <div className="lg:pl-64 flex flex-col flex-1">
        <main className="flex-1">
          <div className="py-4 px-4 xs:py-6 sm:px-6 lg:px-8 safe-area-inset-bottom">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
