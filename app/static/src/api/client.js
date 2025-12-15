import axios from 'axios';

const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth-token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for handling errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear auth and redirect to login
      localStorage.removeItem('auth-storage');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// ============================================================================
// CLIENT MANAGEMENT API
// ============================================================================
export const clientsApi = {
  getAll: (params) => api.get('/clients', { params }),
  getOne: (id, params) => api.get(`/clients/${id}`, { params }),
  create: (data) => api.post('/clients', data),
  update: (id, data) => api.put(`/clients/${id}`, data),
  patch: (id, data) => api.patch(`/clients/${id}`, data),
  delete: (id, permanent = false) => api.delete(`/clients/${id}`, { params: { permanent } }),
  getStats: () => api.get('/clients/stats'),

  // Client-specific progress endpoints
  getProgress: (id) => api.get(`/clients/${id}/progress`),
  getPrograms: (id) => api.get(`/clients/${id}/programs`),
  getSessions: (id) => api.get(`/clients/${id}/sessions`),
};

// ============================================================================
// SESSION MANAGEMENT API
// ============================================================================
export const sessionsApi = {
  getAll: (params) => api.get('/sessions', { params }),
  getOne: (id) => api.get(`/sessions/${id}`),
  create: (data) => api.post('/sessions', data),
  update: (id, data) => api.put(`/sessions/${id}`, data),
  patch: (id, data) => api.patch(`/sessions/${id}`, data),
  delete: (id, permanent = false) => api.delete(`/sessions/${id}`, { params: { permanent } }),
  cancel: (id, reason) => api.post(`/sessions/${id}/cancel`, { reason }),
  complete: (id, data) => api.post(`/sessions/${id}/complete`, data),
  getStats: () => api.get('/sessions/stats'),
  checkAvailability: (date, duration, trainerId) =>
    api.get('/sessions/availability', { params: { date, duration, trainer_id: trainerId } }),
};

// ============================================================================
// PROGRAM MANAGEMENT API
// ============================================================================
export const programsApi = {
  getAll: (params) => api.get('/programs', { params }),
  getOne: (id, params) => api.get(`/programs/${id}`, { params }),
  create: (data) => api.post('/programs', data),
  update: (id, data) => api.put(`/programs/${id}`, data),
  patch: (id, data) => api.patch(`/programs/${id}`, data),
  delete: (id, permanent = false) => api.delete(`/programs/${id}`, { params: { permanent } }),
  clone: (id, clientId) => api.post(`/programs/${id}/clone`, { client_id: clientId }),
  getStats: () => api.get('/programs/stats'),

  // Exercise management within programs
  getExercises: (id) => api.get(`/programs/${id}/exercises`),
  addExercise: (id, data) => api.post(`/programs/${id}/exercises`, data),
  updateExercise: (programId, exerciseId, data) =>
    api.put(`/programs/${programId}/exercises/${exerciseId}`, data),
  patchExercise: (programId, exerciseId, data) =>
    api.patch(`/programs/${programId}/exercises/${exerciseId}`, data),
  deleteExercise: (programId, exerciseId) =>
    api.delete(`/programs/${programId}/exercises/${exerciseId}`),
};

// ============================================================================
// EXERCISE LIBRARY API
// ============================================================================
export const exerciseLibraryApi = {
  getAll: (params) => api.get('/exercises', { params }),
  getOne: (id) => api.get(`/exercises/${id}`),
  create: (data) => api.post('/exercises', data),
  update: (id, data) => api.put(`/exercises/${id}`, data),
  patch: (id, data) => api.patch(`/exercises/${id}`, data),
  delete: (id) => api.delete(`/exercises/${id}`),
  search: (params) => api.get('/exercises/search', { params }),
  getStats: () => api.get('/exercises/stats'),
  getCategories: () => api.get('/exercises/categories'),
  getMuscles: () => api.get('/exercises/muscles'),
  getEquipment: () => api.get('/exercises/equipment'),
};

