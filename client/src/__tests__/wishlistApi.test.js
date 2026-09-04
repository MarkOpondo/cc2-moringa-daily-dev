import { isWishlisted } from "../services/wishlistApi";

describe("wishlist API", () => {
  beforeEach(() => {
    localStorage.clear();
    globalThis.fetch = jest.fn();
  });

  it("does not call the authenticated wishlist endpoint for a public post visitor", async () => {
    await expect(isWishlisted(42)).resolves.toBe(false);
    expect(globalThis.fetch).not.toHaveBeenCalled();
  });

  it("sends the bearer token for an authenticated wishlist lookup", async () => {
    localStorage.setItem("token", "test-token");
    globalThis.fetch.mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => [],
    });

    await expect(isWishlisted(42)).resolves.toBe(false);
    expect(globalThis.fetch).toHaveBeenCalledWith(
      "/api/wishlist",
      expect.objectContaining({
        headers: expect.objectContaining({ Authorization: "Bearer test-token" }),
      })
    );
  });
});
