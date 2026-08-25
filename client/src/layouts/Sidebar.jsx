import { NavLink } from "react-router-dom";
import { useSelector } from "react-redux";
import { Home, LayoutGrid, Bookmark, Bell, PlusCircle, ShieldCheck } from "lucide-react";
import { selectCurrentUser } from "../../features/auth/authSlice";
import { selectUnreadCount } from "../../features/notifications/notificationsSlice";

const NAV_ITEMS = [
  { to: "/", label: "Feed", icon: Home, end: true },
  { to: "/categories", label: "Categories", icon: LayoutGrid },
  { to: "/wishlist", label: "Wishlist", icon: Bookmark },
  { to: "/notifications", label: "Notifications", icon: Bell },
  { to: "/create", label: "Post content", icon: PlusCircle },
];

export default function Sidebar() {
  const user = useSelector(selectCurrentUser);
  const unread = useSelector(selectUnreadCount);
  const isAdmin = user?.role === "admin";

  return (
    <aside className="hidden md:flex md:flex-col w-60 shrink-0 border-r border-slate-800 bg-slate-950 h-screen sticky top-0 py-6 px-4">
      <div className="px-2 mb-8">
        <span className="font-display font-bold text-lg text-white">daily<span className="text-amber-500">.dev</span></span>
        <p className="text-[11px] text-slate-500 mt-0.5">Moringa School</p>
      </div>

      <nav className="flex-1 space-y-1">
        {NAV_ITEMS.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition ${
                isActive
                  ? "bg-amber-500/10 text-amber-400 font-medium"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-900"
              }`
            }
          >
            <Icon className="w-4 h-4" strokeWidth={1.75} />
            {label}
            {label === "Notifications" && unread > 0 && (
              <span className="ml-auto bg-amber-500 text-slate-950 text-[10px] font-mono font-bold rounded-full px-1.5 py-0.5 min-w-[18px] text-center">
                {unread}
              </span>
            )}
          </NavLink>
        ))}

        {isAdmin && (
          <>
            <div className="pt-3 pb-1 px-3 text-[10px] font-mono uppercase tracking-wider text-slate-600">Admin</div>
            <NavLink
              to="/admin"
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition ${
                  isActive
                    ? "bg-sky-400/10 text-sky-400 font-medium"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-900"
                }`
              }
            >
              <ShieldCheck className="w-4 h-4" strokeWidth={1.75} />
              Admin dashboard
            </NavLink>
          </>
        )}
      </nav>
    </aside>
  );
}
