import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import {
  UsersIcon,
  CalendarIcon,
  DocumentTextIcon,
  ChartBarIcon,
  PlusIcon,
} from '@heroicons/react/24/outline';
import { clientsApi, sessionsApi, programsApi } from '../api/client';

export default function Dashboard() {
  const { user, organization } = useAuthStore();
  const [stats, setStats] = useState({
    totalClients: 0,
    totalPrograms: 0,
    todaySessions: 0,
    upcomingSessions: 0,
  });
  const [recentClients, setRecentClients] = useState([]);
  const [upcomingSessions, setUpcomingSessions] = useState([]);
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

      // Calculate stats
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      
      const todaySessions = sessions.filter((s) => {
        const sessionDate = new Date(s.scheduled_start);
        sessionDate.setHours(0, 0, 0, 0);
        return sessionDate.getTime() === today.getTime();
      });

      const upcoming = sessions.filter((s) => {
        const sessionDate = new Date(s.scheduled_start);
        return sessionDate > new Date() && sessionDate.getTime() > today.getTime();
      }).slice(0, 5);

      setStats({
        totalClients: clients.length,
        totalPrograms: programs.length,
        todaySessions: todaySessions.length,
        upcomingSessions: upcoming.length,
      });

      setRecentClients(clients.slice(0, 5));
      setUpcomingSessions(upcoming);
    } catch (error) {
      console.error('Error loading dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const statCards = [
    {
      name: 'Active Clients',
      value: stats.totalClients,
      icon: UsersIcon,
      color: 'from-primary-500 to-primary-600',
      bgColor: 'bg-primary-50',
      textColor: 'text-primary-700',
      href: '/clients',
    },
    {
      name: 'Active Programs',
      value: stats.totalPrograms,
      icon: DocumentTextIcon,
      color: 'from-teal-500 to-teal-600',
      bgColor: 'bg-teal-50',
      textColor: 'text-teal-700',
      href: '/programs',
    },
    {
      name: "Today's Sessions",
      value: stats.todaySessions,
      icon: CalendarIcon,
      color: 'from-accent-500 to-accent-600',
      bgColor: 'bg-accent-50',
      textColor: 'text-accent-700',
      href: '/sessions',
    },
    {
      name: 'Upcoming Sessions',
      value: stats.upcomingSessions,
      icon: ChartBarIcon,
      color: 'from-purple-500 to-purple-600',
      bgColor: 'bg-purple-50',
      textColor: 'text-purple-700',
      href: '/sessions',
    },
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Welcome Header */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 sm:p-8">
        <h1 className="text-3xl font-bold text-gray-900">
          Welcome back, {user?.name}! 👋
        </h1>
        {organization && (
          <p className="mt-2 text-base text-gray-600">{organization.name}</p>
        )}
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 xs:grid-cols-2 lg:grid-cols-4">
        {statCards.map((stat) => (
          <Link
            key={stat.name}
            to={stat.href}
            className={`group relative overflow-hidden rounded-xl bg-white px-5 py-6 shadow-sm border border-gray-100 hover:shadow-md hover:border-gray-200 transition-all duration-200 ${stat.bgColor}/30`}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-600 mb-1">
                  {stat.name}
                </p>
                <p className={`text-3xl font-bold ${stat.textColor}`}>
                  {stat.value}
                </p>
              </div>
              <div className={`rounded-lg bg-gradient-to-br ${stat.color} p-3 shadow-sm`}>
                <stat.icon className="h-6 w-6 text-white" aria-hidden="true" />
              </div>
            </div>
            <div className="mt-3 text-xs text-gray-500 flex items-center group-hover:text-gray-700 transition-colors">
              View all <span className="ml-1">→</span>
            </div>
          </Link>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="bg-white shadow-sm border border-gray-100 rounded-xl p-6 sm:p-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Quick Actions</h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <Link
            to="/clients?action=add"
            className="group flex items-center justify-center px-5 py-3.5 border border-transparent rounded-lg shadow-sm text-sm font-semibold text-white bg-gradient-to-r from-primary-600 to-primary-500 hover:from-primary-700 hover:to-primary-600 transition-all duration-200 min-h-[44px]"
          >
            <PlusIcon className="h-5 w-5 mr-2" />
            Add New Client
          </Link>
          <Link
            to="/sessions?action=add"
            className="group flex items-center justify-center px-5 py-3.5 border border-transparent rounded-lg shadow-sm text-sm font-semibold text-white bg-gradient-to-r from-teal-600 to-teal-500 hover:from-teal-700 hover:to-teal-600 transition-all duration-200 min-h-[44px]"
          >
            <PlusIcon className="h-5 w-5 mr-2" />
            Schedule Session
          </Link>
          <Link
            to="/programs?action=add"
            className="group flex items-center justify-center px-5 py-3.5 border border-transparent rounded-lg shadow-sm text-sm font-semibold text-white bg-gradient-to-r from-accent-600 to-accent-500 hover:from-accent-700 hover:to-accent-600 transition-all duration-200 min-h-[44px]"
          >
            <PlusIcon className="h-5 w-5 mr-2" />
            Create Program
          </Link>
        </div>
      </div>

      {/* Two Column Layout */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Recent Clients */}
        <div className="bg-white shadow-sm border border-gray-100 rounded-xl overflow-hidden">
          <div className="px-6 py-5 border-b border-gray-100">
            <h2 className="text-lg font-semibold text-gray-900">Recent Clients</h2>
          </div>
          <ul className="divide-y divide-gray-100">
            {recentClients.length > 0 ? (
              recentClients.map((client) => (
                <li key={client.id}>
                  <Link
                    to={`/clients/${client.id}`}
                    className="block hover:bg-gray-50 transition-colors"
                  >
                    <div className="px-6 py-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center min-w-0 flex-1">
                          <div className="flex-shrink-0">
                            <div className="h-10 w-10 rounded-full bg-gradient-to-br from-primary-500 to-teal-500 flex items-center justify-center shadow-sm">
                              <span className="text-white font-semibold text-sm">
                                {client.full_name?.charAt(0) || 'C'}
                              </span>
                            </div>
                          </div>
                          <div className="ml-4 min-w-0 flex-1">
                            <p className="text-sm font-semibold text-gray-900 truncate">
                              {client.full_name}
                            </p>
                            <p className="text-sm text-gray-500 truncate">
                              {client.email}
                            </p>
                          </div>
                        </div>
                        <div className="ml-4 flex-shrink-0">
                          <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-success-50 text-success-700 border border-success-100">
                            Active
                          </span>
                        </div>
                      </div>
                    </div>
                  </Link>
                </li>
              ))
            ) : (
              <li className="px-6 py-12 text-center">
                <p className="text-sm text-gray-500 mb-3">No clients yet</p>
                <Link
                  to="/clients?action=add"
                  className="inline-flex items-center text-sm font-medium text-primary-600 hover:text-primary-700"
                >
                  Add your first client <span className="ml-1">→</span>
                </Link>
              </li>
            )}
          </ul>
          {recentClients.length > 0 && (
            <div className="px-6 py-4 bg-gray-50 border-t border-gray-100">
              <Link
                to="/clients"
                className="text-sm font-medium text-primary-600 hover:text-primary-700 flex items-center"
              >
                View all clients <span className="ml-1">→</span>
              </Link>
            </div>
          )}
        </div>

        {/* Upcoming Sessions */}
        <div className="bg-white shadow-sm border border-gray-100 rounded-xl overflow-hidden">
          <div className="px-6 py-5 border-b border-gray-100">
            <h2 className="text-lg font-semibold text-gray-900">Upcoming Sessions</h2>
          </div>
          <ul className="divide-y divide-gray-100">
            {upcomingSessions.length > 0 ? (
              upcomingSessions.map((session) => (
                <li key={session.id}>
                  <Link
                    to={`/sessions/${session.id}`}
                    className="block hover:bg-gray-50 transition-colors"
                  >
                    <div className="px-6 py-4">
                      <div className="flex items-start justify-between">
                        <div className="min-w-0 flex-1">
                          <p className="text-sm font-semibold text-gray-900 mb-1">
                            {session.title || 'Training Session'}
                          </p>
                          <p className="text-sm text-gray-600 mb-2">
                            {session.client?.full_name}
                          </p>
                          <div className="flex items-center text-xs text-gray-500">
                            <CalendarIcon className="h-4 w-4 mr-1.5" />
                            {new Date(session.scheduled_start).toLocaleString('en-US', {
                              month: 'short',
                              day: 'numeric',
                              hour: 'numeric',
                              minute: '2-digit',
                            })}
                          </div>
                        </div>
                        <div className="ml-4 flex-shrink-0">
                          <div className="h-10 w-10 rounded-lg bg-teal-50 flex items-center justify-center">
                            <CalendarIcon className="h-5 w-5 text-teal-600" />
                          </div>
                        </div>
                      </div>
                    </div>
                  </Link>
                </li>
              ))
            ) : (
              <li className="px-6 py-12 text-center">
                <p className="text-sm text-gray-500 mb-3">No upcoming sessions</p>
                <Link
                  to="/sessions?action=add"
                  className="inline-flex items-center text-sm font-medium text-primary-600 hover:text-primary-700"
                >
                  Schedule a session <span className="ml-1">→</span>
                </Link>
              </li>
            )}
          </ul>
          {upcomingSessions.length > 0 && (
            <div className="px-6 py-4 bg-gray-50 border-t border-gray-100">
              <Link
                to="/sessions"
                className="text-sm font-medium text-primary-600 hover:text-primary-700 flex items-center"
              >
                View all sessions <span className="ml-1">→</span>
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
