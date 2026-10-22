import { NextResponse, type NextRequest } from "next/server";

// UX only: send visitors without a session cookie to the login page early.
// Real authentication and authorization are enforced by the API on every request.
export function middleware(request: NextRequest) {
  if (!request.cookies.has("esw_session")) {
    return NextResponse.redirect(new URL("/login", request.url));
  }
  return NextResponse.next();
}

export const config = { matcher: ["/learn/:path*", "/admin/:path*"] };
