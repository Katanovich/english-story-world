"use client";

import Link from "next/link";
import { Panel } from "@/components/admin";
import { ErrorState, LoadingState } from "@/components/ui";
import { STATUS_RU } from "@/lib/adminTypes";
import { useApi } from "@/lib/useApi";

interface Overview {
  students_by_status: Record<keyof typeof STATUS_RU, number>;
  lessons_published: number;
  lessons_draft: number;
  learning_items: number;
  media_assets: number;
  attempts_last_7_days: number;
  active_students_last_7_days: number;
}

function Stat({ label, value, href }: { label: string; value: number; href?: string }) {
  const body = (
    <div className="rounded-xl border border-line bg-surface p-4">
      <p className="text-sm text-muted">{label}</p>
      <p className="text-3xl font-black">{value}</p>
    </div>
  );
  return href ? <Link href={href}>{body}</Link> : body;
}

export default function AdminOverview() {
  const { data, error, loading, reload } = useApi<Overview>("/admin/overview");
  if (loading) return <LoadingState label="Загрузка…" />;
  if (error || !data) return <ErrorState message={error?.message ?? "Ошибка"} onRetry={reload} />;
  return (
    <>
      <h1 className="text-2xl font-black">Обзор</h1>
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        {(Object.keys(STATUS_RU) as (keyof typeof STATUS_RU)[]).map((s) => (
          <Stat key={s} label={`Ученики: ${STATUS_RU[s].toLowerCase()}`} value={data.students_by_status[s] ?? 0} href={`/admin/students?status=${s}`} />
        ))}
        <Stat label="Уроков опубликовано" value={data.lessons_published} href="/admin/courses" />
        <Stat label="Уроков в черновиках" value={data.lessons_draft} href="/admin/courses" />
        <Stat label="Слов и конструкций" value={data.learning_items} href="/admin/items" />
        <Stat label="Медиафайлов" value={data.media_assets} href="/admin/media" />
        <Stat label="Ответов за 7 дней" value={data.attempts_last_7_days} />
        <Stat label="Активных учеников за 7 дней" value={data.active_students_last_7_days} />
      </div>
      <Panel title="Быстрые действия">
        <div className="flex flex-wrap gap-3 text-sm font-bold">
          <Link className="text-sky underline" href="/admin/students">Создать ученика</Link>
          <Link className="text-sky underline" href="/admin/courses">Редактировать уроки</Link>
          <Link className="text-sky underline" href="/admin/media">Загрузить медиа</Link>
        </div>
      </Panel>
    </>
  );
}
