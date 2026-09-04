import apiRequest from "./api";

export async function listNotifications() {
  return apiRequest("/api/notifications");
}

export async function markRead(notificationId) {
  return apiRequest(`/api/notifications/${notificationId}/read`, { method: "PATCH" });
}

export async function markAllRead() {
  return apiRequest("/api/notifications/read-all", { method: "PATCH" });
}
