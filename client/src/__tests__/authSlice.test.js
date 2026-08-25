import authReducer, { setUser, logout, setPreviewRole, hydrateFromStorage } from '../features/auth/authSlice';

describe('authSlice reducer', () => {
  it('returns the initial state', () => {
    const state = authReducer(undefined, { type: '@@INIT' });
    expect(state.user).toBeNull();
  });

  it('setUser stores the logged-in user', () => {
    const state = authReducer(undefined, setUser({ id: 'u1', username: 'amina_dev', role: 'admin' }));
    expect(state.user).toEqual({ id: 'u1', username: 'amina_dev', role: 'admin' });
  });

  it('logout clears the user and removes localStorage entries', () => {
    localStorage.setItem('token', 'fake-token');
    localStorage.setItem('user', JSON.stringify({ id: 'u1' }));

    const loggedInState = { user: { id: 'u1' }, previewRole: null };
    const state = authReducer(loggedInState, logout());

    expect(state.user).toBeNull();
    expect(localStorage.getItem('token')).toBeNull();
    expect(localStorage.getItem('user')).toBeNull();
  });

  it('setPreviewRole updates which role is being previewed', () => {
    const state = authReducer(undefined, setPreviewRole('admin'));
    expect(state.previewRole).toBe('admin');
  });

  it('hydrateFromStorage loads a user from localStorage if present', () => {
    localStorage.setItem('user', JSON.stringify({ id: 'u4', username: 'davidm', role: 'user' }));
    const state = authReducer(undefined, hydrateFromStorage());
    expect(state.user).toEqual({ id: 'u4', username: 'davidm', role: 'user' });
  });

  it('hydrateFromStorage leaves user as null if nothing is stored', () => {
    localStorage.removeItem('user');
    const state = authReducer(undefined, hydrateFromStorage());
    expect(state.user).toBeNull();
  });
});
