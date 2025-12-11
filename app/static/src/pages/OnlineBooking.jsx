import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  PlusIcon,
  CalendarDaysIcon,
  ClockIcon,
  CheckCircleIcon,
  XCircleIcon,
} from '@heroicons/react/24/outline';
import { bookingApi, handleApiError } from '../api/client';

export default function OnlineBooking() {
  const [bookings, setBookings] = useState([]);
  const [availability, setAvailability] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadBookingData();
  }, []);

  const loadBookingData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [bookingsRes, availRes] = await Promise.all([
        bookingApi.getBookings({ limit: 20 }),
        bookingApi.getAvailability({}),
      ]);
      setBookings(bookingsRes.data.bookings || bookingsRes.data || []);
      setAvailability(availRes.data.availability || availRes.data || []);
    } catch (err) {
      console.error('Error loading booking data:', err);
      setError(handleApiError(err));
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const badges = {
      confirmed: 'bg-success-50 text-success-700',
      pending: 'bg-accent-50 text-accent-700',
      cancelled: 'bg-danger-50 text-danger-700',
      completed: 'bg-primary-50 text-primary-700',
    };
    return badges[status] || 'bg-gray-50 text-gray-700';
  };

  if (loading) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin h-12 w-12 border-4 border-primary-200 border-t-primary-600 rounded-full mx-auto mb-4"></div>
          <p className="text-gray-600">Loading booking data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-full flex items-center justify-center">
        <div className="text-center max-w-md mx-auto px-4">
          <XCircleIcon className="h-12 w-12 text-danger-600 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Error Loading Bookings</h2>
          <p className="text-gray-600 mb-6">{error}</p>
          <button
            onClick={loadBookingData}
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
              <h1 className="text-3xl font-bold text-gray-900">Online Booking</h1>
              <p className="mt-1 text-gray-600">
                Manage availability and online booking requests
              </p>
            </div>
            <Link
              to="?action=add-availability"
              className="inline-flex items-center gap-2 bg-primary-600 text-white px-5 py-2.5 rounded-lg font-medium hover:bg-primary-700 transition-colors shadow-button hover:shadow-button-hover"
            >
              <PlusIcon className="h-5 w-5" />
              Add Availability
            </Link>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-white rounded-lg border border-gray-200 p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Total Bookings</p>
                  <p className="text-2xl font-bold text-gray-900">{bookings.length}</p>
                </div>
                <div className="bg-primary-50 rounded-lg p-3">
                  <CalendarDaysIcon className="h-6 w-6 text-primary-600" />
                </div>
              </div>
            </div>
            <div className="bg-white rounded-lg border border-gray-200 p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Confirmed</p>
                  <p className="text-2xl font-bold text-success-600">
                    {bookings.filter((b) => b.status === 'confirmed').length}
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
                  <p className="text-sm text-gray-600">Pending</p>
                  <p className="text-2xl font-bold text-accent-600">
                    {bookings.filter((b) => b.status === 'pending').length}
                  </p>
                </div>
                <div className="bg-accent-50 rounded-lg p-3">
                  <ClockIcon className="h-6 w-6 text-accent-600" />
                </div>
              </div>
            </div>
            <div className="bg-white rounded-lg border border-gray-200 p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Available Slots</p>
                  <p className="text-2xl font-bold text-primary-600">{availability.length}</p>
                </div>
                <div className="bg-primary-50 rounded-lg p-3">
                  <ClockIcon className="h-6 w-6 text-primary-600" />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Bookings List */}
        <div className="bg-white rounded-lg border border-gray-200 shadow-sm mb-6">
          <div className="border-b border-gray-200 px-6 py-4">
            <h2 className="text-lg font-semibold text-gray-900">Recent Bookings</h2>
          </div>
          
          {bookings.length === 0 ? (
            <div className="p-12 text-center">
              <CalendarDaysIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600">No bookings yet</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Date & Time</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Client</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Service</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Duration</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Status</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-700 uppercase">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {bookings.map((booking) => (
                    <tr key={booking.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div>
                          <div className="font-medium text-gray-900">
                            {new Date(booking.date || booking.start_time).toLocaleDateString('en-US', {
                              month: 'short',
                              day: 'numeric',
                              year: 'numeric',
                            })}
                          </div>
                          <div className="text-sm text-gray-600">
                            {new Date(booking.start_time).toLocaleTimeString('en-US', {
                              hour: 'numeric',
                              minute: '2-digit',
                            })}
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="font-medium text-gray-900">{booking.client_name || 'Unknown'}</div>
                        <div className="text-sm text-gray-600">{booking.client_email || ''}</div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="text-gray-900">{booking.service_type || 'Training Session'}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-gray-900">
                        {booking.duration || 60} min
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span
                          className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusBadge(
                            booking.status
                          )}`}
                        >
                          {booking.status?.toUpperCase()}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <Link
                          to={`/booking/${booking.id}`}
                          className="text-primary-600 hover:text-primary-700 font-medium text-sm"
                        >
                          View →
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Availability Slots */}
        <div className="bg-white rounded-lg border border-gray-200 shadow-sm">
          <div className="border-b border-gray-200 px-6 py-4 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900">Available Slots</h2>
            <Link
              to="?action=add-availability"
              className="text-sm text-primary-600 hover:text-primary-700 font-medium"
            >
              Manage Availability →
            </Link>
          </div>
          
          {availability.length === 0 ? (
            <div className="p-12 text-center">
              <ClockIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600 mb-4">No availability slots configured</p>
              <Link
                to="?action=add-availability"
                className="inline-flex items-center gap-2 bg-primary-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-primary-700 transition-colors"
              >
                <PlusIcon className="h-5 w-5" />
                Add Availability
              </Link>
            </div>
          ) : (
            <div className="p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {availability.slice(0, 6).map((slot) => (
                <div key={slot.id} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-semibold text-gray-900">
                      {slot.day_of_week || 'Monday'}
                    </span>
                    <span className="text-xs px-2 py-1 bg-success-50 text-success-700 rounded">
                      Available
                    </span>
                  </div>
                  <p className="text-sm text-gray-600">
                    {slot.start_time} - {slot.end_time}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
