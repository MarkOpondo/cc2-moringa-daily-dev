import apiRequest from "./api";

export async function listSubscriptions() {
  return apiRequest("/api/subscriptions", { requiresAuth: true });
}

export async function subscribe(categoryId) {
  return apiRequest("/api/subscriptions", {
    method: "POST",
    requiresAuth: true,
    body: JSON.stringify({ categoryId }),
  });
}

export async function unsubscribe(categoryId) {
  return apiRequest(`/api/subscriptions/${categoryId}`, {
    method: "DELETE",
    requiresAuth: true,
  });
}
