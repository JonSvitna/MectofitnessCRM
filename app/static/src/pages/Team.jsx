import { useEffect, useState } from 'react';
import {
  UserGroupIcon,
  PlusIcon,
  EnvelopeIcon,
  PhoneIcon,
  ShieldCheckIcon,
  UserIcon,
  XCircleIcon,
} from '@heroicons/react/24/outline';
import { organizationApi, handleApiError } from '../api/client';
import { useAuthStore } from '../store/authStore';
import logger from '../utils/logger';

export default function Team() {
  const { user } = useAuthStore();
  const [members, setMembers] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadTeamData();
  }, []);

  const loadTeamData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [membersRes, statsRes] = await Promise.all([
        organizationApi.getMembers(),
        organizationApi.getStats(),
      ]);
      setMembers(membersRes.data.members || membersRes.data || []);
      setStats(statsRes.data);
    } catch (err) {
      logger.error('Error loading team:', err);
      setError(handleApiError(err));
    } finally {
      setLoading(false);
    }
  };

  const getRoleBadge = (role) => {
    const badges = {
      owner: 'bg-purple-50 dark:bg-purple-500/10 text-purple-700 dark:text-purple-400',
      admin: 'bg-primary-50 dark:bg-orange-500/10 text-primary-700 dark:text-orange-400',
      trainer: 'bg-accent-50 dark:bg-blue-500/10 text-accent-700 dark:text-blue-400',
      client: 'bg-gray-50 dark:bg-white/5 text-gray-700 dark:text-gray-400',
    };
    return badges[role] || badges.client;
  };

  const getRoleIcon = (role) => {
    if (role === 'owner' || role === 'admin') {
      return <ShieldCheckIcon className="h-5 w-5" />;
    }
    return <UserIcon className="h-5 w-5" />;
  };

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center bg-gray-50 dark:bg-black">
        <div className="text-center">
          <div className="animate-spin h-12 w-12 border-4 border-primary-200 dark:border-orange-500/20 border-t-primary-600 dark:border-t-orange-500 rounded-full mx-auto mb-4"></div>
          <p className="text-gray-700 dark:text-gray-300">Loading team...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-full flex items-center justify-center bg-gray-50 dark:bg-black">
        <div className="text-center max-w-md mx-auto px-4">
          <XCircleIcon className="h-12 w-12 text-danger-600 dark:text-danger-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">Error Loading Team</h2>
          <p className="text-gray-700 dark:text-gray-300 mb-6">{error}</p>
          <button
            onClick={loadTeamData}
            className="bg-primary-600 dark:bg-orange-500 text-white px-6 py-3 rounded-lg font-medium hover:bg-primary-700 dark:hover:bg-orange-600 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full bg-gray-50 dark:bg-black">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Team Members</h1>
              <p className="mt-1 text-gray-700 dark:text-gray-300">
                Manage your organization's trainers and staff
              </p>
            </div>
            {(user?.role === 'owner' || user?.role === 'admin') && (
              <button
                onClick={() => alert('Invite member functionality coming soon')}
                className="inline-flex items-center gap-2 bg-primary-600 dark:bg-orange-500 text-white px-5 py-2.5 rounded-lg font-medium hover:bg-primary-700 dark:hover:bg-orange-600 transition-colors shadow-button hover:shadow-button-hover"
              >
                <PlusIcon className="h-5 w-5" />
                Invite Member
              </button>
            )}
          </div>

          {/* Stats Cards */}
          {stats && (
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
              <div className="bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 p-4 backdrop-blur-sm">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-700 dark:text-gray-400">Total Members</p>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">{members.length}</p>
                  </div>
                  <div className="bg-primary-50 dark:bg-orange-500/10 rounded-lg p-3">
                    <UserGroupIcon className="h-6 w-6 text-primary-600 dark:text-orange-500" />
                  </div>
                </div>
              </div>
              
              <div className="bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 p-4 backdrop-blur-sm">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-700 dark:text-gray-400">Active Trainers</p>
                    <p className="text-2xl font-bold text-success-600 dark:text-green-400">
                      {members.filter((m) => m.role === 'trainer' && m.is_active).length}
                    </p>
                  </div>
                  <div className="bg-success-50 dark:bg-green-500/10 rounded-lg p-3">
                    <UserIcon className="h-6 w-6 text-success-600 dark:text-green-400" />
                  </div>
                </div>
              </div>
              
              <div className="bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 p-4 backdrop-blur-sm">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-700 dark:text-gray-400">Total Clients</p>
                    <p className="text-2xl font-bold text-accent-600 dark:text-blue-400">
                      {stats.total_clients || 0}
                    </p>
                  </div>
                  <div className="bg-accent-50 dark:bg-blue-500/10 rounded-lg p-3">
                    <UserGroupIcon className="h-6 w-6 text-accent-600 dark:text-blue-400" />
                  </div>
                </div>
              </div>
              
              <div className="bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 p-4 backdrop-blur-sm">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-700 dark:text-gray-400">Active Programs</p>
                    <p className="text-2xl font-bold text-primary-600 dark:text-orange-400">
                      {stats.active_programs || 0}
                    </p>
                  </div>
                  <div className="bg-primary-50 dark:bg-orange-500/10 rounded-lg p-3">
                    <ShieldCheckIcon className="h-6 w-6 text-primary-600 dark:text-orange-500" />
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Team Members Grid */}
        {members.length === 0 ? (
          <div className="bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 p-12 text-center backdrop-blur-sm">
            <div className="bg-gray-100 dark:bg-white/5 rounded-full h-16 w-16 flex items-center justify-center mx-auto mb-4">
              <UserGroupIcon className="h-8 w-8 text-gray-600 dark:text-gray-400" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">No team members yet</h3>
            <p className="text-gray-700 dark:text-gray-300 mb-6">
              Get started by inviting trainers to your organization
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {members.map((member) => (
              <div
                key={member.id}
                className="bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 p-6 hover:shadow-card dark:hover:shadow-orange-500/10 transition-all backdrop-blur-sm"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="h-12 w-12 rounded-full bg-gradient-to-br from-primary-400 to-purple-400 dark:from-orange-500 dark:to-purple-500 flex items-center justify-center text-white font-semibold text-lg shadow-sm">
                      {member.first_name?.[0] || member.username?.[0] || 'U'}
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900 dark:text-white">
                        {member.full_name || member.username}
                      </h3>
                      <span
                        className={`inline-flex items-center gap-1 px-2 py-1 text-xs font-medium rounded-full ${getRoleBadge(
                          member.role
                        )}`}
                      >
                        {getRoleIcon(member.role)}
                        {member.role?.toUpperCase()}
                      </span>
                    </div>
                  </div>
                  <span
                    className={`px-2 py-1 text-xs font-medium rounded-full ${
                      member.is_active
                        ? 'bg-success-50 dark:bg-green-500/10 text-success-700 dark:text-green-400'
                        : 'bg-gray-100 dark:bg-white/5 text-gray-700 dark:text-gray-400'
                    }`}
                  >
                    {member.is_active ? 'Active' : 'Inactive'}
                  </span>
                </div>

                <div className="space-y-2">
                  {member.email && (
                    <div className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300">
                      <EnvelopeIcon className="h-4 w-4 text-gray-600 dark:text-gray-400" />
                      <span className="truncate">{member.email}</span>
                    </div>
                  )}
                  {member.phone && (
                    <div className="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-300">
                      <PhoneIcon className="h-4 w-4 text-gray-600 dark:text-gray-400" />
                      <span>{member.phone}</span>
                    </div>
                  )}
                  {member.specialization && (
                    <div className="text-sm text-gray-700 dark:text-gray-300 mt-2">
                      <span className="font-medium">Specialization:</span> {member.specialization}
                    </div>
                  )}
                  {member.created_at && (
                    <div className="text-xs text-gray-600 dark:text-gray-400 mt-2">
                      Joined {new Date(member.created_at).toLocaleDateString('en-US', {
                        month: 'short',
                        year: 'numeric',
                      })}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