// ============================================================================
// PROGRESS TRACKING API
// ============================================================================
export const progressApi = {
  // Progress entries
  getEntries: (params) => api.get('/progress/entries', { params }),
  createEntry: (data) => api.post('/progress/entries', data),
  updateEntry: (id, data) => api.put(`/progress/entries/${id}`, data),
  patchEntry: (id, data) => api.patch(`/progress/entries/${id}`, data),
  deleteEntry: (id) => api.delete(`/progress/entries/${id}`),

  // Progress photos
  getPhotos: (params) => api.get('/progress/photos', { params }),

  // Statistics
  getStats: (clientId) => api.get(`/progress/stats/${clientId}`),
};

// ============================================================================
// NUTRITION MANAGEMENT API
// ============================================================================
export const nutritionApi = {
  // Nutrition plans
  getPlans: (params) => api.get('/nutrition/plans', { params }),
  getPlan: (id) => api.get(`/nutrition/plans/${id}`),
  createPlan: (data) => api.post('/nutrition/plans', data),
  updatePlan: (id, data) => api.put(`/nutrition/plans/${id}`, data),
  patchPlan: (id, data) => api.patch(`/nutrition/plans/${id}`, data),
  deletePlan: (id) => api.delete(`/nutrition/plans/${id}`),

  // Food logs
  getLogs: (params) => api.get('/nutrition/logs', { params }),
  createLog: (data) => api.post('/nutrition/logs', data),

  // Summary
  getDailySummary: (clientId, date) =>
    api.get(`/nutrition/logs/summary/${clientId}`, { params: { date } }),
};

// ============================================================================
// PAYMENTS & SUBSCRIPTIONS API
// ============================================================================
export const paymentsApi = {
  // Payment plans
  getPlans: (params) => api.get('/payments/plans', { params }),
  createPlan: (data) => api.post('/payments/plans', data),
  updatePlan: (id, data) => api.put(`/payments/plans/${id}`, data),
  patchPlan: (id, data) => api.patch(`/payments/plans/${id}`, data),

  // Subscriptions
  getSubscriptions: (params) => api.get('/payments/subscriptions', { params }),
  createSubscription: (data) => api.post('/payments/subscriptions', data),
  updateSubscriptionStatus: (id, status) =>
    api.patch(`/payments/subscriptions/${id}/status`, { status }),

  // Transactions
  getTransactions: (params) => api.get('/payments/transactions', { params }),
  recordPayment: (data) => api.post('/payments/transactions', data),

  // Revenue
  getRevenue: (params) => api.get('/payments/revenue', { params }),
};

// ============================================================================
// ONLINE BOOKING API
// ============================================================================
export const bookingApi = {
  // Availability management
  getAvailability: (params) => api.get('/booking/availability', { params }),
  createAvailability: (data) => api.post('/booking/availability', data),
  updateAvailability: (slotId, data) => api.put(`/booking/availability/${slotId}`, data),
  patchAvailability: (slotId, data) => api.patch(`/booking/availability/${slotId}`, data),
  deleteAvailability: (slotId) => api.delete(`/booking/availability/${slotId}`),

  // Booking exceptions
  getExceptions: (params) => api.get('/booking/exceptions', { params }),
  createException: (data) => api.post('/booking/exceptions', data),

  // Bookings
  getBookings: (params) => api.get('/booking/bookings', { params }),
  createBooking: (data) => api.post('/booking/bookings', data),
  updateBookingStatus: (id, status, notes) =>
    api.patch(`/booking/bookings/${id}/status`, { status, notes }),

  // Check availability for specific date
  checkDateAvailability: (date) => api.get(`/booking/check-availability/${date}`),
};

// ============================================================================
// DASHBOARD & ANALYTICS API
// ============================================================================
export const dashboardApi = {
  getOverview: () => api.get('/dashboard/overview'),
  getActivity: (params) => api.get('/dashboard/activity', { params }),
  getCalendar: (params) => api.get('/dashboard/calendar', { params }),
  getClientProgress: (clientId) => api.get(`/dashboard/client-progress/${clientId}`),
  getSessionStats: (params) => api.get('/dashboard/stats/sessions', { params }),
  getRevenueStats: (params) => api.get('/dashboard/stats/revenue', { params }),
};

// ============================================================================
// ORGANIZATION MANAGEMENT API
// ============================================================================
export const organizationApi = {
  get: () => api.get('/organization/'),
  create: (data) => api.post('/organization/', data),
  update: (data) => api.put('/organization/', data),
  patch: (data) => api.patch('/organization/', data),
  getMembers: () => api.get('/organization/members'),
  updateMemberRole: (userId, role) =>
    api.patch(`/organization/members/${userId}/role`, { role }),
  invite: (data) => api.post('/organization/invite', data),
  getStats: () => api.get('/organization/stats'),
};

