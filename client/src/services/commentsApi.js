import { comments, users, genId, delay } from "./mockData";

// Maps to: GET /api/content/:id/comments
// Returns a nested tree (replies inside parents) rather than a flat list,
// since the UI renders threads recursively — building the tree here keeps
// that logic out of components.
export async function listComments(contentId) {
  await delay(300);
  const forContent = comments
    .filter((c) => c.contentId === contentId)
    .map(hydrate)
    .sort((a, b) => new Date(a.createdAt) - new Date(b.createdAt));

  const byId = Object.fromEntries(forContent.map((c) => [c.id, { ...c, replies: [] }]));
  const roots = [];
  for (const c of forContent) {
    if (c.parentCommentId && byId[c.parentCommentId]) {
      byId[c.parentCommentId].replies.push(byId[c.id]);
    } else {
      roots.push(byId[c.id]);
    }
  }
  return roots;
}

// Maps to: POST /api/content/:id/comments  (body includes parent_comment_id for replies)
export async function addComment(contentId, userId, body, parentCommentId = null) {
  await delay(250);
  const comment = {
    id: genId(),
    contentId,
    userId,
    parentCommentId,
    body,
    createdAt: new Date().toISOString(),
  };
  comments.push(comment);
  return hydrate(comment);
}

function hydrate(c) {
  const user = users.find((u) => u.id === c.userId);
  return { ...c, author: user ? { id: user.id, username: user.username, role: user.role } : null };
}
