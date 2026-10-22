"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useState } from "react";
import { Field, Input, Message, Panel, Select, SmallButton, StatusPill, Table } from "@/components/admin";
import { ErrorState, LoadingState, ProgressBar } from "@/components/ui";
import { errorText, send } from "@/lib/api";
import { fmtDate, type AdminUser, type CourseNode } from "@/lib/adminTypes";
import type { LessonProgress, Mastery } from "@/lib/types";
import { useApi } from "@/lib/useApi";

interface StudentProgress {
  lessons: (LessonProgress & { lesson_id: string; lesson_title: string })[];
  mastery: Mastery[];
  enrollments: { id: string; course_id: string; current_level: string; current_lesson_id: string | null; status: string }[];
  recent_attempts: { id: string; exercise_id: string; lesson_id: string; is_correct: boolean | null; score: number; max_score: number; created_at: string; exercise_version: number }[];
}

export default function StudentPage() {
  const { id } = useParams<{ id: string }>();
  const student = useApi<AdminUser>(`/admin/students/${id}`);
  const progress = useApi<StudentProgress>(`/admin/students/${id}/progress`);
  const courses = useApi<CourseNode[]>("/admin/courses");
  const [msg, setMsg] = useState<{ kind: "ok" | "err"; text: string } | null>(null);
  const [edit, setEdit] = useState<{ display_name: string; email: string } | null>(null);
  const [enroll, setEnroll] = useState({ course_id: "", cefr_level: "A1" });

  if (student.loading) return <LoadingState label="Загрузка…" />;
  if (student.error || !student.data) return <ErrorState message={student.error?.message ?? "Ошибка"} onRetry={student.reload} />;
  const u = student.data;

  async function act(fn: () => Promise<unknown>, ok: string) {
    setMsg(null);
    try {
      await fn();
      setMsg({ kind: "ok", text: ok });
      student.reload();
      progress.reload();
    } catch (e) {
      setMsg({ kind: "err", text: errorText(e) });
    }
  }

  const setStatus = (status: string, label: string) => {
    if (status !== "ACTIVE" && !window.confirm(`${label}: ученик потеряет доступ, история обучения сохранится. Продолжить?`)) return;
    act(() => send("POST", `/admin/students/${id}/status`, { status }), `Статус изменён: ${label}.`);
  };
  async function issueReset() {
    setMsg(null);
    try {
      const r = await send<{ token: string; expires_at: string }>("POST", `/admin/students/${id}/password-reset`);
      setMsg({ kind: "ok", text: `Одноразовый код сброса пароля (до ${fmtDate(r.expires_at)}):\n${r.token}\nУченик вводит его на странице /reset-password.` });
    } catch (e) {
      setMsg({ kind: "err", text: errorText(e) });
    }
  }
  const lessonTitle = (lid: string) => progress.data?.lessons.find((l) => l.lesson_id === lid)?.lesson_title ?? lid.slice(0, 8);
  const courseTitle = (cid: string) => courses.data?.find((c) => c.id === cid)?.title ?? cid.slice(0, 8);

  return (
    <>
      <Link href="/admin/students" className="text-sm font-bold text-sky underline">← Все ученики</Link>
      <h1 className="flex flex-wrap items-center gap-3 text-2xl font-black">{u.display_name} <StatusPill status={u.status} /></h1>
      <Message kind={msg?.kind ?? "ok"} text={msg?.text ?? null} />

      <div className="grid gap-4 lg:grid-cols-2">
        <Panel title="Профиль" actions={!edit && <SmallButton onClick={() => setEdit({ display_name: u.display_name, email: u.email ?? "" })}>Изменить</SmallButton>}>
          {edit ? (
            <form className="space-y-3" onSubmit={(e) => { e.preventDefault(); act(() => send("PATCH", `/admin/students/${id}`, { display_name: edit.display_name, email: edit.email || null }), "Профиль сохранён.").then(() => setEdit(null)); }}>
              <Field label="Имя"><Input value={edit.display_name} onChange={(e) => setEdit({ ...edit, display_name: e.target.value })} required /></Field>
              <Field label="Email"><Input type="email" value={edit.email} onChange={(e) => setEdit({ ...edit, email: e.target.value })} /></Field>
              <div className="flex gap-2"><SmallButton type="submit" variant="primary">Сохранить</SmallButton><SmallButton onClick={() => setEdit(null)}>Отмена</SmallButton></div>
            </form>
          ) : (
            <dl className="grid grid-cols-2 gap-1 text-sm">
              <dt className="text-muted">Логин</dt><dd>{u.username}</dd>
              <dt className="text-muted">Email</dt><dd>{u.email ?? "—"}</dd>
              <dt className="text-muted">Создан</dt><dd>{fmtDate(u.created_at)}</dd>
              <dt className="text-muted">Последний вход</dt><dd>{fmtDate(u.last_login_at)}</dd>
              <dt className="text-muted">Активность</dt><dd>{fmtDate(u.last_activity_at)}</dd>
            </dl>
          )}
        </Panel>

        <Panel title="Доступ">
          <div className="flex flex-wrap gap-2">
            {u.status !== "ACTIVE" && u.status !== "INVITED" && <SmallButton variant="primary" onClick={() => setStatus("ACTIVE", "Активен")}>Восстановить доступ</SmallButton>}
            {u.status === "ACTIVE" && <SmallButton onClick={() => setStatus("SUSPENDED", "Приостановлен")}>Приостановить</SmallButton>}
            {u.status !== "INACTIVE" && <SmallButton variant="danger" onClick={() => setStatus("INACTIVE", "Отключён")}>Отключить</SmallButton>}
            {(u.status === "ACTIVE" || u.status === "INVITED") && (
<SmallButton onClick={issueReset}>Код для сброса пароля</SmallButton>
            )}
          </div>
          <p className="text-xs text-muted">Учётные записи не удаляются: история обучения всегда сохраняется.</p>
        </Panel>
      </div>

      <Panel title="Курс и уровень">
        {progress.data?.enrollments.length ? (
          <ul className="text-sm">{progress.data.enrollments.map((e) => <li key={e.id}>{courseTitle(e.course_id)} · уровень {e.current_level} · {e.status}</li>)}</ul>
        ) : <p className="text-sm text-muted">Ученик ещё не записан на курс.</p>}
        <form className="flex flex-wrap items-end gap-2" onSubmit={(e) => { e.preventDefault(); if (enroll.course_id) act(() => send("PUT", `/admin/students/${id}/enrollment`, enroll), "Курс назначен."); }}>
          <Field label="Курс">
            <Select value={enroll.course_id} onChange={(e) => setEnroll({ ...enroll, course_id: e.target.value })} required>
              <option value="">— выберите —</option>
              {courses.data?.map((c) => <option key={c.id} value={c.id}>{c.title}</option>)}
            </Select>
          </Field>
          <Field label="Уровень">
            <Select value={enroll.cefr_level} onChange={(e) => setEnroll({ ...enroll, cefr_level: e.target.value })}>
              {["A1", "A2", "B1", "B2", "C1"].map((l) => <option key={l}>{l}</option>)}
            </Select>
          </Field>
          <SmallButton type="submit" variant="primary">Назначить</SmallButton>
        </form>
      </Panel>

      {progress.loading ? <LoadingState label="Загрузка прогресса…" /> : progress.data && (
        <>
          <Panel title="Уроки">
            {progress.data.lessons.length === 0 ? <p className="text-sm text-muted">Уроки ещё не начаты.</p> : (
              <Table head={["Урок", "Статус", "Баллы", "Тест", "Завершён"]}>
                {progress.data.lessons.map((l) => (
                  <tr key={l.lesson_id}>
                    <td className="px-2 py-2 font-bold">{l.lesson_title}</td>
                    <td className="px-2 py-2">{l.status === "COMPLETED" ? "Пройден" : "В процессе"}</td>
                    <td className="px-2 py-2">{l.score} / {l.max_score}</td>
                    <td className="px-2 py-2">{l.best_quiz_percent != null ? `${Math.round(l.best_quiz_percent)}%` : "—"}</td>
                    <td className="px-2 py-2">{fmtDate(l.completed_at)}</td>
                  </tr>
                ))}
              </Table>
            )}
          </Panel>
          <Panel title="Освоение слов и грамматики">
            <p className="text-xs text-muted">«Освоено» требует и узнавания, и активного воспроизведения (≥ 0.8). Прохождение урока ≠ освоение.</p>
            {progress.data.mastery.length === 0 ? <p className="text-sm text-muted">Нет данных.</p> : (
              <Table head={["Элемент", "Освоение", "Узнал / Воспроизвёл", "Ошибки", "Следующее повторение"]}>
                {progress.data.mastery.map((m) => (
                  <tr key={m.item.id}>
                    <td className="px-2 py-2 font-bold">{m.item.emoji} {m.item.text}</td>
                    <td className="w-40 px-2 py-2"><ProgressBar value={Math.round(m.mastery * 100)} max={100} label={`Освоение ${m.item.text}`} color={m.mastered ? "bg-leaf" : "bg-sun"} /></td>
                    <td className="px-2 py-2">{m.recognition_correct} / {m.recall_correct}</td>
                    <td className="px-2 py-2">{m.incorrect}</td>
                    <td className="px-2 py-2">{fmtDate(m.next_review_at)}</td>
                  </tr>
                ))}
              </Table>
            )}
          </Panel>
          <Panel title="Последние ответы (50)">
            {progress.data.recent_attempts.length === 0 ? <p className="text-sm text-muted">Нет ответов.</p> : (
              <Table head={["Когда", "Урок", "Результат", "Баллы", "Версия упр."]}>
                {progress.data.recent_attempts.map((a) => (
                  <tr key={a.id}>
                    <td className="px-2 py-2">{fmtDate(a.created_at)}</td>
                    <td className="px-2 py-2">{lessonTitle(a.lesson_id)}</td>
                    <td className="px-2 py-2">{a.is_correct === null ? "без оценки" : a.is_correct ? "верно" : "неверно"}</td>
                    <td className="px-2 py-2">{a.score} / {a.max_score}</td>
                    <td className="px-2 py-2">v{a.exercise_version}</td>
                  </tr>
                ))}
              </Table>
            )}
          </Panel>
        </>
      )}
    </>
  );
}
