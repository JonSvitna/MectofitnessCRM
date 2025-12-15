import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  CalendarDaysIcon,
  PlusIcon,
  ClockIcon,
  CheckCircleIcon,
  XCircleIcon,
  UserIcon,
} from '@heroicons/react/24/outline';
import { bookingApi, handleApiError } from '../api/client';
import logger from '../utils/logger';

export default function Scheduling() {
  const [bookings, setBookings] = useState([]);
  const [availability, setAvailability] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [view, setView] = useState('bookings'); // 'bookings' or 'availability'

  useEffect(() => {
    loadSchedulingData();
  }, [view]);

  const loadSchedulingData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      if (view === 'bookings') {
        const response = await bookingApi.getBookings({ limit: 50 });
        setBookings(response.data.bookings || response.data || []);
      } else {
        const response = await bookingApi.getAvailability({ limit: 50 });
        setAvailability(response.data.availability || response.data || []);
      }
    } catch (err) {
      logger.error('Error loading scheduling data:', err);
      setError(handleApiError(err));
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const badges = {
      pending: 'bg-accent-50 dark:bg-blue-500/10 text-accent-700 dark:text-blue-400',
      confirmed: 'bg-success-50 dark:bg-green-500/10 text-success-700 dark:text-green-400',
      cancelled: 'bg-danger-50 dark:bg-danger-500/10 text-danger-700 dark:text-danger-400',
      completed: 'bg-gray-50 dark:bg-white/5 text-gray-700 dark:text-gray-400',
    };
    return badges[status] || badges.pending;
  };

  const formatDateTime = (dateStr) => {
    const date = new Date(dateStr);
    return {
      date: date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
      time: date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' }),
    };
  };

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center bg-gray-50 dark:bg-black">
        <div className="text-center">
          <div className="animate-spin h-12 w-12 border-4 border-primary-200 dark:border-orange-500/20 border-t-primary-600 dark:border-t-orange-500 rounded-full mx-auto mb-4"></div>
          <p className="text-gray-700 dark:text-gray-300">Loading schedule...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-full flex items-center justify-center bg-gray-50 dark:bg-black">
        <div className="text-center max-w-md mx-auto px-4">
          <XCircleIcon className="h-12 w-12 text-danger-600 dark:text-danger-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">Error Loading Schedule</h2>
          <p className="text-gray-700 dark:text-gray-300 mb-6">{error}</p>
          <button
            onClick={loadSchedulingData}
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
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Scheduling</h1>
              <p className="mt-1 text-gray-700 dark:text-gray-300">
                Manage your availability and client bookings
              </p>
            </div>
            <div className="flex gap-3">
              <button
                onClick={() => alert('Set availability functionality coming soon')}
                className="inline-flex items-center gap-2 bg-white dark:bg-white/5 text-gray-700 dark:text-gray-300 px-5 py-2.5 rounded-lg font-medium hover:bg-gray-50 dark:hover:bg-white/10 transition-colors border border-gray-300 dark:border-white/10"
              >
                <ClockIcon className="h-5 w-5" />
                Set Availability
              </button>
              <Link
                to="/sessions?action=add"
                className="inline-flex items-center gap-2 bg-primary-600 dark:bg-orange-500 text-white px-5 py-2.5 rounded-lg font-medium hover:bg-primary-700 dark:hover:bg-orange-600 transition-colors shadow-button hover:shadow-button-hover"
              >
                <PlusIcon className="h-5 w-5" />
                New Booking
              </Link>
            </div>
          </div>

          {/* View Toggle */}
          <div className="flex gap-2 mb-6">
            <button
              onClick={() => setView('bookings')}
              className={`px-4 py-2.5 rounded-lg font-medium transition-colors ${
                view === 'bookings'
                  ? 'bg-primary-600 dark:bg-orange-500 text-white'
                  : 'bg-white dark:bg-white/5 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-white/10 hover:bg-gray-50 dark:hover:bg-white/10'
              }`}
            >
              Bookings
            </button>
            <button
              onClick={() => setView('availability')}
              className={`px-4 py-2.5 rounded-lg font-medium transition-colors ${
                view === 'availability'
                  ? 'bg-primary-600 dark:bg-orange-500 text-white'
                  : 'bg-white dark:bg-white/5 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-white/10 hover:bg-gray-50 dark:hover:bg-white/10'
              }`}
            >
              Availability
            </button>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 p-4 backdrop-blur-sm">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-700 dark:text-gray-400">Total Bookings</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">{bookings.length}</p>
                </div>
                <div className="bg-primary-50 dark:bg-orange-500/10 rounded-lg p-3">
                  <CalendarDaysIcon className="h-6 w-6 text-primary-600 dark:text-orange-500" />
                </div>
              </div>
            </div>
            
            <div className="bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 p-4 backdrop-blur-sm">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-700 dark:text-gray-400">Confirmed</p>
                  <p className="text-2xl font-bold text-success-600 dark:text-green-400">
                    {bookings.filter((b) => b.status === 'confirmed').length}
                  </p>
                </div>
                <div className="bg-success-50 dark:bg-green-500/10 rounded-lg p-3">
                  <CheckCircleIcon className="h-6 w-6 text-success-600 dark:text-green-400" />
                </div>
              </div>
            </div>
            
            <div className="bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 p-4 backdrop-blur-sm">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-700 dark:text-gray-400">Pending</p>
                  <p className="text-2xl font-bold text-accent-600 dark:text-blue-400">
                    {bookings.filter((b) => b.status === 'pending').length}
                  </p>
                </div>
                <div className="bg-accent-50 dark:bg-blue-500/10 rounded-lg p-3">
                  <ClockIcon className="h-6 w-6 text-accent-600 dark:text-blue-400" />
                </div>
              </div>
            </div>
            
            <div className="bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 p-4 backdrop-blur-sm">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-700 dark:text-gray-400">Available Slots</p>
                  <p className="text-2xl font-bold text-primary-600 dark:text-orange-400">
                    {availability.length}
                  </p>
                </div>
                <div className="bg-primary-50 dark:bg-orange-500/10 rounded-lg p-3">
                  <ClockIcon className="h-6 w-6 text-primary-600 dark:text-orange-500" />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Content based on view */}
        {view === 'bookings' ? (
          bookings.length === 0 ? (
            <div className="bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 p-12 text-center backdrop-blur-sm">
              <div className="bg-gray-100 dark:bg-white/5 rounded-full h-16 w-16 flex items-center justify-center mx-auto mb-4">
                <CalendarDaysIcon className="h-8 w-8 text-gray-600 dark:text-gray-400" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">No bookings yet</h3>
              <p className="text-gray-700 dark:text-gray-300 mb-6">
                Your clients can book sessions through your availability
              </p>
              <button
                onClick={() => setView('availability')}
                className="inline-flex items-center gap-2 bg-primary-600 dark:bg-orange-500 text-white px-6 py-3 rounded-lg font-medium hover:bg-primary-700 dark:hover:bg-orange-600 transition-colors"
              >
                <ClockIcon className="h-5 w-5" />
                Set Your Availability
              </button>
            </div>
          ) : (
            <div className="bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 shadow-sm overflow-hidden backdrop-blur-sm">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50 dark:bg-white/5 border-b border-gray-200 dark:border-white/10">
                    <tr>
                      <th className="px-6 py-4 text-left text-xs font-medium text-gray-700 dark:text-gray-400 uppercase tracking-wider">
                        Date & Time
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-medium text-gray-700 dark:text-gray-400 uppercase tracking-wider">
                        Client
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-medium text-gray-700 dark:text-gray-400 uppercase tracking-wider">
                        Service
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-medium text-gray-700 dark:text-gray-400 uppercase tracking-wider">
                        Status
                      </th>
                      <th className="px-6 py-4 text-left text-xs font-medium text-gray-700 dark:text-gray-400 uppercase tracking-wider">
                        Actions
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200 dark:divide-white/10">
                    {bookings.map((booking) => {
                      const { date, time } = formatDateTime(booking.start_time || booking.date);
                      return (
                        <tr key={booking.id} className="hover:bg-gray-50 dark:hover:bg-white/5 transition-colors">
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div>
                              <div className="font-medium text-gray-900 dark:text-white">{date}</div>
                              <div className="text-sm text-gray-700 dark:text-gray-400">{time}</div>
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="flex items-center gap-2">
                              <div className="h-8 w-8 rounded-full bg-gradient-to-br from-primary-400 to-purple-400 dark:from-orange-500 dark:to-purple-500 flex items-center justify-center text-white text-sm font-semibold">
                                {booking.client_name?.[0] || 'C'}
                              </div>
                              <span className="font-medium text-gray-900 dark:text-white">
                                {booking.client_name || 'Unknown'}
                              </span>
                            </div>
                          </td>
                          <td className="px-6 py-4 text-gray-900 dark:text-white">
                            {booking.service_name || booking.title || 'Training Session'}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span
                              className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusBadge(
                                booking.status
                              )}`}
                            >
                              {booking.status?.toUpperCase() || 'PENDING'}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <button className="text-primary-600 dark:text-orange-500 hover:text-primary-700 dark:hover:text-orange-400 font-medium text-sm">
                              View Details
                            </button>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          )
        ) : (
          // Availability View
          availability.length === 0 ? (
            <div className="bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 p-12 text-center backdrop-blur-sm">
              <div className="bg-gray-100 dark:bg-white/5 rounded-full h-16 w-16 flex items-center justify-center mx-auto mb-4">
                <ClockIcon className="h-8 w-8 text-gray-600 dark:text-gray-400" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">No availability set</h3>
              <p className="text-gray-700 dark:text-gray-300 mb-6">
                Set your availability so clients can book sessions with you
              </p>
              <button
                onClick={() => alert('Add availability functionality coming soon')}
                className="inline-flex items-center gap-2 bg-primary-600 dark:bg-orange-500 text-white px-6 py-3 rounded-lg font-medium hover:bg-primary-700 dark:hover:bg-orange-600 transition-colors"
              >
                <PlusIcon className="h-5 w-5" />
                Add Availability
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {availability.map((slot) => (
                <div
                  key={slot.id}
                  className="bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 p-6 hover:shadow-card dark:hover:shadow-orange-500/10 transition-all backdrop-blur-sm"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <div className="bg-primary-100 dark:bg-orange-500/20 rounded-lg p-3">
                        <ClockIcon className="h-6 w-6 text-primary-600 dark:text-orange-500" />
                      </div>
                      <div>
                        <div className="font-medium text-gray-900 dark:text-white">
                          {slot.day_of_week || 'Recurring'}
                        </div>
                        <div className="text-sm text-gray-700 dark:text-gray-400">
                          {slot.start_time} - {slot.end_time}
                        </div>
                      </div>
                    </div>
                  </div>
                  {slot.max_bookings && (
                    <div className="text-sm text-gray-700 dark:text-gray-300">
                      Max bookings: {slot.max_bookings}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )
        )}
      </div>
    </div>
  );
}
