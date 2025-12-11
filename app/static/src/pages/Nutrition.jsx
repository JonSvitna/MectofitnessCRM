import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  PlusIcon,
  DocumentTextIcon,
  ClipboardDocumentListIcon,
  XCircleIcon,
} from '@heroicons/react/24/outline';
import { nutritionApi, handleApiError } from '../api/client';

export default function Nutrition() {
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadNutritionPlans();
  }, []);

  const loadNutritionPlans = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await nutritionApi.getPlans({ limit: 50 });
      setPlans(response.data.plans || response.data || []);
    } catch (err) {
      console.error('Error loading nutrition plans:', err);
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
          <p className="text-gray-600">Loading nutrition plans...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-center max-w-md mx-auto px-4">
          <XCircleIcon className="h-12 w-12 text-danger-600 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Error Loading Nutrition Plans</h2>
          <p className="text-gray-600 mb-6">{error}</p>
          <button
            onClick={loadNutritionPlans}
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
              <h1 className="text-3xl font-bold text-gray-900">Nutrition Management</h1>
              <p className="mt-1 text-gray-600">
                Create and manage nutrition plans and food logs for clients
              </p>
            </div>
            <Link
              to="?action=add"
              className="inline-flex items-center gap-2 bg-primary-600 text-white px-5 py-2.5 rounded-lg font-medium hover:bg-primary-700 transition-colors shadow-button hover:shadow-button-hover"
            >
              <PlusIcon className="h-5 w-5" />
              Create Plan
            </Link>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-white rounded-lg border border-gray-200 p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Total Plans</p>
                  <p className="text-2xl font-bold text-gray-900">{plans.length}</p>
                </div>
                <div className="bg-primary-50 rounded-lg p-3">
                  <DocumentTextIcon className="h-6 w-6 text-primary-600" />
                </div>
              </div>
            </div>
            <div className="bg-white rounded-lg border border-gray-200 p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Active Plans</p>
                  <p className="text-2xl font-bold text-success-600">
                    {plans.filter((p) => p.status === 'active').length}
                  </p>
                </div>
                <div className="bg-success-50 rounded-lg p-3">
                  <DocumentTextIcon className="h-6 w-6 text-success-600" />
                </div>
              </div>
            </div>
            <div className="bg-white rounded-lg border border-gray-200 p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Food Logs</p>
                  <p className="text-2xl font-bold text-accent-600">0</p>
                </div>
                <div className="bg-accent-50 rounded-lg p-3">
                  <ClipboardDocumentListIcon className="h-6 w-6 text-accent-600" />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Plans List */}
        {plans.length === 0 ? (
          <div className="bg-white rounded-lg border border-gray-200 p-12 text-center">
            <div className="bg-gray-100 rounded-full h-16 w-16 flex items-center justify-center mx-auto mb-4">
              <DocumentTextIcon className="h-8 w-8 text-gray-400" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">No nutrition plans yet</h3>
            <p className="text-gray-600 mb-6">
              Create nutrition plans to help clients reach their goals
            </p>
            <Link
              to="?action=add"
              className="inline-flex items-center gap-2 bg-primary-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-primary-700 transition-colors"
            >
              <PlusIcon className="h-5 w-5" />
              Create Your First Plan
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {plans.map((plan) => (
              <Link
                key={plan.id}
                to={`/nutrition/${plan.id}`}
                className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-card hover:border-primary-300 transition-all group"
              >
                <div className="flex items-start justify-between mb-4">
                  <h3 className="font-semibold text-lg text-gray-900 group-hover:text-primary-600 transition-colors">
                    {plan.name || 'Untitled Plan'}
                  </h3>
                  <span
                    className={`px-2 py-1 text-xs font-medium rounded-full ${
                      plan.status === 'active'
                        ? 'bg-success-50 text-success-700'
                        : 'bg-gray-50 text-gray-700'
                    }`}
                  >
                    {plan.status?.toUpperCase() || 'DRAFT'}
                  </span>
                </div>

                <div className="space-y-2 text-sm text-gray-600">
                  {plan.client_name && (
                    <div>Client: <span className="font-medium text-gray-900">{plan.client_name}</span></div>
                  )}
                  {plan.calories && (
                    <div>Calories: <span className="font-medium text-gray-900">{plan.calories} kcal/day</span></div>
                  )}
                  {plan.macros && (
                    <div>Macros: <span className="font-medium text-gray-900">{plan.macros}</span></div>
                  )}
                </div>

                <div className="mt-4 pt-4 border-t border-gray-200">
                  <span className="text-primary-600 hover:text-primary-700 font-medium text-sm">
                    View Details →
                  </span>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
