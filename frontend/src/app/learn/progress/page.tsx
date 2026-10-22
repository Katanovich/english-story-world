"use client";

import { Badge, Card, EmptyState, ErrorState, LoadingState, ProgressBar } from "@/components/ui";
import type { Mastery, ProgressReport } from "@/lib/types";
import { useApi } from "@/lib/useApi";

function level(m: Mastery): { label: string; tone: "ok" | "warn" | "neutral" } {
  if (m.mastered) return { label: "I know it well", tone: "ok" };
  if (m.mastery >= 0.3) return { label: "Getting there", tone: "warn" };
  return { label: "Just started", tone: "neutral" };
}

function when(date: string | null) {
  if (!date) return "—";
  const d = new Date(date);
  return d <= new Date() ? "now" : d.toLocaleDateString(undefined, { day: "numeric", month: "short" });
}

export default function ProgressPage() {
  const { data, error, loading, reload } = useApi<ProgressReport>("/me/progress");
  if (loading) return <LoadingState />;
  if (error || !data) return <ErrorState message={error?.message ?? "Could not load."} onRetry={reload} />;

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-black">My words</h1>
      <p className="text-muted">
        A word is “known well” when you can both <strong>find</strong> it and <strong>use</strong> it
        in a sentence — more than once.
      </p>
      {data.mastery.length === 0 ? (
        <Card><EmptyState icon="🔤" title="No words yet">Start a lesson to collect words!</EmptyState></Card>
      ) : (
        <ul className="grid gap-3 sm:grid-cols-2">
          {data.mastery.map((m) => {
            const l = level(m);
            return (
              <li key={m.item.id}>
                <Card className="space-y-3">
                  <div className="flex items-center gap-3">
                    <span aria-hidden className="text-3xl">{m.item.emoji ?? "💬"}</span>
                    <span className="flex-1 text-xl font-extrabold">{m.item.text}</span>
                    <Badge tone={l.tone}>{l.label}</Badge>
                  </div>
                  <ProgressBar value={Math.round(m.mastery * 100)} max={100} label={`How well I know ${m.item.text}`} color={m.mastered ? "bg-leaf" : "bg-sun"} />
                  <p className="text-sm text-muted">
                    Found it: {m.recognition_correct} · Used it: {m.recall_correct} · Next practice: {when(m.next_review_at)}
                  </p>
                </Card>
              </li>
            );
          })}
        </ul>
      )}

      <section className="space-y-3">
        <h2 className="text-2xl font-black">My lessons</h2>
        {data.lessons.length === 0 ? (
          <p className="text-muted">No lessons started yet.</p>
        ) : (
          <ul className="space-y-2">
            {data.lessons.map((l) => (
              <li key={l.lesson_id} className="flex flex-wrap items-center gap-3 rounded-2xl border-2 border-line bg-surface p-4">
                <span className="flex-1 font-extrabold">{l.lesson_title}</span>
                <Badge tone={l.status === "COMPLETED" ? "ok" : "warn"}>{l.status === "COMPLETED" ? "Done" : "Started"}</Badge>
                <span className="text-sm text-muted">{l.score} / {l.max_score} points</span>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
