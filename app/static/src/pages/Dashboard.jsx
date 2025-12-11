import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import {
  UsersIcon,
  CalendarIcon,
  DocumentTextIcon,
  ChartBarIcon,
  PlusIcon,
  ClockIcon,
  ArrowTrendingUpIcon,
  CheckCircleIcon,
  CurrencyDollarIcon,
  BoltIcon,
} from '@heroicons/react/24/outline';
import { dashboardApi, handleApiError } from '../api/client';

// Helper function to format time ago
const formatTimeAgo = (timestamp) => {
  const date = new Date(timestamp);
  const now = new Date();
  const diffMs = now - date;
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);
  
  if (diffMins < 1) return 'Just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  return `${diffDays}d ago`;
};

// Professional TrueCoach/Trainerize-style Dashboard with Backend API Integration
export default function Dashboard() {
  const { user } = useAuthStore();
  const [overview, setOverview] = useState(null);
  const [activities, setActivities] = useState([]);
  const [upcomingSessions, setUpcomingSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch comprehensive dashboard data from backend
      const [overviewRes, activityRes, calendarRes] = await Promise.all([
        dashboardApi.getOverview(),
        dashboardApi.getActivity({ limit: 10 }),
        dashboardApi.getCalendar({ days: 7 }),
      ]);

      setOverview(overviewRes.data);
      setActivities(activityRes.data.activities || []);
      setUpcomingSessions(calendarRes.data.sessions?.slice(0, 5) || []);
    } catch (err) {
      console.error('Error loading dashboard:', err);
      setError(handleApiError(err));
    } finally {
      setLoading(false);
    }
  };

  // Get greeting based on time of day
  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 18) return 'Good afternoon';
    return 'Good evening';
  };

  // Format currency
  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount || 0);
  };

  // Loading state
  if (loading) {
    return (
      <div className="h-full bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin h-12 w-12 border-4 border-primary-200 border-t-primary-600 rounded-full mx-auto mb-4"></div>
          <p className="text-gray-700">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="h-full bg-gray-50 flex items-center justify-center">
        <div className="text-center max-w-md mx-auto px-4">
          <div className="bg-danger-50 rounded-full h-16 w-16 flex items-center justify-center mx-auto mb-4">
            <BoltIcon className="h-8 w-8 text-danger-600" />
          </div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Unable to Load Dashboard</h2>
          <p className="text-gray-700 mb-6">{error}</p>
          <button
            onClick={loadDashboardData}
            className="inline-flex items-center gap-2 bg-primary-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-primary-700 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

        {/* Header Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            {getGreeting()}, {user?.first_name || 'Trainer'}
          </h1>
          <p className="text-gray-700">Here's what's happening with your clients today</p>
        </div>

        {/* Quick Actions Bar */}
        <div className="mb-8 flex flex-wrap gap-3">
          <Link
            to="/clients?action=add"
            className="inline-flex items-center gap-2 bg-primary-600 text-white px-5 py-2.5 rounded-lg font-medium hover:bg-primary-700 transition-colors shadow-button hover:shadow-button-hover"
          >
            <PlusIcon className="h-5 w-5" />
            New Client
          </Link>
          <Link
            to="/sessions?action=add"
            className="inline-flex items-center gap-2 bg-white text-gray-700 px-5 py-2.5 rounded-lg font-medium hover:bg-gray-50 transition-colors border border-gray-300 shadow-sm"
          >
            <CalendarIcon className="h-5 w-5" />
            Schedule Session
          </Link>
          <Link
            to="/programs?action=add"
            className="inline-flex items-center gap-2 bg-white text-gray-700 px-5 py-2.5 rounded-lg font-medium hover:bg-gray-50 transition-colors border border-gray-300 shadow-sm"
          >
            <DocumentTextIcon className="h-5 w-5" />
            Create Program
          </Link>
        </div>

        {/* Stats Grid - Using Real Backend Data */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">

          {/* Active Clients */}
          <div className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-card transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-primary-50 rounded-lg p-3">
                <UsersIcon className="h-6 w-6 text-primary-600" />
              </div>
            </div>
            <div className="text-3xl font-bold text-gray-900 mb-1">
              {overview?.total_clients || 0}
            </div>
            <div className="text-sm text-gray-700 mb-3">Active Clients</div>
            <div className="flex items-center text-sm text-gray-600">
              <ArrowTrendingUpIcon className="h-4 w-4 text-success-600 mr-1" />
              <span className="text-success-600 font-medium">
                {overview?.active_clients || 0}
              </span>
              <span className="ml-1">active this week</span>
            </div>
          </div>

          {/* Today's Sessions */}
          <div className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-card transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-purple-50 rounded-lg p-3">
                <ClockIcon className="h-6 w-6 text-purple-600" />
              </div>
            </div>
            <div className="text-3xl font-bold text-gray-900 mb-1">
              {overview?.sessions_today || 0}
            </div>
            <div className="text-sm text-gray-700 mb-3">Today's Sessions</div>
            <div className="flex items-center text-sm text-gray-600">
              <CalendarIcon className="h-4 w-4 text-gray-600 mr-1" />
              <span>{overview?.sessions_upcoming || 0} upcoming</span>
            </div>
          </div>

          {/* Active Programs */}
          <div className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-card transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-accent-50 rounded-lg p-3">
                <DocumentTextIcon className="h-6 w-6 text-accent-600" />
              </div>
            </div>
            <div className="text-3xl font-bold text-gray-900 mb-1">
              {overview?.active_programs || 0}
            </div>
            <div className="text-sm text-gray-700 mb-3">Active Programs</div>
            <Link to="/programs" className="text-sm text-primary-600 hover:text-primary-700 font-medium">
              View all →
            </Link>
          </div>

          {/* Monthly Revenue */}
          <div className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-card transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-success-50 rounded-lg p-3">
                <CurrencyDollarIcon className="h-6 w-6 text-success-600" />
              </div>
            </div>
            <div className="text-3xl font-bold text-gray-900 mb-1">
              {formatCurrency(overview?.revenue_this_month)}
            </div>
            <div className="text-sm text-gray-700 mb-3">This Month</div>
            <div className="flex items-center text-sm text-gray-600">
              <span className={`font-medium ${
                overview?.revenue_change >= 0 ? 'text-success-600' : 'text-danger-600'
              }`}>
                {overview?.revenue_change > 0 && '+'}
                {overview?.revenue_change || 0}%
              </span>
              <span className="ml-1">vs last month</span>
            </div>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

          {/* Left Column - Main Content */}
          <div className="lg:col-span-2 space-y-6">

            {/* Upcoming Sessions */}
            <div className="bg-white rounded-lg border border-gray-200 shadow-sm">
              <div className="border-b border-gray-200 px-6 py-4 flex items-center justify-between">
                <h2 className="text-lg font-semibold text-gray-900">Upcoming Sessions</h2>
                <Link to="/sessions" className="text-sm text-primary-600 hover:text-primary-700 font-medium">
                  View all
                </Link>
              </div>

              <div className="p-6">
                {upcomingSessions.length === 0 ? (
                  <div className="text-center py-12">
                    <div className="bg-gray-100 rounded-full h-16 w-16 flex items-center justify-center mx-auto mb-4">
                      <CalendarIcon className="h-8 w-8 text-gray-600" />
                    </div>
                    <p className="text-gray-700 mb-4">No upcoming sessions scheduled</p>
                    <Link
                      to="/sessions?action=add"
                      className="inline-flex items-center text-primary-600 hover:text-primary-700 font-medium"
                    >
                      <PlusIcon className="h-5 w-5 mr-1" />
                      Schedule your first session
                    </Link>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {upcomingSessions.map((session) => (
                      <Link
                        key={session.id}
                        to={`/sessions/${session.id}`}
                        className="flex items-center justify-between p-4 rounded-lg border border-gray-200 hover:border-primary-300 hover:bg-primary-50 transition-all group"
                      >
                        <div className="flex items-center gap-4">
                          <div className="bg-primary-100 rounded-lg p-3 group-hover:bg-primary-200 transition-colors">
                            <ClockIcon className="h-5 w-5 text-primary-700" />
                          </div>
                          <div>
                            <div className="font-medium text-gray-900">
                              {session.title || 'Training Session'}
                            </div>
                            <div className="text-sm text-gray-700 mt-0.5">
                              {session.client_name || 'Client'}
                            </div>
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="text-sm font-medium text-gray-900">
                            {new Date(session.scheduled_start).toLocaleDateString('en-US', {
                              month: 'short',
                              day: 'numeric'
                            })}
                          </div>
                          <div className="text-sm text-gray-700 mt-0.5">
                            {new Date(session.scheduled_start).toLocaleTimeString('en-US', {
                              hour: 'numeric',
                              minute: '2-digit'
                            })}
                          </div>
                        </div>
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Key Metrics */}
            <div className="bg-white rounded-lg border border-gray-200 shadow-sm">
              <div className="border-b border-gray-200 px-6 py-4">
                <h2 className="text-lg font-semibold text-gray-900">Performance Metrics</h2>
              </div>

              <div className="p-6">
                <div className="grid grid-cols-2 gap-6">
                  {/* Session Completion Rate */}
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-gray-800">Completion Rate</span>
                      <span className="text-sm font-bold text-success-600">
                        {overview?.completion_rate || 0}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-success-500 h-2 rounded-full transition-all"
                        style={{ width: `${overview?.completion_rate || 0}%` }}
                      />
                    </div>
                  </div>

                  {/* Client Retention */}
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-gray-800">Client Retention</span>
                      <span className="text-sm font-bold text-primary-600">
                        {overview?.retention_rate || 0}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-primary-500 h-2 rounded-full transition-all"
                        style={{ width: `${overview?.retention_rate || 0}%` }}
                      />
                    </div>
                  </div>

                  {/* Average Sessions per Client */}
                  <div>
                    <div className="text-sm text-gray-700">Avg Sessions/Client</div>
                    <div className="text-2xl font-bold text-gray-900 mt-1">
                      {overview?.avg_sessions_per_client?.toFixed(1) || '0.0'}
                    </div>
                  </div>

                  {/* Total Revenue */}
                  <div>
                    <div className="text-sm text-gray-700">Total Revenue</div>
                    <div className="text-2xl font-bold text-gray-900 mt-1">
                      {formatCurrency(overview?.total_revenue)}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column - Activity Feed */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg border border-gray-200 shadow-sm sticky top-8">
              <div className="border-b border-gray-200 px-6 py-4">
                <h2 className="text-lg font-semibold text-gray-900">Recent Activity</h2>
              </div>

              <div className="p-6">
                {activities.length === 0 ? (
                  <div className="text-center py-12">
                    <div className="bg-gray-100 rounded-full h-16 w-16 flex items-center justify-center mx-auto mb-4">
                      <ChartBarIcon className="h-8 w-8 text-gray-600" />
                    </div>
                    <p className="text-gray-700">No recent activity</p>
                  </div>
                ) : (
                  <div className="space-y-5">
                    {activities.map((activity, idx) => {
                      // Determine the route - all activities link to client detail page
                      const route = activity.client_id ? `/clients/${activity.client_id}` : null;
                      const timeAgo = activity.time_ago || formatTimeAgo(activity.timestamp);

                      const content = (
                        <>
                          <div className="h-10 w-10 rounded-full bg-gradient-to-br from-primary-400 to-purple-400 flex items-center justify-center text-white font-semibold text-sm flex-shrink-0 shadow-sm">
                            {activity.client_initials || activity.user_initials || 'U'}
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className="text-sm text-gray-900">
                              <span className="text-gray-700">{activity.description}</span>
                            </p>
                            <p className="text-xs text-gray-600 mt-1">{timeAgo}</p>
                          </div>
                        </>
                      );

                      // If we have a route, make it a Link, otherwise just a div
                      return route ? (
                        <Link
                          key={idx}
                          to={route}
                          className="flex items-start gap-3 p-2 -mx-2 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer"
                        >
                          {content}
                        </Link>
                      ) : (
                        <div key={idx} className="flex items-start gap-3">
                          {content}
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
