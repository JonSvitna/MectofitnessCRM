import { useEffect, useState } from 'react';
import { useAuthStore } from '../store/authStore';
import { userApi, handleApiError } from '../api/client';
import {
  UserCircleIcon,
  EnvelopeIcon,
  PhoneIcon,
  CalendarIcon,
  BuildingOfficeIcon,
  ShieldCheckIcon,
  CheckCircleIcon,
  XCircleIcon,
  ArrowRightOnRectangleIcon,
} from '@heroicons/react/24/outline';

export default function AccountProfile() {
  const { user, organization, setAuth, logout } = useAuthStore();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState(null);
  const [editing, setEditing] = useState(false);

  // Profile state
  const [profile, setProfile] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    username: '',
  });

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      setLoading(true);
      const response = await userApi.getProfile();
      const userData = response.data.data;
      
      setProfile({
        first_name: userData.first_name || '',
        last_name: userData.last_name || '',
        email: userData.email || '',
        phone: userData.phone || '',
        username: userData.username || '',
      });
    } catch (err) {
      console.error('Error loading profile:', err);
      showMessage(handleApiError(err), 'error');
    } finally {
      setLoading(false);
    }
  };

  const showMessage = (msg, type = 'success') => {
    setMessage({ text: msg, type });
    setTimeout(() => setMessage(null), 5000);
  };

  const handleSave = async (e) => {
    e.preventDefault();
    try {
      setSaving(true);
      const response = await userApi.updateProfile({
        first_name: profile.first_name,
        last_name: profile.last_name,
        phone: profile.phone,
        email: profile.email,
      });
      
      // Update auth store with new data
      const updatedUser = { ...user, ...response.data.data };
      setAuth(updatedUser, organization);
      
      showMessage('Profile updated successfully!', 'success');
      setEditing(false);
    } catch (err) {
      showMessage(handleApiError(err), 'error');
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    loadProfile();
    setEditing(false);
  };

  const handleLogout = () => {
    // Clear local auth state first
    logout();
    // Clear localStorage to ensure complete logout
    localStorage.removeItem('auth-storage');
    // Redirect to Flask logout endpoint which will clear the session and redirect to login
    window.location.href = '/logout';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full bg-gray-50 dark:bg-black min-h-screen">
        <div className="text-center">
          <div className="animate-spin h-12 w-12 border-4 border-primary-200 dark:border-orange-500/20 border-t-primary-600 dark:border-t-orange-500 rounded-full mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Loading profile...</p>
        </div>
      </div>
    );
  }

  const fullName = profile.first_name && profile.last_name 
    ? `${profile.first_name} ${profile.last_name}`
    : profile.first_name || profile.last_name || 'User';

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-black p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Account Profile</h1>
          <p className="text-gray-600 dark:text-gray-400">Manage your personal information and account details</p>
        </div>

        {/* Success/Error Message */}
        {message && (
          <div
            className={`mb-6 p-4 rounded-lg flex items-center gap-3 ${
              message.type === 'success'
                ? 'bg-green-50 dark:bg-green-900/20 text-green-800 dark:text-green-400 border border-green-200 dark:border-green-800'
                : 'bg-red-50 dark:bg-red-900/20 text-red-800 dark:text-red-400 border border-red-200 dark:border-red-800'
            }`}
          >
            {message.type === 'success' ? (
              <CheckCircleIcon className="h-5 w-5 flex-shrink-0" />
            ) : (
              <XCircleIcon className="h-5 w-5 flex-shrink-0" />
            )}
            <span>{message.text}</span>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Profile Card */}
          <div className="lg:col-span-1">
            <div className="bg-white dark:bg-white/5 rounded-lg shadow-sm border border-gray-200 dark:border-white/10 p-6">
              {/* Avatar */}
              <div className="flex flex-col items-center mb-6">
                <div className="h-24 w-24 rounded-full bg-gradient-to-br from-primary-500 to-purple-500 dark:from-orange-500 dark:to-purple-500 flex items-center justify-center text-white text-3xl font-bold shadow-lg mb-4">
                  {fullName.charAt(0).toUpperCase()}
                </div>
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-1">
                  {fullName}
                </h2>
                <p className="text-sm text-gray-500 dark:text-gray-400">{profile.email}</p>
                {organization && (
                  <div className="mt-3 px-3 py-1 bg-gray-100 dark:bg-white/5 rounded-full text-xs text-gray-600 dark:text-gray-400">
                    {organization.name}
                  </div>
                )}
              </div>

              {/* Account Info */}
              <div className="space-y-3 border-t border-gray-200 dark:border-white/10 pt-4">
                <div className="flex items-center gap-3 text-sm">
                  <ShieldCheckIcon className="h-5 w-5 text-gray-400 dark:text-gray-500" />
                  <div>
                    <p className="text-gray-500 dark:text-gray-400">Role</p>
                    <p className="font-medium text-gray-900 dark:text-white capitalize">
                      {user?.role || 'User'}
                    </p>
                  </div>
                </div>
                {user?.created_at && (
                  <div className="flex items-center gap-3 text-sm">
                    <CalendarIcon className="h-5 w-5 text-gray-400 dark:text-gray-500" />
                    <div>
                      <p className="text-gray-500 dark:text-gray-400">Member since</p>
                      <p className="font-medium text-gray-900 dark:text-white">
                        {new Date(user.created_at).toLocaleDateString('en-US', {
                          year: 'numeric',
                          month: 'long',
                        })}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Profile Form */}
          <div className="lg:col-span-2">
            <div className="bg-white dark:bg-white/5 rounded-lg shadow-sm border border-gray-200 dark:border-white/10 p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                  Personal Information
                </h2>
                {!editing && (
                  <button
                    onClick={() => setEditing(true)}
                    className="px-4 py-2 bg-primary-600 dark:bg-orange-500 text-white rounded-lg hover:bg-primary-700 dark:hover:bg-orange-600 transition-colors text-sm font-medium"
                  >
                    Edit Profile
                  </button>
                )}
              </div>

              <form onSubmit={handleSave} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      First Name
                    </label>
                    {editing ? (
                      <input
                        type="text"
                        value={profile.first_name}
                        onChange={(e) => setProfile({ ...profile, first_name: e.target.value })}
                        className="w-full px-4 py-2 border border-gray-300 dark:border-white/10 rounded-lg focus:ring-2 focus:ring-primary-500 dark:focus:ring-orange-500 focus:border-transparent bg-white dark:bg-white/5 text-gray-900 dark:text-white"
                        required
                      />
                    ) : (
                      <div className="px-4 py-2 bg-gray-50 dark:bg-white/5 rounded-lg text-gray-900 dark:text-white">
                        {profile.first_name || '—'}
                      </div>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Last Name
                    </label>
                    {editing ? (
                      <input
                        type="text"
                        value={profile.last_name}
                        onChange={(e) => setProfile({ ...profile, last_name: e.target.value })}
                        className="w-full px-4 py-2 border border-gray-300 dark:border-white/10 rounded-lg focus:ring-2 focus:ring-primary-500 dark:focus:ring-orange-500 focus:border-transparent bg-white dark:bg-white/5 text-gray-900 dark:text-white"
                        required
                      />
                    ) : (
                      <div className="px-4 py-2 bg-gray-50 dark:bg-white/5 rounded-lg text-gray-900 dark:text-white">
                        {profile.last_name || '—'}
                      </div>
                    )}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    <EnvelopeIcon className="h-4 w-4 inline mr-1" />
                    Email Address
                  </label>
                  {editing ? (
                    <input
                      type="email"
                      value={profile.email}
                      onChange={(e) => setProfile({ ...profile, email: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 dark:border-white/10 rounded-lg focus:ring-2 focus:ring-primary-500 dark:focus:ring-orange-500 focus:border-transparent bg-white dark:bg-white/5 text-gray-900 dark:text-white"
                      required
                    />
                  ) : (
                    <div className="px-4 py-2 bg-gray-50 dark:bg-white/5 rounded-lg text-gray-900 dark:text-white">
                      {profile.email || '—'}
                    </div>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    <PhoneIcon className="h-4 w-4 inline mr-1" />
                    Phone Number
                  </label>
                  {editing ? (
                    <input
                      type="tel"
                      value={profile.phone}
                      onChange={(e) => setProfile({ ...profile, phone: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 dark:border-white/10 rounded-lg focus:ring-2 focus:ring-primary-500 dark:focus:ring-orange-500 focus:border-transparent bg-white dark:bg-white/5 text-gray-900 dark:text-white"
                      placeholder="(555) 123-4567"
                    />
                  ) : (
                    <div className="px-4 py-2 bg-gray-50 dark:bg-white/5 rounded-lg text-gray-900 dark:text-white">
                      {profile.phone || '—'}
                    </div>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Username
                  </label>
                  <div className="px-4 py-2 bg-gray-50 dark:bg-white/5 rounded-lg text-gray-900 dark:text-white">
                    {profile.username}
                  </div>
                  <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
                    Username cannot be changed
                  </p>
                </div>

                {editing && (
                  <div className="flex gap-3 pt-4 border-t border-gray-200 dark:border-white/10">
                    <button
                      type="submit"
                      disabled={saving}
                      className="px-6 py-2 bg-primary-600 dark:bg-orange-500 text-white rounded-lg hover:bg-primary-700 dark:hover:bg-orange-600 disabled:opacity-50 transition-colors font-medium"
                    >
                      {saving ? 'Saving...' : 'Save Changes'}
                    </button>
                    <button
                      type="button"
                      onClick={handleCancel}
                      disabled={saving}
                      className="px-6 py-2 bg-gray-100 dark:bg-white/10 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-white/20 disabled:opacity-50 transition-colors font-medium"
                    >
                      Cancel
                    </button>
                  </div>
                )}
              </form>

              {/* Logout Section */}
              <div className="mt-8 pt-6 border-t border-gray-200 dark:border-white/10">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                  Account Actions
                </h3>
                <button
                  onClick={handleLogout}
                  className="flex items-center gap-2 px-4 py-2 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors font-medium"
                >
                  <ArrowRightOnRectangleIcon className="h-5 w-5" />
                  Logout
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

