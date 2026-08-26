import apiRequest from "./api";

export async function getProfile() {
  return apiRequest("/api/profiles/me");
}

export async function fetchProfile() {
  return getProfile();
}

export async function updateProfile({
  bio,
  interests,
  profileImage,
}) {
  return apiRequest("/api/profiles/me", {
    method: "PUT",
    body: JSON.stringify({
      bio,
      interests,
      profile_image: profileImage,
    }),
  });
}
