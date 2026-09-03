import { useState } from "react";
import { Video, Headphones, ExternalLink } from "lucide-react";
import { getEmbedInfo } from "../../utils/mediaEmbed";

export default function MediaPlayer({ type, url }) {
  const [failed, setFailed] = useState(false);
  const embed = getEmbedInfo(url);

  if (!embed || failed) {
    return (
      <div className="aspect-video bg-surface border border-line rounded-xl flex flex-col items-center justify-center gap-2 text-center px-6">
        {type === "audio" ? (
          <Headphones className="w-8 h-8 text-navy/70" />
        ) : (
          <Video className="w-8 h-8 text-navy/70" />
        )}
        <p className="text-xs text-muted">
          {embed ? "Couldn't load this media." : "No valid media link was provided."}
        </p>
        {url && (
          <a
            href={url}
            target="_blank"
            rel="noreferrer"
            className="flex items-center gap-1 text-xs text-brand-600 hover:underline"
          >
            Open original link <ExternalLink className="w-3 h-3" />
          </a>
        )}
      </div>
    );
  }

  if (embed.provider === "youtube" || embed.provider === "vimeo") {
    return (
      <div className="aspect-video rounded-xl overflow-hidden border border-line bg-black">
        <iframe
          src={embed.embedUrl}
          title="Embedded media player"
          className="w-full h-full"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
          onError={() => setFailed(true)}
        />
      </div>
    );
  }

  if (type === "audio") {
    return (
      <div className="p-6 bg-surface border border-line rounded-xl">
        <audio controls className="w-full" onError={() => setFailed(true)}>
          <source src={embed.embedUrl} />
        </audio>
      </div>
    );
  }

  return (
    <video
      controls
      className="w-full rounded-xl border border-line bg-black aspect-video"
      onError={() => setFailed(true)}
    >
      <source src={embed.embedUrl} />
    </video>
  );
}

