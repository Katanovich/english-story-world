"use client";

import { useState } from "react";
import { ExerciseCard } from "@/components/exercises/ExerciseCard";
import { Card, EmptyState, ErrorState, LinkButton, LoadingState, Button } from "@/components/ui";
import type { ReviewEntry } from "@/lib/types";
import { useApi } from "@/lib/useApi";

export default function ReviewPage() {
  const { data, error, loading, reload } = useApi<ReviewEntry[]>("/me/review?limit=10");
  const [index, setIndex] = useState(0);

  if (loading) return <LoadingState />;
  if (error || !data) return <ErrorState message={error?.message ?? "Could not load."} onRetry={reload} />;

  const entries = data.filter((e) => e.exercise);
  if (entries.length === 0) {
    return (
      <Card>
        <EmptyState icon="🎉" title="Nothing to review right now">
          Words come back here when it is a good time to practise them again.
        </EmptyState>
        <div className="text-center"><LinkButton href="/learn">Back home</LinkButton></div>
      </Card>
    );
  }
  if (index >= entries.length) {
    return (
      <Card className="space-y-4 text-center">
        <span aria-hidden className="text-6xl">🌟</span>
        <h1 className="text-2xl font-black">Review done! Great memory!</h1>
        <div className="flex justify-center gap-3">
          <Button onClick={() => { setIndex(0); reload(); }}>Check for more</Button>
          <LinkButton href="/learn" variant="secondary">Back home</LinkButton>
        </div>
      </Card>
    );
  }
  const entry = entries[index];
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-black">Review · {index + 1} of {entries.length}</h1>
      <p className="text-muted">
        Remember <strong>{entry.item.emoji} {entry.item.text}</strong>?
      </p>
      <ExerciseCard
        key={entry.exercise!.id + index}
        exercise={entry.exercise!}
        media={{}}
        onContinue={() => setIndex(index + 1)}
        continueLabel={index + 1 === entries.length ? "Finish" : "Next"}
      />
    </div>
  );
}
