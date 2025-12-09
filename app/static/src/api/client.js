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

// API methods
export const clientsApi = {
  getAll: () => api.get('/clients'),
  getOne: (id) => api.get(`/clients/${id}`),
  create: (data) => api.post('/clients', data),
  update: (id, data) => api.put(`/clients/${id}`, data),
  delete: (id) => api.delete(`/clients/${id}`),
  getProgress: (id) => api.get(`/clients/${id}/progress`),
  getPrograms: (id) => api.get(`/clients/${id}/programs`),
  getSessions: (id) => api.get(`/clients/${id}/sessions`),
};

export const sessionsApi = {
  getAll: () => api.get('/sessions'),
  getOne: (id) => api.get(`/sessions/${id}`),
  create: (data) => api.post('/sessions', data),
  update: (id, data) => api.put(`/sessions/${id}`, data),
  delete: (id) => api.delete(`/sessions/${id}`),
  cancel: (id) => api.post(`/sessions/${id}/cancel`),
  complete: (id, data) => api.post(`/sessions/${id}/complete`, data),
};

export const programsApi = {
  getAll: () => api.get('/programs'),
  getOne: (id) => api.get(`/programs/${id}`),
  create: (data) => api.post('/programs', data),
  update: (id, data) => api.put(`/programs/${id}`, data),
  delete: (id) => api.delete(`/programs/${id}`),
  addWorkout: (id, data) => api.post(`/programs/${id}/workouts`, data),
  updateWorkout: (programId, workoutId, data) => 
    api.put(`/programs/${programId}/workouts/${workoutId}`, data),
  deleteWorkout: (programId, workoutId) => 
    api.delete(`/programs/${programId}/workouts/${workoutId}`),
};

export const organizationApi = {
  get: () => api.get('/organization'),
  update: (data) => api.put('/organization', data),
  getMembers: () => api.get('/organization/members'),
  updateMemberRole: (userId, role) => 
    api.patch(`/organization/members/${userId}/role`, { role }),
  invite: (data) => api.post('/organization/invite', data),
  getStats: () => api.get('/organization/stats'),
};

export const exerciseLibraryApi = {
  getAll: () => api.get('/exercises'),
  getOne: (id) => api.get(`/exercises/${id}`),
  create: (data) => api.post('/exercises', data),
  update: (id, data) => api.put(`/exercises/${id}`, data),
  delete: (id) => api.delete(`/exercises/${id}`),
  search: (params) => api.get('/exercises/search', { params }),
};

export const progressApi = {
  getClientProgress: (clientId) => api.get(`/clients/${clientId}/progress`),
  addProgress: (clientId, data) => api.post(`/clients/${clientId}/progress`, data),
  updateProgress: (clientId, progressId, data) => 
    api.put(`/clients/${clientId}/progress/${progressId}`, data),
  deleteProgress: (clientId, progressId) => 
    api.delete(`/clients/${clientId}/progress/${progressId}`),
};

export const settingsApi = {
  getProfile: () => api.get('/user/profile'),
  updateProfile: (data) => api.put('/user/profile', data),
  updatePassword: (data) => api.put('/user/password', data),
  getSettings: () => api.get('/settings'),
  updateSettings: (data) => api.put('/settings', data),
};

export default api;
