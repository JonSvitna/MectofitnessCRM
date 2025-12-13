import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { useThemeStore } from '../store/themeStore';
import { useState, useEffect, useRef } from 'react';
import {
  HomeIcon,
  UsersIcon,
  CalendarIcon,
  DocumentTextIcon,
  Cog6ToothIcon,
  ArrowRightOnRectangleIcon,
  Bars3Icon,
  XMarkIcon,
  ChatBubbleLeftRightIcon,
  UserGroupIcon,
  TrophyIcon,
  CreditCardIcon,
  BookOpenIcon,
  BellIcon,
  ChartBarIcon,
  ClockIcon,
  AcademicCapIcon,
  ChevronDownIcon,
  ChevronRightIcon,
  MagnifyingGlassIcon,
  SunIcon,
  MoonIcon,
  UserCircleIcon,
} from '@heroicons/react/24/outline';

// Navigation structure with categories
const navigationCategories = [
  {
    name: 'Workspace',
    items: [
      { name: 'Overview', href: '/dashboard', icon: HomeIcon },
      { name: 'Calendar', href: '/calendar', icon: CalendarIcon },
    ],
  },
  {
    name: 'Clients & Training',
    items: [
      { name: 'Clients', href: '/clients', icon: UsersIcon },
      { name: 'Sessions', href: '/sessions', icon: ClockIcon },
      { name: 'Programs', href: '/programs', icon: DocumentTextIcon },
      { name: 'Progress Tracking', href: '/progress', icon: ChartBarIcon },
    ],
  },
  {
    name: 'Engagement',
    items: [
      { name: 'Messages', href: '/messages', icon: ChatBubbleLeftRightIcon },
      { name: 'Groups', href: '/groups', icon: UserGroupIcon },
      { name: 'Challenges', href: '/challenges', icon: TrophyIcon },
      { name: 'Announcements', href: '/announcements', icon: BellIcon },
    ],
  },
  {
    name: 'Business',
    items: [
      { name: 'Payments', href: '/payments', icon: CreditCardIcon },
      { name: 'Team', href: '/team', icon: UserGroupIcon },
      { name: 'Scheduling', href: '/scheduling', icon: CalendarIcon },
    ],
  },
  {
    name: 'Resources',
    items: [
      { name: 'Master Libraries', href: '/master-libraries', icon: BookOpenIcon },
      { name: 'Exercise Library', href: '/exercise-library', icon: AcademicCapIcon },
    ],
  },
  {
    name: 'Account',
    items: [
      { name: 'Profile', href: '/account', icon: UserCircleIcon },
      { name: 'Settings', href: '/settings', icon: Cog6ToothIcon },
    ],
  },
];

