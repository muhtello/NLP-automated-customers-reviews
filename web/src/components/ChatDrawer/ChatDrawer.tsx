"use client";

import { useState } from "react";
import { usePathname } from "next/navigation";

import { ChatIcon } from "@/components/AppShell/navIcons";
import { useCategories } from "@/lib/useCategories";

type Message = { from: "user" | "ai"; text: string };
type ApiRole = "user" | "assistant";

const OPENING: Message[] = [
  {
    from: "ai",
    text: "Ask me about a category, a product, or a sentiment trend and I'll point you to the right dashboard view.",
  },
];

function slugFromPathname(pathname: string): string | null {
  const match = pathname.match(/^\/dashboard\/([^/]+)$/);
  if (!match) return null;
  const [, slug] = match;
  if (["sentiment", "clustering", "products"].includes(slug)) return null;
  return slug;
}

export default function ChatDrawer({ open, onClose }: { open: boolean; onClose: () => void }) {
  const [messages, setMessages] = useState<Message[]>(OPENING);
  const [draft, setDraft] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");

  const pathname = usePathname();
  const { categories } = useCategories();
  const categorySlug = slugFromPathname(pathname) ?? categories[0]?.slug ?? null;

  async function send() {
    const text = draft.trim();
    if (text === "" || sending) return;

    const history = messages
      .filter((message) => message !== OPENING[0])
      .map((message) => ({ role: (message.from === "ai" ? "assistant" : "user") as ApiRole, content: message.text }));

    setMessages((prev) => [...prev, { from: "user", text }]);
    setDraft("");
    setSending(true);
    setError("");

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text, category_slug: categorySlug, history }),
      });
      if (!response.ok) throw new Error(`Request failed: ${response.status}`);
      const data = await response.json();
      setMessages((prev) => [...prev, { from: "ai", text: data.reply }]);
    } catch {
      setError("Could not reach the assistant. Is the API running on port 8000?");
    } finally {
      setSending(false);
    }
  }

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

        <div className="flex flex-1 flex-col gap-3 overflow-y-auto pr-1">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex gap-2 ${message.from === "user" ? "flex-row-reverse text-right" : ""}`}
            >
              <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-primary-soft text-primary">
                {message.from === "ai" ? <ChatIcon className="h-3.5 w-3.5" /> : <span className="text-xs font-semibold">You</span>}
              </span>
              <p
                className={`max-w-[80%] rounded-lg p-3 text-sm ${
                  message.from === "ai" ? "glass-panel rounded-tl-none text-ink" : "rounded-tr-none bg-primary text-white"
                }`}
              >
                {message.text}
              </p>
            </div>
          ))}
          {sending && <p className="font-mono text-[10px] uppercase tracking-widest text-ink-faint">Thinking...</p>}
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
