"use client";

import Link from "next/link";
import { Badge, Card, EmptyState, ErrorState, LinkButton, LoadingState, ProgressBar } from "@/components/ui";
import type { Dashboard, LessonSummary, ProgressStatus } from "@/lib/types";
import { useApi } from "@/lib/useApi";

const STATUS: Record<ProgressStatus, { icon: string; label: string }> = {
  COMPLETED: { icon: "✅", label: "Done" },
  IN_PROGRESS: { icon: "▶️", label: "Started" },
  NOT_STARTED: { icon: "⭐", label: "New" },
};

function LessonTile({ lesson, current }: { lesson: LessonSummary; current: boolean }) {
  const s = STATUS[lesson.progress_status];
  return (
    <Link
      href={`/learn/lessons/${lesson.id}`}
      className={`flex min-h-20 items-center gap-4 rounded-3xl border-2 p-4 transition-colors hover:border-sky ${current ? "border-brand bg-brand/5" : "border-line bg-surface"}`}
    >
      <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-sun text-xl font-black">
        {lesson.position}
      </span>
      <span className="flex-1">
        <span className="block text-lg font-extrabold">{lesson.title}</span>
        <span className="text-sm text-muted">{lesson.estimated_minutes} min</span>
      </span>
      <span className="text-right text-sm font-bold">
        <span aria-hidden className="text-2xl">{s.icon}</span>
        <span className="block">{s.label}</span>
      </span>
    </Link>
  );
}

export default function DashboardPage() {
  const { data, error, loading, reload } = useApi<Dashboard>("/me/dashboard");
  if (loading) return <LoadingState />;
  if (error || !data) return <ErrorState message={error?.message ?? "Could not load."} onRetry={reload} />;

  const current = data.current_lesson;
  const allDone = data.lessons_total > 0 && data.lessons_completed === data.lessons_total;

  return (
    <div className="space-y-8">
      <section className="space-y-1">
        <h1 className="text-3xl font-black">Hello, {data.display_name}! <span aria-hidden>👋</span></h1>
        {data.course && (
          <p className="flex flex-wrap items-center gap-2 text-muted">
            {data.course.title}
            {data.course.current_level && <Badge tone="brand">Level {data.course.current_level}</Badge>}
          </p>
        )}
      </section>

      {!data.course ? (
        <Card>
          <EmptyState icon="📚" title="No course yet">
            Your teacher will add you to a course soon. Then your lessons will appear here.
          </EmptyState>
        </Card>
      ) : (
        <>
          {current && (
            <Card className="flex flex-col gap-4 border-brand sm:flex-row sm:items-center">
              <span aria-hidden className="text-6xl">{current.progress_status === "IN_PROGRESS" ? "🚀" : "🌟"}</span>
              <div className="flex-1">
                <p className="font-bold text-muted">{allDone ? "Play again" : current.progress_status === "IN_PROGRESS" ? "Keep going" : "Next lesson"}</p>
                <h2 className="text-2xl font-black">{current.title}</h2>
                <p className="text-muted">{current.description}</p>
              </div>
              <LinkButton href={`/learn/lessons/${current.id}`} size="lg">
                {current.progress_status === "IN_PROGRESS" ? "Continue" : "Start"}
              </LinkButton>
            </Card>
          )}

          <section aria-labelledby="progress-h" className="grid gap-4 sm:grid-cols-3">
            <h2 id="progress-h" className="sr-only">My progress</h2>
            <Card className="space-y-3">
              <p className="font-bold">Lessons finished</p>
              <p className="text-3xl font-black">{data.lessons_completed} / {data.lessons_total}</p>
              <ProgressBar value={data.lessons_completed} max={data.lessons_total} label="Lessons finished" />
            </Card>
            <Card className="space-y-1">
              <p className="font-bold">Words and phrases</p>
              <p className="text-3xl font-black">{data.items_practiced}</p>
              <p className="text-muted">practised · {data.items_mastered} you know well</p>
              <Link href="/learn/progress" className="font-bold text-sky underline">See my words</Link>
            </Card>
            <Card className="space-y-2">
              <p className="font-bold">Review</p>
              <p className="text-3xl font-black">{data.reviews_due}</p>
              <p className="text-muted">{data.reviews_due ? "words are ready to practise" : "Nothing to review now"}</p>
              {data.reviews_due > 0 && <LinkButton href="/learn/review" variant="secondary">Practise</LinkButton>}
            </Card>
          </section>

          {data.course.levels.map((level) => (
            <section key={level.id} className="space-y-4" aria-label={level.title}>
              {level.units.map((unit) => (
                <div key={unit.id} className="space-y-3">
                  <h2 className="text-2xl font-black">{unit.title}</h2>
                  <p className="text-muted">{unit.description}</p>
                  <div className="grid gap-3 sm:grid-cols-2">
                    {unit.lessons.map((l) => (
                      <LessonTile key={l.id} lesson={l} current={l.id === current?.id} />
                    ))}
                  </div>
                </div>
              ))}
            </section>
          ))}

          <section aria-labelledby="ach-h" className="space-y-3">
            <h2 id="ach-h" className="text-2xl font-black">My stickers</h2>
            <ul className="grid grid-cols-2 gap-3 sm:grid-cols-5">
              {data.achievements.map((a) => (
                <li key={a.key} className={`rounded-3xl border-2 p-4 text-center ${a.earned ? "border-sun bg-sun/20" : "border-dashed border-line text-muted"}`}>
                  <span aria-hidden className="block text-3xl">{a.earned ? "🏅" : "🔒"}</span>
                  <span className="text-sm font-bold">{a.title}</span>
                  <span className="sr-only">{a.earned ? " (earned)" : " (not yet)"}</span>
                </li>
              ))}
            </ul>
          </section>
        </>
      )}
    </div>
  );
}
