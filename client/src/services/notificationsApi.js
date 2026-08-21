import { notifications, delay } from "./mockData";

// Maps to: GET /api/users/me/notifications
export async function listNotifications(userId) {
  await delay(250);
  return notifications
    .filter((n) => n.userId === userId)
    .slice()
    .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
}

// Maps to: PATCH /api/notifications/:id/read
export async function markRead(id) {
  await delay(100);
  const n = notifications.find((n) => n.id === id);
  if (n) n.isRead = true;
  return n;
}

export async function markAllRead(userId) {
  await delay(150);
  notifications.filter((n) => n.userId === userId).forEach((n) => (n.isRead = true));
}
