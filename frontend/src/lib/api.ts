// Thin fetch wrapper. All calls go to the same origin (/api/v1, proxied to FastAPI),
// so the HttpOnly session cookie is sent automatically.

export const API = "/api/v1";

export class ApiError extends Error {
  constructor(
    public status: number,
    public code: string,
    message: string,
    public details?: unknown,
  ) {
    super(message);
  }
}

export async function api<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers);
  const isForm = typeof FormData !== "undefined" && init.body instanceof FormData;
  if (init.body && !isForm && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }
  let res: Response;
  try {
    res = await fetch(`${API}${path}`, { ...init, headers, credentials: "same-origin" });
  } catch {
    throw new ApiError(0, "network_error", "Cannot reach the server. Check your connection.");
  }
  if (res.status === 204) return undefined as T;
  const body = await res.json().catch(() => null);
  if (!res.ok) {
    const err = body?.error;
    throw new ApiError(
      res.status,
      err?.code ?? "error",
      err?.message ?? "Something went wrong.",
      err?.details,
    );
  }
  return body as T;
}

export const post = <T>(path: string, data?: unknown) =>
  api<T>(path, { method: "POST", body: data === undefined ? undefined : JSON.stringify(data) });

export const mediaUrl = (id: string) => `${API}/media/${id}`;

export const send = <T>(method: "POST" | "PUT" | "PATCH" | "DELETE", path: string, data?: unknown) =>
  api<T>(path, { method, body: data === undefined ? undefined : JSON.stringify(data) });

/** Human-readable message including server validation details. */
export function errorText(e: unknown): string {
  if (!(e instanceof ApiError)) return "Неизвестная ошибка.";
  const d = e.details;
  if (Array.isArray(d) && d.length) {
    const lines = d.map((x) =>
      typeof x === "string" ? x : `${(x.loc ?? []).join(".")}: ${x.msg ?? ""}`,
    );
    return `${e.message}\n• ${lines.join("\n• ")}`;
  }
  return e.message;
}
