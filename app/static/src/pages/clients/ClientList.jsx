import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  UserPlusIcon,
  MagnifyingGlassIcon,
  FunnelIcon,
  ChartBarIcon,
  ClockIcon,
  CheckCircleIcon,
  XMarkIcon,
} from '@heroicons/react/24/outline';
import { clientsApi, handleApiError } from '../../api/client';
import logger from '../utils/logger';

export default function ClientList() {
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [stats, setStats] = useState(null);

  useEffect(() => {
    loadClients();
    loadStats();
  }, [filterStatus]);

  const loadClients = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const params = {};
      if (filterStatus !== 'all') {
        params.is_active = filterStatus === 'active';
      }
      
      const response = await clientsApi.getAll(params);
      setClients(response.data.clients || response.data || []);
    } catch (err) {
      logger.error('Error loading clients:', err);
      setError(handleApiError(err));
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const response = await clientsApi.getStats();
      setStats(response.data);
    } catch (err) {
      logger.error('Error loading stats:', err);
    }
  };

  const filteredClients = clients.filter((client) => {
    if (!searchTerm) return true;
    const search = searchTerm.toLowerCase();
    return (
      client.first_name?.toLowerCase().includes(search) ||
      client.last_name?.toLowerCase().includes(search) ||
      client.email?.toLowerCase().includes(search)
    );
  });

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin h-12 w-12 border-4 border-primary-200 border-t-primary-600 rounded-full mx-auto mb-4"></div>
          <p className="text-gray-600">Loading clients...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-center max-w-md mx-auto px-4">
          <XMarkIcon className="h-12 w-12 text-danger-600 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Error Loading Clients</h2>
          <p className="text-gray-600 mb-6">{error}</p>
          <button
            onClick={loadClients}
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
              <h1 className="text-3xl font-bold text-gray-900">Clients</h1>
              <p className="mt-1 text-gray-600">
                Manage your client relationships and track progress
              </p>
            </div>
            <Link
              to="?action=add"
              className="inline-flex items-center gap-2 bg-primary-600 text-white px-5 py-2.5 rounded-lg font-medium hover:bg-primary-700 transition-colors shadow-button hover:shadow-button-hover"
            >
              <UserPlusIcon className="h-5 w-5" />
              Add Client
            </Link>
          </div>

          {/* Stats Cards */}
          {stats && (
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
              <div className="bg-white rounded-lg border border-gray-200 p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Total Clients</p>
                    <p className="text-2xl font-bold text-gray-900">{stats.total || 0}</p>
                  </div>
                  <div className="bg-primary-50 rounded-lg p-3">
                    <ChartBarIcon className="h-6 w-6 text-primary-600" />
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
                    <p className="text-sm text-gray-600">This Month</p>
                    <p className="text-2xl font-bold text-accent-600">{stats.new_this_month || 0}</p>
                  </div>
                  <div className="bg-accent-50 rounded-lg p-3">
                    <ClockIcon className="h-6 w-6 text-accent-600" />
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-lg border border-gray-200 p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Avg Progress</p>
                    <p className="text-2xl font-bold text-primary-600">{stats.avg_progress || 0}%</p>
                  </div>
                  <div className="bg-primary-50 rounded-lg p-3">
                    <ChartBarIcon className="h-6 w-6 text-primary-600" />
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Search and Filters */}
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1 relative">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-600" />
              <input
                type="text"
                placeholder="Search clients by name or email..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              />
            </div>
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
                onClick={() => setFilterStatus('inactive')}
                className={`px-4 py-2.5 rounded-lg font-medium transition-colors ${
                  filterStatus === 'inactive'
                    ? 'bg-primary-600 text-white'
                    : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
                }`}
              >
                Inactive
              </button>
            </div>
          </div>
        </div>

        {/* Clients Grid */}
        {filteredClients.length === 0 ? (
          <div className="bg-white rounded-lg border border-gray-200 p-12 text-center">
            <div className="bg-gray-100 rounded-full h-16 w-16 flex items-center justify-center mx-auto mb-4">
              <UserPlusIcon className="h-8 w-8 text-gray-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">No clients found</h3>
            <p className="text-gray-600 mb-6">
              {searchTerm
                ? 'Try adjusting your search or filters'
                : 'Get started by adding your first client'}
            </p>
            {!searchTerm && (
              <Link
                to="?action=add"
                className="inline-flex items-center gap-2 bg-primary-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-primary-700 transition-colors"
              >
                <UserPlusIcon className="h-5 w-5" />
                Add Your First Client
              </Link>
            )}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredClients.map((client) => (
              <Link
                key={client.id}
                to={`/clients/${client.id}`}
                className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-card hover:border-primary-300 transition-all group"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="h-12 w-12 rounded-full bg-gradient-to-br from-primary-400 to-purple-400 flex items-center justify-center text-white font-semibold text-lg shadow-sm">
                      {client.first_name?.[0]}{client.last_name?.[0]}
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900 group-hover:text-primary-600 transition-colors">
                        {client.first_name} {client.last_name}
                      </h3>
                      <p className="text-sm text-gray-600">{client.email}</p>
                    </div>
                  </div>
                  <span
                    className={`px-2 py-1 text-xs font-medium rounded-full ${
                      client.is_active
                        ? 'bg-success-50 text-success-700'
                        : 'bg-gray-100 text-gray-700'
                    }`}
                  >
                    {client.is_active ? 'Active' : 'Inactive'}
                  </span>
                </div>
                
                <div className="space-y-2">
                  {client.fitness_goal && (
                    <div className="flex items-center text-sm text-gray-600">
                      <span className="font-medium mr-2">Goal:</span>
                      <span>{client.fitness_goal}</span>
                    </div>
                  )}
                  {client.program_count !== undefined && (
                    <div className="flex items-center text-sm text-gray-600">
                      <span className="font-medium mr-2">Programs:</span>
                      <span>{client.program_count || 0}</span>
                    </div>
                  )}
                  {client.session_count !== undefined && (
                    <div className="flex items-center text-sm text-gray-600">
                      <span className="font-medium mr-2">Sessions:</span>
                      <span>{client.session_count || 0}</span>
                    </div>
                  )}
                </div>

                {client.progress_percentage !== undefined && (
                  <div className="mt-4">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs font-medium text-gray-700">Progress</span>
                      <span className="text-xs font-bold text-primary-600">
                        {client.progress_percentage}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-primary-500 h-2 rounded-full transition-all"
                        style={{ width: `${client.progress_percentage}%` }}
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
