import apiRequest from "./api";
import { clearAuthStorage, persistAuth } from "./authStorage";

export async function register({ username, email, password }) {
  const data = await apiRequest("/api/auth/register", {
    method: "POST",
    body: JSON.stringify({ username, email, password }),
  });
  return persistAuth(data);
}

export async function signUpUser(values) {
  return register(values);
}

export async function login({ identifier, username, password }) {
  const data = await apiRequest("/api/auth/login", {
    method: "POST",
    body: JSON.stringify({ identifier: identifier || username, password }),
  });
  return persistAuth(data);
}

export async function loginUser(values) {
  return login(values);
}

export async function logout() {
  try {
    await apiRequest("/api/auth/logout", { method: "POST" });
  } finally {
    clearAuthStorage();
  }
}

export async function requestPasswordReset(email) {
  return apiRequest("/api/auth/forgot-password", {
    method: "POST",
    body: JSON.stringify({ email }),
  });
}

export async function resetPassword(token, password) {
  return apiRequest("/api/auth/reset-password", {
    method: "POST",
    body: JSON.stringify({ token, password }),
  });
}
