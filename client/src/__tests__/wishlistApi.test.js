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
});
