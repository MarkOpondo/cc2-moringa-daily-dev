import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";
import { Menu, Search, Plus, Bell, Rss } from "lucide-react";
import { selectCurrentUser } from "../../features/auth/authSlice";
import { selectUnreadCount } from "../../features/notifications/notificationsSlice";
import Avatar from "../ui/Avatar";
import NavDrawer from "./NavDrawer";

export default function Topbar({ search, onSearchChange }) {
  const user = useSelector(selectCurrentUser);
  const unread = useSelector(selectUnreadCount);
  const navigate = useNavigate();
  const [drawerOpen, setDrawerOpen] = useState(false);

  return (
    <>
      <header className="sticky top-0 z-20 bg-navy border-b border-navy-border">
        <div className="flex items-center gap-4 px-4 sm:px-6 py-3">
          <button
            onClick={() => setDrawerOpen(true)}
            className="text-slate-400 hover:text-cream shrink-0"
            aria-label="Open menu"
          >
            <Menu className="w-6 h-6" strokeWidth={1.75} />
          </button>

          <button
            onClick={() => navigate("/")}
            className="flex items-center gap-2 shrink-0"
          >
            <span className="w-8 h-8 rounded-lg bg-brand-500 flex items-center justify-center">
              <Rss className="w-4 h-4 text-slate-950" strokeWidth={2.25} />
            </span>
            <span className="font-display italic font-bold text-lg text-cream hidden sm:inline">
              MoringaHub
            </span>
          </button>

          <div className="relative flex-1 max-w-xl">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="search"
              value={search}
              onChange={(e) => onSearchChange?.(e.target.value)}
              placeholder="Search articles, videos, topics…"
              className="w-full pl-10 pr-4 py-2.5 rounded-full bg-navy-raised border border-navy-border text-sm text-cream placeholder:text-slate-400 focus:outline-none focus:border-brand-500"
            />
          </div>

          <button
            onClick={() => navigate("/create")}
            className="hidden sm:flex items-center gap-1.5 px-4 py-2 rounded-full bg-brand-500 hover:bg-brand-600 text-slate-950 text-sm font-semibold transition shrink-0"
          >
            <Plus className="w-4 h-4" strokeWidth={2.5} /> Write
          </button>

          <button
            onClick={() => navigate("/notifications")}
            className="relative text-slate-400 hover:text-cream shrink-0"
            aria-label="Notifications"
          >
            <Bell className="w-5 h-5" strokeWidth={1.75} />
            {unread > 0 && (
              <span className="absolute -top-0.5 -right-0.5 w-2.5 h-2.5 rounded-full bg-brand-500 ring-2 ring-navy" />
            )}
          </button>

          <button onClick={() => navigate("/profile")} className="shrink-0">
            <Avatar username={user?.username} role={user?.role} />
          </button>
        </div>
      </header>

      <NavDrawer open={drawerOpen} onClose={() => setDrawerOpen(false)} />
    </>
  );
}
