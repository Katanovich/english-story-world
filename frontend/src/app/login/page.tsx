"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { Button, Card, Notice } from "@/components/ui";
import { ApiError } from "@/lib/api";
import { homeFor, useAuth } from "@/lib/auth";

export default function LoginPage() {
  const { user, login } = useAuth();
  const router = useRouter();
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (user) router.replace(homeFor(user.role));
  }, [user, router]);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    if (!name.trim() || !password) {
      setError("Please enter your name and password.");
      return;
    }
    setBusy(true);
    try {
      const u = await login(name.trim(), password);
      router.replace(homeFor(u.role));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not log in.");
      setBusy(false);
    }
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-md flex-col justify-center px-4 py-10">
      <div className="mb-6 text-center">
        <span aria-hidden className="text-6xl">👋</span>
        <h1 className="mt-2 text-3xl font-black">Welcome back!</h1>
      </div>
      <Card>
        <form onSubmit={submit} className="space-y-5" noValidate>
          <div className="space-y-2">
            <label htmlFor="login" className="block font-bold">Username or email</label>
            <input
              id="login"
              autoComplete="username"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="min-h-12 w-full rounded-2xl border-2 border-line px-4 text-lg"
            />
          </div>
          <div className="space-y-2">
            <label htmlFor="password" className="block font-bold">Password</label>
            <input
              id="password"
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="min-h-12 w-full rounded-2xl border-2 border-line px-4 text-lg"
            />
          </div>
          {error && <Notice tone="err">{error}</Notice>}
          <Button type="submit" size="lg" className="w-full" disabled={busy}>
            {busy ? "Logging in…" : "Log in"}
          </Button>
        </form>
      </Card>
      <p className="mt-4 text-center">
        <Link href="/forgot-password" className="font-bold text-sky underline">Forgot your password?</Link>
      </p>
    </main>
  );
}
