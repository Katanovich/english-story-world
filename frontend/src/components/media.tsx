"use client";

import { useEffect, useState } from "react";
import { mediaUrl } from "@/lib/api";
import { canSpeak, speak, stopSpeaking } from "@/lib/speech";
import type { Episode, ListeningTrack, MediaRef } from "@/lib/types";
import { Button } from "./ui";

/** Image asset if present, else emoji, else nothing. Images are lesson artwork (decorative
 * when text is shown next to them), so they use the alt text from the CMS. */
export function Illustration({
  imageId,
  emoji,
  media,
  size = "text-5xl",
  label,
}: {
  imageId?: string | null;
  emoji?: string | null;
  media?: Record<string, MediaRef>;
  size?: string;
  label?: string;
}) {
  if (imageId) {
    const alt = media?.[imageId]?.alt_text ?? label ?? "";
    // eslint-disable-next-line @next/next/no-img-element
    return <img src={mediaUrl(imageId)} alt={alt} className="mx-auto max-h-32 rounded-2xl" />;
  }
  if (emoji) {
    return (
      <span role={label ? "img" : undefined} aria-label={label} aria-hidden={!label} className={size}>
        {emoji}
      </span>
    );
  }
  return null;
}

function useSpeechSupport() {
  const [supported, setSupported] = useState<boolean | null>(null);
  useEffect(() => {
    setSupported(canSpeak());
    return () => stopSpeaking();
  }, []);
  return supported;
}

/** Plays a recorded audio file if one exists; otherwise offers the browser voice, clearly
 * labelled. Never pretends a recording exists. */
export function ListenButton({ text, audioId }: { text: string; audioId?: string | null }) {
  const supported = useSpeechSupport();
  if (audioId) {
    return <audio controls preload="none" src={mediaUrl(audioId)} className="w-full" />;
  }
  if (supported === false) {
    return (
      <p className="text-sm text-muted">
        No recording yet, and this browser cannot read text aloud.
      </p>
    );
  }
  return (
    <div className="flex flex-wrap items-center gap-3">
      <Button variant="secondary" size="lg" onClick={() => speak(text)} disabled={!supported}>
        <span aria-hidden>🔊</span> Listen
      </Button>
      <Button variant="ghost" onClick={() => speak(text, 0.6)} disabled={!supported}>
        <span aria-hidden>🐢</span> Slow
      </Button>
      <span className="text-xs text-muted">Computer voice · recording coming soon</span>
    </div>
  );
}

export function ListeningTrackPlayer({
  track,
  showTranscriptDefault = false,
}: {
  track: ListeningTrack;
  showTranscriptDefault?: boolean;
}) {
  const [showText, setShowText] = useState(showTranscriptDefault);
  const fullText = track.transcript.map((l) => l.text).join(" ");
  return (
    <div className="space-y-4">
      <h3 className="text-xl font-extrabold">{track.title}</h3>
      {track.audio_id ? (
        <audio controls preload="metadata" className="w-full" src={mediaUrl(track.audio_id)}>
          {track.subtitle_id && (
            <track kind="captions" srcLang="en" label="English" src={mediaUrl(track.subtitle_id)} />
          )}
        </audio>
      ) : (
        <ListenButton text={fullText} />
      )}
      <Button variant="ghost" onClick={() => setShowText((s) => !s)} aria-expanded={showText}>
        {showText ? "Hide the words" : "Show the words"}
      </Button>
      {showText && (
        <ul className="space-y-2">
          {track.transcript.map((line, i) => (
            <li key={i} className="flex items-start gap-2">
              <span className="min-w-16 font-extrabold text-sky">{line.speaker}:</span>
              <span>{line.text}</span>
              {!track.audio_id && (
                <button
                  type="button"
                  className="ml-auto rounded-lg px-2 text-lg hover:bg-line"
                  aria-label={`Listen: ${line.text}`}
                  onClick={() => speak(line.text)}
                >
                  🔈
                </button>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export function EpisodePlayer({
  episode,
  media,
}: {
  episode: Episode;
  media?: Record<string, MediaRef>;
}) {
  const video = episode.video_asset_id ? media?.[episode.video_asset_id] : undefined;
  return (
    <div className="space-y-3">
      {episode.has_video && episode.video_asset_id ? (
        <video
          controls
          preload="metadata"
          className="aspect-video w-full rounded-2xl bg-black"
          poster={episode.poster_image_id ? mediaUrl(episode.poster_image_id) : undefined}
        >
          <source src={mediaUrl(episode.video_asset_id)} type={video?.mime_type ?? "video/mp4"} />
          {episode.subtitle_asset_id && (
            <track
              kind="subtitles"
              srcLang="en"
              label="English"
              src={mediaUrl(episode.subtitle_asset_id)}
              default
            />
          )}
          Your browser cannot play this video.
        </video>
      ) : (
        <div className="flex min-h-36 w-full flex-col items-center justify-center gap-1 rounded-2xl border-2 border-dashed p-4 border-line bg-bg text-center">
          <span aria-hidden className="text-5xl">
            🎬
          </span>
          <p className="font-extrabold">Cartoon coming soon!</p>
          <p className="max-w-xs text-sm text-muted">Read the story below for now.</p>
        </div>
      )}
      <div>
        <h3 className="text-lg font-extrabold">{episode.title}</h3>
        <p className="text-muted">{episode.synopsis}</p>
      </div>
    </div>
  );
}
