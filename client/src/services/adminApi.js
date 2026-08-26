import api from "./api";

// GET /api/users
export async function listUsers() {
  const response = await api.get("/users");
  return response.data;
}

// POST /api/users
export async function addUser({ username, email, role }) {
  const response = await api.post("/users", {
    username,
    email,
    role,
  });

  return response.data;
}

// PATCH /api/users/:id/deactivate
export async function toggleUserActive(id) {
  const response = await api.patch(`/users/${id}/deactivate`);
  return response.data;
}

// GET /api/content?status=pending
export async function listPendingContent() {
  const response = await api.get("/content", {
    params: {
      status: "pending",
    },
  });

  return response.data;
}

// GET /api/reports
export async function listReports() {
  const response = await api.get("/reports");
  return response.data;
}

// PATCH /api/reports/:id
export async function resolveReport(id, status = "resolved") {
  const response = await api.patch(`/reports/${id}`, {
    status,
  });

  return response.data;
}

// POST /api/content/:id/report
export async function reportContent(contentId, reason) {
  const response = await api.post(`/content/${contentId}/report`, {
    reason,
  });

  return response.data;
}