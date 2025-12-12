import { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from './store/authStore';
import { userApi, organizationApi } from './api/client';
import Layout from './components/Layout';
import AIChatbot from './components/AIChatbot';
import Dashboard from './pages/Dashboard';
import Calendar from './pages/Calendar';
import ClientList from './pages/clients/ClientList';
import ClientDetail from './pages/clients/ClientDetail';
import SessionList from './pages/sessions/SessionList';
import ProgramList from './pages/programs/ProgramList';
import Progress from './pages/Progress';
import Nutrition from './pages/Nutrition';
import Payments from './pages/Payments';
import OnlineBooking from './pages/OnlineBooking';
import Messages from './pages/Messages';
import Groups from './pages/Groups';
import Challenges from './pages/Challenges';
import Announcements from './pages/Announcements';
import Team from './pages/Team';
import Scheduling from './pages/Scheduling';
import MasterLibraries from './pages/MasterLibraries';
import Settings from './pages/settings/Settings';
import ExerciseLibrary from './pages/ExerciseLibrary';

// Protected Route wrapper - redirects to Flask login if not authenticated
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuthStore();
  
  if (!isAuthenticated) {
    // Redirect to Flask login page
    window.location.href = '/login';
    return null;
  }
  
  return children;
};

function App() {
  const { isAuthenticated, setAuth, logout } = useAuthStore();

  // Check authentication status on app load
  useEffect(() => {
    const checkAuth = async () => {
      try {
        // Try to fetch user profile from backend
        const userResponse = await userApi.getProfile();
        
        if (userResponse.data.success && userResponse.data.data) {
          // Try to fetch organization data (optional)
          let orgData = null;
          try {
            const orgResponse = await organizationApi.get();
            orgData = orgResponse.data.data;
          } catch (orgError) {
            // Organization fetch is optional - continue without it
            console.warn('Could not fetch organization data:', orgError);
          }
          
          // User is authenticated via Flask session
          setAuth(userResponse.data.data, orgData);
        }
      } catch (error) {
        // If API returns 401, user is not authenticated
        if (error.response?.status === 401) {
          // Just redirect - Flask will handle session clearing
          window.location.href = '/login';
        }
      }
    };

    checkAuth();
  }, [setAuth]);

  return (
    <Router>
      <Routes>
        {/* No React-based login/register routes - use Flask auth */}
        {/* Public route for exercise library */}
        <Route path="/exercise-library" element={<ExerciseLibrary />} />

        {/* Protected Routes */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route index element={<Dashboard />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="calendar" element={<Calendar />} />
          <Route path="clients" element={<ClientList />} />
          <Route path="clients/:id" element={<ClientDetail />} />
          <Route path="sessions" element={<SessionList />} />
          <Route path="programs" element={<ProgramList />} />
          <Route path="progress" element={<Progress />} />
          <Route path="nutrition" element={<Nutrition />} />
          <Route path="payments" element={<Payments />} />
          <Route path="booking" element={<OnlineBooking />} />
          <Route path="messages" element={<Messages />} />
          <Route path="groups" element={<Groups />} />
          <Route path="challenges" element={<Challenges />} />
          <Route path="announcements" element={<Announcements />} />
          <Route path="team" element={<Team />} />
          <Route path="scheduling" element={<Scheduling />} />
          <Route path="master-libraries" element={<MasterLibraries />} />
          <Route path="settings/*" element={<Settings />} />
        </Route>

        {/* 404 - redirect to dashboard if authenticated, login if not */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>

      {/* AI Chatbot - Only show when authenticated */}
      {isAuthenticated && <AIChatbot />}
    </Router>
  );
}

export default App;
