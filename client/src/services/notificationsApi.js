import apiRequest from "./api";

const auth = { requiresAuth: true };

export async function listNotifications() {
  return apiRequest("/api/notifications", auth);
}

export async function markRead(notificationId) {
  return apiRequest(`/api/notifications/${notificationId}/read`, {
    method: "PATCH",
    requiresAuth: true,
  });
}

export async function markAllRead() {
  return apiRequest("/api/notifications/read-all", {
    method: "PATCH",
    requiresAuth: true,
  });
}
