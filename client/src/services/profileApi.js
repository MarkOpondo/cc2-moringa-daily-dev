// get auth token from local storage
const getToken = () => localStorage.getItem('token');

// fetch current user profile data from the backend
export const fetchProfile = async () => {
  const token = getToken();
  
  const response = await fetch('/api/users/me', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.message || 'Failed to fetch profile');
  }

  return data;
};

// send updated profile details to the backend
export const updateProfile = async (profileData) => {
  const token = getToken();

  const response = await fetch('/api/users/me', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({
      bio: profileData.bio,
      interests: profileData.interests,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.message || 'Failed to update profile');
  }

  return data;
};