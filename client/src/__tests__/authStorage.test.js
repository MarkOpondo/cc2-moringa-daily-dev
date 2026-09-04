import { clearAuthStorage, getAuthToken, persistAuth } from "../services/authStorage";

describe("auth storage", () => {
  beforeEach(() => localStorage.clear());

  it("persists the token returned by the login response", () => {
    const response = persistAuth({
      access_token: "access-token",
      user: { id: "u1" },
    });

    expect(response.token).toBe("access-token");
    expect(localStorage.getItem("token")).toBe("access-token");
    expect(JSON.parse(localStorage.getItem("user"))).toEqual({ id: "u1" });
  });

  it("migrates tokens stored under legacy keys", () => {
    localStorage.setItem("accessToken", "legacy-token");

    expect(getAuthToken()).toBe("legacy-token");
    expect(localStorage.getItem("token")).toBe("legacy-token");
  });

  it("uses a token included in the stored auth user as a fallback", () => {
    localStorage.setItem("user", JSON.stringify({ id: "u1", access_token: "user-token" }));

    expect(getAuthToken()).toBe("user-token");
    expect(localStorage.getItem("token")).toBe("user-token");
  });

  it("clears all supported auth storage keys", () => {
    localStorage.setItem("token", "token");
    localStorage.setItem("authToken", "legacy-token");
    localStorage.setItem("user", JSON.stringify({ id: "u1" }));

    clearAuthStorage();

    expect(localStorage.getItem("token")).toBeNull();
    expect(localStorage.getItem("authToken")).toBeNull();
    expect(localStorage.getItem("user")).toBeNull();
  });
});