export default function Layout() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, organization, logout } = useAuthStore();
  const { theme, toggleTheme } = useThemeStore();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [collapsedCategories, setCollapsedCategories] = useState({});
  const [searchQuery, setSearchQuery] = useState('');
  const [profileDropdownOpen, setProfileDropdownOpen] = useState(false);
  const profileDropdownRef = useRef(null);

  // Prevent body scroll when mobile menu is open
  useEffect(() => {
    if (mobileMenuOpen) {
      document.body.classList.add('overflow-hidden');
      document.body.style.touchAction = 'none';
    } else {
      document.body.classList.remove('overflow-hidden');
      document.body.style.touchAction = 'auto';
    }

    return () => {
      document.body.classList.remove('overflow-hidden');
      document.body.style.touchAction = 'auto';
    };
  }, [mobileMenuOpen]);

  // Close profile dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (profileDropdownRef.current && !profileDropdownRef.current.contains(event.target)) {
        setProfileDropdownOpen(false);
      }
    };

    if (profileDropdownOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [profileDropdownOpen]);

  const handleLogout = async () => {
    try {
      // Clear local auth state first
      logout();
      // Clear localStorage to ensure complete logout
      localStorage.removeItem('auth-storage');
      // Call Flask logout endpoint to clear server session
      // Use fetch with credentials to ensure cookies are sent
      await fetch('/logout', {
        method: 'GET',
        credentials: 'include'
      });
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Always redirect to login page, regardless of API call success
      window.location.href = '/login';
    }
  };

  const toggleCategory = (categoryName) => {
    setCollapsedCategories(prev => ({
      ...prev,
      [categoryName]: !prev[categoryName]
    }));
  };

  // Filter navigation items based on search
  const filteredCategories = searchQuery
    ? navigationCategories.map(category => ({
        ...category,
        items: category.items.filter(item =>
          item.name.toLowerCase().includes(searchQuery.toLowerCase())
        )
      })).filter(category => category.items.length > 0)
    : navigationCategories;

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-black">
      {/* Desktop Sidebar */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-64 lg:flex-col">
        <div className="flex min-h-0 flex-1 flex-col bg-white dark:bg-black border-r border-gray-200 dark:border-white/10 shadow-sidebar">
          <div className="flex flex-col pt-5 pb-4 h-full">
            {/* Logo and Theme Toggle */}
            <div className="flex flex-shrink-0 items-center justify-between px-5 mb-6">
              <h1 className="text-2xl font-bold bg-gradient-to-r from-primary-500 to-purple-500 dark:from-orange-500 dark:to-orange-600 bg-clip-text text-transparent">
                MectoFitness
              </h1>
              <button
                onClick={toggleTheme}
                className="p-2 rounded-lg text-gray-400 hover:text-gray-600 dark:text-gray-400 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-white/5 transition-colors"
                aria-label="Toggle theme"
                title={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
              >
                {theme === 'dark' ? (
                  <SunIcon className="h-5 w-5" />
                ) : (
                  <MoonIcon className="h-5 w-5" />
                )}
              </button>
            </div>

            {/* Search bar */}
            <div className="px-4 mb-4">
              <div className="relative">
                <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-9 pr-3 py-2 text-sm border border-gray-200 dark:border-white/10 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 dark:focus:ring-orange-500 focus:border-transparent transition-all bg-white dark:bg-white/5 text-gray-900 dark:text-white"
                />
              </div>
            </div>

            {/* Navigation */}
            <nav className="flex-1 space-y-6 px-3 overflow-y-auto">
              {filteredCategories.map((category) => (
                <div key={category.name}>
                  {/* Category Header */}
                  <button
                    onClick={() => toggleCategory(category.name)}
                    className="flex items-center justify-between w-full px-2 mb-2 text-xs font-semibold text-gray-500 dark:text-gray-400 tracking-wider hover:text-gray-700 dark:hover:text-gray-200 transition-colors"
                  >
                    <span>{category.name}</span>
                    {collapsedCategories[category.name] ? (
                      <ChevronRightIcon className="h-3 w-3" />
                    ) : (
                      <ChevronDownIcon className="h-3 w-3" />
                    )}
                  </button>

                  {/* Category Items */}
                  {!collapsedCategories[category.name] && (
                    <div className="space-y-1">
                      {category.items.map((item) => {
                        const isActive = location.pathname.startsWith(item.href);
                        return (
                          <Link
                            key={item.name}
                            to={item.href}
                            className={`
                              group flex items-center px-3 py-2.5 text-sm font-medium rounded-lg transition-all duration-150
                              ${
                                isActive
                                  ? 'bg-primary-50 dark:bg-orange-500/10 text-primary-700 dark:text-orange-400 shadow-sm'
                                  : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-white/5 hover:text-gray-900 dark:hover:text-white'
                              }
                            `}
                          >
                            <item.icon
                              className={`mr-3 h-5 w-5 flex-shrink-0 transition-colors ${
                                isActive ? 'text-primary-600 dark:text-orange-500' : 'text-gray-400 dark:text-gray-500 group-hover:text-gray-600 dark:group-hover:text-gray-300'
                              }`}
                              aria-hidden="true"
                            />
                            {item.name}
                          </Link>
                        );
                      })}
                    </div>
                  )}
                </div>
              ))}
            </nav>
          </div>

          {/* User section */}
          <div className="flex flex-shrink-0 border-t border-gray-200 dark:border-white/10 p-4 bg-gray-50 dark:bg-white/5">
            <div className="w-full">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="h-10 w-10 rounded-full bg-gradient-to-br from-primary-500 to-purple-500 dark:from-orange-500 dark:to-purple-500 flex items-center justify-center text-white font-semibold shadow-sm">
                    {user?.first_name?.charAt(0) || user?.name?.charAt(0) || 'U'}
                  </div>
                </div>
                <div className="ml-3 flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                    {user?.first_name || user?.name || 'User'}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400 truncate">{user?.email}</p>
                </div>
                <Link
                  to="/settings"
                  className="ml-2 flex-shrink-0 text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 transition-colors p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-white/5"
                  title="Settings"
                  aria-label="Settings"
                >
                  <Cog6ToothIcon className="h-5 w-5" />
                </Link>
                <button
                  onClick={handleLogout}
                  className="ml-2 flex-shrink-0 text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 transition-colors p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-white/5"
                  title="Logout"
                  aria-label="Logout"
                >
                  <ArrowRightOnRectangleIcon className="h-5 w-5" />
                </button>
              </div>
              {organization && (
                <div className="mt-2 px-2 py-1 bg-white dark:bg-white/5 border border-gray-200 dark:border-white/10 rounded text-xs text-gray-600 dark:text-gray-400 truncate">
                  {organization.name}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Mobile Header */}
      <div className="lg:hidden sticky top-0 z-40 bg-white dark:bg-black border-b border-gray-200 dark:border-white/10 shadow-sm">
        <div className="flex items-center justify-between px-4 py-3">
          <h1 className="text-xl font-bold bg-gradient-to-r from-primary-500 to-purple-500 dark:from-orange-500 dark:to-orange-600 bg-clip-text text-transparent">
            MectoFitness
          </h1>
          <div className="flex items-center gap-2">
            {/* Mobile Profile Dropdown */}
            <div className="relative" ref={profileDropdownRef}>
              <button
                onClick={() => setProfileDropdownOpen(!profileDropdownOpen)}
                className="h-10 w-10 rounded-full bg-gradient-to-br from-primary-500 to-purple-500 dark:from-orange-500 dark:to-purple-500 flex items-center justify-center text-white font-semibold shadow-sm hover:shadow-md transition-shadow"
              >
                {user?.first_name?.charAt(0) || user?.name?.charAt(0) || 'U'}
              </button>

              {/* Dropdown Menu */}
              {profileDropdownOpen && (
                <div className="absolute right-0 mt-2 w-64 bg-white dark:bg-gray-900 border border-gray-200 dark:border-white/10 rounded-lg shadow-lg py-2">
                  {/* User Info */}
                  <div className="px-4 py-3 border-b border-gray-200 dark:border-white/10">
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      {user?.first_name || user?.name || 'User'} {user?.last_name || ''}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">{user?.email}</p>
                    {organization && (
                      <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">{organization.name}</p>
                    )}
                  </div>

                  {/* Menu Items */}
                  <Link
                    to="/account"
                    onClick={() => setProfileDropdownOpen(false)}
                    className="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-white/5 transition-colors"
                  >
                    <UserCircleIcon className="h-5 w-5" />
                    <span>Account Profile</span>
                  </Link>

                  <Link
                    to="/settings"
                    onClick={() => setProfileDropdownOpen(false)}
                    className="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-white/5 transition-colors"
                  >
                    <Cog6ToothIcon className="h-5 w-5" />
                    <span>Settings</span>
                  </Link>

                  <button
                    onClick={() => {
                      setProfileDropdownOpen(false);
                      toggleTheme();
                    }}
                    className="flex items-center gap-3 w-full px-4 py-2.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-white/5 transition-colors"
                  >
                    {theme === 'dark' ? (
                      <>
                        <SunIcon className="h-5 w-5" />
                        <span>Light Mode</span>
                      </>
                    ) : (
                      <>
                        <MoonIcon className="h-5 w-5" />
                        <span>Dark Mode</span>
                      </>
                    )}
                  </button>

                  <div className="border-t border-gray-200 dark:border-white/10 my-2"></div>

                  <button
                    onClick={() => {
                      setProfileDropdownOpen(false);
                      handleLogout();
                    }}
                    className="flex items-center gap-3 w-full px-4 py-2.5 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
                  >
                    <ArrowRightOnRectangleIcon className="h-5 w-5" />
                    <span>Logout</span>
                  </button>
                </div>
              )}
            </div>

            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-white/5 transition-colors"
              aria-label={mobileMenuOpen ? "Close menu" : "Open menu"}
              aria-expanded={mobileMenuOpen}
            >
              {mobileMenuOpen ? (
                <XMarkIcon className="h-6 w-6" />
              ) : (
                <Bars3Icon className="h-6 w-6" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile menu panel */}
        {mobileMenuOpen && (
          <div
            className="fixed inset-0 z-50 bg-gray-900 bg-opacity-50 dark:bg-black dark:bg-opacity-70 lg:hidden"
            onClick={() => setMobileMenuOpen(false)}
          >
            <div
              className="fixed inset-y-0 left-0 flex w-full max-w-sm flex-col bg-white dark:bg-black border-r dark:border-white/10 shadow-xl"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex flex-1 flex-col overflow-y-auto pt-5 pb-4">
                <div className="flex items-center justify-between px-4 mb-6">
                  <h1 className="text-2xl font-bold bg-gradient-to-r from-primary-500 to-purple-500 dark:from-orange-500 dark:to-orange-600 bg-clip-text text-transparent">
                    MectoFitness
                  </h1>
                  <button
                    onClick={() => setMobileMenuOpen(false)}
                    className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-white/5"
                    aria-label="Close menu"
                  >
                    <XMarkIcon className="h-6 w-6" />
                  </button>
                </div>

                {/* Mobile Search */}
                <div className="px-4 mb-4">
                  <div className="relative">
                    <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                    <input
                      type="text"
                      placeholder="Search..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="w-full pl-9 pr-3 py-2 text-sm border border-gray-200 dark:border-white/10 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 dark:focus:ring-orange-500 bg-white dark:bg-white/5 text-gray-900 dark:text-white"
                    />
                  </div>
                </div>

                <nav className="flex-1 space-y-6 px-3">
                  {filteredCategories.map((category) => (
                    <div key={category.name}>
                      <div className="px-2 mb-2 text-xs font-semibold text-gray-500 dark:text-gray-400 tracking-wider">
                        {category.name}
                      </div>
                      <div className="space-y-1">
                        {category.items.map((item) => {
                          const isActive = location.pathname.startsWith(item.href);
                          return (
                            <Link
                              key={item.name}
                              to={item.href}
                              onClick={() => setMobileMenuOpen(false)}
                              className={`
                                group flex items-center px-3 py-3 text-sm font-medium rounded-lg transition-all
                                ${
                                  isActive
                                    ? 'bg-primary-50 dark:bg-orange-500/10 text-primary-700 dark:text-orange-400'
                                    : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-white/5'
                                }
                              `}
                            >
                              <item.icon className={`mr-3 h-5 w-5 flex-shrink-0 ${
                                isActive ? 'text-primary-600 dark:text-orange-500' : 'text-gray-400 dark:text-gray-500'
                              }`} />
                              {item.name}
                            </Link>
                          );
                        })}
                      </div>
                    </div>
                  ))}
                </nav>
              </div>

              {/* Mobile User Section */}
              <div className="flex flex-shrink-0 border-t border-gray-200 dark:border-white/10 p-4 bg-gray-50 dark:bg-white/5">
                <div className="w-full">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <div className="h-10 w-10 rounded-full bg-gradient-to-br from-primary-500 to-purple-500 dark:from-orange-500 dark:to-purple-500 flex items-center justify-center text-white font-semibold">
                        {user?.first_name?.charAt(0) || user?.name?.charAt(0) || 'U'}
                      </div>
                    </div>
                    <div className="ml-3 flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                        {user?.first_name || user?.name}
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-400 truncate">{user?.email}</p>
                    </div>
                    <Link
                      to="/settings"
                      onClick={() => setMobileMenuOpen(false)}
                      className="ml-2 text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-white/5"
                      title="Settings"
                      aria-label="Settings"
                    >
                      <Cog6ToothIcon className="h-5 w-5" />
                    </Link>
                    <button
                      onClick={handleLogout}
                      className="ml-2 text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-white/5"
                      aria-label="Logout"
                    >
                      <ArrowRightOnRectangleIcon className="h-5 w-5" />
                    </button>
                  </div>
                  {organization && (
                    <div className="mt-2 px-2 py-1 bg-white dark:bg-white/5 border border-gray-200 dark:border-white/10 rounded text-xs text-gray-600 dark:text-gray-400 truncate">
                      {organization.name}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Main content */}
      <div className="lg:pl-64 flex flex-col min-h-screen">
        {/* Desktop Top Header */}
        <div className="hidden lg:block sticky top-0 z-30 bg-white dark:bg-black border-b border-gray-200 dark:border-white/10 shadow-sm">
          <div className="px-6 py-4 flex items-center justify-end">
            {/* Profile Dropdown */}
            <div className="relative" ref={profileDropdownRef}>
              <button
                onClick={() => setProfileDropdownOpen(!profileDropdownOpen)}
                className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-white/5 transition-colors"
              >
                <div className="h-10 w-10 rounded-full bg-gradient-to-br from-primary-500 to-purple-500 dark:from-orange-500 dark:to-purple-500 flex items-center justify-center text-white font-semibold shadow-sm">
                  {user?.first_name?.charAt(0) || user?.name?.charAt(0) || 'U'}
                </div>
                <div className="text-left hidden xl:block">
                  <p className="text-sm font-medium text-gray-900 dark:text-white">
                    {user?.first_name || user?.name || 'User'}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">{user?.email}</p>
                </div>
                <ChevronDownIcon className={`h-4 w-4 text-gray-500 dark:text-gray-400 transition-transform ${profileDropdownOpen ? 'rotate-180' : ''}`} />
              </button>

              {/* Dropdown Menu */}
              {profileDropdownOpen && (
                <div className="absolute right-0 mt-2 w-64 bg-white dark:bg-gray-900 border border-gray-200 dark:border-white/10 rounded-lg shadow-lg py-2">
                  {/* User Info */}
                  <div className="px-4 py-3 border-b border-gray-200 dark:border-white/10">
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      {user?.first_name || user?.name || 'User'} {user?.last_name || ''}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">{user?.email}</p>
                    {organization && (
                      <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">{organization.name}</p>
                    )}
                  </div>

                  {/* Menu Items */}
                  <Link
                    to="/account"
                    onClick={() => setProfileDropdownOpen(false)}
                    className="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-white/5 transition-colors"
                  >
                    <UserCircleIcon className="h-5 w-5" />
                    <span>Account Profile</span>
                  </Link>

                  <Link
                    to="/settings"
                    onClick={() => setProfileDropdownOpen(false)}
                    className="flex items-center gap-3 px-4 py-2.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-white/5 transition-colors"
                  >
                    <Cog6ToothIcon className="h-5 w-5" />
                    <span>Settings</span>
                  </Link>

                  <button
                    onClick={toggleTheme}
                    className="flex items-center gap-3 w-full px-4 py-2.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-white/5 transition-colors"
                  >
                    {theme === 'dark' ? (
                      <>
                        <SunIcon className="h-5 w-5" />
                        <span>Light Mode</span>
                      </>
                    ) : (
                      <>
                        <MoonIcon className="h-5 w-5" />
                        <span>Dark Mode</span>
                      </>
                    )}
                  </button>

                  <div className="border-t border-gray-200 dark:border-white/10 my-2"></div>

                  <button
                    onClick={() => {
                      setProfileDropdownOpen(false);
                      handleLogout();
                    }}
                    className="flex items-center gap-3 w-full px-4 py-2.5 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
                  >
                    <ArrowRightOnRectangleIcon className="h-5 w-5" />
                    <span>Logout</span>
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>

        <main className="flex-1">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
