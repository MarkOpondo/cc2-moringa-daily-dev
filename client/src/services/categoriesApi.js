import { categories, subscriptions, content, genId, delay } from "./mockData";

// Maps to: GET /api/categories
export async function listCategories() {
  await delay(200);
  return categories.map((cat) => ({
    ...cat,
    contentCount: content.filter((c) => c.categoryId === cat.id && c.status === "approved").length,
  }));
}

// Maps to: GET /api/users/me/subscriptions
export async function listSubscriptions(userId) {
  await delay(200);
  return subscriptions.filter((s) => s.userId === userId).map((s) => s.categoryId);
}

// Maps to: POST /api/subscriptions  /  DELETE /api/subscriptions/:id
export async function toggleSubscription(categoryId, userId) {
  await delay(150);
  const idx = subscriptions.findIndex((s) => s.categoryId === categoryId && s.userId === userId);
  if (idx >= 0) {
    subscriptions.splice(idx, 1);
    return false;
  }
  subscriptions.push({ id: genId(), userId, categoryId });
  return true;
}

// Maps to: POST /api/categories  (admin / tech writer)
export async function createCategory({ name, description, createdBy }) {
  await delay(300);
  const cat = { id: genId(), name, description, createdBy };
  categories.push(cat);
  return cat;
}
