import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import {
  listNotifications,
  markRead,
  markAllRead,
} from "../../services/notificationsApi";

export const fetchNotifications = createAsyncThunk(
  "notifications/fetchAll",
  async () => {
    return await listNotifications();
  }
);

export const markNotificationRead = createAsyncThunk(
  "notifications/markRead",
  async (id) => {
    await markRead(id);
    return id;
  }
);

export const markAllNotificationsRead = createAsyncThunk(
  "notifications/markAllRead",
  async () => {
    await markAllRead();
  }
);

const notificationsSlice = createSlice({
  name: "notifications",

  initialState: {
    items: [],
    status: "idle",
  },

  reducers: {},

  extraReducers: (builder) => {
    builder
      .addCase(fetchNotifications.pending, (state) => {
        state.status = "loading";
      })

      .addCase(fetchNotifications.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.items = action.payload;
      })

      .addCase(fetchNotifications.rejected, (state) => {
        state.status = "failed";
      })

      .addCase(markNotificationRead.fulfilled, (state, action) => {
        const notification = state.items.find(
          (n) => n.id === action.payload
        );

        if (notification) {
          notification.isRead = true;
        }
      })

      .addCase(markAllNotificationsRead.fulfilled, (state) => {
        state.items.forEach((notification) => {
          notification.isRead = true;
        });
      });
  },
});

export default notificationsSlice.reducer;

export const selectUnreadCount = (state) =>
  state.notifications.items.filter((n) => !n.isRead).length;