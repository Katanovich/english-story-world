import Link from "next/link";
import type { ComponentProps, ReactNode } from "react";

type Variant = "primary" | "secondary" | "ghost" | "danger";
type Size = "md" | "lg";

const base =
  "inline-flex items-center justify-center gap-2 rounded-2xl font-bold transition-colors " +
  "disabled:cursor-not-allowed disabled:opacity-50 select-none";
const variants: Record<Variant, string> = {
  primary: "bg-brand text-brand-ink hover:bg-brand-strong shadow-[0_4px_0_var(--brand-strong)]",
  secondary: "bg-surface text-ink border-2 border-line hover:border-sky",
  ghost: "text-ink hover:bg-line/60",
  danger: "bg-err-bg text-err-ink hover:bg-berry hover:text-white",
};
const sizes: Record<Size, string> = {
  md: "min-h-11 px-4 text-base",
  lg: "min-h-14 px-6 text-lg",
};

export function buttonClass(variant: Variant = "primary", size: Size = "md", extra = "") {
  return `${base} ${variants[variant]} ${sizes[size]} ${extra}`;
}

export function Button({
  variant = "primary",
  size = "md",
  className = "",
  ...props
}: ComponentProps<"button"> & { variant?: Variant; size?: Size }) {
  return <button type="button" className={buttonClass(variant, size, className)} {...props} />;
}

export function LinkButton({
  variant = "primary",
  size = "md",
  className = "",
  ...props
}: ComponentProps<typeof Link> & { variant?: Variant; size?: Size }) {
  return <Link className={buttonClass(variant, size, className)} {...props} />;
}

export function Card({ className = "", ...props }: ComponentProps<"div">) {
  return (
    <div
      className={`rounded-3xl border-2 border-line bg-surface p-5 sm:p-6 ${className}`}
      {...props}
    />
  );
}

export function ProgressBar({
  value,
  max,
  label,
  color = "bg-leaf",
}: {
  value: number;
  max: number;
  label: string;
  color?: string;
}) {
  const pct = max > 0 ? Math.round((value / max) * 100) : 0;
  return (
    <div
      role="progressbar"
      aria-label={label}
      aria-valuemin={0}
      aria-valuemax={max}
      aria-valuenow={value}
      className="h-4 w-full overflow-hidden rounded-full bg-line"
    >
      <div className={`h-full rounded-full ${color} transition-all`} style={{ width: `${pct}%` }} />
    </div>
  );
}

export function LoadingState({ label = "Loading…" }: { label?: string }) {
  return (
    <div role="status" className="flex flex-col items-center gap-3 py-16 text-muted">
      <span className="h-10 w-10 animate-spin rounded-full border-4 border-line border-t-brand" />
      <span className="font-semibold">{label}</span>
    </div>
  );
}

export function ErrorState({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return (
    <div role="alert" className="flex flex-col items-center gap-4 py-12 text-center">
      <span aria-hidden className="text-5xl">
        🙈
      </span>
      <p className="max-w-md font-semibold text-err-ink">{message}</p>
      {onRetry && (
        <Button variant="secondary" onClick={onRetry}>
          Try again
        </Button>
      )}
    </div>
  );
}

export function EmptyState({
  icon = "🌱",
  title,
  children,
}: {
  icon?: string;
  title: string;
  children?: ReactNode;
}) {
  return (
    <div className="flex flex-col items-center gap-3 py-12 text-center">
      <span aria-hidden className="text-5xl">
        {icon}
      </span>
      <h2 className="text-xl font-extrabold">{title}</h2>
      {children && <div className="max-w-md text-muted">{children}</div>}
    </div>
  );
}

export function Badge({
  children,
  tone = "neutral",
}: {
  children: ReactNode;
  tone?: "neutral" | "ok" | "warn" | "brand";
}) {
  const tones = {
    neutral: "bg-line text-ink",
    ok: "bg-ok-bg text-ok-ink",
    warn: "bg-warn-bg text-warn-ink",
    brand: "bg-brand text-brand-ink",
  };
  return (
    <span className={`inline-flex rounded-full px-3 py-1 text-sm font-bold ${tones[tone]}`}>
      {children}
    </span>
  );
}

export function Notice({
  tone = "warn",
  children,
}: {
  tone?: "warn" | "ok" | "err";
  children: ReactNode;
}) {
  const tones = {
    warn: "bg-warn-bg text-warn-ink",
    ok: "bg-ok-bg text-ok-ink",
    err: "bg-err-bg text-err-ink",
  };
  return <div className={`rounded-2xl px-4 py-3 font-semibold ${tones[tone]}`}>{children}</div>;
}
