import { useState } from "react";
import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { createContent } from "../services/contentApi";
import { selectCurrentUser } from "../features/auth/authSlice";
import Button from "../components/ui/Button";

const TYPES = [
  { value: "article", label: "Article" },
  { value: "video", label: "Video" },
  { value: "audio", label: "Audio" },
];

export default function CreateContent() {
  const user = useSelector(selectCurrentUser);
  const categories = useSelector((state) => state.categories.items);
  const navigate = useNavigate();

  const [form, setForm] = useState({ title: "", body: "", type: "article", mediaUrl: "", categoryId: "" });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  function update(field, value) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!form.title.trim() || !form.body.trim() || !form.categoryId) {
      setError("Title, content, and a category are all required.");
      return;
    }
    if (form.type !== "article" && !form.mediaUrl.trim()) {
      setError(`Add a ${form.type} URL before publishing.`);
      return;
    }
    setError(null);
    setSubmitting(true);
    try {
      const created = await createContent({ ...form, authorId: user.id });
      navigate(`/content/${created.id}`);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="max-w-2xl">
      <p className="text-xs font-mono text-brand-500 mb-1">// new post</p>
      <h1 className="text-2xl font-bold text-navy mb-1">Share something with the community</h1>
      <p className="text-sm text-muted mb-6">
        Posts go to a review queue before appearing in the public feed — an admin or tech writer approves it first.
      </p>

      {error && (
        <div className="mb-4 p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm">{error}</div>
      )}

      <form onSubmit={handleSubmit} className="space-y-5 bg-white border border-line rounded-xl p-6">
        <div className="flex gap-2">
          {TYPES.map((t) => (
            <button
              type="button"
              key={t.value}
              onClick={() => update("type", t.value)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition ${
                form.type === t.value
                  ? "bg-brand-500 text-navy border-brand-500"
                  : "border-line text-muted hover:border-navy/30"
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>

        <div>
          <label className="block text-xs font-medium text-navy/70 mb-1">Title</label>
          <input
            value={form.title}
            onChange={(e) => update("title", e.target.value)}
            placeholder="A clear, specific title"
            className="w-full px-3.5 py-2.5 rounded-lg bg-white border border-line text-sm text-navy focus:outline-none focus:border-brand-500"
          />
        </div>

        <div>
          <label className="block text-xs font-medium text-navy/70 mb-1">Category</label>
          <select
            value={form.categoryId}
            onChange={(e) => update("categoryId", e.target.value)}
            className="w-full px-3.5 py-2.5 rounded-lg bg-white border border-line text-sm text-navy focus:outline-none focus:border-brand-500"
          >
            <option value="">Select a category…</option>
            {categories.map((c) => (
              <option key={c.id} value={c.id}>{c.name}</option>
            ))}
          </select>
        </div>

        {form.type !== "article" && (
          <div>
            <label className="block text-xs font-medium text-navy/70 mb-1">
              {form.type === "video" ? "Video URL" : "Audio URL"}
            </label>
            <input
              value={form.mediaUrl}
              onChange={(e) => update("mediaUrl", e.target.value)}
              placeholder="https://…"
              className="w-full px-3.5 py-2.5 rounded-lg bg-white border border-line text-sm text-navy focus:outline-none focus:border-brand-500"
            />
          </div>
        )}

        <div>
          <label className="block text-xs font-medium text-navy/70 mb-1">
            {form.type === "article" ? "Body" : "Description"}
          </label>
          <textarea
            value={form.body}
            onChange={(e) => update("body", e.target.value)}
            rows={form.type === "article" ? 10 : 4}
            placeholder={form.type === "article" ? "Write your article…" : "What's this piece about?"}
            className="w-full px-3.5 py-2.5 rounded-lg bg-white border border-line text-sm text-navy focus:outline-none focus:border-brand-500"
          />
        </div>

        <Button type="submit" size="lg" disabled={submitting}>
          {submitting ? "Submitting…" : "Submit for review"}
        </Button>
      </form>
    </div>
  );
}

