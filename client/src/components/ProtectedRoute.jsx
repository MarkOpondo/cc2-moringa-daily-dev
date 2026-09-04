import { Navigate, Outlet } from 'react-router-dom';
import { getAuthToken } from '../services/authStorage';

export default function ProtectedRoute() {
  const token = getAuthToken();

  // Dev-only bypass: without this, the "Preview as" role switcher (which
  // lives inside the pages this route protects) is unreachable whenever
  // there's no real backend to log in against — a chicken-and-egg problem.
  // import.meta.env.DEV is false in a production build, so this never
  // weakens real auth once deployed.
  const devPreviewAllowed = import.meta.env.DEV;

  if (!token && !devPreviewAllowed) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}
