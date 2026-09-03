const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:5001";

export async function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem("token");

  const isFormData =
    typeof FormData !== "undefined" && options.body instanceof FormData;

  // Never set Content-Type for FormData — the browser must add the boundary.
  const headers = {
    ...(isFormData ? {} : { "Content-Type": "application/json" }),
    ...(options.headers || {}),
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  let data = null;

  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    throw new Error(
      data?.error ||
        data?.message ||
        `Request failed with status ${response.status}`
    );
  }

  return data;
}

export default apiRequest;
