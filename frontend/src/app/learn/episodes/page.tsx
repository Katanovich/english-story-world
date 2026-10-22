"use client";

import Link from "next/link";
import { EpisodePlayer } from "@/components/media";
import { Card, EmptyState, ErrorState, LoadingState } from "@/components/ui";
import type { EpisodeListItem } from "@/lib/types";
import { useApi } from "@/lib/useApi";

export default function EpisodesPage() {
  const { data, error, loading, reload } = useApi<EpisodeListItem[]>("/me/episodes");
  if (loading) return <LoadingState />;
  if (error || !data) return <ErrorState message={error?.message ?? "Could not load."} onRetry={reload} />;
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-black">Cartoons with Alex and Mia</h1>
      {data.length === 0 ? (
        <Card><EmptyState icon="🎬" title="No cartoons yet" /></Card>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2">
          {data.map((ep) => (
            <Card key={ep.id} className="space-y-3">
              <EpisodePlayer episode={ep} />
              <Link href={`/learn/lessons/${ep.lesson_id}`} className="font-bold text-sky underline">
                Lesson {ep.lesson_position}: {ep.lesson_title}
              </Link>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
