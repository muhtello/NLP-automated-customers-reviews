"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

import { ChatIcon, ClusteringIcon, DashboardIcon, SearchIcon, SentimentIcon } from "@/components/AppShell/navIcons";
import ChatDrawer from "@/components/ChatDrawer/ChatDrawer";

const NAV_ITEMS = [
  { href: "/dashboard", label: "Dashboard", icon: DashboardIcon },
  { href: "/dashboard/sentiment", label: "Sentiment", icon: SentimentIcon },
  { href: "/dashboard/clustering", label: "Clustering", icon: ClusteringIcon },
  { href: "/dashboard/products", label: "Products", icon: SearchIcon },
];

const PAGE_TITLE: Record<string, string> = {
  "/dashboard": "Category overview",
  "/dashboard/sentiment": "Sentiment analysis",
  "/dashboard/clustering": "Category clustering",
  "/dashboard/products": "Product explorer",
};

export default function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const [chatOpen, setChatOpen] = useState(false);
  const title = PAGE_TITLE[pathname] ?? "Review detail";

  return (
    <div className="min-h-screen bg-bg">
      <aside className="fixed left-0 top-0 hidden h-screen w-60 flex-col border-r border-line bg-surface md:flex">
        <div className="flex items-center gap-2.5 px-5 py-5">
          <span className="flex h-8 w-8 items-center justify-center rounded bg-primary text-sm font-semibold text-white">S</span>
          <div className="flex flex-col leading-tight">
            <span className="text-sm font-semibold text-ink">Signal NLP Review</span>
            <span className="font-mono text-[10px] uppercase tracking-widest text-ink-faint">NLP review intelligence</span>
          </div>
        </div>

        <nav className="flex flex-col gap-1 px-3 py-2">
          {NAV_ITEMS.map(({ href, label, icon: Icon }) => {
            const active = pathname === href;
            return (
              <Link
                key={href}
                href={href}
                className={`flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors ${
                  active ? "bg-primary-soft text-primary" : "text-ink-soft hover:bg-surface-sunken hover:text-ink"
                }`}
              >
                <Icon className="h-4.5 w-4.5" />
                {label}
              </Link>
            );
          })}
        </nav>

        <div className="mt-auto p-3">
          <button
            onClick={() => setChatOpen(true)}
            className="glass-panel flex w-full items-center justify-center gap-2 rounded-xl py-3 text-sm font-semibold text-primary transition-shadow hover:shadow-sm"
          >
            <ChatIcon className="h-4 w-4" />
            Chat with AI
          </button>
        </div>
      </aside>

      <div className="flex flex-col md:ml-60">
        <header className="sticky top-0 z-30 flex items-center justify-between border-b border-line bg-surface/90 px-6 py-4 backdrop-blur-sm">
          <div className="flex items-center gap-3">
            <span className="flex h-8 w-8 items-center justify-center rounded bg-primary text-sm font-semibold text-white md:hidden">
              S
            </span>
            <h1 className="text-base font-semibold tracking-tight text-ink">{title}</h1>
          </div>
          <nav className="flex gap-4 md:hidden">
            {NAV_ITEMS.map(({ href, label }) => (
              <Link key={href} href={href} className="text-xs font-medium text-secondary hover:text-primary">
                {label}
              </Link>
            ))}
          </nav>
        </header>

        <main className="mx-auto w-full max-w-[1440px] px-6 py-8">{children}</main>
      </div>

      <ChatDrawer open={chatOpen} onClose={() => setChatOpen(false)} />
    </div>
  );
}
