import { timeAgo, roleLabel, initials } from '../utils/format';

describe('timeAgo', () => {
  it('returns "just now" for a timestamp seconds ago', () => {
    const now = new Date().toISOString();
    expect(timeAgo(now)).toBe('just now');
  });

  it('returns days for a timestamp several days ago', () => {
    const threeDaysAgo = new Date(Date.now() - 3 * 86400000).toISOString();
    expect(timeAgo(threeDaysAgo)).toBe('3d ago');
  });

  it('returns hours for a timestamp a few hours ago', () => {
    const fiveHoursAgo = new Date(Date.now() - 5 * 3600000).toISOString();
    expect(timeAgo(fiveHoursAgo)).toBe('5h ago');
  });
});

describe('roleLabel', () => {
  it('labels admin correctly', () => {
    expect(roleLabel('admin')).toBe('Admin');
  });

  it('labels tech_writer correctly', () => {
    expect(roleLabel('tech_writer')).toBe('Tech Writer');
  });

  it('falls back to Member for a plain user or unknown role', () => {
    expect(roleLabel('user')).toBe('Member');
    expect(roleLabel(undefined)).toBe('Member');
  });
});

describe('initials', () => {
  it('takes the first two characters and uppercases them', () => {
    expect(initials('davidm')).toBe('DA');
  });

  it('handles an empty or missing username without throwing', () => {
    expect(initials('')).toBe('');
    expect(initials()).toBe('');
  });
});
