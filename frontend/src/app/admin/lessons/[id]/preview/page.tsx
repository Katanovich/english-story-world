"use client";

import { useParams } from "next/navigation";
import { LessonPlayer } from "@/components/LessonPlayer";
import { ErrorState, LoadingState } from "@/components/ui";
import type { LessonDetail } from "@/lib/types";
import { useApi } from "@/lib/useApi";

/** Admin sees the lesson exactly as a student would (drafts included); nothing is saved. */
export default function LessonPreviewPage() {
  const { id } = useParams<{ id: string }>();
  const { data, error, loading, reload } = useApi<LessonDetail>(`/lessons/${id}`);
  if (loading) return <LoadingState />;
  if (error || !data) return <ErrorState message={error?.message ?? "Ошибка"} onRetry={reload} />;
  return (
    <div lang="en" className="mx-auto max-w-3xl rounded-3xl bg-bg p-4">
      <LessonPlayer lesson={data} backHref={`/admin/lessons/${id}`} preview />
    </div>
  );
}
