import { content, users, categories, reactions, wishlist, genId, delay } from "./mockData";

// Maps to: GET /api/content?category=&search=&status=
// Returns approved content by default (the public feed); pass includeAll
// for admin/tech-writer views that also need pending/flagged items.
export async function listContent({ categoryId, search, includeAll = false } = {}) {
  await delay();
  let results = content.filter((c) => (includeAll ? true : c.status === "approved"));
  if (categoryId) results = results.filter((c) => c.categoryId === categoryId);
  if (search) {
    const q = search.toLowerCase();
    results = results.filter(
      (c) => c.title.toLowerCase().includes(q) || c.body.toLowerCase().includes(q)
    );
  }
  return results
    .slice()
    .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
    .map(hydrate);
}

// Maps to: GET /api/content/:id
export async function getContent(id) {
  await delay();
  const item = content.find((c) => c.id === id);
  return item ? hydrate(item) : null;
}

// Maps to: POST /api/content
export async function createContent({ title, body, type, mediaUrl, categoryId, authorId }) {
  await delay();
  const item = {
    id: genId(),
    title,
    body,
    type,
    mediaUrl: mediaUrl || "",
    authorId,
    categoryId,
    status: "pending",
    createdAt: new Date().toISOString(),
  };
  content.unshift(item);
  return hydrate(item);
}

// Maps to: PATCH /api/content/:id/approve
export async function approveContent(id) {
  await delay(200);
  const item = content.find((c) => c.id === id);
  if (item) item.status = "approved";
  return item ? hydrate(item) : null;
}

// Maps to: PATCH /api/content/:id/flag
export async function flagContent(id) {
  await delay(200);
  const item = content.find((c) => c.id === id);
  if (item) item.status = "flagged";
  return item ? hydrate(item) : null;
}

// Maps to: POST /api/content/:id/reactions  (type: 'like' | 'dislike')
// Toggles: reacting again with the same type removes it; a different type replaces it.
export async function react(contentId, userId, type) {
  await delay(150);
  const existingIndex = reactions.findIndex((r) => r.contentId === contentId && r.userId === userId);
  if (existingIndex >= 0) {
    if (reactions[existingIndex].type === type) {
      reactions.splice(existingIndex, 1);
    } else {
      reactions[existingIndex].type = type;
    }
  } else {
    reactions.push({ id: genId(), userId, contentId, type });
  }
  return reactionSummary(contentId, userId);
}

export function reactionSummary(contentId, userId) {
  const forContent = reactions.filter((r) => r.contentId === contentId);
  return {
    likes: forContent.filter((r) => r.type === "like").length,
    dislikes: forContent.filter((r) => r.type === "dislike").length,
    userReaction: forContent.find((r) => r.userId === userId)?.type || null,
  };
}

// Maps to: POST /api/wishlist  /  DELETE /api/wishlist/:id
export async function toggleWishlist(contentId, userId) {
  await delay(150);
  const idx = wishlist.findIndex((w) => w.contentId === contentId && w.userId === userId);
  if (idx >= 0) {
    wishlist.splice(idx, 1);
    return false;
  }
  wishlist.push({ id: genId(), userId, contentId });
  return true;
}

export function isWishlisted(contentId, userId) {
  return wishlist.some((w) => w.contentId === contentId && w.userId === userId);
}

// Maps to: GET /api/users/me/wishlist
export async function listWishlist(userId) {
  await delay();
  const ids = wishlist.filter((w) => w.userId === userId).map((w) => w.contentId);
  return content.filter((c) => ids.includes(c.id)).map(hydrate);
}

// Attaches author/category display info + reaction counts to a raw content row,
// the way a real API response would after a JOIN.
function hydrate(item) {
  const author = users.find((u) => u.id === item.authorId);
  const category = categories.find((c) => c.id === item.categoryId);
  const forContent = reactions.filter((r) => r.contentId === item.id);
  return {
    ...item,
    author: author ? { id: author.id, username: author.username, role: author.role } : null,
    category: category ? { id: category.id, name: category.name } : null,
    likes: forContent.filter((r) => r.type === "like").length,
    dislikes: forContent.filter((r) => r.type === "dislike").length,
  };
}
