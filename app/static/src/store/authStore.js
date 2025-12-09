import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useAuthStore = create(
  persist(
    (set) => ({
      user: null,
      organization: null,
      isAuthenticated: false,
      token: null,

      setAuth: (user, organization = null, token = null) =>
        set({
          user,
          organization,
          isAuthenticated: true,
          token,
        }),

      logout: () =>
        set({
          user: null,
          organization: null,
          isAuthenticated: false,
          token: null,
        }),

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
