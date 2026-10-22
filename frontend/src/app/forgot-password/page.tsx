"use client";

import Link from "next/link";
import { useState } from "react";
import { Button, Card, Notice } from "@/components/ui";
import { ApiError, post } from "@/lib/api";

export default function ForgotPasswordPage() {
  const [login, setLogin] = useState("");
  const [done, setDone] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!login.trim()) return setError("Please enter your username or email.");
    setBusy(true);
    setError(null);
    try {
      await post("/auth/password-reset/request", { login: login.trim() });
      setDone(true);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Something went wrong.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-md flex-col justify-center px-4 py-10">
      <h1 className="mb-6 text-center text-3xl font-black">Forgot your password?</h1>
      <Card className="space-y-5">
        {done ? (
          <Notice tone="ok">
            Thank you! If this account exists, a reset code is on its way. You can also ask your
            teacher for a new code.
          </Notice>
        ) : (
          <form onSubmit={submit} className="space-y-5" noValidate>
            <p className="text-muted">Children: please ask your teacher or parent for help.</p>
            <label htmlFor="login" className="block font-bold">Username or email</label>
            <input
              id="login"
              value={login}
              onChange={(e) => setLogin(e.target.value)}
              className="min-h-12 w-full rounded-2xl border-2 border-line px-4 text-lg"
            />
            {error && <Notice tone="err">{error}</Notice>}
            <Button type="submit" size="lg" className="w-full" disabled={busy}>
              {busy ? "Sending…" : "Send reset code"}
            </Button>
          </form>
        )}
        <p className="text-center">
          <Link href="/reset-password" className="font-bold text-sky underline">I have a code</Link>
          {" · "}
          <Link href="/login" className="font-bold text-sky underline">Back to login</Link>
        </p>
      </Card>
    </main>
  );
}
