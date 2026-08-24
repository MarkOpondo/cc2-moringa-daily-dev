import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { listCategories, listSubscriptions, toggleSubscription } from "../../services/categoriesApi";

export const fetchCategories = createAsyncThunk("categories/fetchAll", async () => {
  return await listCategories();
});

export const fetchSubscriptions = createAsyncThunk("categories/fetchSubscriptions", async (userId) => {
  return await listSubscriptions(userId);
});

export const toggleCategorySubscription = createAsyncThunk(
  "categories/toggleSubscription",
  async ({ categoryId, userId }) => {
    const subscribed = await toggleSubscription(categoryId, userId);
    return { categoryId, subscribed };
  }
);

const categoriesSlice = createSlice({
  name: "categories",
  initialState: {
    items: [],
    subscribedIds: [],
    status: "idle", // idle | loading | succeeded | failed
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchCategories.pending, (state) => {
        state.status = "loading";
      })
      .addCase(fetchCategories.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.items = action.payload;
      })
      .addCase(fetchCategories.rejected, (state) => {
        state.status = "failed";
      })
      .addCase(fetchSubscriptions.fulfilled, (state, action) => {
        state.subscribedIds = action.payload;
      })
      .addCase(toggleCategorySubscription.fulfilled, (state, action) => {
        const { categoryId, subscribed } = action.payload;
        state.subscribedIds = subscribed
          ? [...state.subscribedIds, categoryId]
          : state.subscribedIds.filter((id) => id !== categoryId);
      });
  },
});

export default categoriesSlice.reducer;
