import apiRequest from "./api";

export async function listComments(contentId) {
  return apiRequest(`/api/content/${contentId}/comments`);
}

export async function addComment(contentId, body, parentId = null) {
  return apiRequest(`/api/content/${contentId}/comments`, {
    method: "POST",
    requiresAuth: true,
    body: JSON.stringify({ body, parentId }),
  });
}

export async function updateComment(commentId, body) {
  return apiRequest(`/api/comments/${commentId}`, {
    method: "PATCH",
    requiresAuth: true,
    body: JSON.stringify({ body }),
  });
}

export async function deleteComment(commentId) {
  return apiRequest(`/api/comments/${commentId}`, {
    method: "DELETE",
    requiresAuth: true,
  });
}
