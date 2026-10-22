"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Suspense, useState } from "react";
import { Field, Input, Message, Pager, Panel, Select, SmallButton, StatusPill, Table } from "@/components/admin";
import { ErrorState, LoadingState } from "@/components/ui";
import { errorText, send } from "@/lib/api";
import { fmtDate, STATUS_RU, type AdminUser } from "@/lib/adminTypes";
import type { Page } from "@/lib/types";
import { useApi } from "@/lib/useApi";

function CreateStudent({ onCreated }: { onCreated: () => void }) {
  const [form, setForm] = useState({ username: "", display_name: "", email: "", password: "" });
  const [msg, setMsg] = useState<{ kind: "ok" | "err"; text: string } | null>(null);
  const [busy, setBusy] = useState(false);
  const set = (k: keyof typeof form) => (e: React.ChangeEvent<HTMLInputElement>) => setForm({ ...form, [k]: e.target.value });

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);
    setMsg(null);
    try {
      const r = await send<{ user: AdminUser; set_password_token: string | null }>("POST", "/admin/students", {
        username: form.username,
        display_name: form.display_name,
        email: form.email || null,
        password: form.password || null,
      });
      setMsg({
        kind: "ok",
        text: r.set_password_token
          ? `Ученик создан (приглашён). Одноразовый код для установки пароля (действует 7 дней):\n${r.set_password_token}\nСсылка: /reset-password?token=…`
          : "Ученик создан и активен.",
      });
      setForm({ username: "", display_name: "", email: "", password: "" });
      onCreated();
    } catch (err) {
      setMsg({ kind: "err", text: errorText(err) });
    } finally {
      setBusy(false);
    }
  }

  return (
    <Panel title="Новый ученик">
      <form onSubmit={submit} className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <Field label="Логин *" hint="латиница, цифры, _ . -"><Input required value={form.username} onChange={set("username")} pattern="[a-zA-Z0-9_.\-]{3,64}" /></Field>
        <Field label="Имя для отображения *"><Input required value={form.display_name} onChange={set("display_name")} maxLength={80} /></Field>
        <Field label="Email (необязательно)"><Input type="email" value={form.email} onChange={set("email")} /></Field>
        <Field label="Пароль" hint="Пусто — ученик получит код приглашения"><Input type="password" autoComplete="new-password" value={form.password} onChange={set("password")} /></Field>
        <div className="sm:col-span-2 lg:col-span-4"><SmallButton type="submit" variant="primary" disabled={busy}>{busy ? "Создание…" : "Создать"}</SmallButton></div>
      </form>
      {msg && <Message kind={msg.kind} text={msg.text} />}
      <p className="text-xs text-muted">Храните только необходимые данные о детях: email не обязателен.</p>
    </Panel>
  );
}

function StudentsList() {
  const params = useSearchParams();
  const [q, setQ] = useState("");
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState(params.get("status") ?? "");
  const [page, setPage] = useState(1);
  const qs = new URLSearchParams({ page: String(page), page_size: "20" });
  if (query) qs.set("q", query);
  if (status) qs.set("status", status);
  const { data, error, loading, reload } = useApi<Page<AdminUser>>(`/admin/students?${qs}`);

  return (
    <>
      <h1 className="text-2xl font-black">Ученики</h1>
      <CreateStudent onCreated={reload} />
      <Panel title="Список">
        <form className="flex flex-wrap items-end gap-2" onSubmit={(e) => { e.preventDefault(); setPage(1); setQuery(q.trim()); }}>
          <Field label="Поиск"><Input value={q} onChange={(e) => setQ(e.target.value)} placeholder="имя, логин, email" /></Field>
          <Field label="Статус">
            <Select value={status} onChange={(e) => { setStatus(e.target.value); setPage(1); }}>
              <option value="">Все</option>
              {Object.entries(STATUS_RU).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
            </Select>
          </Field>
          <SmallButton type="submit">Найти</SmallButton>
        </form>
        {loading ? <LoadingState label="Загрузка…" /> : error || !data ? <ErrorState message={error?.message ?? "Ошибка"} onRetry={reload} /> : data.items.length === 0 ? (
          <p className="py-6 text-center text-muted">Учеников не найдено.</p>
        ) : (
          <>
            <Table head={["Имя", "Логин", "Статус", "Последняя активность", ""]}>
              {data.items.map((u) => (
                <tr key={u.id}>
                  <td className="px-2 py-2 font-bold">{u.display_name}</td>
                  <td className="px-2 py-2">{u.username}</td>
                  <td className="px-2 py-2"><StatusPill status={u.status} /></td>
                  <td className="px-2 py-2">{fmtDate(u.last_activity_at)}</td>
                  <td className="px-2 py-2 text-right"><Link className="font-bold text-sky underline" href={`/admin/students/${u.id}`}>Открыть</Link></td>
                </tr>
              ))}
            </Table>
            <Pager page={data.page} pageSize={data.page_size} total={data.total} onPage={setPage} />
          </>
        )}
      </Panel>
    </>
  );
}

export default function StudentsPage() {
  return <Suspense fallback={<LoadingState />}><StudentsList /></Suspense>;
}
