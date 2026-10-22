"use client";

import { useState } from "react";
import { ApiError, post } from "@/lib/api";
import type { AttemptResult, Exercise, LessonContent, MediaRef } from "@/lib/types";
import { Button, Card, Notice } from "@/components/ui";
import { describeSolution, initialValue, isReady, RENDERERS, toResponse, type Response } from "./renderers";

/** One exercise at a time: answer → Check → feedback → Try again / Continue.
 * `preview` (admin) shows the exercise but never submits. */
export function ExerciseCard({
  exercise,
  media,
  content,
  onAnswered,
  onContinue,
  continueLabel = "Continue",
  preview = false,
}: {
  exercise: Exercise;
  media: Record<string, MediaRef>;
  content?: LessonContent;
  onAnswered?: (r: AttemptResult) => void;
  onContinue?: () => void;
  continueLabel?: string;
  preview?: boolean;
}) {
  const [value, setValue] = useState<Response>(() => initialValue(exercise));
  const [result, setResult] = useState<AttemptResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const Renderer = RENDERERS[exercise.type];

  async function check() {
    if (preview) return;
    setSubmitting(true);
    setError(null);
    try {
      const r = await post<AttemptResult>(`/exercises/${exercise.id}/attempts`, {
        response: toResponse(value),
      });
      setResult(r);
      onAnswered?.(r);
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Could not check your answer.");
    } finally {
      setSubmitting(false);
    }
  }

  function retry() {
    setResult(null);
    setValue(initialValue(exercise));
  }

  const ready = isReady(exercise, value);
  const isSpeaking = exercise.type === "SPEAKING";

  return (
    <Card className="space-y-6">
      <h2 className="text-lg font-bold text-muted">{exercise.instructions}</h2>
      {Renderer ? (
        <Renderer
          exercise={exercise}
          media={media}
          content={content}
          value={value}
          setValue={setValue}
          locked={result !== null || submitting}
          result={result}
          canRecord={!preview}
        />
      ) : (
        <Notice tone="err">This exercise type is not supported yet.</Notice>
      )}

      {error && <Notice tone="err">{error}</Notice>}

      {result && (
        <div
          role="status"
          className={`space-y-2 rounded-2xl p-4 ${result.is_correct === false ? "bg-warn-bg text-warn-ink" : "bg-ok-bg text-ok-ink"}`}
        >
          <p className="text-xl font-extrabold">
            <span aria-hidden>{result.is_correct === false ? "🤔 " : "🎉 "}</span>
            {result.message}
          </p>
          {result.explanation && <p>{result.explanation}</p>}
          {result.solution && result.is_correct === false && (
            <p>
              <span className="font-bold">Answer: </span>
              {describeSolution(exercise, result.solution)}
            </p>
          )}
        </div>
      )}

      <div className="flex flex-wrap gap-3">
        {!result && !preview && (
          <Button size="lg" onClick={check} disabled={!ready || submitting}>
            {submitting ? "Checking…" : isSpeaking ? "I said it!" : "Check"}
          </Button>
        )}
        {preview && <Notice>Preview mode — answers are not saved.</Notice>}
        {result?.is_correct === false && (
          <Button variant="secondary" size="lg" onClick={retry}>
            Try again
          </Button>
        )}
        {(result || preview) && onContinue && (
          <Button size="lg" variant={result?.is_correct === false ? "ghost" : "primary"} onClick={onContinue}>
            {continueLabel}
          </Button>
        )}
      </div>
    </Card>
  );
}
