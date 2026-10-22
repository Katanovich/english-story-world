"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { LinkButton, LoadingState } from "@/components/ui";
import { homeFor, useAuth } from "@/lib/auth";

export default function Home() {
  const { user, loading } = useAuth();
  const router = useRouter();
  useEffect(() => {
    if (user) router.replace(homeFor(user.role));
  }, [user, router]);

  if (loading || user) return <LoadingState />;
  return (
    <main className="mx-auto flex min-h-screen max-w-xl flex-col items-center justify-center gap-6 px-6 text-center">
      <span aria-hidden className="text-7xl">👦👧</span>
      <h1 className="text-4xl font-black">English Story World</h1>
      <p className="text-lg text-muted">Learn English with family stories, games and talking.</p>
      <LinkButton href="/login" size="lg">Log in</LinkButton>
    </main>
  );
}
