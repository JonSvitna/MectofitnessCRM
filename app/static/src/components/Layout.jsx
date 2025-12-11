import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { useState, useEffect } from 'react';
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
} from '@heroicons/react/24/outline';

// Navigation structure with categories
const navigationCategories = [
  {
    name: 'WORKSPACE',
    items: [
      { name: 'Overview', href: '/dashboard', icon: HomeIcon },
      { name: 'Calendar', href: '/calendar', icon: CalendarIcon },
    ],
  },
  {
    name: 'CLIENTS & TRAINING',
    items: [
      { name: 'Clients', href: '/clients', icon: UsersIcon },
      { name: 'Sessions', href: '/sessions', icon: ClockIcon },
      { name: 'Programs', href: '/programs', icon: DocumentTextIcon },
      { name: 'Progress Tracking', href: '/progress', icon: ChartBarIcon },
    ],
  },
  {
    name: 'ENGAGEMENT',
    items: [
      { name: 'Messages', href: '/messages', icon: ChatBubbleLeftRightIcon },
      { name: 'Groups', href: '/groups', icon: UserGroupIcon },
      { name: 'Challenges', href: '/challenges', icon: TrophyIcon },
      { name: 'Announcements', href: '/announcements', icon: BellIcon },
    ],
  },
  {
    name: 'BUSINESS',
    items: [
      { name: 'Payments', href: '/payments', icon: CreditCardIcon },
      { name: 'Team', href: '/team', icon: UserGroupIcon },
      { name: 'Scheduling', href: '/scheduling', icon: CalendarIcon },
    ],
  },
  {
    name: 'RESOURCES',
    items: [
      { name: 'Master Libraries', href: '/master-libraries', icon: BookOpenIcon },
      { name: 'Exercise Library', href: '/exercise-library', icon: AcademicCapIcon },
    ],
  },
  {
    name: 'ACCOUNT',
    items: [
      { name: 'Settings', href: '/settings', icon: Cog6ToothIcon },
    ],
  },
];

