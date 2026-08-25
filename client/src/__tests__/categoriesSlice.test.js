import categoriesReducer, {
  fetchCategories,
  toggleCategorySubscription,
} from '../features/categories/categoriesSlice';

describe('categoriesSlice reducer', () => {
  it('starts with an empty list and no subscriptions', () => {
    const state = categoriesReducer(undefined, { type: '@@INIT' });
    expect(state.items).toEqual([]);
    expect(state.subscribedIds).toEqual([]);
  });

  it('stores categories once fetchCategories succeeds', () => {
    const mockCategories = [{ id: 'c1', name: 'Frontend' }, { id: 'c2', name: 'Backend' }];
    const action = { type: fetchCategories.fulfilled.type, payload: mockCategories };
    const state = categoriesReducer(undefined, action);

    expect(state.status).toBe('succeeded');
    expect(state.items).toHaveLength(2);
  });

  it('adds a category id when subscribing', () => {
    const initial = { items: [], subscribedIds: ['c1'], status: 'idle' };
    const action = {
      type: toggleCategorySubscription.fulfilled.type,
      payload: { categoryId: 'c2', subscribed: true },
    };
    const state = categoriesReducer(initial, action);

    expect(state.subscribedIds).toEqual(['c1', 'c2']);
  });

  it('removes a category id when unsubscribing', () => {
    const initial = { items: [], subscribedIds: ['c1', 'c2'], status: 'idle' };
    const action = {
      type: toggleCategorySubscription.fulfilled.type,
      payload: { categoryId: 'c1', subscribed: false },
    };
    const state = categoriesReducer(initial, action);

    expect(state.subscribedIds).toEqual(['c2']);
  });
});
