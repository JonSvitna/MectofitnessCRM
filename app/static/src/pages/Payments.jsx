import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  PlusIcon,
  CurrencyDollarIcon,
  CreditCardIcon,
  CheckCircleIcon,
  ClockIcon,
  XCircleIcon,
} from '@heroicons/react/24/outline';
import { paymentsApi, handleApiError } from '../api/client';

export default function Payments() {
  const [transactions, setTransactions] = useState([]);
  const [subscriptions, setSubscriptions] = useState([]);
  const [revenue, setRevenue] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadPaymentData();
  }, []);

  const loadPaymentData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [txnRes, subRes, revRes] = await Promise.all([
        paymentsApi.getTransactions({ limit: 20 }),
        paymentsApi.getSubscriptions({ limit: 20 }),
        paymentsApi.getRevenue({}),
      ]);
      setTransactions(txnRes.data.transactions || txnRes.data || []);
      setSubscriptions(subRes.data.subscriptions || subRes.data || []);
      setRevenue(revRes.data);
    } catch (err) {
      console.error('Error loading payment data:', err);
      setError(handleApiError(err));
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount || 0);
  };

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin h-12 w-12 border-4 border-primary-200 border-t-primary-600 rounded-full mx-auto mb-4"></div>
          <p className="text-gray-600">Loading payment data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-center max-w-md mx-auto px-4">
          <XCircleIcon className="h-12 w-12 text-danger-600 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Error Loading Payments</h2>
          <p className="text-gray-600 mb-6">{error}</p>
          <button
            onClick={loadPaymentData}
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
              <h1 className="text-3xl font-bold text-gray-900">Payments & Subscriptions</h1>
              <p className="mt-1 text-gray-600">
                Manage payment plans, subscriptions, and track revenue
              </p>
            </div>
            <Link
              to="?action=add"
              className="inline-flex items-center gap-2 bg-primary-600 text-white px-5 py-2.5 rounded-lg font-medium hover:bg-primary-700 transition-colors shadow-button hover:shadow-button-hover"
            >
              <PlusIcon className="h-5 w-5" />
              Record Payment
            </Link>
          </div>

          {/* Revenue Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-white rounded-lg border border-gray-200 p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Monthly Revenue</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {formatCurrency(revenue?.monthly || 0)}
                  </p>
                </div>
                <div className="bg-success-50 rounded-lg p-3">
                  <CurrencyDollarIcon className="h-6 w-6 text-success-600" />
                </div>
              </div>
            </div>
            <div className="bg-white rounded-lg border border-gray-200 p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Total Revenue</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {formatCurrency(revenue?.total || 0)}
                  </p>
                </div>
                <div className="bg-primary-50 rounded-lg p-3">
                  <CurrencyDollarIcon className="h-6 w-6 text-primary-600" />
                </div>
              </div>
            </div>
            <div className="bg-white rounded-lg border border-gray-200 p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Active Subscriptions</p>
                  <p className="text-2xl font-bold text-success-600">
                    {subscriptions.filter((s) => s.status === 'active').length}
                  </p>
                </div>
                <div className="bg-success-50 rounded-lg p-3">
                  <CheckCircleIcon className="h-6 w-6 text-success-600" />
                </div>
              </div>
            </div>
            <div className="bg-white rounded-lg border border-gray-200 p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Pending Payments</p>
                  <p className="text-2xl font-bold text-accent-600">
                    {transactions.filter((t) => t.status === 'pending').length}
                  </p>
                </div>
                <div className="bg-accent-50 rounded-lg p-3">
                  <ClockIcon className="h-6 w-6 text-accent-600" />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Transactions */}
        <div className="bg-white rounded-lg border border-gray-200 shadow-sm mb-6">
          <div className="border-b border-gray-200 px-6 py-4 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900">Recent Transactions</h2>
            <Link to="/payments/all" className="text-sm text-primary-600 hover:text-primary-700 font-medium">
              View all →
            </Link>
          </div>
          
          {transactions.length === 0 ? (
            <div className="p-12 text-center">
              <CreditCardIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600">No transactions yet</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Date</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Client</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Amount</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Status</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Method</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {transactions.slice(0, 10).map((txn) => (
                    <tr key={txn.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {new Date(txn.created_at || txn.date).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap font-medium text-gray-900">
                        {txn.client_name || 'Unknown'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap font-semibold text-gray-900">
                        {formatCurrency(txn.amount)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span
                          className={`px-2 py-1 text-xs font-medium rounded-full ${
                            txn.status === 'completed'
                              ? 'bg-success-50 text-success-700'
                              : txn.status === 'pending'
                              ? 'bg-accent-50 text-accent-700'
                              : 'bg-danger-50 text-danger-700'
                          }`}
                        >
                          {txn.status?.toUpperCase()}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                        {txn.payment_method || 'N/A'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Active Subscriptions */}
        <div className="bg-white rounded-lg border border-gray-200 shadow-sm">
          <div className="border-b border-gray-200 px-6 py-4">
            <h2 className="text-lg font-semibold text-gray-900">Active Subscriptions</h2>
          </div>
          
          {subscriptions.filter((s) => s.status === 'active').length === 0 ? (
            <div className="p-12 text-center">
              <CreditCardIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600">No active subscriptions</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-6">
              {subscriptions
                .filter((s) => s.status === 'active')
                .map((sub) => (
                  <div key={sub.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="font-semibold text-gray-900">{sub.client_name || 'Unknown'}</h3>
                      <span className="px-2 py-1 bg-success-50 text-success-700 text-xs font-medium rounded">
                        ACTIVE
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 mb-2">{sub.plan_name || 'Standard Plan'}</p>
                    <p className="text-lg font-bold text-primary-600">
                      {formatCurrency(sub.amount)}/{sub.interval || 'month'}
                    </p>
                    {sub.next_billing_date && (
                      <p className="text-xs text-gray-500 mt-2">
                        Next billing: {new Date(sub.next_billing_date).toLocaleDateString()}
                      </p>
                    )}
                  </div>
                ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
