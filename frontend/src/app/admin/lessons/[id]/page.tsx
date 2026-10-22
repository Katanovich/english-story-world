"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useCallback, useEffect, useState } from "react";
import { Field, Input, Message, Panel, Select, SmallButton, StatusPill, Table, TextArea } from "@/components/admin";
import { ExerciseEditor, TYPES } from "@/components/adminLesson/ExerciseEditor";
import { ErrorState, LoadingState } from "@/components/ui";
import { api, errorText, send } from "@/lib/api";
import { fmtDate, type ExerciseAdmin, type LearningItemAdmin, type LessonAdmin, type MediaAdmin, type ValidationReport } from "@/lib/adminTypes";
import type { Page } from "@/lib/types";
import { useApi } from "@/lib/useApi";

type Tab = "main" | "content" | "items" | "exercises" | "episodes";
const TAB_LABELS: Record<Tab, string> = { main: "Основное", content: "Контент", items: "Слова", exercises: "Упражнения", episodes: "Эпизоды и видео" };

/* ---------- Main ---------- */
function MainTab({ lesson, onSaved }: { lesson: LessonAdmin; onSaved: (m: string) => void }) {
  const [f, setF] = useState({ title: lesson.title, slug: lesson.slug, description: lesson.description, objectives: lesson.objectives.join("\n"), position: lesson.position, estimated_minutes: lesson.estimated_minutes });
  const [err, setErr] = useState<string | null>(null);
  async function save(e: React.FormEvent) {
    e.preventDefault();
    try {
      await send("PATCH", `/admin/lessons/${lesson.id}`, { ...f, objectives: f.objectives.split("\n") });
      setErr(null);
      onSaved("Сохранено.");
    } catch (e2) { setErr(errorText(e2)); }
  }
  return (
    <form onSubmit={save} className="grid gap-3 sm:grid-cols-2">
      <Field label="Название"><Input value={f.title} onChange={(e) => setF({ ...f, title: e.target.value })} required /></Field>
      <Field label="Slug"><Input value={f.slug} onChange={(e) => setF({ ...f, slug: e.target.value })} required /></Field>
      <Field label="Описание (для ученика, англ.)"><TextArea rows={3} value={f.description} onChange={(e) => setF({ ...f, description: e.target.value })} /></Field>
      <Field label="Учебные цели" hint="по одной на строку"><TextArea rows={4} value={f.objectives} onChange={(e) => setF({ ...f, objectives: e.target.value })} /></Field>
      <Field label="Порядок в разделе"><Input type="number" min={0} value={f.position} onChange={(e) => setF({ ...f, position: Number(e.target.value) })} /></Field>
      <Field label="Длительность, мин"><Input type="number" min={1} value={f.estimated_minutes} onChange={(e) => setF({ ...f, estimated_minutes: Number(e.target.value) })} /></Field>
      <div className="sm:col-span-2"><SmallButton type="submit" variant="primary">Сохранить</SmallButton></div>
      {err && <div className="sm:col-span-2"><Message kind="err" text={err} /></div>}
    </form>
  );
}

