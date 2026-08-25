// Figures out how to play a pasted media URL. The backend only ever stores
// and returns this URL as a plain string — everything below is frontend-only
// logic to turn that string into something playable.
export function getEmbedInfo(url) {
  if (!url) return null;

  let parsed;
  try {
    parsed = new URL(url);
  } catch {
    return null; // not a valid URL at all
  }

  const host = parsed.hostname.replace(/^www\./, "");

  if (host === "youtube.com" || host === "m.youtube.com") {
    const id = parsed.searchParams.get("v");
    if (id) return { provider: "youtube", embedUrl: `https://www.youtube.com/embed/${id}` };
  }
  if (host === "youtu.be") {
    const id = parsed.pathname.slice(1);
    if (id) return { provider: "youtube", embedUrl: `https://www.youtube.com/embed/${id}` };
  }
  if (host === "vimeo.com") {
    const id = parsed.pathname.split("/").filter(Boolean)[0];
    if (id && /^\d+$/.test(id)) return { provider: "vimeo", embedUrl: `https://player.vimeo.com/video/${id}` };
  }

  // Anything else is treated as a direct file link (e.g. .mp4, .mp3, or a
  // link straight to cloud storage) and handed to a native <video>/<audio>
  // element, which will simply fail to load if it isn't actually a media file.
  return { provider: "direct", embedUrl: url };
}
