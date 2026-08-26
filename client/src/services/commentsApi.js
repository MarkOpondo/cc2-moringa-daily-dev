import apiRequest from "./api";

export async function listComments(contentId) {
  return apiRequest(`/api/content/${contentId}/comments`);
}

export async function addComment(
  contentId,
  body,
  parentCommentId = null
) {
  return apiRequest(`/api/content/${contentId}/comments`, {
    method: "POST",
    body: JSON.stringify({
      text: body,
      parent_comment_id: parentCommentId,
    }),
  });
}

export async function updateComment(commentId, body) {
  return apiRequest(`/api/comments/${commentId}`, {
    method: "PATCH",
    body: JSON.stringify({
      text: body,
    }),
  });
}

export async function deleteComment(commentId) {
  return apiRequest(`/api/comments/${commentId}`, {
    method: "DELETE",
  });
}