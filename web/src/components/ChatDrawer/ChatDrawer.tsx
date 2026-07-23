"use client";

import { useState } from "react";

import { ChatIcon } from "@/components/AppShell/navIcons";

type Message = { from: "user" | "ai"; text: string };

const OPENING: Message[] = [
  {
    from: "ai",
    text: "Ask me about a category, a product, or a sentiment trend and I'll point you to the right dashboard view.",
  },
];

const CANNED_REPLY =
  "This is a UI preview of the assistant — wire it up to a live model when the summarization endpoint is ready. For now, browse Clustering and Sentiment for real data.";

export default function ChatDrawer({ open, onClose }: { open: boolean; onClose: () => void }) {
  const [messages, setMessages] = useState<Message[]>(OPENING);
  const [draft, setDraft] = useState("");

  function send() {
    const text = draft.trim();
    if (text === "") return;
    setMessages((prev) => [...prev, { from: "user", text }, { from: "ai", text: CANNED_REPLY }]);
    setDraft("");
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
            <p className="text-xs text-ink-soft">UI preview &middot; not wired to a model yet</p>
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
        </div>

        <div className="mt-4 flex items-center gap-2 border-t border-line pt-4">
          <input
            value={draft}
            onChange={(event) => setDraft(event.target.value)}
            onKeyDown={(event) => event.key === "Enter" && send()}
            placeholder="Ask about the reviews..."
            className="flex-1 rounded-full border border-line bg-surface px-4 py-2 text-sm text-ink outline-none focus:border-primary"
          />
          <button
            onClick={send}
            className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-primary text-white transition-colors hover:bg-primary-strong"
            aria-label="Send message"
          >
            &rarr;
          </button>
        </div>
      </aside>
    </>
  );
}
