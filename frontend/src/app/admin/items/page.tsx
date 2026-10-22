"use client";

import { useState } from "react";
import { Field, Input, Message, Pager, Panel, Select, SmallButton, Table, TextArea } from "@/components/admin";
import { ErrorState, LoadingState } from "@/components/ui";
import { errorText, send } from "@/lib/api";
import type { LearningItemAdmin } from "@/lib/adminTypes";
import type { Page } from "@/lib/types";
import { useApi } from "@/lib/useApi";

const KINDS = ["VOCABULARY", "PHRASE", "GRAMMAR", "PRONUNCIATION", "READING", "LISTENING"];
const empty = { key: "", kind: "VOCABULARY", text: "", emoji: "", translation_ru: "", explanation: "", cefr_level: "A1", examples: "" };

function ItemForm({ initial, onSaved, onCancel }: { initial?: LearningItemAdmin; onSaved: () => void; onCancel: () => void }) {
  const [f, setF] = useState(initial ? { ...empty, ...initial, emoji: initial.emoji ?? "", translation_ru: initial.translation_ru ?? "", explanation: initial.explanation ?? "", examples: initial.examples.join("\n") } : empty);
  const [err, setErr] = useState<string | null>(null);
  const set = (k: keyof typeof f) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => setF({ ...f, [k]: e.target.value });
  async function submit(e: React.FormEvent) {
    e.preventDefault();
    const body = {
      kind: f.kind, text: f.text, emoji: f.emoji || null, translation_ru: f.translation_ru || null,
      explanation: f.explanation || null, cefr_level: f.cefr_level,
      examples: f.examples.split("\n").map((x) => x.trim()).filter(Boolean),
    };
    try {
      if (initial) await send("PATCH", `/admin/learning-items/${initial.id}`, body);
      else await send("POST", "/admin/learning-items", { ...body, key: f.key });
      onSaved();
    } catch (e2) {
      setErr(errorText(e2));
    }
  }
  return (
    <form onSubmit={submit} className="grid gap-3 rounded-lg bg-bg p-3 sm:grid-cols-3">
      <Field label="Ключ *" hint="стабильный, напр. vocab.cat"><Input value={f.key} onChange={set("key")} required disabled={!!initial} pattern="[a-z0-9_.\-]+" /></Field>
      <Field label="Тип"><Select value={f.kind} onChange={set("kind")}>{KINDS.map((k) => <option key={k}>{k}</option>)}</Select></Field>
      <Field label="Уровень"><Select value={f.cefr_level} onChange={set("cefr_level")}>{["A1", "A2", "B1", "B2", "C1", "C2"].map((l) => <option key={l}>{l}</option>)}</Select></Field>
      <Field label="Текст *"><Input value={f.text} onChange={set("text")} required /></Field>
      <Field label="Эмодзи-иллюстрация"><Input value={f.emoji} onChange={set("emoji")} maxLength={16} /></Field>
      <Field label="Перевод"><Input value={f.translation_ru} onChange={set("translation_ru")} /></Field>
      <Field label="Пояснение"><TextArea rows={2} value={f.explanation} onChange={set("explanation")} /></Field>
      <Field label="Примеры" hint="по одному на строку"><TextArea rows={2} value={f.examples} onChange={set("examples")} /></Field>
      <div className="flex items-end gap-2"><SmallButton type="submit" variant="primary">Сохранить</SmallButton><SmallButton onClick={onCancel}>Отмена</SmallButton></div>
      {err && <div className="sm:col-span-3"><Message kind="err" text={err} /></div>}
    </form>
  );
}

export default function ItemsPage() {
  const [q, setQ] = useState("");
  const [query, setQuery] = useState("");
  const [page, setPage] = useState(1);
  const [editing, setEditing] = useState<LearningItemAdmin | "new" | null>(null);
  const qs = new URLSearchParams({ page: String(page), page_size: "50" });
  if (query) qs.set("q", query);
  const { data, error, loading, reload } = useApi<Page<LearningItemAdmin>>(`/admin/learning-items?${qs}`);
  const saved = () => { setEditing(null); reload(); };

  return (
    <>
      <div className="flex items-center gap-2">
        <h1 className="text-2xl font-black">Слова и грамматика</h1>
        <SmallButton className="ml-auto" variant="primary" onClick={() => setEditing("new")}>+ Элемент</SmallButton>
      </div>
      <p className="text-sm text-muted">Элементы переиспользуются в уроках и упражнениях; ключ не меняется, чтобы сохранить историю повторений.</p>
      {editing === "new" && <ItemForm onSaved={saved} onCancel={() => setEditing(null)} />}
      <Panel>
        <form className="flex items-end gap-2" onSubmit={(e) => { e.preventDefault(); setPage(1); setQuery(q); }}>
          <Field label="Поиск"><Input value={q} onChange={(e) => setQ(e.target.value)} placeholder="текст, ключ, перевод" /></Field>
          <SmallButton type="submit">Найти</SmallButton>
        </form>
        {loading ? <LoadingState /> : error || !data ? <ErrorState message={error?.message ?? "Ошибка"} onRetry={reload} /> : (
          <>
            <Table head={["", "Текст", "Ключ", "Тип", "Перевод", ""]}>
              {data.items.map((i) => editing !== "new" && editing?.id === i.id ? (
                <tr key={i.id}><td colSpan={6}><ItemForm initial={i} onSaved={saved} onCancel={() => setEditing(null)} /></td></tr>
              ) : (
                <tr key={i.id}>
                  <td className="px-2 py-2 text-xl">{i.emoji}</td>
                  <td className="px-2 py-2 font-bold">{i.text}</td>
                  <td className="px-2 py-2 font-mono text-xs">{i.key}</td>
                  <td className="px-2 py-2">{i.kind}</td>
                  <td className="px-2 py-2">{i.translation_ru}</td>
                  <td className="px-2 py-2 text-right"><SmallButton onClick={() => setEditing(i)}>Изменить</SmallButton></td>
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
