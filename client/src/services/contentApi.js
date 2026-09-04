import apiRequest from "./api";

export async function listContent({ categoryId, search, status } = {}) {
  const params = new URLSearchParams();
  if (categoryId) params.set("category", categoryId);
  if (search) params.set("search", search);
  if (status) params.set("status", status);
  const query = params.toString();
  return apiRequest(`/api/content${query ? `?${query}` : ""}`);
}

export async function getContent(id) {
  return apiRequest(`/api/content/${id}`);
}

export async function createContent({ title, body, type, mediaUrl, categoryId }) {
  return apiRequest("/api/content", {
    method: "POST",
    requiresAuth: true,
    body: JSON.stringify({ title, body, type, mediaUrl: mediaUrl || null, categoryId }),
  });
}

export async function updateContent(id, values) {
  return apiRequest(`/api/content/${id}`, {
    method: "PATCH",
    requiresAuth: true,
    body: JSON.stringify(values),
  });
}

export async function deleteContent(id) {
  return apiRequest(`/api/content/${id}`, {
    method: "DELETE",
    requiresAuth: true,
  });
}

export async function react(contentId, type) {
  return apiRequest(`/api/content/${contentId}/reactions`, {
    method: "POST",
    requiresAuth: true,
    body: JSON.stringify({ type }),
  });
}

export async function reactionSummary(contentId) {
  return apiRequest(`/api/content/${contentId}/reactions`);
}
