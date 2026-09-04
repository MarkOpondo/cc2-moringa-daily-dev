import apiRequest from "./api";

const auth = { requiresAuth: true };

export async function listUsers() {
  return apiRequest("/api/admin/users", auth);
}

export async function addUser({ username, email, password, role }) {
  return apiRequest("/api/admin/users", {
    method: "POST",
    requiresAuth: true,
    body: JSON.stringify({ username, email, password, role }),
  });
}

export async function toggleUserActive(id) {
  return apiRequest(`/api/admin/users/${id}/status`, {
    method: "PATCH",
    requiresAuth: true,
  });
}

export async function listPendingContent() {
  return apiRequest("/api/admin/content?status=draft", auth);
}

export async function updateContentStatus(id, status, reason) {
  return apiRequest(`/api/admin/content/${id}/status`, {
    method: "PATCH",
    requiresAuth: true,
    body: JSON.stringify({ status, reason }),
  });
}

export async function listReports() {
  return apiRequest("/api/admin/reports", auth);
}

export async function resolveReport(id) {
  return apiRequest(`/api/admin/reports/${id}`, {
    method: "PATCH",
    requiresAuth: true,
  });
}

export async function reportContent(contentId, reason) {
  return apiRequest(`/api/content/${contentId}/report`, {
    method: "POST",
    requiresAuth: true,
    body: JSON.stringify({ reason }),
  });
}
