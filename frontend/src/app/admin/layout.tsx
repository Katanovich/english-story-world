"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { LoadingState } from "@/components/ui";
import { useAuth, useRequireRole } from "@/lib/auth";

const NAV = [
  { href: "/admin", label: "Обзор" },
  { href: "/admin/students", label: "Ученики" },
  { href: "/admin/courses", label: "Курсы и уроки" },
  { href: "/admin/items", label: "Слова и грамматика" },
  { href: "/admin/media", label: "Медиафайлы" },
  { href: "/admin/audit", label: "Журнал действий" },
];

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  const user = useRequireRole("ADMIN");
  const { logout } = useAuth();
  const pathname = usePathname();
  const router = useRouter();
  if (!user) return <LoadingState label="Загрузка…" />;
  const active = (href: string) => (href === "/admin" ? pathname === href : pathname.startsWith(href));
  return (
    <div lang="ru" className="min-h-screen bg-[#f6f7fb] md:flex">
      <aside className="border-b border-line bg-surface md:min-h-screen md:w-60 md:border-r md:border-b-0">
        <div className="flex items-center gap-2 px-4 py-4 font-black">English Story World · Админ</div>
        <nav aria-label="Администрирование" className="flex gap-1 overflow-x-auto px-2 pb-2 md:flex-col md:pb-0">
          {NAV.map((n) => (
            <Link
              key={n.href}
              href={n.href}
              aria-current={active(n.href) ? "page" : undefined}
              className={`whitespace-nowrap rounded-lg px-3 py-2 text-sm font-bold ${active(n.href) ? "bg-ink text-white" : "hover:bg-line"}`}
            >
              {n.label}
            </Link>
          ))}
          <button
            type="button"
            className="whitespace-nowrap rounded-lg px-3 py-2 text-left text-sm font-bold text-muted hover:bg-line md:mt-6"
            onClick={async () => { await logout(); router.replace("/login"); }}
          >
            Выйти ({user.username})
          </button>
        </nav>
      </aside>
      <main className="min-w-0 flex-1 space-y-4 p-4 md:p-6">{children}</main>
    </div>
  );
}
