import apiRequest from "./api";

export async function listUsers() {
  return apiRequest("/api/admin/users");
}

export async function addUser({ username, email, password, role }) {
  return apiRequest("/api/admin/users", {
    method: "POST",
    body: JSON.stringify({ username, email, password, role }),
  });
}

export async function toggleUserActive(id) {
  return apiRequest(`/api/admin/users/${id}/status`, { method: "PATCH" });
}

export async function listPendingContent() {
  return apiRequest("/api/admin/content?status=draft");
}

export async function updateContentStatus(id, status, reason) {
  return apiRequest(`/api/admin/content/${id}/status`, {
    method: "PATCH",
    body: JSON.stringify({ status, reason }),
  });
}

export async function listReports() {
  return apiRequest("/api/admin/reports");
}

export async function resolveReport(id) {
  return apiRequest(`/api/admin/reports/${id}`, { method: "PATCH" });
}

export async function reportContent(contentId, reason) {
  return apiRequest(`/api/content/${contentId}/report`, {
    method: "POST",
    body: JSON.stringify({ reason }),
  });
}
