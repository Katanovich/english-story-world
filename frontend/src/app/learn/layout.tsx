"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { LoadingState } from "@/components/ui";
import { useAuth, useRequireRole } from "@/lib/auth";

const NAV = [
  { href: "/learn", label: "Home", icon: "🏠" },
  { href: "/learn/review", label: "Review", icon: "🔁" },
  { href: "/learn/progress", label: "My words", icon: "⭐" },
  { href: "/learn/episodes", label: "Cartoons", icon: "🎬" },
];

export default function LearnLayout({ children }: { children: React.ReactNode }) {
  const user = useRequireRole("STUDENT");
  const { logout } = useAuth();
  const pathname = usePathname();
  const router = useRouter();
  if (!user) return <LoadingState />;

  return (
    <div className="min-h-screen pb-24 sm:pb-0">
      <header className="sticky top-0 z-10 border-b-2 border-line bg-surface/95 backdrop-blur">
        <div className="mx-auto flex max-w-5xl items-center gap-4 px-4 py-3">
          <Link href="/learn" className="text-xl font-black">
            <span aria-hidden>🌍 </span>English Story World
          </Link>
          <nav aria-label="Main" className="ml-auto hidden gap-1 sm:flex">
            {NAV.map((n) => (
              <Link
                key={n.href}
                href={n.href}
                aria-current={pathname === n.href ? "page" : undefined}
                className={`rounded-xl px-3 py-2 font-bold ${pathname === n.href ? "bg-brand text-brand-ink" : "hover:bg-line"}`}
              >
                {n.label}
              </Link>
            ))}
          </nav>
          <button
            type="button"
            onClick={async () => {
              await logout();
              router.replace("/login");
            }}
            className="ml-auto rounded-xl px-3 py-2 font-bold text-muted hover:bg-line sm:ml-0"
          >
            Log out
          </button>
        </div>
      </header>
      <main className="mx-auto max-w-5xl px-4 py-6">{children}</main>
      {/* Bottom navigation on phones: large touch targets. */}
      <nav aria-label="Main" className="fixed inset-x-0 bottom-0 z-10 grid grid-cols-4 border-t-2 border-line bg-surface sm:hidden">
        {NAV.map((n) => (
          <Link
            key={n.href}
            href={n.href}
            aria-current={pathname === n.href ? "page" : undefined}
            className={`flex min-h-16 flex-col items-center justify-center text-sm font-bold ${pathname === n.href ? "text-brand-strong" : "text-muted"}`}
          >
            <span aria-hidden className="text-2xl">{n.icon}</span>
            {n.label}
          </Link>
        ))}
      </nav>
    </div>
  );
}
