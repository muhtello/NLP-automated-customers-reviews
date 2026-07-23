"use client";

import { useState } from "react";
import { usePathname } from "next/navigation";

import ChatAvatar from "@/components/ChatAvatar/ChatAvatar";
import ChatMessageBubble from "@/components/ChatMessageBubble/ChatMessageBubble";
import ChatModeToggle, { type ChatMode } from "@/components/ChatModeToggle/ChatModeToggle";
import { useCategories } from "@/lib/useCategories";

import { useChatSession } from "./useChatSession";

function slugFromPathname(pathname: string): string | null {
  const match = pathname.match(/^\/dashboard\/([^/]+)$/);
  if (!match) return null;
  const [, slug] = match;
  if (["sentiment", "clustering", "products"].includes(slug)) return null;
  return slug;
}

export default function ChatDrawer({ open, onClose }: { open: boolean; onClose: () => void }) {
  const [mode, setMode] = useState<ChatMode>("recommender");

  const pathname = usePathname();
  const { categories } = useCategories();
  const categorySlug = slugFromPathname(pathname) ?? categories[0]?.slug ?? null;

  const { messages, draft, setDraft, sending, error, send } = useChatSession(categorySlug, mode);

  return (
    <>
      {open && <div className="fixed inset-0 z-40 bg-ink/10" onClick={onClose} />}
      <aside
        className={`fixed right-0 top-0 z-50 flex h-screen w-96 max-w-[90vw] flex-col border-l border-glass-border bg-glass p-5 backdrop-blur-md transition-transform ${
          open ? "translate-x-0" : "translate-x-full"
        }`}
      >
        <div className="mb-5 flex items-start justify-between">
          <div>
            <h2 className="text-lg font-semibold tracking-tight text-primary">Research assistant</h2>
            <p className="text-xs text-ink-soft">
              {categorySlug ? `Context: ${categorySlug}` : "No category selected"}
            </p>
          </div>
          <button onClick={onClose} className="text-ink-soft transition-colors hover:text-primary" aria-label="Close chat">
            &times;
          </button>
        </div>

        <ChatModeToggle mode={mode} onChange={setMode} />

        <div className="flex flex-1 flex-col gap-3 overflow-y-auto pr-1">
          {messages.map((message, index) => (
            <ChatMessageBubble key={index} message={message} />
          ))}
          {sending && (
            <div className="flex items-end gap-2">
              <ChatAvatar from="ai" />
              <span className="glass-panel flex items-center gap-2 rounded-lg rounded-bl-none p-3 shadow-sm">
                <span className="text-xs text-ink-soft">Checking reviews...</span>
                <span className="h-1.5 w-1.5 animate-pulse-dot rounded-full bg-primary/60" style={{ animationDelay: "0ms" }} />
                <span className="h-1.5 w-1.5 animate-pulse-dot rounded-full bg-primary/60" style={{ animationDelay: "160ms" }} />
                <span className="h-1.5 w-1.5 animate-pulse-dot rounded-full bg-primary/60" style={{ animationDelay: "320ms" }} />
              </span>
            </div>
          )}
          {error && <p className="text-xs text-negative-strong">{error}</p>}
        </div>

        <div className="mt-4 flex items-center gap-2 border-t border-line pt-4">
          <input
            value={draft}
            onChange={(event) => setDraft(event.target.value)}
            onKeyDown={(event) => event.key === "Enter" && send()}
            placeholder="Ask about the reviews..."
            disabled={sending}
            className="flex-1 rounded-full border border-line bg-surface px-4 py-2 text-sm text-ink outline-none focus:border-primary disabled:opacity-60"
          />
          <button
            onClick={send}
            disabled={sending}
            className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-primary text-white transition-colors hover:bg-primary-strong disabled:opacity-60"
            aria-label="Send message"
          >
            &rarr;
          </button>
        </div>
      </aside>
    </>
  );
}
