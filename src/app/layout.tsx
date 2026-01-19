import type { Metadata } from "next";
import "@/styles/globals.css";
import { validateEnv } from "@/lib/env";

export const metadata: Metadata = {
  title: "TikTok 选品决策系统",
  description: "用四维画像筛选 TikTok 选品池，快速得到推荐层级。"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  validateEnv();
  return (
    <html lang="zh-Hans">
      <body className="min-h-screen bg-canvas text-ink">{children}</body>
    </html>
  );
}
