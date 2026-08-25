import { getEmbedInfo } from '../utils/mediaEmbed';

describe('getEmbedInfo', () => {
  it('returns null for an empty or missing URL', () => {
    expect(getEmbedInfo('')).toBeNull();
    expect(getEmbedInfo(undefined)).toBeNull();
  });

  it('returns null for a string that is not a valid URL', () => {
    expect(getEmbedInfo('not a url at all')).toBeNull();
  });

  it('builds a YouTube embed URL from a standard youtube.com watch link', () => {
    const result = getEmbedInfo('https://www.youtube.com/watch?v=dQw4w9WgXcQ');
    expect(result.provider).toBe('youtube');
    expect(result.embedUrl).toBe('https://www.youtube.com/embed/dQw4w9WgXcQ');
  });

  it('builds a YouTube embed URL from a shortened youtu.be link', () => {
    const result = getEmbedInfo('https://youtu.be/dQw4w9WgXcQ');
    expect(result.provider).toBe('youtube');
    expect(result.embedUrl).toBe('https://www.youtube.com/embed/dQw4w9WgXcQ');
  });

  it('builds a Vimeo embed URL from a standard vimeo.com link', () => {
    const result = getEmbedInfo('https://vimeo.com/76979871');
    expect(result.provider).toBe('vimeo');
    expect(result.embedUrl).toBe('https://player.vimeo.com/video/76979871');
  });

  it('treats a direct file link as a direct-play source', () => {
    const result = getEmbedInfo('https://example.com/videos/lecture.mp4');
    expect(result.provider).toBe('direct');
    expect(result.embedUrl).toBe('https://example.com/videos/lecture.mp4');
  });

  it('does not treat a non-numeric vimeo path as a valid video ID', () => {
    const result = getEmbedInfo('https://vimeo.com/about');
    expect(result.provider).toBe('direct');
  });
});
