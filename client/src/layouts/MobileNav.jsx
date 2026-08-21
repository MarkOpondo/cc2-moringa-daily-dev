import { NavLink } from "react-router-dom";
import { Home, LayoutGrid, PlusCircle, Bell, Bookmark } from "lucide-react";

const ITEMS = [
  { to: "/", icon: Home, end: true, label: "Feed" },
  { to: "/categories", icon: LayoutGrid, label: "Categories" },
  { to: "/create", icon: PlusCircle, label: "Post" },
  { to: "/notifications", icon: Bell, label: "Alerts" },
  { to: "/wishlist", icon: Bookmark, label: "Saved" },
];

export default function MobileNav() {
  return (
    <nav className="md:hidden fixed bottom-0 inset-x-0 z-10 bg-slate-950/95 backdrop-blur border-t border-slate-800 flex justify-around py-2">
      {ITEMS.map(({ to, icon: Icon, end, label }) => (
        <NavLink
          key={to}
          to={to}
          end={end}
          className={({ isActive }) =>
            `flex flex-col items-center gap-0.5 px-3 py-1 text-[10px] ${
              isActive ? "text-amber-400" : "text-slate-500"
            }`
          }
        >
          <Icon className="w-5 h-5" strokeWidth={1.75} />
          {label}
        </NavLink>
      ))}
    </nav>
  );
}