/* ---------- Content ---------- */
function ContentTab({ lesson, onSaved }: { lesson: LessonAdmin; onSaved: (m: string) => void }) {
  const c = lesson.content;
  const [intro, setIntro] = useState<string>(c.story_intro ?? "");
  const [rTitle, setRTitle] = useState<string>(c.reading?.title ?? "");
  const [paras, setParas] = useState<string>((c.reading?.paragraphs ?? []).map((p: { sentences: string[] }) => p.sentences.join("\n")).join("\n\n"));
  const [highlight, setHighlight] = useState<string>((c.reading?.highlight ?? []).join(", "));
  const [listening, setListening] = useState(JSON.stringify(c.listening ?? [], null, 2));
  const [grammar, setGrammar] = useState(JSON.stringify(c.grammar ?? [], null, 2));
  const [err, setErr] = useState<string | null>(null);

  async function save(e: React.FormEvent) {
    e.preventDefault();
    setErr(null);
    let listeningJson, grammarJson;
    try { listeningJson = JSON.parse(listening); grammarJson = JSON.parse(grammar); } catch { setErr("Аудирование или грамматика: некорректный JSON."); return; }
    const paragraphs = paras.split(/\n\s*\n/).map((block) => ({ sentences: block.split("\n").map((s) => s.trim()).filter(Boolean) })).filter((p) => p.sentences.length);
    // Keep paragraph illustrations that were set before.
    paragraphs.forEach((p, i) => { const old = c.reading?.paragraphs?.[i]; if (old?.image_id) Object.assign(p, { image_id: old.image_id }); });
    const content = {
      story_intro: intro || undefined,
      reading: paragraphs.length ? { title: rTitle, paragraphs, highlight: highlight.split(",").map((s) => s.trim()).filter(Boolean) } : undefined,
      listening: listeningJson,
      grammar: grammarJson,
    };
    try { await send("PATCH", `/admin/lessons/${lesson.id}`, { content }); onSaved("Контент сохранён."); } catch (e2) { setErr(errorText(e2)); }
  }
  return (
    <form onSubmit={save} className="space-y-3">
      <Field label="Вступление к истории (англ.)"><TextArea rows={2} value={intro} onChange={(e) => setIntro(e.target.value)} /></Field>
      <div className="grid gap-3 lg:grid-cols-3">
        <Field label="Текст для чтения: заголовок"><Input value={rTitle} onChange={(e) => setRTitle(e.target.value)} /></Field>
        <div className="lg:col-span-2"><Field label="Выделяемые слова" hint="через запятую"><Input value={highlight} onChange={(e) => setHighlight(e.target.value)} /></Field></div>
      </div>
      <Field label="Абзацы" hint="каждое предложение — с новой строки; пустая строка — новый абзац"><TextArea rows={10} value={paras} onChange={(e) => setParas(e.target.value)} /></Field>
      <div className="grid gap-3 lg:grid-cols-2">
        <Field label="Аудирование (JSON)" hint='[{"id":"l1","title":"…","audio_id":null,"transcript":[{"speaker":"Alex","text":"Hello!"}]}]'><TextArea rows={12} value={listening} onChange={(e) => setListening(e.target.value)} spellCheck={false} /></Field>
        <Field label="Грамматика (JSON)" hint='[{"title":"…","explanation":"…","explanation_ru":"…","examples":["…"]}]'><TextArea rows={12} value={grammar} onChange={(e) => setGrammar(e.target.value)} spellCheck={false} /></Field>
      </div>
      <p className="text-xs text-muted">Чтобы добавить аудиофайл к диалогу, загрузите его в «Медиафайлы» и укажите его id в поле audio_id (субтитры — subtitle_id).</p>
      {err && <Message kind="err" text={err} />}
      <SmallButton type="submit" variant="primary">Сохранить контент</SmallButton>
    </form>
  );
}

/* ---------- Items ---------- */
function ItemsTab({ lesson, items, onSaved }: { lesson: LessonAdmin; items: LearningItemAdmin[]; onSaved: (m: string) => void }) {
  const [roles, setRoles] = useState<Record<string, string>>(Object.fromEntries(lesson.items.map((i) => [i.learning_item_id, i.role])));
  const [filter, setFilter] = useState("");
  const [err, setErr] = useState<string | null>(null);
  async function save() {
    try {
      await send("PUT", `/admin/lessons/${lesson.id}/items`, Object.entries(roles).filter(([, r]) => r).map(([learning_item_id, role]) => ({ learning_item_id, role })));
      setErr(null);
      onSaved("Связи сохранены.");
    } catch (e) { setErr(errorText(e)); }
  }
  const shown = items.filter((i) => roles[i.id] || !filter || `${i.text} ${i.key}`.toLowerCase().includes(filter.toLowerCase()));
  return (
    <div className="space-y-3">
      <p className="text-sm text-muted">NEW — вводится в этом уроке; RECENT — из прошлого урока; OLDER — более раннее повторение. Повторяйте выборочно, не все старые слова сразу.</p>
      <div className="flex gap-2"><Input placeholder="фильтр…" value={filter} onChange={(e) => setFilter(e.target.value)} aria-label="Фильтр" /><SmallButton variant="primary" onClick={save}>Сохранить</SmallButton></div>
      {err && <Message kind="err" text={err} />}
      <Table head={["", "Элемент", "Ключ", "Роль в уроке"]}>
        {shown.map((i) => (
          <tr key={i.id}>
            <td className="px-2 py-1">{i.emoji}</td>
            <td className="px-2 py-1 font-bold">{i.text}</td>
            <td className="px-2 py-1 font-mono text-xs">{i.key}</td>
            <td className="px-2 py-1">
              <Select value={roles[i.id] ?? ""} onChange={(e) => setRoles({ ...roles, [i.id]: e.target.value })} aria-label={`Роль ${i.text}`}>
                <option value="">не используется</option><option value="NEW">NEW</option><option value="RECENT_REVIEW">RECENT_REVIEW</option><option value="OLDER_REVIEW">OLDER_REVIEW</option>
              </Select>
            </td>
          </tr>
        ))}
      </Table>
    </div>
  );
}

