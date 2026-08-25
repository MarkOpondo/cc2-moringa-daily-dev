import { Link } from "react-router-dom";
import { MessageSquare, ThumbsUp, Video, Headphones, FileText } from "lucide-react";
import { categoryColor } from "../../utils/categoryColors";
import { timeAgo } from "../../utils/format";
import Avatar from "../ui/Avatar";
import RoleBadge from "../ui/RoleBadge";

const TYPE_ICON = { video: Video, audio: Headphones, article: FileText };

export default function ContentCard({ item, commentCount }) {
  const colors = categoryColor(item.category?.name);
  const TypeIcon = TYPE_ICON[item.type] || FileText;

  return (
    <Link
      to={`/content/${item.id}`}
      className="group flex gap-4 p-4 rounded-xl border border-slate-800 bg-slate-900/40 hover:bg-slate-900 hover:border-slate-700 transition"
    >
      <div className={`w-1 shrink-0 rounded-full ${colors.bg}`} aria-hidden="true" />

      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-1.5">
          <span className={`text-[11px] font-mono uppercase tracking-wide ${colors.text}`}>
            {item.category?.name}
          </span>
          <span className="text-slate-700">·</span>
          <TypeIcon className="w-3 h-3 text-slate-500" strokeWidth={1.75} />
          <span className="text-[11px] text-slate-500">
            {item.type ? item.type.charAt(0).toUpperCase() + item.type.slice(1) : ""}
          </span>
          {item.status && item.status !== "approved" && (
            <span className="text-[10px] font-mono uppercase text-amber-500 border border-amber-500/30 rounded px-1.5 py-0.5 ml-auto">
              {item.status}
            </span>
          )}
        </div>

        <h3 className="font-display font-semibold text-slate-100 group-hover:text-white leading-snug">
          {item.title}
        </h3>
        <p className="text-sm text-slate-500 mt-1 line-clamp-2">{item.body}</p>

        <div className="flex items-center gap-3 mt-3 text-[11px] text-slate-500 font-mono">
          <div className="flex items-center gap-1.5">
            <Avatar username={item.author?.username} role={item.author?.role} size="sm" />
            <span className="text-slate-400">{item.author?.username}</span>
            <RoleBadge role={item.author?.role} />
          </div>
          <span>·</span>
          <span>{timeAgo(item.createdAt)}</span>
          {(item.type === "video" || item.type === "audio") && item.duration && (
            <>
              <span>·</span>
              <span>{item.duration}</span>
            </>
          )}
          {item.type === "article" && item.readTime && (
            <>
              <span>·</span>
              <span>{item.readTime}</span>
            </>
          )}
          <span className="ml-auto flex items-center gap-3">
            <span className="flex items-center gap-1">
              <ThumbsUp className="w-3 h-3" /> {item.likes ?? 0}
            </span>
            {commentCount !== undefined && (
              <span className="flex items-center gap-1">
                <MessageSquare className="w-3 h-3" /> {commentCount}
              </span>
            )}
          </span>
        </div>
      </div>
    </Link>
  );
}
