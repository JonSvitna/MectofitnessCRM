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
      color: 'bg-blue-500',
      href: '/clients',
    },
    {
      name: 'Active Programs',
      value: stats.totalPrograms,
      icon: DocumentTextIcon,
      color: 'bg-green-500',
      href: '/programs',
    },
    {
      name: "Today's Sessions",
      value: stats.todaySessions,
      icon: CalendarIcon,
      color: 'bg-orange-500',
      href: '/sessions',
    },
    {
      name: 'Upcoming Sessions',
      value: stats.upcomingSessions,
      icon: ChartBarIcon,
      color: 'bg-purple-500',
      href: '/sessions',
    },
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Welcome Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">
          Welcome back, {user?.name}!
        </h1>
        {organization && (
          <p className="mt-1 text-sm text-gray-500">{organization.name}</p>
        )}
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {statCards.map((stat) => (
          <Link
            key={stat.name}
            to={stat.href}
            className="relative overflow-hidden rounded-lg bg-white px-4 py-5 shadow hover:shadow-md transition-shadow sm:px-6"
          >
            <dt>
              <div className={`absolute rounded-md p-3 ${stat.color}`}>
                <stat.icon className="h-6 w-6 text-white" aria-hidden="true" />
              </div>
              <p className="ml-16 truncate text-sm font-medium text-gray-500">
                {stat.name}
              </p>
            </dt>
            <dd className="ml-16 flex items-baseline">
              <p className="text-2xl font-semibold text-gray-900">{stat.value}</p>
            </dd>
          </Link>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <Link
            to="/clients?action=add"
            className="flex items-center justify-center px-4 py-3 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-orange-600 hover:bg-orange-700 transition-colors"
          >
            <PlusIcon className="h-5 w-5 mr-2" />
            Add New Client
          </Link>
          <Link
            to="/sessions?action=add"
            className="flex items-center justify-center px-4 py-3 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 transition-colors"
          >
            <PlusIcon className="h-5 w-5 mr-2" />
            Schedule Session
          </Link>
          <Link
            to="/programs?action=add"
            className="flex items-center justify-center px-4 py-3 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 transition-colors"
          >
            <PlusIcon className="h-5 w-5 mr-2" />
            Create Program
          </Link>
        </div>
      </div>

      {/* Two Column Layout */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Recent Clients */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-medium text-gray-900">Recent Clients</h2>
          </div>
          <ul className="divide-y divide-gray-200">
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
                            <div className="h-10 w-10 rounded-full bg-orange-100 flex items-center justify-center">
                              <span className="text-orange-600 font-medium">
                                {client.full_name?.charAt(0) || 'C'}
                              </span>
                            </div>
                          </div>
                          <div className="ml-4 min-w-0 flex-1">
                            <p className="text-sm font-medium text-gray-900 truncate">
                              {client.full_name}
                            </p>
                            <p className="text-sm text-gray-500 truncate">
                              {client.email}
                            </p>
                          </div>
                        </div>
                        <div className="ml-4 flex-shrink-0">
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                            Active
                          </span>
                        </div>
                      </div>
                    </div>
                  </Link>
                </li>
              ))
            ) : (
              <li className="px-6 py-8 text-center">
                <p className="text-sm text-gray-500">No clients yet</p>
                <Link
                  to="/clients?action=add"
                  className="mt-2 inline-block text-sm text-orange-600 hover:text-orange-700"
                >
                  Add your first client
                </Link>
              </li>
            )}
          </ul>
          {recentClients.length > 0 && (
            <div className="px-6 py-3 border-t border-gray-200">
              <Link
                to="/clients"
                className="text-sm font-medium text-orange-600 hover:text-orange-700"
              >
                View all clients →
              </Link>
            </div>
          )}
        </div>

        {/* Upcoming Sessions */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-medium text-gray-900">Upcoming Sessions</h2>
          </div>
          <ul className="divide-y divide-gray-200">
            {upcomingSessions.length > 0 ? (
              upcomingSessions.map((session) => (
                <li key={session.id}>
                  <Link
                    to={`/sessions/${session.id}`}
                    className="block hover:bg-gray-50 transition-colors"
                  >
                    <div className="px-6 py-4">
                      <div className="flex items-center justify-between">
                        <div className="min-w-0 flex-1">
                          <p className="text-sm font-medium text-gray-900">
                            {session.title || 'Training Session'}
                          </p>
                          <p className="text-sm text-gray-500">
                            {session.client?.full_name}
                          </p>
                          <p className="mt-1 text-xs text-gray-400">
                            {new Date(session.scheduled_start).toLocaleString()}
                          </p>
                        </div>
                        <div className="ml-4 flex-shrink-0">
                          <CalendarIcon className="h-5 w-5 text-gray-400" />
                        </div>
                      </div>
                    </div>
                  </Link>
                </li>
              ))
            ) : (
              <li className="px-6 py-8 text-center">
                <p className="text-sm text-gray-500">No upcoming sessions</p>
                <Link
                  to="/sessions?action=add"
                  className="mt-2 inline-block text-sm text-orange-600 hover:text-orange-700"
                >
                  Schedule a session
                </Link>
              </li>
            )}
          </ul>
          {upcomingSessions.length > 0 && (
            <div className="px-6 py-3 border-t border-gray-200">
              <Link
                to="/sessions"
                className="text-sm font-medium text-orange-600 hover:text-orange-700"
              >
                View all sessions →
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
