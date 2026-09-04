import apiRequest from "./api";

export async function listWishlist() {
  return apiRequest("/api/wishlist");
}

export async function addToWishlist(contentId) {
  return apiRequest("/api/wishlist", {
    method: "POST",
    body: JSON.stringify({ contentId }),
  });
}

export async function removeFromWishlist(contentId) {
  return apiRequest(`/api/wishlist/${contentId}`, { method: "DELETE" });
}

export async function isWishlisted(contentId) {
  // Public post pages can be opened in the development preview without a
  // login. Do not call the authenticated wishlist endpoint in that case.
  if (!localStorage.getItem("token")) return false;

  const items = await listWishlist();
  return items.some((item) => String(item.id) === String(contentId));
}

export async function toggleWishlist(contentId, currentlyWishlisted) {
  if (currentlyWishlisted) {
    await removeFromWishlist(contentId);
    return false;
  }
  await addToWishlist(contentId);
  return true;
}
