import { createSlice } from "@reduxjs/toolkit";
import { profiles } from "../../services/mockData";

// Real auth (once the Flask backend exists): LoginPage/SignUpPage already
// write a token to localStorage. `hydrateFromStorage` below reads it back
// on app load so the rest of the UI can reactively know who's logged in
// and what role they have, without every page reading localStorage itself.
//
// DEV-ONLY PREVIEW: there's no backend yet, so there's currently no way
// to actually log in and see the app. `previewRole` lets anyone browsing
// this repo locally switch between Admin / Tech Writer / User to see
// role-gated UI, without a real login. It only ever activates when
// import.meta.env.DEV is true (Vite sets this to false in production
// builds), and `selectCurrentUser` always prefers a real logged-in user
// over the preview if one exists.
const previewUsers = {
  admin: { id: "u1", username: "amina_dev", role: "admin" },
  tech_writer: { id: "u2", username: "brian_writes", role: "tech_writer" },
  user: { id: "u4", username: "davidm", role: "user" },
};

const initialState = {
  user: null, // real authenticated user, once backend auth exists
  previewRole: import.meta.env.DEV ? "user" : null,
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setUser(state, action) {
      state.user = action.payload;
    },
    logout(state) {
      state.user = null;
      localStorage.removeItem("token");
      localStorage.removeItem("user");
    },
    setPreviewRole(state, action) {
      state.previewRole = action.payload;
    },
    hydrateFromStorage(state) {
      const stored = localStorage.getItem("user");
      if (stored) {
        try {
          state.user = JSON.parse(stored);
        } catch {
          state.user = null;
        }
      }
    },
  },
});

export const { setUser, logout, setPreviewRole, hydrateFromStorage } = authSlice.actions;
export default authSlice.reducer;

// Resolves to whichever user should drive the UI right now: a real logged
// in user if one exists, otherwise the dev preview user (dev builds only).
export function selectCurrentUser(state) {
  if (state.auth.user) return state.auth.user;
  if (state.auth.previewRole) {
    const preview = previewUsers[state.auth.previewRole];
    const profile = profiles[preview.id];
    return { ...preview, ...profile, isPreview: true };
  }
  return null;
}

export function selectIsPreview(state) {
  return !state.auth.user && !!state.auth.previewRole;
}
