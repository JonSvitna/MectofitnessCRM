import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useAuthStore = create(
  persist(
    (set) => ({
      user: null,
      organization: null,
      isAuthenticated: false,
      token: null,
      loading: true, // Add loading state to prevent premature redirects

      setAuth: (user, organization = null, token = null) =>
        set({
          user,
          organization,
          isAuthenticated: true,
          token,
          loading: false,
        }),

      logout: () =>
        set({
          user: null,
          organization: null,
          isAuthenticated: false,
          token: null,
          loading: false,
        }),

      setLoading: (loading) =>
        set({ loading }),

      updateUser: (userData) =>
        set((state) => ({
          user: { ...state.user, ...userData },
        })),

      updateOrganization: (orgData) =>
        set((state) => ({
          organization: { ...state.organization, ...orgData },
        })),
    }),
    {
      name: 'auth-storage',
    }
  )
);
