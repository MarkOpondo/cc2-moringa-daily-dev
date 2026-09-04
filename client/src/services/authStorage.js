const TOKEN_STORAGE_KEYS = ["token", "access_token", "accessToken", "authToken"];
const TOKEN_FIELDS = ["token", "access_token", "accessToken", "authToken"];

function tokenFromValue(value) {
  if (typeof value !== "string") return null;
  const token = value.trim();
  return token && token !== "undefined" && token !== "null" ? token : null;
}

function tokenFromObject(value) {
  if (!value || typeof value !== "object") return null;

  for (const field of TOKEN_FIELDS) {
    const token = tokenFromValue(value[field]);
    if (token) return token;
  }

  return tokenFromObject(value.auth) || tokenFromObject(value.session);
}

function parseStoredValue(key) {
  try {
    return JSON.parse(localStorage.getItem(key));
  } catch {
    return null;
  }
}

export function getAuthToken() {
  for (const key of TOKEN_STORAGE_KEYS) {
    const token = tokenFromValue(localStorage.getItem(key));
    if (token) {
      // Keep one canonical key so newly mounted components and older code
      // see the same token even when a previous build used another key.
      if (key !== "token") localStorage.setItem("token", token);
      return token;
    }
  }

  const token = tokenFromObject(parseStoredValue("user"));
  if (token) localStorage.setItem("token", token);
  return token;
}

export function persistAuth(data) {
  const token = tokenFromValue(data?.token) || tokenFromObject(data);
  if (token) localStorage.setItem("token", token);
  if (data?.user) localStorage.setItem("user", JSON.stringify(data.user));
  return token && !data?.token ? { ...data, token } : data;
}

export function clearAuthStorage() {
  TOKEN_STORAGE_KEYS.forEach((key) => localStorage.removeItem(key));
  localStorage.removeItem("user");
}
