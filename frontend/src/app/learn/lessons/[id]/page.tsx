"use client";

import { useParams } from "next/navigation";
import { LessonPlayer } from "@/components/LessonPlayer";
import { ErrorState, LoadingState } from "@/components/ui";
import type { LessonDetail } from "@/lib/types";
import { useApi } from "@/lib/useApi";

export default function LessonPage() {
  const { id } = useParams<{ id: string }>();
  const { data, error, loading, reload } = useApi<LessonDetail>(`/lessons/${id}`);
  if (loading) return <LoadingState label="Opening your lesson…" />;
  if (error || !data) {
    const msg = error?.status === 404 ? "This lesson is not available." : (error?.message ?? "Could not load.");
    return <ErrorState message={msg} onRetry={error?.status === 404 ? undefined : reload} />;
  }
  return <LessonPlayer key={data.id} lesson={data} backHref="/learn" />;
}
