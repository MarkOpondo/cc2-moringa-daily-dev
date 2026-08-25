import { users, content, reports, categories, genId, delay } from "./mockData";

// Maps to: GET /api/users  (admin)
export async function listUsers() {
  await delay(300);
  return users.slice();
}

// Maps to: POST /api/users  (admin)
export async function addUser({ username, email, role }) {
  await delay(300);
  const user = { id: genId(), username, email, role, isActive: true, createdAt: new Date().toISOString() };
  users.push(user);
  return user;
}

// Maps to: PATCH /api/users/:id/deactivate  (admin)
export async function toggleUserActive(id) {
  await delay(200);
  const user = users.find((u) => u.id === id);
  if (user) user.isActive = !user.isActive;
  return user;
}

// Maps to: GET /api/content?status=pending  (moderation queue, admin/tech writer)
export async function listPendingContent() {
  await delay(300);
  return content
    .filter((c) => c.status === "pending" || c.status === "flagged")
    .map((c) => ({
      ...c,
      author: users.find((u) => u.id === c.authorId),
      category: categories.find((cat) => cat.id === c.categoryId),
    }));
}

// Maps to: GET /api/reports  (admin)
export async function listReports() {
  await delay(300);
  return reports.map((r) => ({
    ...r,
    content: content.find((c) => c.id === r.contentId),
    reporter: users.find((u) => u.id === r.reportedBy),
  }));
}

// Maps to: PATCH /api/reports/:id  (admin resolves)
export async function resolveReport(id, status = "resolved") {
  await delay(200);
  const report = reports.find((r) => r.id === id);
  if (report) report.status = status;
  return report;
}

// Maps to: POST /api/content/:id/report  (any user)
export async function reportContent(contentId, reportedBy, reason) {
  await delay(250);
  const report = { id: genId(), contentId, reportedBy, reason, status: "open", createdAt: new Date().toISOString() };
  reports.push(report);
  return report;
}
