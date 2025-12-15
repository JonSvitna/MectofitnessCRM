import { useEffect, useState } from 'react';
import {
  UserGroupIcon,
  PlusIcon,
  XCircleIcon,
} from '@heroicons/react/24/outline';
import { engagementApi, handleApiError } from '../api/client';
import logger from '../utils/logger';

export default function Groups() {
  const [groups, setGroups] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadGroups();
  }, []);

  const loadGroups = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await engagementApi.getGroups();
      setGroups(response.data.data?.groups || response.data.groups || []);
    } catch (err) {
      logger.error('Error loading groups:', err);
      setError(handleApiError(err));
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center bg-gray-50 dark:bg-black">
        <div className="text-center">
          <div className="animate-spin h-12 w-12 border-4 border-primary-200 dark:border-orange-500/20 border-t-primary-600 dark:border-t-orange-500 rounded-full mx-auto mb-4"></div>
          <p className="text-gray-700 dark:text-gray-300">Loading groups...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-full flex items-center justify-center bg-gray-50 dark:bg-black">
        <div className="text-center max-w-md mx-auto px-4">
          <XCircleIcon className="h-12 w-12 text-danger-600 dark:text-danger-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">Error Loading Groups</h2>
          <p className="text-gray-700 dark:text-gray-300 mb-6">{error}</p>
          <button
            onClick={loadGroups}
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
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Groups</h1>
              <p className="mt-1 text-gray-700 dark:text-gray-300">
                Create and manage client groups for class sessions and group training programs
              </p>
            </div>
            <button
              onClick={() => alert('Group creation functionality coming soon')}
              className="inline-flex items-center gap-2 bg-primary-600 dark:bg-orange-500 text-white px-5 py-2.5 rounded-lg font-medium hover:bg-primary-700 dark:hover:bg-orange-600 transition-colors shadow-button hover:shadow-button-hover"
            >
              <PlusIcon className="h-5 w-5" />
              Create Group
            </button>
          </div>
        </div>

        {groups.length === 0 ? (
          <div className="bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 p-12 text-center backdrop-blur-sm">
            <UserGroupIcon className="h-16 w-16 text-gray-600 dark:text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">No groups yet</h3>
            <p className="text-gray-700 dark:text-gray-300 mb-6">
              Create client groups to organize class sessions and group training programs
            </p>
            <p className="text-sm text-gray-600 dark:text-gray-400 bg-accent-50 dark:bg-blue-500/10 px-4 py-2 rounded-lg inline-block">
              This feature is under development
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {groups.map((group) => (
              <div
                key={group.id}
                className="bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 p-6 hover:shadow-card dark:hover:shadow-orange-500/10 transition-all backdrop-blur-sm"
              >
                <h3 className="font-semibold text-lg text-gray-900 dark:text-white mb-2">
                  {group.name || 'Untitled Group'}
                </h3>
                {group.description && (
                  <p className="text-sm text-gray-700 dark:text-gray-300 mb-4">
                    {group.description}
                  </p>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
