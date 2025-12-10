import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from './store/authStore';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Calendar from './pages/Calendar';
import ClientList from './pages/clients/ClientList';
import ClientDetail from './pages/clients/ClientDetail';
import SessionList from './pages/sessions/SessionList';
import ProgramList from './pages/programs/ProgramList';
import Progress from './pages/Progress';
import Messages from './pages/Messages';
import Groups from './pages/Groups';
import Challenges from './pages/Challenges';
import Announcements from './pages/Announcements';
import Payments from './pages/Payments';
import Team from './pages/Team';
import Scheduling from './pages/Scheduling';
import MasterLibraries from './pages/MasterLibraries';
import Settings from './pages/settings/Settings';
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import ExerciseLibrary from './pages/ExerciseLibrary';

// Protected Route wrapper
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuthStore();
  return isAuthenticated ? children : <Navigate to="/login" replace />;
};

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
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
          <Route path="messages" element={<Messages />} />
          <Route path="groups" element={<Groups />} />
          <Route path="challenges" element={<Challenges />} />
          <Route path="announcements" element={<Announcements />} />
          <Route path="payments" element={<Payments />} />
          <Route path="team" element={<Team />} />
          <Route path="scheduling" element={<Scheduling />} />
          <Route path="master-libraries" element={<MasterLibraries />} />
          <Route path="settings/*" element={<Settings />} />
        </Route>

        {/* 404 */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
