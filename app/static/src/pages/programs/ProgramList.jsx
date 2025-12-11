import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  PlusIcon,
  DocumentTextIcon,
  UserGroupIcon,
  ClockIcon,
  CheckCircleIcon,
  ArrowPathIcon,
  XCircleIcon,
} from '@heroicons/react/24/outline';
import { programsApi, handleApiError } from '../../api/client';

export default function ProgramList() {
  const [programs, setPrograms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filterStatus, setFilterStatus] = useState('all');
  const [stats, setStats] = useState(null);

  useEffect(() => {
    loadPrograms();
    loadStats();
  }, [filterStatus]);

  const loadPrograms = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const params = {};
      if (filterStatus !== 'all') {
        params.status = filterStatus;
      }
      
      const response = await programsApi.getAll(params);
      setPrograms(response.data.programs || response.data || []);
    } catch (err) {
      console.error('Error loading programs:', err);
      setError(handleApiError(err));
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const response = await programsApi.getStats();
      setStats(response.data);
    } catch (err) {
      console.error('Error loading stats:', err);
    }
  };

  const getStatusBadge = (status) => {
    const badges = {
      active: 'bg-success-50 text-success-700',
      completed: 'bg-primary-50 text-primary-700',
      paused: 'bg-accent-50 text-accent-700',
      draft: 'bg-gray-50 text-gray-700',
    };
    return badges[status] || 'bg-gray-50 text-gray-700';
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return 'N/A';
    return new Date(dateStr).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin h-12 w-12 border-4 border-primary-200 border-t-primary-600 rounded-full mx-auto mb-4"></div>
          <p className="text-gray-600">Loading programs...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-center max-w-md mx-auto px-4">
          <XCircleIcon className="h-12 w-12 text-danger-600 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Error Loading Programs</h2>
          <p className="text-gray-600 mb-6">{error}</p>
          <button
            onClick={loadPrograms}
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
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Programs</h1>
              <p className="mt-1 text-gray-600">
                Create and manage training programs with exercise integration
              </p>
            </div>
            <Link
              to="?action=add"
              className="inline-flex items-center gap-2 bg-primary-600 text-white px-5 py-2.5 rounded-lg font-medium hover:bg-primary-700 transition-colors shadow-button hover:shadow-button-hover"
            >
              <PlusIcon className="h-5 w-5" />
              Create Program
            </Link>
          </div>

          {/* Stats Cards */}
          {stats && (
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
              <div className="bg-white rounded-lg border border-gray-200 p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Total Programs</p>
                    <p className="text-2xl font-bold text-gray-900">{stats.total || 0}</p>
                  </div>
                  <div className="bg-primary-50 rounded-lg p-3">
                    <DocumentTextIcon className="h-6 w-6 text-primary-600" />
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-lg border border-gray-200 p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Active</p>
                    <p className="text-2xl font-bold text-success-600">{stats.active || 0}</p>
                  </div>
                  <div className="bg-success-50 rounded-lg p-3">
                    <CheckCircleIcon className="h-6 w-6 text-success-600" />
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-lg border border-gray-200 p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Clients Assigned</p>
                    <p className="text-2xl font-bold text-accent-600">{stats.clients_assigned || 0}</p>
                  </div>
                  <div className="bg-accent-50 rounded-lg p-3">
                    <UserGroupIcon className="h-6 w-6 text-accent-600" />
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-lg border border-gray-200 p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Avg Completion</p>
                    <p className="text-2xl font-bold text-primary-600">{stats.avg_completion || 0}%</p>
                  </div>
                  <div className="bg-primary-50 rounded-lg p-3">
                    <ArrowPathIcon className="h-6 w-6 text-primary-600" />
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Filters */}
          <div className="flex gap-2">
            <button
              onClick={() => setFilterStatus('all')}
              className={`px-4 py-2.5 rounded-lg font-medium transition-colors ${
                filterStatus === 'all'
                  ? 'bg-primary-600 text-white'
                  : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
              }`}
            >
              All
            </button>
            <button
              onClick={() => setFilterStatus('active')}
              className={`px-4 py-2.5 rounded-lg font-medium transition-colors ${
                filterStatus === 'active'
                  ? 'bg-primary-600 text-white'
                  : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
              }`}
            >
              Active
            </button>
            <button
              onClick={() => setFilterStatus('completed')}
              className={`px-4 py-2.5 rounded-lg font-medium transition-colors ${
                filterStatus === 'completed'
                  ? 'bg-primary-600 text-white'
                  : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
              }`}
            >
              Completed
            </button>
            <button
              onClick={() => setFilterStatus('draft')}
              className={`px-4 py-2.5 rounded-lg font-medium transition-colors ${
                filterStatus === 'draft'
                  ? 'bg-primary-600 text-white'
                  : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
              }`}
            >
              Draft
            </button>
          </div>
        </div>

        {/* Programs Grid */}
        {programs.length === 0 ? (
          <div className="bg-white rounded-lg border border-gray-200 p-12 text-center">
            <div className="bg-gray-100 rounded-full h-16 w-16 flex items-center justify-center mx-auto mb-4">
              <DocumentTextIcon className="h-8 w-8 text-gray-400" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">No programs found</h3>
            <p className="text-gray-600 mb-6">
              Get started by creating your first training program
            </p>
            <Link
              to="?action=add"
              className="inline-flex items-center gap-2 bg-primary-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-primary-700 transition-colors"
            >
              <PlusIcon className="h-5 w-5" />
              Create Your First Program
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {programs.map((program) => (
              <Link
                key={program.id}
                to={`/programs/${program.id}`}
                className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-card hover:border-primary-300 transition-all group"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <h3 className="font-semibold text-lg text-gray-900 group-hover:text-primary-600 transition-colors mb-1">
                      {program.name || 'Untitled Program'}
                    </h3>
                    {program.description && (
                      <p className="text-sm text-gray-600 line-clamp-2">{program.description}</p>
                    )}
                  </div>
                  <span
                    className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusBadge(
                      program.status
                    )}`}
                  >
                    {program.status?.toUpperCase() || 'DRAFT'}
                  </span>
                </div>

                <div className="space-y-3 mb-4">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-600">Exercises</span>
                    <span className="font-medium text-gray-900">
                      {program.exercise_count || 0}
                    </span>
                  </div>
                  
                  {program.client_name && (
                    <div className="flex items-center gap-2 text-sm">
                      <UserGroupIcon className="h-4 w-4 text-gray-400" />
                      <span className="text-gray-600">Assigned to:</span>
                      <span className="font-medium text-gray-900">{program.client_name}</span>
                    </div>
                  )}
                  
                  <div className="flex items-center gap-2 text-sm">
                    <ClockIcon className="h-4 w-4 text-gray-400" />
                    <span className="text-gray-600">
                      {program.duration_weeks
                        ? `${program.duration_weeks} weeks`
                        : 'Duration not set'}
                    </span>
                  </div>
                  
                  {program.start_date && (
                    <div className="text-sm text-gray-600">
                      Started: {formatDate(program.start_date)}
                    </div>
                  )}
                </div>

                {program.completion_percentage !== undefined && (
                  <div>
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs font-medium text-gray-700">Progress</span>
                      <span className="text-xs font-bold text-primary-600">
                        {program.completion_percentage}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-primary-500 h-2 rounded-full transition-all"
                        style={{ width: `${program.completion_percentage}%` }}
                      />
                    </div>
                  </div>
                )}
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
