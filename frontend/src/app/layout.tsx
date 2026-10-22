import type { Metadata, Viewport } from "next";
import { Nunito } from "next/font/google";
import { AuthProvider } from "@/lib/auth";
import "./globals.css";

const nunito = Nunito({ subsets: ["latin", "cyrillic"], variable: "--font-nunito" });

export const metadata: Metadata = {
  title: { default: "English Story World", template: "%s · English Story World" },
  description: "Learn English through family stories, games and talking.",
  robots: { index: false, follow: false },
};

export const viewport: Viewport = { width: "device-width", initialScale: 1, themeColor: "#ff7a45" };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={nunito.variable}>
      <body className="min-h-screen antialiased">
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
