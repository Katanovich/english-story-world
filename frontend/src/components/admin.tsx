"use client";

import type { ComponentProps, ReactNode } from "react";
import { Button } from "./ui";

/* Compact, efficient controls for the admin area (not the child-facing style). */

export const inputCls =
  "w-full rounded-lg border border-line bg-surface px-3 py-2 text-sm focus:border-sky disabled:bg-bg";

export function Field({ label, hint, children }: { label: string; hint?: string; children: ReactNode }) {
  return (
    <label className="block space-y-1">
      <span className="text-sm font-bold">{label}</span>
      {children}
      {hint && <span className="block text-xs text-muted">{hint}</span>}
    </label>
  );
}

export function Input(props: ComponentProps<"input">) {
  return <input {...props} className={`${inputCls} ${props.className ?? ""}`} />;
}

export function TextArea(props: ComponentProps<"textarea">) {
  return <textarea {...props} className={`${inputCls} font-mono ${props.className ?? ""}`} />;
}

export function Select(props: ComponentProps<"select">) {
  return <select {...props} className={`${inputCls} ${props.className ?? ""}`} />;
}

export function SmallButton({ variant = "secondary", ...props }: ComponentProps<typeof Button>) {
  return <Button variant={variant} {...props} className={`!min-h-9 !rounded-lg !px-3 !text-sm !shadow-none ${props.className ?? ""}`} />;
}

export function Panel({ title, actions, children }: { title?: string; actions?: ReactNode; children: ReactNode }) {
  return (
    <section className="space-y-3 rounded-xl border border-line bg-surface p-4">
      {(title || actions) && (
        <div className="flex flex-wrap items-center gap-2">
          {title && <h2 className="text-lg font-extrabold">{title}</h2>}
          <div className="ml-auto flex flex-wrap gap-2">{actions}</div>
        </div>
      )}
      {children}
    </section>
  );
}

export function Message({ kind, text }: { kind: "ok" | "err"; text: string | null }) {
  if (!text) return null;
  return (
    <p role={kind === "err" ? "alert" : "status"} className={`whitespace-pre-line rounded-lg px-3 py-2 text-sm ${kind === "err" ? "bg-err-bg text-err-ink" : "bg-ok-bg text-ok-ink"}`}>
      {text}
    </p>
  );
}

export function Table({ head, children }: { head: string[]; children: ReactNode }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left text-sm">
        <thead className="border-b border-line text-muted">
          <tr>{head.map((h) => <th key={h} className="px-2 py-2 font-bold">{h}</th>)}</tr>
        </thead>
        <tbody className="divide-y divide-line">{children}</tbody>
      </table>
    </div>
  );
}

export function Pager({ page, pageSize, total, onPage }: { page: number; pageSize: number; total: number; onPage: (p: number) => void }) {
  const pages = Math.max(1, Math.ceil(total / pageSize));
  return (
    <div className="flex items-center gap-2 text-sm">
      <SmallButton disabled={page <= 1} onClick={() => onPage(page - 1)}>←</SmallButton>
      <span>Стр. {page} из {pages} · всего {total}</span>
      <SmallButton disabled={page >= pages} onClick={() => onPage(page + 1)}>→</SmallButton>
    </div>
  );
}

export function StatusPill({ status }: { status: string }) {
  const map: Record<string, string> = {
    PUBLISHED: "bg-ok-bg text-ok-ink",
    ACTIVE: "bg-ok-bg text-ok-ink",
    DRAFT: "bg-warn-bg text-warn-ink",
    INVITED: "bg-warn-bg text-warn-ink",
    SUSPENDED: "bg-err-bg text-err-ink",
    INACTIVE: "bg-line text-muted",
  };
  const ru: Record<string, string> = {
    PUBLISHED: "Опубликован", DRAFT: "Черновик", ACTIVE: "Активен", INVITED: "Приглашён",
    SUSPENDED: "Приостановлен", INACTIVE: "Отключён",
  };
  return <span className={`rounded-full px-2 py-0.5 text-xs font-bold ${map[status] ?? "bg-line"}`}>{ru[status] ?? status}</span>;
}
