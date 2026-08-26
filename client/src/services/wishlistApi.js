import apiRequest from "./api";

export async function listWishlist() {
  return apiRequest("/api/users/me/wishlist");
}

export async function addToWishlist(contentId) {
  return apiRequest("/api/wishlist", {
    method: "POST",
    body: JSON.stringify({
      content_id: contentId,
    }),
  });
}

export async function removeFromWishlist(contentId) {
  return apiRequest(`/api/wishlist/${contentId}`, {
    method: "DELETE",
  });
}

export async function isWishlisted(contentId) {
  const items = await listWishlist();

  return items.some(
    (item) =>
      String(item.contentId ?? item.content_id ?? item.ContentID) ===
      String(contentId)
  );
}

export async function toggleWishlist(contentId, currentlyWishlisted) {
  if (currentlyWishlisted) {
    await removeFromWishlist(contentId);
    return false;
  }

  await addToWishlist(contentId);
  return true;
}