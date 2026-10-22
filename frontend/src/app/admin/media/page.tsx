"use client";

import { useState } from "react";
import { Field, Input, Message, Pager, Panel, Select, SmallButton, Table } from "@/components/admin";
import { ErrorState, LoadingState } from "@/components/ui";
import { api, errorText } from "@/lib/api";
import { fmtDate, type MediaAdmin } from "@/lib/adminTypes";
import type { Page } from "@/lib/types";
import { useApi } from "@/lib/useApi";

const TYPES = { IMAGE: "Изображение (png, jpg, webp)", AUDIO: "Аудио (mp3, wav, ogg, m4a, webm)", VIDEO: "Видео (mp4, webm)", SUBTITLE: "Субтитры (WebVTT .vtt)" };

export default function MediaPage() {
  const [type, setType] = useState("");
  const [page, setPage] = useState(1);
  const qs = new URLSearchParams({ page: String(page), page_size: "20" });
  if (type) qs.set("media_type", type);
  const { data, error, loading, reload } = useApi<Page<MediaAdmin>>(`/admin/media?${qs}`);
  const [upType, setUpType] = useState("IMAGE");
  const [file, setFile] = useState<File | null>(null);
  const [alt, setAlt] = useState("");
  const [msg, setMsg] = useState<{ kind: "ok" | "err"; text: string } | null>(null);
  const [busy, setBusy] = useState(false);

  async function upload(e: React.FormEvent) {
    e.preventDefault();
    if (!file) return;
    const form = new FormData();
    form.append("file", file);
    form.append("media_type", upType);
    if (alt) form.append("alt_text", alt);
    setBusy(true);
    setMsg(null);
    try {
      const a = await api<MediaAdmin>("/admin/media", { method: "POST", body: form });
      setMsg({ kind: "ok", text: `Загружено: ${a.original_filename} (id ${a.id})` });
      setFile(null);
      setAlt("");
      (e.target as HTMLFormElement).reset();
      reload();
    } catch (err) {
      setMsg({ kind: "err", text: errorText(err) });
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      <h1 className="text-2xl font-black">Медиафайлы</h1>
      <Panel title="Загрузить">
        <form onSubmit={upload} className="flex flex-wrap items-end gap-3">
          <Field label="Тип"><Select value={upType} onChange={(e) => setUpType(e.target.value)}>{Object.entries(TYPES).map(([k, v]) => <option key={k} value={k}>{v}</option>)}</Select></Field>
          <Field label="Файл"><Input type="file" required onChange={(e) => setFile(e.target.files?.[0] ?? null)} /></Field>
          <Field label="Альтернативный текст" hint="описание для незрячих"><Input value={alt} onChange={(e) => setAlt(e.target.value)} maxLength={255} /></Field>
          <SmallButton type="submit" variant="primary" disabled={busy || !file}>{busy ? "Загрузка…" : "Загрузить"}</SmallButton>
        </form>
        {msg && <Message kind={msg.kind} text={msg.text} />}
        <p className="text-xs text-muted">Файлы проверяются по расширению и содержимому; хранятся приватно (локальное хранилище; S3 — см. README). Видео прикрепляется к эпизоду на странице урока.</p>
      </Panel>
      <Panel title="Библиотека" actions={
        <Select value={type} onChange={(e) => { setType(e.target.value); setPage(1); }} aria-label="Фильтр по типу">
          <option value="">Все типы</option>{Object.keys(TYPES).map((k) => <option key={k}>{k}</option>)}
        </Select>}>
        {loading ? <LoadingState /> : error || !data ? <ErrorState message={error?.message ?? "Ошибка"} onRetry={reload} /> : data.items.length === 0 ? <p className="text-sm text-muted">Файлов пока нет.</p> : (
          <>
            <Table head={["", "Файл", "Тип", "Размер", "Загружен", "ID"]}>
              {data.items.map((m) => (
                <tr key={m.id}>
                  <td className="px-2 py-2">
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    {m.media_type === "IMAGE" ? <img src={m.url} alt={m.alt_text ?? ""} className="h-10 w-10 rounded object-cover" /> : <a className="text-sky underline" href={m.url} target="_blank" rel="noreferrer">открыть</a>}
                  </td>
                  <td className="px-2 py-2">{m.original_filename}</td>
                  <td className="px-2 py-2">{m.media_type}</td>
                  <td className="px-2 py-2">{(m.size_bytes / 1024).toFixed(0)} КБ</td>
                  <td className="px-2 py-2">{fmtDate(m.created_at)}</td>
                  <td className="px-2 py-2 font-mono text-xs">{m.id}</td>
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
