"use client";

import Link from "next/link";
import { useState } from "react";
import { Field, Input, Message, Panel, Select, SmallButton, StatusPill } from "@/components/admin";
import { ErrorState, LoadingState } from "@/components/ui";
import { errorText, send } from "@/lib/api";
import type { CourseNode } from "@/lib/adminTypes";
import { useApi } from "@/lib/useApi";

type FormKind = { kind: "course" } | { kind: "level"; parent: string } | { kind: "unit"; parent: string } | { kind: "lesson"; parent: string };

const slugify = (s: string) => s.toLowerCase().trim().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");

function CreateForm({ form, onDone }: { form: FormKind; onDone: (id?: string) => void }) {
  const [title, setTitle] = useState("");
  const [slug, setSlug] = useState("");
  const [cefr, setCefr] = useState("A1");
  const [position, setPosition] = useState(1);
  const [err, setErr] = useState<string | null>(null);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setErr(null);
    try {
      const s = slug || slugify(title);
      let r: { id: string };
      if (form.kind === "course") r = await send("POST", "/admin/courses", { slug: s, title });
      else if (form.kind === "level") r = await send("POST", `/admin/courses/${form.parent}/levels`, { cefr_level: cefr, title: title || cefr, position });
      else if (form.kind === "unit") r = await send("POST", `/admin/levels/${form.parent}/units`, { slug: s, title, position });
      else r = await send("POST", `/admin/units/${form.parent}/lessons`, { slug: s, title, position });
      onDone(form.kind === "lesson" ? r.id : undefined);
    } catch (e2) {
      setErr(errorText(e2));
    }
  }
  return (
    <form onSubmit={submit} className="mt-2 flex flex-wrap items-end gap-2 rounded-lg bg-bg p-3">
      {form.kind === "level" && (
        <Field label="Уровень CEFR"><Select value={cefr} onChange={(e) => setCefr(e.target.value)}>{["A1", "A2", "B1", "B2", "C1"].map((l) => <option key={l}>{l}</option>)}</Select></Field>
      )}
      <Field label="Название"><Input value={title} onChange={(e) => setTitle(e.target.value)} required={form.kind !== "level"} /></Field>
      {form.kind !== "level" && <Field label="Slug" hint="латиница и дефисы; пусто — из названия"><Input value={slug} onChange={(e) => setSlug(e.target.value)} /></Field>}
      {form.kind !== "course" && <Field label="Порядок"><Input type="number" min={0} value={position} onChange={(e) => setPosition(Number(e.target.value))} className="w-20" /></Field>}
      <SmallButton type="submit" variant="primary">Создать</SmallButton>
      <SmallButton onClick={() => onDone()}>Отмена</SmallButton>
      {err && <div className="w-full"><Message kind="err" text={err} /></div>}
    </form>
  );
}

export default function CoursesPage() {
  const { data, error, loading, reload } = useApi<CourseNode[]>("/admin/courses");
  const [form, setForm] = useState<FormKind | null>(null);
  const [msg, setMsg] = useState<string | null>(null);
  const isOpen = (f: FormKind) => form && form.kind === f.kind && ("parent" in form ? form.parent : "") === ("parent" in f ? f.parent : "");

  const done = (id?: string) => {
    setForm(null);
    reload();
    if (id) window.location.href = `/admin/lessons/${id}`;
  };

  async function toggleCourse(c: CourseNode) {
    try {
      await send("PATCH", `/admin/courses/${c.id}`, { status: c.status === "PUBLISHED" ? "DRAFT" : "PUBLISHED" });
      reload();
    } catch (e) {
      setMsg(errorText(e));
    }
  }

  if (loading) return <LoadingState label="Загрузка…" />;
  if (error || !data) return <ErrorState message={error?.message ?? "Ошибка"} onRetry={reload} />;
  return (
    <>
      <div className="flex items-center gap-2">
        <h1 className="text-2xl font-black">Курсы и уроки</h1>
        <SmallButton className="ml-auto" variant="primary" onClick={() => setForm({ kind: "course" })}>+ Курс</SmallButton>
      </div>
      <Message kind="err" text={msg} />
      {form?.kind === "course" && <CreateForm form={form} onDone={done} />}
      {data.length === 0 && <p className="text-muted">Курсов пока нет. Запустите seed или создайте курс.</p>}
      {data.map((c) => (
        <Panel key={c.id} title={c.title} actions={<>
          <StatusPill status={c.status} />
          <SmallButton onClick={() => toggleCourse(c)}>{c.status === "PUBLISHED" ? "Снять с публикации" : "Опубликовать курс"}</SmallButton>
          <SmallButton onClick={() => setForm({ kind: "level", parent: c.id })}>+ Уровень</SmallButton>
        </>}>
          {isOpen({ kind: "level", parent: c.id }) && <CreateForm form={form!} onDone={done} />}
          {c.levels.map((lv) => (
            <div key={lv.id} className="space-y-2 border-l-4 border-sun pl-3">
              <div className="flex items-center gap-2">
                <h3 className="font-extrabold">{lv.cefr_level} · {lv.title}</h3>
                <SmallButton className="ml-auto" onClick={() => setForm({ kind: "unit", parent: lv.id })}>+ Раздел</SmallButton>
              </div>
              {isOpen({ kind: "unit", parent: lv.id }) && <CreateForm form={form!} onDone={done} />}
              {lv.units.map((u) => (
                <div key={u.id} className="space-y-1 border-l-4 border-sky pl-3">
                  <div className="flex items-center gap-2">
                    <h4 className="font-bold">{u.title}</h4>
                    <SmallButton className="ml-auto" onClick={() => setForm({ kind: "lesson", parent: u.id })}>+ Урок</SmallButton>
                  </div>
                  {isOpen({ kind: "lesson", parent: u.id }) && <CreateForm form={form!} onDone={done} />}
                  <ul className="divide-y divide-line">
                    {u.lessons.map((l) => (
                      <li key={l.id} className="flex flex-wrap items-center gap-2 py-2 text-sm">
                        <span className="w-6 text-muted">{l.position}</span>
                        <Link href={`/admin/lessons/${l.id}`} className="font-bold text-sky underline">{l.title}</Link>
                        <StatusPill status={l.status} />
                        <span className="text-muted">v{l.content_version} · упражнений: {l.exercise_count}</span>
                        <Link href={`/admin/lessons/${l.id}/preview`} className="ml-auto text-sky underline">Просмотр</Link>
                      </li>
                    ))}
                    {u.lessons.length === 0 && <li className="py-2 text-sm text-muted">Уроков нет.</li>}
                  </ul>
                </div>
              ))}
            </div>
          ))}
        </Panel>
      ))}
    </>
  );
}