/* ---------- Exercises ---------- */
function ExercisesTab({ lesson, items, media, onSaved }: { lesson: LessonAdmin; items: LearningItemAdmin[]; media: MediaAdmin[]; onSaved: (m: string) => void }) {
  const [editing, setEditing] = useState<ExerciseAdmin | "new" | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const typeLabel = (t: string) => TYPES.find((x) => x.value === t)?.label ?? t;
  async function remove(ex: ExerciseAdmin) {
    if (!window.confirm(`Удалить упражнение «${ex.key}»?`)) return;
    try { await send("DELETE", `/admin/exercises/${ex.id}`); onSaved("Упражнение удалено."); } catch (e) { setErr(errorText(e)); }
  }
  const nextPosition = Math.max(0, ...lesson.exercises.map((e) => e.position)) + 1;
  const done = (m: string) => { setEditing(null); onSaved(m); };
  return (
    <div className="space-y-3">
      <SmallButton variant="primary" onClick={() => setEditing("new")}>+ Упражнение</SmallButton>
      {err && <Message kind="err" text={err} />}
      {editing === "new" && <ExerciseEditor lessonId={lesson.id} items={items} media={media} nextPosition={nextPosition} onSaved={() => done("Упражнение создано.")} onCancel={() => setEditing(null)} />}
      <Table head={["#", "Ключ", "Тип", "Раздел", "Режим", "Баллы", "Версия", "Ответов", ""]}>
        {lesson.exercises.map((ex) => editing !== "new" && editing?.id === ex.id ? (
          <tr key={ex.id}><td colSpan={9}><ExerciseEditor lessonId={lesson.id} exercise={ex} items={items} media={media} nextPosition={nextPosition} onSaved={() => done("Упражнение сохранено.")} onCancel={() => setEditing(null)} /></td></tr>
        ) : (
          <tr key={ex.id}>
            <td className="px-2 py-1">{ex.position}</td>
            <td className="px-2 py-1 font-mono text-xs">{ex.key}</td>
            <td className="px-2 py-1">{typeLabel(ex.type)}</td>
            <td className="px-2 py-1">{ex.section}</td>
            <td className="px-2 py-1">{ex.recall_mode === "RECALL" ? "воспр." : "узнав."}</td>
            <td className="px-2 py-1">{ex.points}</td>
            <td className="px-2 py-1">v{ex.version}</td>
            <td className="px-2 py-1">{ex.attempt_count}</td>
            <td className="whitespace-nowrap px-2 py-1 text-right">
              <SmallButton onClick={() => setEditing(ex)}>Изменить</SmallButton>{" "}
              <SmallButton variant="danger" disabled={ex.attempt_count > 0} title={ex.attempt_count > 0 ? "Есть ответы учеников — удалить нельзя" : undefined} onClick={() => remove(ex)}>Удалить</SmallButton>
            </td>
          </tr>
        ))}
      </Table>
    </div>
  );
}

