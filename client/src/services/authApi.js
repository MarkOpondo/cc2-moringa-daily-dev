const API_URL = 'http://localhost:5000/api/auth';

// Register a new user
export async function signUpUser(userData) {
  const response = await fetch(`${API_URL}/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData)
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || data.message || 'Registration failed.');
  }

  return data;
}

// Log an existing user in
export async function loginUser(credentials) {
  const response = await fetch(`${API_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials)
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || data.message || 'Login failed.');
  }

  return data;
}

// Request a password reset
export async function requestPasswordReset(email) {
  const response = await fetch(`${API_URL}/forgot-password`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email })
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.error || data.message || 'Password reset request failed.'
    );
  }

  return data;
}

// Reset password
export async function resetPassword(token, password) {
  const response = await fetch(`${API_URL}/reset-password`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      token,
      password
    })
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.error || data.message || 'Password reset failed.'
    );
  }

  return data;
}