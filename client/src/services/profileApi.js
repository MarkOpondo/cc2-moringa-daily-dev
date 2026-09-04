import apiRequest from "./api";

export async function getProfile() {
  return apiRequest("/api/profiles/me");
}

export async function fetchProfile() {
  const data = await getProfile();
  return {
    ...data,
    ...(data.user || {}),
    github_url: data.githubUrl,
    profile_image: data.profileImage,
  };
}

export async function updateProfile({ bio, interests, profileImage, skills, githubUrl }) {
  return apiRequest("/api/profiles/me", {
    method: "PUT",
    body: JSON.stringify({ bio, interests, profileImage, skills, githubUrl }),
  });
}
