import apiRequest from "./api";

export async function register({ username, email, password }) {
  return apiRequest("/api/auth/register", {
    method: "POST",
    body: JSON.stringify({
      username,
      email,
      password,
    }),
  });
}

export async function signUpUser({ username, email, password }) {
  return register({ username, email, password });
}

export async function login({ username, password }) {
  const data = await apiRequest("/api/auth/login", {
    method: "POST",
    body: JSON.stringify({
      username,
      password,
    }),
  });

  if (data?.token) {
    localStorage.setItem("token", data.token);
  }

  if (data?.user) {
    localStorage.setItem("user", JSON.stringify(data.user));
  }

  return data;
}

export async function loginUser({ username, password }) {
  return login({ username, password });
}

export async function logout() {
  try {
    await apiRequest("/api/auth/logout", {
      method: "POST",
    });
  } finally {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
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
    body: JSON.stringify({
      token,
      password,
    }),
  });
}
