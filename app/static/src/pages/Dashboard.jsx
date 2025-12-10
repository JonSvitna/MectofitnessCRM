import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import {
  UsersIcon,
  CalendarIcon,
  DocumentTextIcon,
  ChartBarIcon,
  PlusIcon,
  FireIcon,
  TrophyIcon,
  BoltIcon,
} from '@heroicons/react/24/outline';
import { clientsApi, sessionsApi, programsApi } from '../api/client';

// Trainerize/TrueCoach-style Professional Dashboard
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

  // Mock user level/gamification data
  const userLevel = 5;
  const userXP = 750;
  const nextLevelXP = 1000;
  const streak = 7;

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
        { name: 'Tiffany Gosnell', activity: 'completed a 0.34 mile walk', time: '15m 49s', date: '21 Oct 2025', avatar: 'TG' },
        { name: 'Donavan Weston', activity: 'completed functional strength training', time: '44m 43s', date: '16 Oct 2025', avatar: 'DW' },
        { name: 'Rob Walker', activity: 'set 1 new PR in Full Body workout', time: '', date: '12 Oct 2025', avatar: 'RW' },
      ]);
    } catch (error) {
      console.error('Error loading dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const progressPercent = (userXP / nextLevelXP) * 100;

  return (
    <div className="h-full flex flex-col bg-gray-50">
      {/* Welcome Header with Gamification */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-8 shadow-lg">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold mb-1">Welcome Back, {user?.first_name || 'Trainer'}! 💪</h1>
              <p className="text-blue-100">Let's crush today's training goals</p>
            </div>
            <div className="flex items-center gap-4">
              {/* Streak Badge */}
              <div className="bg-white/20 backdrop-blur-sm rounded-xl px-4 py-3 flex items-center gap-2">
                <FireIcon className="h-6 w-6 text-orange-300" />
                <div>
                  <div className="text-2xl font-bold">{streak}</div>
                  <div className="text-xs text-blue-100">Day Streak</div>
                </div>
              </div>
              {/* Level Badge */}
              <div className="bg-white/20 backdrop-blur-sm rounded-xl px-4 py-3 flex items-center gap-2">
                <TrophyIcon className="h-6 w-6 text-yellow-300" />
                <div>
                  <div className="text-2xl font-bold">Level {userLevel}</div>
                  <div className="text-xs text-blue-100">{userXP}/{nextLevelXP} XP</div>
                </div>
              </div>
            </div>
          </div>

          {/* Progress to Next Level */}
          <div className="bg-white/10 backdrop-blur-sm rounded-full h-3 overflow-hidden">
            <div
              className="bg-gradient-to-r from-green-400 to-blue-400 h-full transition-all duration-500 flex items-center justify-end pr-2"
              style={{ width: `${progressPercent}%` }}
            >
              <span className="text-xs font-bold text-white">{Math.round(progressPercent)}%</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Dashboard Content */}
      <div className="flex-1 overflow-auto">
        <div className="max-w-7xl mx-auto px-6 py-8">

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between mb-3">
                <div className="bg-blue-50 rounded-lg p-3">
                  <UsersIcon className="h-6 w-6 text-blue-600" />
                </div>
                <div className="text-right">
                  <div className="text-3xl font-bold text-gray-900">{stats.totalClients}</div>
                  <div className="text-sm text-gray-500 mt-1">Active Clients</div>
                </div>
              </div>
              <div className="flex items-center text-sm">
                <span className="text-green-600 font-semibold">+{stats.activeThisWeek}</span>
                <span className="text-gray-500 ml-1">active this week</span>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between mb-3">
                <div className="bg-teal-50 rounded-lg p-3">
                  <CalendarIcon className="h-6 w-6 text-teal-600" />
                </div>
                <div className="text-right">
                  <div className="text-3xl font-bold text-gray-900">{stats.todaySessions}</div>
                  <div className="text-sm text-gray-500 mt-1">Today's Sessions</div>
                </div>
              </div>
              <div className="flex items-center text-sm">
                <span className="text-blue-600 font-semibold">{stats.upcomingSessions}</span>
                <span className="text-gray-500 ml-1">upcoming</span>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between mb-3">
                <div className="bg-purple-50 rounded-lg p-3">
                  <DocumentTextIcon className="h-6 w-6 text-purple-600" />
                </div>
                <div className="text-right">
                  <div className="text-3xl font-bold text-gray-900">{stats.totalPrograms}</div>
                  <div className="text-sm text-gray-500 mt-1">Active Programs</div>
                </div>
              </div>
              <div className="flex items-center text-sm">
                <span className="text-purple-600 font-semibold">Manage</span>
                <span className="text-gray-500 ml-1">your workouts</span>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
              <div className="flex items-center justify-between mb-3">
                <div className="bg-orange-50 rounded-lg p-3">
                  <ChartBarIcon className="h-6 w-6 text-orange-600" />
                </div>
                <div className="text-right">
                  <div className="text-3xl font-bold text-gray-900">{stats.completionRate}%</div>
                  <div className="text-sm text-gray-500 mt-1">Completion Rate</div>
                </div>
              </div>
              <div className="flex items-center text-sm">
                <BoltIcon className="h-4 w-4 text-orange-500 mr-1" />
                <span className="text-orange-600 font-semibold">Excellent!</span>
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
            <h2 className="text-lg font-bold text-gray-900 mb-4">Quick Actions</h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <Link
                to="/clients?action=add"
                className="flex items-center justify-center gap-3 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg px-6 py-4 font-semibold hover:from-blue-700 hover:to-blue-800 transition-all shadow-md hover:shadow-lg"
              >
                <PlusIcon className="h-5 w-5" />
                Add Client
              </Link>
              <Link
                to="/sessions?action=add"
                className="flex items-center justify-center gap-3 bg-gradient-to-r from-teal-600 to-teal-700 text-white rounded-lg px-6 py-4 font-semibold hover:from-teal-700 hover:to-teal-800 transition-all shadow-md hover:shadow-lg"
              >
                <CalendarIcon className="h-5 w-5" />
                Schedule Session
              </Link>
              <Link
                to="/programs?action=add"
                className="flex items-center justify-center gap-3 bg-gradient-to-r from-purple-600 to-purple-700 text-white rounded-lg px-6 py-4 font-semibold hover:from-purple-700 hover:to-purple-800 transition-all shadow-md hover:shadow-lg"
              >
                <DocumentTextIcon className="h-5 w-5" />
                Create Program
              </Link>
              <Link
                to="/exercise-library"
                className="flex items-center justify-center gap-3 bg-gradient-to-r from-orange-600 to-orange-700 text-white rounded-lg px-6 py-4 font-semibold hover:from-orange-700 hover:to-orange-800 transition-all shadow-md hover:shadow-lg"
              >
                <BoltIcon className="h-5 w-5" />
                Exercise Library
              </Link>
            </div>
          </div>

          {/* Two Column Layout */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

            {/* Left Column - Recent Clients & Upcoming Sessions */}
            <div className="lg:col-span-2 space-y-8">

              {/* Recent Clients */}
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-lg font-bold text-gray-900">Recent Clients</h2>
                  <Link to="/clients" className="text-sm text-blue-600 hover:text-blue-700 font-semibold">
                    View All →
                  </Link>
                </div>

                {loading ? (
                  <div className="text-center py-8 text-gray-500">Loading...</div>
                ) : recentClients.length === 0 ? (
                  <div className="text-center py-12">
                    <UsersIcon className="h-12 w-12 text-gray-300 mx-auto mb-3" />
                    <p className="text-gray-500 mb-4">No clients yet</p>
                    <Link
                      to="/clients?action=add"
                      className="inline-flex items-center text-blue-600 hover:text-blue-700 font-semibold"
                    >
                      <PlusIcon className="h-5 w-5 mr-1" />
                      Add your first client
                    </Link>
                  </div>
                ) : (
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    {recentClients.map((client) => (
                      <Link
                        key={client.id}
                        to={`/clients/${client.id}`}
                        className="group bg-gray-50 rounded-lg p-4 hover:bg-blue-50 hover:shadow-md transition-all border border-transparent hover:border-blue-200"
                      >
                        <div className="flex flex-col items-center text-center">
                          <div className="h-16 w-16 rounded-full bg-gradient-to-br from-blue-500 to-teal-500 flex items-center justify-center text-white font-bold text-xl mb-3 shadow-md group-hover:scale-110 transition-transform">
                            {client.first_name?.charAt(0) || 'C'}
                          </div>
                          <div className="font-semibold text-gray-900 mb-1">
                            {client.first_name} {client.last_name}
                          </div>
                          <div className="text-xs text-gray-500">{client.fitness_goal || 'General Fitness'}</div>
                        </div>
                      </Link>
                    ))}
                  </div>
                )}
              </div>

              {/* Upcoming Sessions */}
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-lg font-bold text-gray-900">Upcoming Sessions</h2>
                  <Link to="/sessions" className="text-sm text-blue-600 hover:text-blue-700 font-semibold">
                    View All →
                  </Link>
                </div>

                {loading ? (
                  <div className="text-center py-8 text-gray-500">Loading...</div>
                ) : upcomingSessions.length === 0 ? (
                  <div className="text-center py-12">
                    <CalendarIcon className="h-12 w-12 text-gray-300 mx-auto mb-3" />
                    <p className="text-gray-500 mb-4">No upcoming sessions</p>
                    <Link
                      to="/sessions?action=add"
                      className="inline-flex items-center text-blue-600 hover:text-blue-700 font-semibold"
                    >
                      <PlusIcon className="h-5 w-5 mr-1" />
                      Schedule a session
                    </Link>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {upcomingSessions.map((session) => (
                      <Link
                        key={session.id}
                        to={`/sessions/${session.id}`}
                        className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-teal-50 hover:shadow-md transition-all border border-transparent hover:border-teal-200"
                      >
                        <div className="flex items-center gap-4">
                          <div className="bg-teal-100 rounded-lg p-3">
                            <CalendarIcon className="h-6 w-6 text-teal-600" />
                          </div>
                          <div>
                            <div className="font-semibold text-gray-900">{session.title || 'Training Session'}</div>
                            <div className="text-sm text-gray-500">{session.client?.full_name}</div>
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="text-sm font-medium text-gray-700">
                            {new Date(session.scheduled_start).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                          </div>
                          <div className="text-xs text-gray-500">
                            {new Date(session.scheduled_start).toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })}
                          </div>
                        </div>
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Right Column - Recent Activity Feed */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 sticky top-4">
                <h2 className="text-lg font-bold text-gray-900 mb-6">Recent Activity</h2>

                {recentActivities.length === 0 ? (
                  <div className="text-center py-12 text-gray-500">
                    <ChartBarIcon className="h-12 w-12 text-gray-300 mx-auto mb-3" />
                    <p>No recent activity</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {recentActivities.map((activity, idx) => (
                      <div key={idx} className="flex items-start gap-3 pb-4 border-b border-gray-100 last:border-0">
                        <div className="h-10 w-10 rounded-full bg-gradient-to-br from-orange-400 to-pink-400 flex items-center justify-center text-white font-bold text-sm flex-shrink-0 shadow-sm">
                          {activity.avatar}
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="font-semibold text-gray-900 text-sm">{activity.name}</div>
                          <div className="text-sm text-gray-600 mt-1">{activity.activity}</div>
                          {activity.time && (
                            <div className="text-xs text-teal-600 font-semibold mt-1">{activity.time}</div>
                          )}
                          <div className="text-xs text-gray-400 mt-1">{activity.date}</div>
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