// ============================================================================
// AI CHATBOT API
// ============================================================================
export const chatbotApi = {
  sendMessage: (message, context) => api.post('/chatbot/', { message, context }),
  getSuggestions: (page) => api.get('/chatbot/suggestions', { params: { page } }),
};

// ============================================================================
// USER & SETTINGS API (To be created in backend)
// ============================================================================
export const userApi = {
  getProfile: () => api.get('/user/profile'),
  updateProfile: (data) => api.put('/user/profile', data),
  changePassword: (data) => api.put('/user/password', data),
};

export const settingsApi = {
  getAll: () => api.get('/settings'),
  update: (data) => api.put('/settings', data),
  patch: (data) => api.patch('/settings', data),
};

// ============================================================================
// MESSAGING API
// ============================================================================
export const messagingApi = {
  getAll: (params) => api.get('/messages', { params }),
  getOne: (id) => api.get(`/messages/${id}`),
  create: (data) => api.post('/messages', data),
  markAsRead: (id) => api.post(`/messages/${id}/read`),
  archive: (id, archive = true) => api.post(`/messages/${id}/archive`, { archive }),
  getStats: () => api.get('/messages/stats'),
};

// ============================================================================
// ENGAGEMENT API (Groups, Challenges, Announcements)
// ============================================================================
export const engagementApi = {
  // Groups
  getGroups: (params) => api.get('/engagement/groups', { params }),
  createGroup: (data) => api.post('/engagement/groups', data),
  
  // Challenges
  getChallenges: (params) => api.get('/engagement/challenges', { params }),
  createChallenge: (data) => api.post('/engagement/challenges', data),
  
  // Announcements
  getAnnouncements: (params) => api.get('/engagement/announcements', { params }),
  createAnnouncement: (data) => api.post('/engagement/announcements', data),
};

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

/**
 * Build query params for pagination
 * @param {number} page - Page number (1-indexed)
 * @param {number} perPage - Items per page
 * @param {object} filters - Additional filters
 * @returns {object} Query params object
 */
export const buildPaginationParams = (page = 1, perPage = 20, filters = {}) => ({
  page,
  per_page: perPage,
  ...filters,
});

/**
 * Build query params for sorting
 * @param {string} sortBy - Field to sort by
 * @param {string} sortOrder - 'asc' or 'desc'
 * @returns {object} Query params object
 */
export const buildSortParams = (sortBy, sortOrder = 'asc') => ({
  sort_by: sortBy,
  sort_order: sortOrder,
});

/**
 * Build date range params
 * @param {string} startDate - ISO date string
 * @param {string} endDate - ISO date string
 * @returns {object} Query params object
 */
export const buildDateRangeParams = (startDate, endDate) => ({
  start_date: startDate,
  end_date: endDate,
});

/**
 * Handle API errors with user-friendly messages
 * @param {Error} error - Axios error object
 * @returns {string} User-friendly error message
 */
export const handleApiError = (error) => {
  if (error.response) {
    // Server responded with error status
    const { status, data } = error.response;

    switch (status) {
      case 400:
        return data.message || 'Invalid request. Please check your input.';
      case 401:
        return 'Your session has expired. Please log in again.';
      case 403:
        return 'You do not have permission to perform this action.';
      case 404:
        return data.message || 'The requested resource was not found.';
      case 409:
        return data.message || 'A conflict occurred. Please try again.';
      case 422:
        return data.message || 'Validation error. Please check your input.';
      case 500:
        return 'A server error occurred. Please try again later.';
      default:
        return data.message || `An error occurred (${status}). Please try again.`;
    }
  } else if (error.request) {
    // Request made but no response received
    return 'Network error. Please check your connection and try again.';
  } else {
    // Error in request setup
    return error.message || 'An unexpected error occurred. Please try again.';
  }
};

/**
 * Format API success response
 * @param {object} response - Axios response object
 * @returns {object} Formatted data
 */
export const formatResponse = (response) => ({
  success: true,
  data: response.data,
  status: response.status,
});

export default api;
