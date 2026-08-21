import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { Search, LogOut, User as UserIcon, FlaskConical } from "lucide-react";
import { selectCurrentUser, selectIsPreview, setPreviewRole, logout } from "../../features/auth/authSlice";
import { roleLabel } from "../../utils/format";
import Avatar from "../ui/Avatar";

export default function Topbar({ search, onSearchChange }) {
  const user = useSelector(selectCurrentUser);
  const isPreview = useSelector(selectIsPreview);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);

  function handleLogout() {
    dispatch(logout());
    navigate("/login");
  }

  return (
    <header className="sticky top-0 z-10 flex items-center gap-4 px-6 py-4 border-b border-slate-800 bg-slate-950/90 backdrop-blur">
      <div className="relative flex-1 max-w-md">
        <Search className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
        <input
          type="search"
          value={search}
          onChange={(e) => onSearchChange?.(e.target.value)}
          placeholder="Search articles, videos, audio…"
          className="w-full pl-9 pr-3 py-2 rounded-lg bg-slate-900 border border-slate-800 text-sm text-white placeholder:text-slate-500 focus:outline-none focus:border-amber-500"
        />
      </div>

      {/* Dev-only: lets anyone browsing this repo preview role-gated UI
          before real backend auth exists. Never rendered in production
          builds (import.meta.env.DEV is false there). */}
      {isPreview && (
        <label className="hidden lg:flex items-center gap-2 text-[11px] text-slate-500 border border-dashed border-slate-700 rounded-lg px-2.5 py-1.5">
          <FlaskConical className="w-3.5 h-3.5 text-amber-500" />
          Preview as
          <select
            value={user?.role}
            onChange={(e) => dispatch(setPreviewRole(e.target.value))}
            className="bg-transparent text-slate-300 font-mono text-[11px] focus:outline-none"
          >
            <option value="admin">Admin</option>
            <option value="tech_writer">Tech Writer</option>
            <option value="user">User</option>
          </select>
        </label>
      )}

      <div className="relative">
        <button
          onClick={() => setMenuOpen((v) => !v)}
          className="flex items-center gap-2"
          aria-label="Account menu"
        >
          <Avatar username={user?.username} role={user?.role} />
        </button>

        {menuOpen && (
          <div
            className="absolute right-0 mt-2 w-52 bg-slate-900 border border-slate-800 rounded-xl shadow-2xl py-1.5 text-sm"
            onMouseLeave={() => setMenuOpen(false)}
          >
            <div className="px-3.5 py-2 border-b border-slate-800">
              <p className="text-slate-200 font-medium">{user?.username}</p>
              <p className="text-[11px] text-slate-500">{roleLabel(user?.role)}</p>
            </div>
            <Link
              to="/profile"
              onClick={() => setMenuOpen(false)}
              className="flex items-center gap-2 px-3.5 py-2 text-slate-300 hover:bg-slate-800"
            >
              <UserIcon className="w-3.5 h-3.5" /> Profile
            </Link>
            <button
              onClick={handleLogout}
              className="w-full flex items-center gap-2 px-3.5 py-2 text-red-400 hover:bg-slate-800 text-left"
            >
              <LogOut className="w-3.5 h-3.5" /> Log out
            </button>
          </div>
        )}
      </div>
    </header>
  );
}
