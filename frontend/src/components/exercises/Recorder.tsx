"use client";

import { useEffect, useRef, useState } from "react";
import { api, ApiError } from "@/lib/api";
import type { MediaRef } from "@/lib/types";
import { Button } from "@/components/ui";

type State = "idle" | "recording" | "recorded" | "saving" | "saved" | "error" | "unsupported";

/** Records the learner's voice in the browser (MediaRecorder), lets them replay it, and
 * stores it privately on our server. Nothing is sent to external services. */
export function Recorder({ onSaved, disabled }: { onSaved: (assetId: string) => void; disabled?: boolean }) {
  const [state, setState] = useState<State>("idle");
  const [message, setMessage] = useState("");
  const [url, setUrl] = useState<string | null>(null);
  const recorder = useRef<MediaRecorder | null>(null);
  const chunks = useRef<Blob[]>([]);
  const blob = useRef<Blob | null>(null);

  useEffect(() => {
    if (typeof window !== "undefined" && (!navigator.mediaDevices || !("MediaRecorder" in window))) {
      setState("unsupported");
    }
  }, []);
  useEffect(() => () => {
    if (url) URL.revokeObjectURL(url);
  }, [url]);

  async function start() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const rec = new MediaRecorder(stream);
      chunks.current = [];
      rec.ondataavailable = (e) => e.data.size && chunks.current.push(e.data);
      rec.onstop = () => {
        stream.getTracks().forEach((t) => t.stop());
        blob.current = new Blob(chunks.current, { type: rec.mimeType || "audio/webm" });
        setUrl(URL.createObjectURL(blob.current));
        setState("recorded");
      };
      recorder.current = rec;
      rec.start();
      setState("recording");
    } catch {
      setMessage("We could not use the microphone. You can still practise by speaking out loud.");
      setState("error");
    }
  }

  async function save() {
    if (!blob.current) return;
    setState("saving");
    const type = blob.current.type;
    const ext = type.includes("ogg") ? "ogg" : type.includes("mp4") ? "m4a" : "webm";
    const form = new FormData();
    form.append("file", blob.current, `recording.${ext}`);
    try {
      const asset = await api<MediaRef>("/me/recordings", { method: "POST", body: form });
      onSaved(asset.id);
      setState("saved");
    } catch (e) {
      setMessage(e instanceof ApiError ? e.message : "Could not save the recording.");
      setState("error");
    }
  }

  if (state === "unsupported") {
    return <p className="text-sm text-muted">This browser cannot record. Practise by speaking out loud.</p>;
  }

  return (
    <div className="space-y-3 rounded-2xl border-2 border-line p-4">
      <div className="flex flex-wrap gap-3">
        {state !== "recording" ? (
          <Button variant="secondary" size="lg" onClick={start} disabled={disabled || state === "saving"}>
            <span aria-hidden>🎙️</span> {state === "idle" ? "Record" : "Record again"}
          </Button>
        ) : (
          <Button variant="danger" size="lg" onClick={() => recorder.current?.stop()}>
            <span aria-hidden>⏹️</span> Stop
          </Button>
        )}
        {(state === "recorded" || state === "error") && blob.current && (
          <Button size="lg" onClick={save} disabled={disabled}>
            Keep my recording
          </Button>
        )}
      </div>
      {state === "recording" && (
        <p role="status" className="font-bold text-berry">
          ● Recording… speak now!
        </p>
      )}
      {url && <audio controls src={url} className="w-full" aria-label="Your recording" />}
      {state === "saving" && <p role="status">Saving…</p>}
      {state === "saved" && <p role="status" className="font-bold text-ok-ink">Saved! Only you and your teacher can hear it.</p>}
      {state === "error" && <p role="alert" className="text-err-ink">{message}</p>}
    </div>
  );
}
