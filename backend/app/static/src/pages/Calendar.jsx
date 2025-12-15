import { useEffect, useState } from 'react';
import { dashboardApi, handleApiError } from '../api/client';
import { CalendarIcon, ClockIcon, MapPinIcon, XCircleIcon } from '@heroicons/react/24/outline';
import logger from '../utils/logger';

export default function Calendar() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [startDate, setStartDate] = useState(new Date().toISOString().split('T')[0]);
  const [endDate, setEndDate] = useState(
    new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
  );

  useEffect(() => {
    loadCalendarEvents();
  }, [startDate, endDate]);

  const loadCalendarEvents = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await dashboardApi.getCalendar({
        start_date: startDate,
        end_date: endDate,
      });
      setEvents(response.data.data?.events || response.data.events || []);
    } catch (err) {
      logger.error('Error loading calendar:', err);
      setError(handleApiError(err));
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'scheduled':
        return 'bg-blue-50 dark:bg-blue-500/10 text-blue-700 dark:text-blue-400';
      case 'completed':
        return 'bg-success-50 dark:bg-green-500/10 text-success-700 dark:text-green-400';
      case 'cancelled':
        return 'bg-danger-50 dark:bg-danger-500/10 text-danger-700 dark:text-danger-400';
      default:
        return 'bg-gray-50 dark:bg-white/5 text-gray-700 dark:text-gray-400';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full bg-gray-50 dark:bg-black">
        <div className="text-center">
          <div className="animate-spin h-12 w-12 border-4 border-primary-200 dark:border-orange-500/20 border-t-primary-600 dark:border-t-orange-500 rounded-full mx-auto mb-4"></div>
          <p className="text-gray-700 dark:text-gray-300">Loading calendar...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-full bg-gray-50 dark:bg-black">
        <div className="text-center max-w-md px-4">
          <XCircleIcon className="h-12 w-12 text-danger-600 dark:text-danger-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">Unable to Load Calendar</h2>
          <p className="text-gray-700 dark:text-gray-300 mb-6">{error}</p>
          <button
            onClick={loadCalendarEvents}
            className="bg-primary-600 dark:bg-orange-500 text-white px-6 py-3 rounded-lg font-medium hover:bg-primary-700 dark:hover:bg-orange-600 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full bg-gray-50 dark:bg-black p-6 overflow-y-auto">
      <div className="max-w-6xl mx-auto">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-6 gap-4">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
            <CalendarIcon className="h-8 w-8 text-primary-600 dark:text-orange-500" />
            Calendar
          </h1>
          <div className="flex gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">From</label>
              <input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                className="px-3 py-2 border border-gray-300 dark:border-white/10 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 dark:focus:ring-orange-500 bg-white dark:bg-white/5 text-gray-900 dark:text-white"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">To</label>
              <input
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                className="px-3 py-2 border border-gray-300 dark:border-white/10 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 dark:focus:ring-orange-500 bg-white dark:bg-white/5 text-gray-900 dark:text-white"
              />
            </div>
          </div>
        </div>

        {events.length === 0 ? (
          <div className="bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 p-12 text-center backdrop-blur-sm">
            <CalendarIcon className="h-16 w-16 text-gray-600 dark:text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">No Events Found</h3>
            <p className="text-gray-700 dark:text-gray-300">
              No sessions scheduled for the selected date range.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {events.map((event) => (
              <div
                key={event.id}
                className="bg-white dark:bg-white/5 rounded-lg border border-gray-200 dark:border-white/10 p-5 hover:shadow-card dark:hover:shadow-orange-500/10 transition-all backdrop-blur-sm"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex flex-wrap items-center gap-3 mb-3">
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                        {event.session_type || event.title || 'Training Session'}
                      </h3>
                      <span
                        className={`px-2.5 py-0.5 text-xs font-medium rounded-full ${getStatusColor(
                          event.status
                        )}`}
                      >
                        {event.status?.toUpperCase() || 'SCHEDULED'}
                      </span>
                    </div>
                    <div className="space-y-2">
                      <div className="flex items-center gap-2 text-gray-700 dark:text-gray-300">
                        <CalendarIcon className="h-4 w-4 text-gray-600 dark:text-gray-400" />
                        <span>{new Date(event.date || event.scheduled_start).toLocaleDateString('en-US', {
                          weekday: 'long',
                          month: 'long',
                          day: 'numeric',
                          year: 'numeric'
                        })}</span>
                      </div>
                      {(event.time || event.scheduled_start) && (
                        <div className="flex items-center gap-2 text-gray-700 dark:text-gray-300">
                          <ClockIcon className="h-4 w-4 text-gray-600 dark:text-gray-400" />
                          <span>
                            {event.time || new Date(event.scheduled_start).toLocaleTimeString('en-US', {
                              hour: 'numeric',
                              minute: '2-digit'
                            })}
                            {event.duration && ` (${event.duration} min)`}
                          </span>
                        </div>
                      )}
                      {event.location && (
                        <div className="flex items-center gap-2 text-gray-700 dark:text-gray-300">
                          <MapPinIcon className="h-4 w-4 text-gray-600 dark:text-gray-400" />
                          <span>{event.location}</span>
                        </div>
                      )}
                      {event.client_name && (
                        <div className="mt-2 text-sm text-gray-700 dark:text-gray-300">
                          <span className="font-medium">Client:</span> {event.client_name}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
