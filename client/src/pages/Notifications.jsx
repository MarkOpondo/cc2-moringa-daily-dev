import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Link } from "react-router-dom";
import { Bell, BellOff } from "lucide-react";
import { fetchNotifications, markNotificationRead, markAllNotificationsRead } from "../features/notifications/notificationsSlice";
import { selectCurrentUser } from "../features/auth/authSlice";
import { timeAgo } from "../utils/format";
import EmptyState from "../components/ui/EmptyState";
import Button from "../components/ui/Button";

export default function Notifications() {
  const user = useSelector(selectCurrentUser);
  const items = useSelector((state) => state.notifications.items);
  const dispatch = useDispatch();

  useEffect(() => {
    if (user?.id) dispatch(fetchNotifications(user.id));
  }, [dispatch, user?.id]);

  const unreadCount = items.filter((n) => !n.isRead).length;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs font-mono text-amber-500 mb-1">// notifications</p>
          <h1 className="text-2xl font-bold text-white">Notifications</h1>
        </div>
        {unreadCount > 0 && (
          <Button variant="ghost" size="sm" onClick={() => dispatch(markAllNotificationsRead(user.id))}>
            Mark all as read
          </Button>
        )}
      </div>

      {items.length === 0 ? (
        <EmptyState
          icon={BellOff}
          title="You're all caught up"
          description="Subscribe to categories to hear about new posts as they're published."
        />
      ) : (
        <div className="divide-y divide-slate-800 border border-slate-800 rounded-xl overflow-hidden">
          {items.map((n) => (
            <Link
              key={n.id}
              to={n.contentId ? `/content/${n.contentId}` : "#"}
              onClick={() => !n.isRead && dispatch(markNotificationRead(n.id))}
              className={`flex items-start gap-3 p-4 hover:bg-slate-900/60 transition ${
                !n.isRead ? "bg-amber-500/5" : ""
              }`}
            >
              <Bell className={`w-4 h-4 mt-0.5 shrink-0 ${!n.isRead ? "text-amber-500" : "text-slate-600"}`} />
              <div className="flex-1 min-w-0">
                <p className={`text-sm ${!n.isRead ? "text-slate-100" : "text-slate-400"}`}>{n.message}</p>
                <p className="text-[11px] text-slate-500 font-mono mt-0.5">{timeAgo(n.createdAt)}</p>
              </div>
              {!n.isRead && <span className="w-2 h-2 rounded-full bg-amber-500 mt-1.5 shrink-0" />}
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
