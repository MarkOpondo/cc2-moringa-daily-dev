import { Navigate, Outlet } from "react-router-dom";
import { useSelector } from "react-redux";
import { selectCurrentUser } from "../features/auth/authSlice";

// ProtectedRoute only checks "is someone logged in" — this additionally
// checks "does that person's role allow this page", so typing /admin
// directly into the URL bar doesn't bypass role restrictions.
export default function RoleRoute({ allow }) {
  const user = useSelector(selectCurrentUser);
  if (!user || !allow.includes(user.role)) {
    return <Navigate to="/" replace />;
  }
  return <Outlet />;
}
