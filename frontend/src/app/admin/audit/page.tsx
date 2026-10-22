"use client";

import { useState } from "react";
import { Field, Input, Pager, Panel, SmallButton, Table } from "@/components/admin";
import { ErrorState, LoadingState } from "@/components/ui";
import { fmtDate } from "@/lib/adminTypes";
import type { Page } from "@/lib/types";
import { useApi } from "@/lib/useApi";

interface Entry { id: string; actor_username: string | null; action: string; entity_type: string; entity_id: string | null; details: Record<string, unknown>; created_at: string }

export default function AuditPage() {
  const [a, setA] = useState("");
  const [action, setAction] = useState("");
  const [page, setPage] = useState(1);
  const qs = new URLSearchParams({ page: String(page), page_size: "50" });
  if (action) qs.set("action", action);
  const { data, error, loading, reload } = useApi<Page<Entry>>(`/admin/audit-logs?${qs}`);
  return (
    <>
      <h1 className="text-2xl font-black">Журнал действий</h1>
      <Panel>
        <form className="flex items-end gap-2" onSubmit={(e) => { e.preventDefault(); setPage(1); setAction(a.trim()); }}>
          <Field label="Действие начинается с"><Input value={a} onChange={(e) => setA(e.target.value)} placeholder="lesson, student, media…" /></Field>
          <SmallButton type="submit">Фильтр</SmallButton>
        </form>
        {loading ? <LoadingState /> : error || !data ? <ErrorState message={error?.message ?? "Ошибка"} onRetry={reload} /> : (
          <>
            <Table head={["Когда", "Кто", "Действие", "Объект", "Детали"]}>
              {data.items.map((e) => (
                <tr key={e.id}>
                  <td className="whitespace-nowrap px-2 py-2">{fmtDate(e.created_at)}</td>
                  <td className="px-2 py-2">{e.actor_username ?? "система"}</td>
                  <td className="px-2 py-2 font-mono text-xs">{e.action}</td>
                  <td className="px-2 py-2 font-mono text-xs">{e.entity_type} {e.entity_id?.slice(0, 8)}</td>
                  <td className="max-w-md truncate px-2 py-2 font-mono text-xs" title={JSON.stringify(e.details)}>{JSON.stringify(e.details)}</td>
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
