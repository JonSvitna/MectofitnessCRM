import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  ChartBarIcon,
  PlusIcon,
  CameraIcon,
  ScaleIcon,
  ArrowTrendingUpIcon,
  XCircleIcon,
} from '@heroicons/react/24/outline';
import { progressApi, handleApiError } from '../api/client';
import logger from '../utils/logger';

export default function Progress() {
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadProgressEntries();
  }, []);

  const loadProgressEntries = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await progressApi.getEntries({ limit: 50 });
      setEntries(response.data.entries || response.data || []);
    } catch (err) {
      logger.error('Error loading progress:', err);
      setError(handleApiError(err));
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin h-12 w-12 border-4 border-primary-200 border-t-primary-600 rounded-full mx-auto mb-4"></div>
          <p className="text-gray-600">Loading progress data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-center max-w-md mx-auto px-4">
          <XCircleIcon className="h-12 w-12 text-danger-600 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Error Loading Progress</h2>
          <p className="text-gray-600 mb-6">{error}</p>
          <button
            onClick={loadProgressEntries}
            className="bg-primary-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-primary-700 transition-colors"
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
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Progress Tracking</h1>
              <p className="mt-1 text-gray-600">
                Track client progress with measurements, photos, and milestones
              </p>
            </div>
            <Link
              to="?action=add"
              className="inline-flex items-center gap-2 bg-primary-600 text-white px-5 py-2.5 rounded-lg font-medium hover:bg-primary-700 transition-colors shadow-button hover:shadow-button-hover"
            >
              <PlusIcon className="h-5 w-5" />
              Add Progress Entry
            </Link>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-white rounded-lg border border-gray-200 p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Total Entries</p>
                  <p className="text-2xl font-bold text-gray-900">{entries.length}</p>
                </div>
                <div className="bg-primary-50 rounded-lg p-3">
                  <ChartBarIcon className="h-6 w-6 text-primary-600" />
                </div>
              </div>
            </div>
            <div className="bg-white rounded-lg border border-gray-200 p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Progress Photos</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {entries.filter((e) => e.has_photo).length || 0}
                  </p>
                </div>
                <div className="bg-accent-50 rounded-lg p-3">
                  <CameraIcon className="h-6 w-6 text-accent-600" />
                </div>
              </div>
            </div>
            <div className="bg-white rounded-lg border border-gray-200 p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Avg Progress</p>
                  <p className="text-2xl font-bold text-success-600">+12%</p>
                </div>
                <div className="bg-success-50 rounded-lg p-3">
                  <ArrowTrendingUpIcon className="h-6 w-6 text-success-600" />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Progress Entries */}
        {entries.length === 0 ? (
          <div className="bg-white rounded-lg border border-gray-200 p-12 text-center">
            <div className="bg-gray-100 rounded-full h-16 w-16 flex items-center justify-center mx-auto mb-4">
              <ChartBarIcon className="h-8 w-8 text-gray-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">No progress entries yet</h3>
            <p className="text-gray-600 mb-6">
              Start tracking client progress with measurements and photos
            </p>
            <Link
              to="?action=add"
              className="inline-flex items-center gap-2 bg-primary-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-primary-700 transition-colors"
            >
              <PlusIcon className="h-5 w-5" />
              Add Your First Entry
            </Link>
          </div>
        ) : (
          <div className="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-700 uppercase">Date</th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-700 uppercase">Client</th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-700 uppercase">Weight</th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-700 uppercase">Measurements</th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-700 uppercase">Photos</th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-700 uppercase">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {entries.map((entry) => (
                    <tr key={entry.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap font-medium text-gray-900">
                        {new Date(entry.date || entry.created_at).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="font-medium text-gray-900">{entry.client_name || 'Unknown'}</span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {entry.weight ? `${entry.weight} lbs` : '-'}
                      </td>
                      <td className="px-6 py-4">
                        <div className="text-sm text-gray-600">
                          {entry.chest && `Chest: ${entry.chest}"`}
                          {entry.waist && `, Waist: ${entry.waist}"`}
                          {!entry.chest && !entry.waist && '-'}
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        {entry.has_photo ? (
                          <span className="text-success-600 flex items-center gap-1">
                            <CameraIcon className="h-4 w-4" />
                            <span className="text-sm">Yes</span>
                          </span>
                        ) : (
                          <span className="text-gray-600 text-sm">No</span>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <Link
                          to={`/progress/${entry.id}`}
                          className="text-primary-600 hover:text-primary-700 font-medium text-sm"
                        >
                          View Details →
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
