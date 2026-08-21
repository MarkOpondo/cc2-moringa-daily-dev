import { useState } from "react";
import { CornerDownRight } from "lucide-react";
import { timeAgo } from "../../utils/format";
import Avatar from "../ui/Avatar";
import RoleBadge from "../ui/RoleBadge";

export default function CommentThread({ comment, onReply, depth = 0 }) {
  const [replying, setReplying] = useState(false);
  const [replyText, setReplyText] = useState("");

  async function submitReply(e) {
    e.preventDefault();
    if (!replyText.trim()) return;
    await onReply(comment.id, replyText.trim());
    setReplyText("");
    setReplying(false);
  }

  return (
    <div className={depth > 0 ? "ml-6 pl-4 border-l border-slate-800" : ""}>
      <div className="flex gap-3">
        <Avatar username={comment.author?.username} role={comment.author?.role} size="sm" />
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-slate-200">{comment.author?.username}</span>
            <RoleBadge role={comment.author?.role} />
            <span className="text-[11px] text-slate-500 font-mono">{timeAgo(comment.createdAt)}</span>
          </div>
          <p className="text-sm text-slate-300 mt-0.5">{comment.body}</p>
          <button
            onClick={() => setReplying((v) => !v)}
            className="flex items-center gap-1 text-[11px] text-slate-500 hover:text-amber-400 mt-1.5"
          >
            <CornerDownRight className="w-3 h-3" /> Reply
          </button>

          {replying && (
            <form onSubmit={submitReply} className="mt-2 flex gap-2">
              <input
                autoFocus
                value={replyText}
                onChange={(e) => setReplyText(e.target.value)}
                placeholder={`Reply to ${comment.author?.username}…`}
                className="flex-1 px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-amber-500"
              />
              <button
                type="submit"
                className="px-3 py-1.5 bg-amber-500 hover:bg-amber-400 text-slate-950 text-xs font-semibold rounded-lg"
              >
                Reply
              </button>
            </form>
          )}

          {comment.replies?.length > 0 && (
            <div className="mt-3 space-y-3">
              {comment.replies.map((reply) => (
                <CommentThread key={reply.id} comment={reply} onReply={onReply} depth={depth + 1} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
