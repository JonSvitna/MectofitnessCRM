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

  // Onboarding, upgrade, referral, and auto-tagged clients
  const onboardingCard = (
    <div className="bg-white rounded-xl shadow p-6 mb-6 flex items-center justify-between">
      <div>
        <div className="text-xs font-bold text-blue-600 mb-1">LIVE Q&A</div>
        <h2 className="text-lg font-bold mb-2">Join a Live Getting Started Masterclass Session</h2>
        <p className="text-sm text-gray-600 mb-2">Get ready to master the essentials. We'll guide you through account setup, creating programs, and setting up new clients with ease.</p>
        <Link to="/register" className="bg-blue-500 text-white px-4 py-2 rounded font-semibold">REGISTER</Link>
      </div>
      <img src="/static/img/masterclass-phone.png" alt="Masterclass" className="h-24 hidden md:block" />
    </div>
  );

  const upgradeCTA = (
    <div className="bg-pink-100 rounded-xl shadow p-4 mb-6 flex items-center justify-between">
      <span className="font-bold text-pink-700">Your Free plan has limited client seats and features. Upgrade today to unlock more.</span>
      <Link to="/settings/billing" className="bg-pink-500 text-white px-4 py-2 rounded font-semibold">UPGRADE PLAN</Link>
    </div>
  );

  const referralCard = (
    <div className="bg-white rounded-xl shadow p-4 mb-6 flex items-center justify-between">
      <span>Share the love and your next month could be free! Invite other trainers to the platform and you can earn credits for your subscription.</span>
      <button className="bg-blue-100 text-blue-700 px-4 py-2 rounded font-semibold">EARN NOW</button>
    </div>
  );

  // Example dynamic tagging logic (replace with real API data)
  const needNewPhase = recentClients.filter(c => c.last_program_date && (Date.now() - new Date(c.last_program_date).getTime()) > 1000 * 60 * 60 * 24 * 30);
  const notMessagedLately = recentClients.filter(c => c.last_message_date && (Date.now() - new Date(c.last_message_date).getTime()) > 1000 * 60 * 60 * 24 * 14);

  const autoTaggedClients = (
    <div className="bg-white rounded-xl shadow p-4 mb-6">
      <div className="font-bold mb-2">We've auto-tagged your clients based on their needs.</div>
      <div className="flex gap-8">
        <div>
          <div className="flex items-center gap-2 mb-2"><span className="text-red-500">●</span> Need new training phases</div>
          <div className="flex gap-2">
            {needNewPhase.length === 0 && <span className="text-xs text-gray-400">All up to date!</span>}
            {needNewPhase.map(c => (
              <div key={c.id} className="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center font-bold text-gray-500" title={c.first_name + ' ' + c.last_name}>
                {c.first_name?.charAt(0)}
              </div>
            ))}
          </div>
        </div>
        <div>
          <div className="flex items-center gap-2 mb-2"><span className="text-orange-500">●</span> Not messaged lately</div>
          <div className="flex gap-2">
            {notMessagedLately.length === 0 && <span className="text-xs text-gray-400">All engaged!</span>}
            {notMessagedLately.map(c => (
              <div key={c.id} className="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center font-bold text-gray-500" title={c.first_name + ' ' + c.last_name}>
                {c.first_name?.charAt(0)}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  // Recent activities feed (mock data for now)
  const recentActivities = [
    { name: 'Tiffany Gosnell', activity: 'completed a 0.34 mile walk in 15m 49s.', date: '21 Oct 2025' },
    { name: 'Donavan Weston', activity: 'completed a functional strength training session in 44m 43s.', date: '16 Oct 2025' },
    { name: 'Donavan Weston', activity: 'completed a functional strength training session in 46m 39s.', date: '16 Oct 2025' },
    { name: 'Rob Walker', activity: 'completed Full Body - Lunges, Abs, & Accessories and rated it as RPE 9/10 (extremely hard). Rob set 1 new personal best and added 1 comment.', date: '12 Oct 2025' },
    { name: 'Donavan Weston', activity: 'completed a functional strength training session in 35m 50s.', date: '10 Oct 2025' },
    { name: 'Rob Walker', activity: 'completed Full Body - Deadlift & Pull and rated it as RPE 8/10 (really hard). Rob set 2 new personal bests and added 1 comment.', date: '3 Oct 2025' },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">
          Welcome back, {user?.full_name || 'Trainer'}
        </h1>
        <p className="text-sm text-gray-600 mt-1">
          Here's what's happening with your clients today
        </p>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4 mb-8">
        <div className="bg-white overflow-hidden shadow-sm border border-gray-100 rounded-xl">
          <div className="px-6 py-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="h-12 w-12 rounded-lg bg-primary-50 flex items-center justify-center">
                  <UsersIcon className="h-6 w-6 text-primary-600" />
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Total Clients
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats.totalClients}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow-sm border border-gray-100 rounded-xl">
          <div className="px-6 py-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="h-12 w-12 rounded-lg bg-success-50 flex items-center justify-center">
                  <CalendarIcon className="h-6 w-6 text-success-600" />
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Today's Sessions
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats.todaySessions}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow-sm border border-gray-100 rounded-xl">
          <div className="px-6 py-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="h-12 w-12 rounded-lg bg-warning-50 flex items-center justify-center">
                  <DocumentTextIcon className="h-6 w-6 text-warning-600" />
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Active Programs
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats.totalPrograms}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow-sm border border-gray-100 rounded-xl">
          <div className="px-6 py-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="h-12 w-12 rounded-lg bg-accent-50 flex items-center justify-center">
                  <ChartBarIcon className="h-6 w-6 text-accent-600" />
                </div>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Upcoming Sessions
                  </dt>
                  <dd className="text-2xl font-semibold text-gray-900">
                    {stats.upcomingSessions}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
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
