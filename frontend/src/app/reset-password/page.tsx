"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Suspense, useState } from "react";
import { Button, Card, LoadingState, Notice } from "@/components/ui";
import { ApiError, post } from "@/lib/api";

function ResetForm() {
  const params = useSearchParams();
  const [token, setToken] = useState(params.get("token") ?? "");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [done, setDone] = useState(false);
  const [busy, setBusy] = useState(false);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    if (!token.trim()) return setError("Please enter your code.");
    if (password.length < 8) return setError("The password needs at least 8 characters.");
    if (password !== confirm) return setError("The two passwords are not the same.");
    setBusy(true);
    try {
      await post("/auth/password-reset/confirm", { token: token.trim(), new_password: password });
      setDone(true);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Something went wrong.");
    } finally {
      setBusy(false);
    }
  }

  if (done) {
    return (
      <Card className="space-y-4 text-center">
        <Notice tone="ok">Your new password is ready!</Notice>
        <Link href="/login" className="font-bold text-sky underline">Go to login</Link>
      </Card>
    );
  }
  return (
    <Card>
      <form onSubmit={submit} className="space-y-4" noValidate>
        <label htmlFor="token" className="block font-bold">Code</label>
        <input id="token" value={token} onChange={(e) => setToken(e.target.value)} autoComplete="off" className="min-h-12 w-full rounded-2xl border-2 border-line px-4" />
        <label htmlFor="pw" className="block font-bold">New password</label>
        <input id="pw" type="password" autoComplete="new-password" value={password} onChange={(e) => setPassword(e.target.value)} className="min-h-12 w-full rounded-2xl border-2 border-line px-4" />
        <p className="text-sm text-muted">At least 8 characters, with letters and numbers.</p>
        <label htmlFor="pw2" className="block font-bold">New password again</label>
        <input id="pw2" type="password" autoComplete="new-password" value={confirm} onChange={(e) => setConfirm(e.target.value)} className="min-h-12 w-full rounded-2xl border-2 border-line px-4" />
        {error && <Notice tone="err">{error}</Notice>}
        <Button type="submit" size="lg" className="w-full" disabled={busy}>
          {busy ? "Saving…" : "Save new password"}
        </Button>
      </form>
    </Card>
  );
}

export default function ResetPasswordPage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-md flex-col justify-center px-4 py-10">
      <h1 className="mb-6 text-center text-3xl font-black">Set a new password</h1>
      <Suspense fallback={<LoadingState />}>
        <ResetForm />
      </Suspense>
    </main>
  );
}