/* ---------- Episodes ---------- */
function EpisodesTab({ lesson, media, onSaved }: { lesson: LessonAdmin; media: MediaAdmin[]; onSaved: (m: string) => void }) {
  const [err, setErr] = useState<string | null>(null);
  const [title, setTitle] = useState("");
  const run = async (fn: () => Promise<unknown>, m: string) => { try { await fn(); setErr(null); onSaved(m); } catch (e) { setErr(errorText(e)); } };
  const opts = (t: MediaAdmin["media_type"]) => media.filter((m) => m.media_type === t);
  return (
    <div className="space-y-4">
      <p className="text-sm text-muted">Мультфильмы пока не готовы. Эпизод без видео показывает ученикам заглушку «Cartoon coming soon». Чтобы добавить видео: загрузите MP4/WebM (и субтитры .vtt) в «Медиафайлы», затем выберите их здесь.</p>
      {err && <Message kind="err" text={err} />}
      {lesson.episodes.map((ep) => (
        <EpisodeRow key={ep.id} ep={ep} videos={opts("VIDEO")} subs={opts("SUBTITLE")} images={opts("IMAGE")} run={run} />
      ))}
      <form className="flex items-end gap-2" onSubmit={(e) => { e.preventDefault(); run(() => send("POST", `/admin/lessons/${lesson.id}/episodes`, { title, position: lesson.episodes.length + 1 }), "Эпизод создан."); setTitle(""); }}>
        <Field label="Новый эпизод"><Input value={title} onChange={(e) => setTitle(e.target.value)} required placeholder="Название" /></Field>
        <SmallButton type="submit">Добавить</SmallButton>
      </form>
    </div>
  );
}

function EpisodeRow({ ep, videos, subs, images, run }: { ep: LessonAdmin["episodes"][number]; videos: MediaAdmin[]; subs: MediaAdmin[]; images: MediaAdmin[]; run: (fn: () => Promise<unknown>, m: string) => void }) {
  const [f, setF] = useState({ title: ep.title, synopsis: ep.synopsis, video: ep.video_asset_id ?? "", sub: ep.subtitle_asset_id ?? "", poster: ep.poster_image_id ?? "" });
  return (
    <div className="grid gap-2 rounded-lg border border-line p-3 lg:grid-cols-2">
      <Field label="Название"><Input value={f.title} onChange={(e) => setF({ ...f, title: e.target.value })} /></Field>
      <Field label="Краткое содержание"><Input value={f.synopsis} onChange={(e) => setF({ ...f, synopsis: e.target.value })} /></Field>
      <Field label="Видео"><Select value={f.video} onChange={(e) => setF({ ...f, video: e.target.value })}><option value="">— нет видео —</option>{videos.map((m) => <option key={m.id} value={m.id}>{m.original_filename}</option>)}</Select></Field>
      <Field label="Субтитры (WebVTT)"><Select value={f.sub} onChange={(e) => setF({ ...f, sub: e.target.value })}><option value="">—</option>{subs.map((m) => <option key={m.id} value={m.id}>{m.original_filename}</option>)}</Select></Field>
      <Field label="Постер"><Select value={f.poster} onChange={(e) => setF({ ...f, poster: e.target.value })}><option value="">—</option>{images.map((m) => <option key={m.id} value={m.id}>{m.original_filename}</option>)}</Select></Field>
      <div className="flex flex-wrap items-end gap-2">
        <StatusPill status={ep.status} />
        <SmallButton variant="primary" onClick={() => run(async () => {
          await send("PATCH", `/admin/episodes/${ep.id}`, { title: f.title, synopsis: f.synopsis });
          await send("PUT", `/admin/episodes/${ep.id}/media`, { video_asset_id: f.video || null, subtitle_asset_id: f.sub || null, poster_image_id: f.poster || null });
        }, "Эпизод сохранён.")}>Сохранить</SmallButton>
        <SmallButton onClick={() => run(() => send("PATCH", `/admin/episodes/${ep.id}`, { status: ep.status === "PUBLISHED" ? "DRAFT" : "PUBLISHED" }), "Статус эпизода изменён.")}>
          {ep.status === "PUBLISHED" ? "Скрыть" : "Показать ученикам"}
        </SmallButton>
      </div>
    </div>
  );
}

