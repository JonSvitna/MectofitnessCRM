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
} from '@heroicons/react/24/outline';
import { clientsApi, sessionsApi, programsApi } from '../api/client';

// Professional TrueCoach-style Dashboard
export default function Dashboard() {
  const { user } = useAuthStore();
  const [stats, setStats] = useState({
    totalClients: 0,
    totalPrograms: 0,
    todaySessions: 0,
    upcomingSessions: 0,
    activeThisWeek: 0,
    completionRate: 0,
  });
  const [recentClients, setRecentClients] = useState([]);
  const [upcomingSessions, setUpcomingSessions] = useState([]);
  const [recentActivities, setRecentActivities] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const [clientsRes, sessionsRes, programsRes] = await Promise.all([
        clientsApi.getAll(),
        sessionsApi.getAll(),
        programsApi.getAll(),
      ]);

      const clients = clientsRes.data.clients || [];
      const sessions = sessionsRes.data.sessions || [];
      const programs = programsRes.data.programs || [];

      const today = new Date();
      today.setHours(0, 0, 0, 0);

      const todaySessions = sessions.filter((s) => {
        const sessionDate = new Date(s.scheduled_start);
        sessionDate.setHours(0, 0, 0, 0);
        return sessionDate.getTime() === today.getTime();
      });

      const upcoming = sessions.filter((s) => {
        const sessionDate = new Date(s.scheduled_start);
        return sessionDate > new Date();
      }).slice(0, 5);

      setStats({
        totalClients: clients.length,
        totalPrograms: programs.length,
        todaySessions: todaySessions.length,
        upcomingSessions: upcoming.length,
        activeThisWeek: Math.floor(clients.length * 0.7),
        completionRate: 85,
      });

      setRecentClients(clients.slice(0, 6));
      setUpcomingSessions(upcoming);

      // Mock recent activities
      setRecentActivities([
        { name: 'Tiffany Gosnell', activity: 'completed a workout', time: '2h ago', avatar: 'TG', type: 'workout' },
        { name: 'Donavan Weston', activity: 'checked in for session', time: '4h ago', avatar: 'DW', type: 'checkin' },
        { name: 'Rob Walker', activity: 'achieved new personal record', time: '1d ago', avatar: 'RW', type: 'pr' },
        { name: 'Sarah Johnson', activity: 'completed program week 4', time: '2d ago', avatar: 'SJ', type: 'milestone' },
      ]);
    } catch (error) {
      console.error('Error loading dashboard:', error);
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

  return (
    <div className="h-full bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

        {/* Header Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            {getGreeting()}, {user?.first_name || 'Trainer'}
          </h1>
          <p className="text-gray-600">Here's what's happening with your clients today</p>
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

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Active Clients */}
          <div className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-card transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-primary-50 rounded-lg p-3">
                <UsersIcon className="h-6 w-6 text-primary-600" />
              </div>
            </div>
            <div className="text-3xl font-bold text-gray-900 mb-1">{stats.totalClients}</div>
            <div className="text-sm text-gray-600 mb-3">Active Clients</div>
            <div className="flex items-center text-sm text-gray-500">
              <ArrowTrendingUpIcon className="h-4 w-4 text-success-600 mr-1" />
              <span className="text-success-600 font-medium">{stats.activeThisWeek}</span>
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
            <div className="text-3xl font-bold text-gray-900 mb-1">{stats.todaySessions}</div>
            <div className="text-sm text-gray-600 mb-3">Today's Sessions</div>
            <div className="flex items-center text-sm text-gray-500">
              <CalendarIcon className="h-4 w-4 text-gray-400 mr-1" />
              <span>{stats.upcomingSessions} upcoming</span>
            </div>
          </div>

          {/* Active Programs */}
          <div className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-card transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-accent-50 rounded-lg p-3">
                <DocumentTextIcon className="h-6 w-6 text-accent-600" />
              </div>
            </div>
            <div className="text-3xl font-bold text-gray-900 mb-1">{stats.totalPrograms}</div>
            <div className="text-sm text-gray-600 mb-3">Active Programs</div>
            <Link to="/programs" className="text-sm text-primary-600 hover:text-primary-700 font-medium">
              View all →
            </Link>
          </div>

          {/* Completion Rate */}
          <div className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-card transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-success-50 rounded-lg p-3">
                <ChartBarIcon className="h-6 w-6 text-success-600" />
              </div>
            </div>
            <div className="text-3xl font-bold text-gray-900 mb-1">{stats.completionRate}%</div>
            <div className="text-sm text-gray-600 mb-3">Completion Rate</div>
            <div className="flex items-center text-sm text-success-600 font-medium">
              <CheckCircleIcon className="h-4 w-4 mr-1" />
              Excellent
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
                {loading ? (
                  <div className="text-center py-12 text-gray-500">
                    <div className="animate-spin h-8 w-8 border-4 border-primary-200 border-t-primary-600 rounded-full mx-auto"></div>
                    <p className="mt-4">Loading sessions...</p>
                  </div>
                ) : upcomingSessions.length === 0 ? (
                  <div className="text-center py-12">
                    <div className="bg-gray-100 rounded-full h-16 w-16 flex items-center justify-center mx-auto mb-4">
                      <CalendarIcon className="h-8 w-8 text-gray-400" />
                    </div>
                    <p className="text-gray-600 mb-4">No upcoming sessions scheduled</p>
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
                            <div className="font-medium text-gray-900">{session.title || 'Training Session'}</div>
                            <div className="text-sm text-gray-600 mt-0.5">{session.client?.full_name || 'Client'}</div>
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="text-sm font-medium text-gray-900">
                            {new Date(session.scheduled_start).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                          </div>
                          <div className="text-sm text-gray-600 mt-0.5">
                            {new Date(session.scheduled_start).toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })}
                          </div>
                        </div>
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Recent Clients */}
            <div className="bg-white rounded-lg border border-gray-200 shadow-sm">
              <div className="border-b border-gray-200 px-6 py-4 flex items-center justify-between">
                <h2 className="text-lg font-semibold text-gray-900">Recent Clients</h2>
                <Link to="/clients" className="text-sm text-primary-600 hover:text-primary-700 font-medium">
                  View all
                </Link>
              </div>

              <div className="p-6">
                {loading ? (
                  <div className="text-center py-12 text-gray-500">
                    <div className="animate-spin h-8 w-8 border-4 border-primary-200 border-t-primary-600 rounded-full mx-auto"></div>
                    <p className="mt-4">Loading clients...</p>
                  </div>
                ) : recentClients.length === 0 ? (
                  <div className="text-center py-12">
                    <div className="bg-gray-100 rounded-full h-16 w-16 flex items-center justify-center mx-auto mb-4">
                      <UsersIcon className="h-8 w-8 text-gray-400" />
                    </div>
                    <p className="text-gray-600 mb-4">No clients yet</p>
                    <Link
                      to="/clients?action=add"
                      className="inline-flex items-center text-primary-600 hover:text-primary-700 font-medium"
                    >
                      <PlusIcon className="h-5 w-5 mr-1" />
                      Add your first client
                    </Link>
                  </div>
                ) : (
                  <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
                    {recentClients.map((client) => (
                      <Link
                        key={client.id}
                        to={`/clients/${client.id}`}
                        className="group p-4 rounded-lg border border-gray-200 hover:border-primary-300 hover:bg-primary-50 transition-all text-center"
                      >
                        <div className="h-14 w-14 rounded-full bg-gradient-to-br from-primary-500 to-purple-500 flex items-center justify-center text-white font-semibold text-lg mx-auto mb-3 shadow-sm group-hover:scale-105 transition-transform">
                          {client.first_name?.charAt(0) || 'C'}
                        </div>
                        <div className="font-medium text-gray-900 text-sm truncate mb-1">
                          {client.first_name} {client.last_name}
                        </div>
                        <div className="text-xs text-gray-500 truncate">{client.fitness_goal || 'General Fitness'}</div>
                      </Link>
                    ))}
                  </div>
                )}
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
                {recentActivities.length === 0 ? (
                  <div className="text-center py-12">
                    <div className="bg-gray-100 rounded-full h-16 w-16 flex items-center justify-center mx-auto mb-4">
                      <ChartBarIcon className="h-8 w-8 text-gray-400" />
                    </div>
                    <p className="text-gray-600">No recent activity</p>
                  </div>
                ) : (
                  <div className="space-y-5">
                    {recentActivities.map((activity, idx) => (
                      <div key={idx} className="flex items-start gap-3">
                        <div className="h-10 w-10 rounded-full bg-gradient-to-br from-primary-400 to-purple-400 flex items-center justify-center text-white font-semibold text-sm flex-shrink-0 shadow-sm">
                          {activity.avatar}
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm text-gray-900">
                            <span className="font-semibold">{activity.name}</span>
                            {' '}
                            <span className="text-gray-600">{activity.activity}</span>
                          </p>
                          <p className="text-xs text-gray-500 mt-1">{activity.time}</p>
                        </div>
                      </div>
                    ))}
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
