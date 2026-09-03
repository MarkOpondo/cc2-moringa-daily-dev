import apiRequest from "./api";

export async function listContent({
  categoryId,
  search,
  status,
  includeAll = false,
} = {}) {
  const params = new URLSearchParams();

  if (categoryId) {
    params.set("category_id", categoryId);
  }

  if (search) {
    params.set("search", search);
  }

  if (status) {
    params.set("status", status);
  }

  if (includeAll) {
    params.set("include_all", "true");
  }

  const query = params.toString();

  return apiRequest(`/api/content${query ? `?${query}` : ""}`);
}

export async function getContent(id) {
  return apiRequest(`/api/content/${id}`);
}

export async function createContent({
  title,
  body,
  type,
  mediaUrl,
  categoryId,
}) {
  return apiRequest("/api/content", {
    method: "POST",
    body: JSON.stringify({
      title,
      description: body,
      type,
      url: mediaUrl || "",
      category_id: categoryId,
    }),
  });
}

export async function approveContent(id) {
  return apiRequest(`/api/content/${id}/approve`, {
    method: "PATCH",
  });
}

export async function flagContent(id) {
  return apiRequest(`/api/content/${id}/flag`, {
    method: "PATCH",
  });
}

export async function react(contentId, type) {
  return apiRequest(`/api/content/${contentId}/reactions`, {
    method: "POST",
    body: JSON.stringify({
      type,
    }),
  });
}

export async function reactionSummary(contentId) {
  return apiRequest(`/api/content/${contentId}/reactions`);
}