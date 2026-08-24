import { useEffect } from "react";
import { Outlet, useNavigate, useSearchParams } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import Sidebar from "./SideBar";
import Topbar from "./Topbar";
import MobileNav from "./MobileNav";
import { selectCurrentUser } from "../../features/auth/authSlice";
import { fetchCategories, fetchSubscriptions } from "../../features/categories/categoriesSlice";
import { fetchNotifications } from "../../features/notifications/notificationsSlice";

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
      dispatch(fetchSubscriptions(user.id));
      dispatch(fetchNotifications(user.id));
    }
  }, [dispatch, user?.id]);

  function handleSearchChange(value) {
    navigate(value ? `/?q=${encodeURIComponent(value)}` : "/");
  }

  return (
    <div className="flex bg-slate-950 min-h-screen">
      <Sidebar />
      <div className="flex-1 min-w-0">
        <Topbar search={searchParams.get("q") || ""} onSearchChange={handleSearchChange} />
        <main className="p-6 pb-24 md:pb-6 max-w-4xl mx-auto">
          <Outlet />
        </main>
      </div>
      <MobileNav />
    </div>
  );
}
