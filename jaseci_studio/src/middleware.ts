import { NextRequest, NextResponse } from "next/server";

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  console.log({ pathname });

  const token = request.cookies.get("token")?.value;
  const serverUrl = request.cookies.get("serverUrl")?.value;

  if (!token || !serverUrl) {
    return NextResponse.redirect(new URL("/", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/graph-viewer", "/dashboard"],
};
