const API_URL = 'http://localhost:5000/api/profile';

const getAuthHeader = () => {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
  };
};

export const fetchProfile = async () => {
  const res = await fetch(API_URL, {
    method: 'GET',
    headers: getAuthHeader(),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.message || 'Failed to fetch profile');
  return data;
};

export const updateProfile = async (profileData) => {
  const res = await fetch(API_URL, {
    method: 'PUT',
    headers: getAuthHeader(),
    body: JSON.stringify(profileData),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.message || 'Failed to update profile');
  return data;
};