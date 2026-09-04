import { useEffect } from "react";
import { Outlet, useNavigate, useSearchParams } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import Topbar from "./Topbar";
import { selectCurrentUser } from "../features/auth/authSlice";
import { fetchCategories, fetchSubscriptions } from "../features/categories/categoriesSlice";
import { fetchNotifications } from "../features/notifications/notificationsSlice";

// Loads data every page might need (categories for filters/forms,
// subscriptions for the "subscribed" indicator, notification count for the
// badge) once per session, here, rather than duplicating fetches in every
// page that happens to need them.
export default function AppShell() {
  const user = useSelector(selectCurrentUser);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  useEffect(() => {
    dispatch(fetchCategories());
    if (user?.id) {
      dispatch(fetchSubscriptions());
      dispatch(fetchNotifications());
    }
  }, [dispatch, user?.id]);

  function handleSearchChange(value) {
    navigate(value ? `/?q=${encodeURIComponent(value)}` : "/");
  }

  return (
    <div className="bg-navy min-h-screen">
      <Topbar search={searchParams.get("q") || ""} onSearchChange={handleSearchChange} />
      <main className="max-w-5xl mx-auto px-4 sm:px-6 py-6">
        <Outlet />
      </main>
    </div>
  );
}
