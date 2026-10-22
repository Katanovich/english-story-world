"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { ExerciseCard } from "@/components/exercises/ExerciseCard";
import { SECTION_INFO, SectionIntro } from "@/components/LessonSections";
import { EpisodePlayer } from "@/components/media";
import { Button, Card, LinkButton, Notice, ProgressBar } from "@/components/ui";
import { post } from "@/lib/api";
import type { Exercise, LessonDetail, LessonProgress, Section } from "@/lib/types";

const ORDER: Section[] = ["VOCABULARY", "READING", "LISTENING", "GRAMMAR", "SPEAKING", "QUIZ"];

type Step = { kind: "intro"; section: Section } | { kind: "exercise"; section: Section; exercise: Exercise };

/** Plays a lesson as a sequence of single tasks: each section starts with a short
 * learning card, followed by its exercises one at a time. */
export function LessonPlayer({
  lesson,
  backHref,
  preview = false,
}: {
  lesson: LessonDetail;
  backHref: string;
  preview?: boolean;
}) {
  const steps: Step[] = useMemo(() => {
    const out: Step[] = [];
    for (const section of ORDER) {
      const exercises = lesson.exercises.filter((e) => e.section === section);
      const hasContent =
        (section === "READING" && lesson.content.reading) ||
        (section === "LISTENING" && lesson.content.listening?.length) ||
        (section === "GRAMMAR" && lesson.content.grammar?.length) ||
        (section === "VOCABULARY" && lesson.items.length);
      if (!exercises.length && !hasContent) continue;
      out.push({ kind: "intro", section });
      exercises.forEach((exercise) => out.push({ kind: "exercise", section, exercise }));
    }
    return out;
  }, [lesson]);

  const [progress, setProgress] = useState<LessonProgress | null>(lesson.progress);
  const attempted = new Set(progress?.attempted_exercise_ids ?? []);
  const [index, setIndex] = useState<number | null>(null); // null = lesson start screen
  const [finished, setFinished] = useState(false);

  const total = lesson.exercises.length;
  const done = lesson.exercises.filter((e) => attempted.has(e.id)).length;

  function resumeIndex(): number {
    const first = steps.findIndex((s) => s.kind === "exercise" && !attempted.has(s.exercise.id));
    if (first === -1) return 0;
    // Start at the learning card of that section so the learner sees the material again.
    const section = steps[first].section;
    return steps.findIndex((s) => s.kind === "intro" && s.section === section);
  }

  async function begin() {
    if (!preview && (!progress || progress.status === "NOT_STARTED")) {
      const p = await post<LessonProgress>(`/lessons/${lesson.id}/start`).catch(() => null);
      if (p) setProgress(p);
    }
    setIndex(resumeIndex());
    window.scrollTo({ top: 0 });
  }

  function next() {
    if (index === null) return;
    if (index + 1 >= steps.length) setFinished(true);
    else setIndex(index + 1);
    window.scrollTo({ top: 0 });
  }

  const header = (
    <div className="space-y-3">
      <div className="flex items-center gap-3">
        <Link href={backHref} className="rounded-xl px-3 py-2 font-bold hover:bg-line" aria-label="Back to my course">
          ← Back
        </Link>
        <p className="font-extrabold">Lesson {lesson.position}: {lesson.title}</p>
      </div>
      <ProgressBar value={done} max={total} label="Lesson progress" />
      <p className="text-sm text-muted">{done} of {total} activities done</p>
    </div>
  );

  if (finished) {
    const completed = progress?.status === "COMPLETED";
    return (
      <div className="space-y-6">
        {header}
        <Card className="space-y-4 text-center">
          <span aria-hidden className="text-7xl">{completed ? "🏆" : "👏"}</span>
          <h1 className="text-3xl font-black">{completed ? "Lesson finished!" : "Good work!"}</h1>
          {preview ? (
            <Notice>Preview finished. Nothing was saved.</Notice>
          ) : completed ? (
            <p className="text-lg">
              You got <strong>{progress?.score}</strong> of <strong>{progress?.max_score}</strong> points.
              {progress?.best_quiz_percent != null && <> Quiz: <strong>{Math.round(progress.best_quiz_percent)}%</strong>.</>}
            </p>
          ) : (
            <p className="text-lg">Some activities are not done yet. You can do them now or later.</p>
          )}
          <div className="flex flex-wrap justify-center gap-3">
            {!completed && !preview && (
              <Button size="lg" onClick={() => { setFinished(false); setIndex(resumeIndex()); }}>
                Do the rest
              </Button>
            )}
            {lesson.next_lesson_id && completed && (
              <LinkButton size="lg" href={`/learn/lessons/${lesson.next_lesson_id}`}>Next lesson</LinkButton>
            )}
            <LinkButton size="lg" variant="secondary" href={backHref}>Back to my course</LinkButton>
          </div>
        </Card>
      </div>
    );
  }

  if (index === null) {
    return (
      <div className="space-y-6">
        {header}
        <Card className="space-y-5">
          {preview && <Notice>Student preview{lesson.is_published ? "" : " · DRAFT (students cannot see it yet)"}</Notice>}
          <h1 className="text-3xl font-black">{lesson.title}</h1>
          {lesson.content.story_intro && <p className="text-xl">{lesson.content.story_intro}</p>}
          {lesson.episodes.map((ep) => <EpisodePlayer key={ep.id} episode={ep} media={lesson.media} />)}
          <div>
            <h2 className="mb-2 font-extrabold">Today you will:</h2>
            <ul className="space-y-1">
              {lesson.objectives.map((o) => (
                <li key={o} className="flex gap-2"><span aria-hidden>✔️</span>{o}</li>
              ))}
            </ul>
          </div>
          <p className="text-muted">About {lesson.estimated_minutes} minutes</p>
          <Button size="lg" onClick={begin}>
            {done === 0 ? "Start the lesson" : done === total ? "Practise again" : "Continue"}
          </Button>
        </Card>
      </div>
    );
  }

  const step = steps[index];
  return (
    <div className="space-y-6">
      {header}
      <nav aria-label="Lesson parts" className="flex flex-wrap gap-2">
        {ORDER.filter((s) => steps.some((st) => st.section === s)).map((s) => (
          <button
            key={s}
            type="button"
            onClick={() => setIndex(steps.findIndex((st) => st.section === s))}
            aria-current={step.section === s ? "step" : undefined}
            className={`rounded-full px-3 py-1 text-sm font-bold ${step.section === s ? "bg-brand text-brand-ink" : "bg-surface border-2 border-line"}`}
          >
            <span aria-hidden>{SECTION_INFO[s].icon} </span>{SECTION_INFO[s].title}
          </button>
        ))}
      </nav>
      {step.kind === "intro" ? (
        <Card className="space-y-6">
          <SectionIntro lesson={lesson} section={step.section} />
          <div className="flex gap-3">
            {index > 0 && <Button variant="ghost" onClick={() => setIndex(index - 1)}>Back</Button>}
            <Button size="lg" onClick={next}>I am ready!</Button>
          </div>
        </Card>
      ) : (
        <ExerciseCard
          key={step.exercise.id}
          exercise={step.exercise}
          media={lesson.media}
          content={lesson.content}
          preview={preview}
          onAnswered={(r) => setProgress(r.lesson_progress)}
          onContinue={next}
          continueLabel={index + 1 >= steps.length ? "Finish" : "Continue"}
        />
      )}
    </div>
  );
}
