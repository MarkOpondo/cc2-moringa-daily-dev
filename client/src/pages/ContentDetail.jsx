import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { useSelector } from "react-redux";
import { ThumbsUp, ThumbsDown, Bookmark, Share2, Flag, Video, Headphones, FileText, Check } from "lucide-react";
import { getContent, react, reactionSummary, toggleWishlist, isWishlisted } from "../services/contentApi";
import { listComments, addComment, updateComment, deleteComment } from "../services/commentsApi";
import { reportContent } from "../services/adminApi";
import { selectCurrentUser } from "../features/auth/authSlice";
import { categoryColor } from "../utils/categoryColors";
import { timeAgo } from "../utils/format";
import Avatar from "../components/ui/Avatar";
import RoleBadge from "../components/ui/RoleBadge";
import CommentThread from "../components/content/CommentThread";
import MediaPlayer from "../components/content/MediaPlayer";
import { ContentCardSkeleton } from "../components/ui/Skeleton";

const TYPE_ICON = { video: Video, audio: Headphones, article: FileText };

export default function ContentDetail() {
  const { id } = useParams();
  const user = useSelector(selectCurrentUser);
  const [item, setItem] = useState(null);
  const [comments, setComments] = useState([]);
  const [reactionState, setReactionState] = useState({ likes: 0, dislikes: 0, userReaction: null });
  const [saved, setSaved] = useState(false);
  const [newComment, setNewComment] = useState("");
  const [copied, setCopied] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      setLoading(true);
      const [contentItem, commentTree] = await Promise.all([getContent(id), listComments(id)]);
      if (cancelled) return;
      setItem(contentItem);
      setComments(commentTree);
      setReactionState(reactionSummary(id, user?.id));
      setSaved(isWishlisted(id, user?.id));
      setLoading(false);
    }
    load();
    return () => {
      cancelled = true;
    };
  }, [id, user?.id]);

  async function handleReact(type) {
    const summary = await react(id, user.id, type);
    setReactionState(summary);
  }

  async function handleWishlist() {
    const nowSaved = await toggleWishlist(id, user.id);
    setSaved(nowSaved);
  }

  async function handleShare() {
    try {
      await navigator.clipboard.writeText(window.location.href);
    } catch {
      // clipboard API may be unavailable — link copy is best-effort
    }
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  async function handleReport() {
    const reason = window.prompt("What's wrong with this content?");
    if (reason) {
      await reportContent(id, user.id, reason);
      window.alert("Thanks — this has been flagged for review.");
    }
  }

  async function handleTopLevelComment(e) {
    e.preventDefault();
    if (!newComment.trim()) return;
    await addComment(id, user.id, newComment.trim());
    setNewComment("");
    const tree = await listComments(id);
    setComments(tree);
  }

  async function handleReply(parentId, body) {
    await addComment(id, user.id, body, parentId);
    const tree = await listComments(id);
    setComments(tree);
  }

  async function handleEditComment(commentId, newBody) {
    await updateComment(commentId, newBody);
    const tree = await listComments(id);
    setComments(tree);
  }

  async function handleDeleteComment(commentId) {
    await deleteComment(commentId);
    const tree = await listComments(id);
    setComments(tree);
  }

  if (loading) return <ContentCardSkeleton />;
  if (!item) return <p className="text-slate-400">This post couldn't be found.</p>;

  const colors = categoryColor(item.category?.name);
  const TypeIcon = TYPE_ICON[item.type] || FileText;

  return (
    <article className="space-y-8">
      <div>
        <Link to="/" className="text-xs text-slate-400 hover:text-slate-300">← Back to feed</Link>

        <div className="flex items-center gap-2 mt-4 mb-2">
          <span className={`text-[11px] font-mono uppercase tracking-wide ${colors.text}`}>{item.category?.name}</span>
          <span className="text-slate-300">·</span>
          <TypeIcon className="w-3.5 h-3.5 text-slate-400" />
          <span className="text-[11px] text-slate-400 capitalize">{item.type}</span>
        </div>

        <h1 className="text-3xl font-display font-bold text-cream leading-tight">{item.title}</h1>

        <div className="flex items-center gap-2 mt-4">
          <Avatar username={item.author?.username} role={item.author?.role} />
          <div>
            <div className="flex items-center gap-2">
              <span className="text-sm font-medium text-cream">{item.author?.username}</span>
              <RoleBadge role={item.author?.role} />
            </div>
            <span className="text-[11px] text-slate-400 font-mono">{timeAgo(item.createdAt)}</span>
          </div>
        </div>
      </div>

      {(item.type === "video" || item.type === "audio") && (
        <MediaPlayer type={item.type} url={item.mediaUrl} />
      )}

      <div className="prose-content text-slate-300 leading-relaxed whitespace-pre-line text-[15px]">
        {item.body}
      </div>

      <div className="flex items-center gap-2 py-4 border-y border-navy-border">
        <button
          onClick={() => handleReact("like")}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium border transition ${
            reactionState.userReaction === "like"
              ? "bg-brand-500/10 border-brand-500/40 text-brand-600"
              : "border-navy-border text-slate-400 hover:border-navy-border"
          }`}
        >
          <ThumbsUp className="w-3.5 h-3.5" /> {reactionState.likes}
        </button>
        <button
          onClick={() => handleReact("dislike")}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium border transition ${
            reactionState.userReaction === "dislike"
              ? "bg-red-500/10 border-red-500/40 text-red-400"
              : "border-navy-border text-slate-400 hover:border-navy-border"
          }`}
        >
          <ThumbsDown className="w-3.5 h-3.5" /> {reactionState.dislikes}
        </button>
        <button
          onClick={handleWishlist}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium border transition ${
            saved ? "bg-brand-500/10 border-brand-500/40 text-brand-600" : "border-navy-border text-slate-400 hover:border-navy-border"
          }`}
        >
          <Bookmark className="w-3.5 h-3.5" /> {saved ? "Saved" : "Save"}
        </button>
        <button
          onClick={handleShare}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium border border-navy-border text-slate-400 hover:border-navy-border transition"
        >
          {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Share2 className="w-3.5 h-3.5" />}
          {copied ? "Link copied" : "Share"}
        </button>
        <button
          onClick={handleReport}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-slate-400 hover:text-red-400 ml-auto"
        >
          <Flag className="w-3.5 h-3.5" /> Report
        </button>
      </div>

      <section className="space-y-5">
        <h2 className="text-sm font-semibold text-slate-300">
          Discussion <span className="text-slate-400 font-mono">({comments.length})</span>
        </h2>

        <form onSubmit={handleTopLevelComment} className="flex gap-2">
          <Avatar username={user?.username} role={user?.role} size="sm" />
          <input
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            placeholder="Add to the discussion…"
            className="flex-1 px-3.5 py-2 rounded-lg bg-navy-raised border border-navy-border text-sm text-cream placeholder:text-slate-400 focus:outline-none focus:border-brand-500"
          />
          <button type="submit" className="px-4 py-2 bg-brand-500 hover:bg-brand-600 text-slate-950 text-xs font-semibold rounded-lg">
            Post
          </button>
        </form>

        <div className="space-y-5">
          {comments.length === 0 ? (
            <p className="text-sm text-slate-400">No comments yet — start the discussion.</p>
          ) : (
            comments.map((comment) => (
              <CommentThread
                key={comment.id}
                comment={comment}
                onReply={handleReply}
                onEdit={handleEditComment}
                onDelete={handleDeleteComment}
              />
            ))
          )}
        </div>
      </section>
    </article>
  );
}