export default function Layout() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, organization, logout } = useAuthStore();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [collapsedCategories, setCollapsedCategories] = useState({});
  const [searchQuery, setSearchQuery] = useState('');

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

  const handleLogout = () => {
    logout();
    navigate('/login');
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
    <div className="min-h-screen bg-gray-50">
      {/* Desktop Sidebar */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-64 lg:flex-col">
        <div className="flex min-h-0 flex-1 flex-col bg-white border-r border-gray-200 shadow-sidebar">
          <div className="flex flex-col pt-5 pb-4 h-full">
            {/* Logo */}
            <div className="flex flex-shrink-0 items-center px-5 mb-6">
              <h1 className="text-2xl font-bold bg-gradient-to-r from-primary-500 to-purple-500 bg-clip-text text-transparent">
                MectoFitness
              </h1>
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
                  className="w-full pl-9 pr-3 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
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
                    className="flex items-center justify-between w-full px-2 mb-2 text-xs font-semibold text-gray-500 uppercase tracking-wider hover:text-gray-700 transition-colors"
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
                                  ? 'bg-primary-50 text-primary-700 shadow-sm'
                                  : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                              }
                            `}
                          >
                            <item.icon
                              className={`mr-3 h-5 w-5 flex-shrink-0 transition-colors ${
                                isActive ? 'text-primary-600' : 'text-gray-400 group-hover:text-gray-600'
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
          <div className="flex flex-shrink-0 border-t border-gray-200 p-4 bg-gray-50">
            <div className="w-full">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="h-10 w-10 rounded-full bg-gradient-to-br from-primary-500 to-purple-500 flex items-center justify-center text-white font-semibold shadow-sm">
                    {user?.first_name?.charAt(0) || user?.name?.charAt(0) || 'U'}
                  </div>
                </div>
                <div className="ml-3 flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {user?.first_name || user?.name || 'User'}
                  </p>
                  <p className="text-xs text-gray-500 truncate">{user?.email}</p>
                </div>
                <Link
                  to="/settings"
                  className="ml-2 flex-shrink-0 text-gray-400 hover:text-gray-600 transition-colors p-2 rounded-lg hover:bg-gray-100"
                  title="Settings"
                  aria-label="Settings"
                >
                  <Cog6ToothIcon className="h-5 w-5" />
                </Link>
                <button
                  onClick={handleLogout}
                  className="ml-2 flex-shrink-0 text-gray-400 hover:text-gray-600 transition-colors p-2 rounded-lg hover:bg-gray-100"
                  title="Logout"
                  aria-label="Logout"
                >
                  <ArrowRightOnRectangleIcon className="h-5 w-5" />
                </button>
              </div>
              {organization && (
                <div className="mt-2 px-2 py-1 bg-white border border-gray-200 rounded text-xs text-gray-600 truncate">
                  {organization.name}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Mobile Header */}
      <div className="lg:hidden sticky top-0 z-40 bg-white border-b border-gray-200 shadow-sm">
        <div className="flex items-center justify-between px-4 py-3">
          <h1 className="text-xl font-bold bg-gradient-to-r from-primary-500 to-purple-500 bg-clip-text text-transparent">
            MectoFitness
          </h1>
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="text-gray-600 hover:text-gray-900 p-2 rounded-lg hover:bg-gray-100 transition-colors"
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

        {/* Mobile menu panel */}
        {mobileMenuOpen && (
          <div
            className="fixed inset-0 z-50 bg-gray-900 bg-opacity-50 lg:hidden"
            onClick={() => setMobileMenuOpen(false)}
          >
            <div
              className="fixed inset-y-0 left-0 flex w-full max-w-sm flex-col bg-white shadow-xl"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex flex-1 flex-col overflow-y-auto pt-5 pb-4">
                <div className="flex items-center justify-between px-4 mb-6">
                  <h1 className="text-2xl font-bold bg-gradient-to-r from-primary-500 to-purple-500 bg-clip-text text-transparent">
                    MectoFitness
                  </h1>
                  <button
                    onClick={() => setMobileMenuOpen(false)}
                    className="text-gray-600 hover:text-gray-900 p-2 rounded-lg hover:bg-gray-100"
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
                      className="w-full pl-9 pr-3 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                    />
                  </div>
                </div>

                <nav className="flex-1 space-y-6 px-3">
                  {filteredCategories.map((category) => (
                    <div key={category.name}>
                      <div className="px-2 mb-2 text-xs font-semibold text-gray-500 uppercase tracking-wider">
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
                                    ? 'bg-primary-50 text-primary-700'
                                    : 'text-gray-700 hover:bg-gray-50'
                                }
                              `}
                            >
                              <item.icon className={`mr-3 h-5 w-5 flex-shrink-0 ${
                                isActive ? 'text-primary-600' : 'text-gray-400'
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
              <div className="flex flex-shrink-0 border-t border-gray-200 p-4 bg-gray-50">
                <div className="w-full">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <div className="h-10 w-10 rounded-full bg-gradient-to-br from-primary-500 to-purple-500 flex items-center justify-center text-white font-semibold">
                        {user?.first_name?.charAt(0) || user?.name?.charAt(0) || 'U'}
                      </div>
                    </div>
                    <div className="ml-3 flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {user?.first_name || user?.name}
                      </p>
                      <p className="text-xs text-gray-500 truncate">{user?.email}</p>
                    </div>
                    <Link
                      to="/settings"
                      onClick={() => setMobileMenuOpen(false)}
                      className="ml-2 text-gray-400 hover:text-gray-600 p-2 rounded-lg hover:bg-gray-100"
                      title="Settings"
                      aria-label="Settings"
                    >
                      <Cog6ToothIcon className="h-5 w-5" />
                    </Link>
                    <button
                      onClick={handleLogout}
                      className="ml-2 text-gray-400 hover:text-gray-600 p-2 rounded-lg hover:bg-gray-100"
                      aria-label="Logout"
                    >
                      <ArrowRightOnRectangleIcon className="h-5 w-5" />
                    </button>
                  </div>
                  {organization && (
                    <div className="mt-2 px-2 py-1 bg-white border border-gray-200 rounded text-xs text-gray-600 truncate">
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
        <main className="flex-1">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
