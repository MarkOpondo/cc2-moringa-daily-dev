import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { listNotifications, markRead, markAllRead } from "../../services/notificationsApi";

export const fetchNotifications = createAsyncThunk("notifications/fetchAll", async (userId) => {
  return await listNotifications(userId);
});

export const markNotificationRead = createAsyncThunk("notifications/markRead", async (id) => {
  await markRead(id);
  return id;
});

export const markAllNotificationsRead = createAsyncThunk("notifications/markAllRead", async (userId) => {
  await markAllRead(userId);
  return userId;
});

const notificationsSlice = createSlice({
  name: "notifications",
  initialState: {
    items: [],
    status: "idle",
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchNotifications.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.items = action.payload;
      })
      .addCase(markNotificationRead.fulfilled, (state, action) => {
        const n = state.items.find((n) => n.id === action.payload);
        if (n) n.isRead = true;
      })
      .addCase(markAllNotificationsRead.fulfilled, (state) => {
        state.items.forEach((n) => (n.isRead = true));
      });
  },
});

export default notificationsSlice.reducer;

export const selectUnreadCount = (state) => state.notifications.items.filter((n) => !n.isRead).length;
