import { comments, users, genId, delay } from "./mockData";

// Maps to: GET /api/content/:id/comments
export async function listComments(contentId) {
  await delay(300);

  const forContent = comments
    .filter((c) => c.contentId === contentId)
    .map(hydrate)
    .sort((a, b) => new Date(a.createdAt) - new Date(b.createdAt));

  const byId = Object.fromEntries(
    forContent.map((c) => [c.id, { ...c, replies: [] }])
  );

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

// Maps to: POST /api/content/:id/comments
export async function addComment(
  contentId,
  userId,
  body,
  parentCommentId = null
) {
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

// Maps to: DELETE /api/comments/:id
export async function deleteComment(commentId) {
  await delay(250);

  const index = comments.findIndex((c) => c.id === commentId);

  if (index === -1) {
    throw new Error("Comment not found");
  }

  comments.splice(index, 1);

  return { success: true };
}
// Maps to: PATCH /api/comments/:id
export async function updateComment(commentId, body) {
  await delay(250);

  const comment = comments.find((c) => c.id === commentId);

  if (!comment) {
    throw new Error("Comment not found");
  }

  comment.body = body;

  return hydrate(comment);
}

function hydrate(c) {
  const user = users.find((u) => u.id === c.userId);

  return {
    ...c,
    author: user
      ? {
          id: user.id,
          username: user.username,
          role: user.role,
        }
      : null,
  };
}