/* ---------- Page ---------- */
export default function LessonEditorPage() {
  const { id } = useParams<{ id: string }>();
  const lesson = useApi<LessonAdmin>(`/admin/lessons/${id}`);
  const items = useApi<Page<LearningItemAdmin>>("/admin/learning-items?page_size=500");
  const media = useApi<Page<MediaAdmin>>("/admin/media?page_size=100");
  const [report, setReport] = useState<ValidationReport | null>(null);
  const [tab, setTab] = useState<Tab>("main");
  const [msg, setMsg] = useState<{ kind: "ok" | "err"; text: string } | null>(null);
  const reloadLesson = lesson.reload;

  const validate = useCallback(() => {
    api<ValidationReport>(`/admin/lessons/${id}/validation`).then(setReport).catch(() => setReport(null));
  }, [id]);
  useEffect(validate, [validate, lesson.data]);

  const saved = (text: string) => { setMsg({ kind: "ok", text }); reloadLesson(); };

  if (lesson.loading && !lesson.data) return <LoadingState label="Загрузка урока…" />;
  if (lesson.error || !lesson.data) return <ErrorState message={lesson.error?.message ?? "Ошибка"} onRetry={lesson.reload} />;
  const l = lesson.data;

  async function publish(action: "publish" | "unpublish") {
    try {
      await send("POST", `/admin/lessons/${id}/${action}`);
      saved(action === "publish" ? "Урок опубликован." : "Урок снят с публикации. Прогресс учеников сохранён.");
    } catch (e) { setMsg({ kind: "err", text: errorText(e) }); }
  }

  return (
    <>
      <Link href="/admin/courses" className="text-sm font-bold text-sky underline">← Курсы и уроки</Link>
      <div className="flex flex-wrap items-center gap-3">
        <h1 className="text-2xl font-black">{l.title}</h1>
        <StatusPill status={l.status} />
        <span className="text-sm text-muted">версия контента v{l.content_version} · {l.cefr_level} · изменён {fmtDate(l.updated_at)}</span>
      </div>

      <Panel title="Публикация" actions={<>
        <Link href={`/admin/lessons/${id}/preview`} className="rounded-lg border border-line px-3 py-1.5 text-sm font-bold hover:border-sky">Просмотр как ученик</Link>
        {l.status === "PUBLISHED"
          ? <SmallButton onClick={() => publish("unpublish")}>Снять с публикации</SmallButton>
          : <SmallButton variant="primary" disabled={!report || report.errors.length > 0} onClick={() => publish("publish")}>Опубликовать</SmallButton>}
      </>}>
        {!report ? <p className="text-sm text-muted">Проверка…</p> : (
          <div className="grid gap-2 text-sm md:grid-cols-2">
            <div>
              <p className="font-bold">{report.errors.length ? `Ошибки (${report.errors.length}) — публикация невозможна` : "Ошибок нет ✓"}</p>
              <ul className="list-disc pl-5 text-err-ink">{report.errors.map((e) => <li key={e}>{e}</li>)}</ul>
            </div>
            <div>
              <p className="font-bold">Предупреждения ({report.warnings.length})</p>
              <ul className="list-disc pl-5 text-warn-ink">{report.warnings.map((w) => <li key={w}>{w}</li>)}</ul>
            </div>
          </div>
        )}
        {l.status === "PUBLISHED" && <p className="text-xs text-muted">Урок опубликован: изменения видны ученикам сразу и увеличивают версию контента.</p>}
      </Panel>
      {msg && <Message kind={msg.kind} text={msg.text} />}

      <div role="tablist" aria-label="Разделы редактора" className="flex flex-wrap gap-1">
        {(Object.keys(TAB_LABELS) as Tab[]).map((t) => (
          <button key={t} role="tab" type="button" aria-selected={tab === t} onClick={() => { setTab(t); setMsg(null); }}
            className={`rounded-lg px-3 py-2 text-sm font-bold ${tab === t ? "bg-ink text-white" : "bg-surface hover:bg-line"}`}>
            {TAB_LABELS[t]}{t === "exercises" ? ` (${l.exercises.length})` : ""}
          </button>
        ))}
      </div>
      <Panel>
        {tab === "main" && <MainTab key={l.updated_at} lesson={l} onSaved={saved} />}
        {tab === "content" && <ContentTab key={l.updated_at} lesson={l} onSaved={saved} />}
        {tab === "items" && <ItemsTab key={l.updated_at} lesson={l} items={items.data?.items ?? []} onSaved={saved} />}
        {tab === "exercises" && <ExercisesTab lesson={l} items={items.data?.items ?? []} media={media.data?.items ?? []} onSaved={saved} />}
        {tab === "episodes" && <EpisodesTab lesson={l} media={media.data?.items ?? []} onSaved={saved} />}
      </Panel>
    </>
  );
}
