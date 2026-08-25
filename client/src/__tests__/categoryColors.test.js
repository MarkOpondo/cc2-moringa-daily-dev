import { categoryColor } from '../utils/categoryColors';

describe('categoryColor', () => {
  it('returns the defined palette for a known category', () => {
    const colors = categoryColor('Frontend');
    expect(colors.text).toBe('text-sky-400');
    expect(colors.bg).toBe('bg-sky-400');
  });

  it('returns a distinct color for each known category (no accidental duplicates)', () => {
    const names = ['Frontend', 'Backend', 'DevOps', 'Fullstack', 'Career', 'Data Science'];
    const bgClasses = names.map((n) => categoryColor(n).bg);
    expect(new Set(bgClasses).size).toBe(names.length);
  });

  it('falls back to a neutral color for an unknown category', () => {
    const colors = categoryColor('Some Made Up Category');
    expect(colors.text).toBe('text-slate-400');
  });

  it('falls back gracefully when no name is provided', () => {
    expect(() => categoryColor(undefined)).not.toThrow();
    expect(categoryColor(undefined).text).toBe('text-slate-400');
  });
});
