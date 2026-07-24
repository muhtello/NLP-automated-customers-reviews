import { useState } from "react";

import { apiErrorMessage } from "@/lib/apiError";
import type { ChatMessage } from "@/components/ChatMessageBubble/ChatMessageBubble";
import type { ChatMode } from "@/components/ChatModeToggle/ChatModeToggle";

type ApiRole = "user" | "assistant";

// Must match KEEP_RECENT_MESSAGES in api/src/chatbot_engine.py: when the backend condenses
// history, it keeps this many trailing messages raw (not folded into the summary), so the
// client must keep resending exactly that many even after a summary is cached.
const KEEP_RECENT_MESSAGES = 4;

export const OPENING: ChatMessage[] = [
  {
    from: "ai",
    text: "Ask me about a category, a product, or a sentiment trend and I'll point you to the right dashboard view.",
  },
];

export function useChatSession(categorySlug: string | null, mode: ChatMode) {
  const [messages, setMessages] = useState<ChatMessage[]>(OPENING);
  const [draft, setDraft] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");
  // Set once the backend has condensed older turns; sent back so it can skip re-summarizing
  // messages it has already seen (see ChatResponse.summary in api/src/chatbot_engine.py).
  const [summary, setSummary] = useState<string | null>(null);
  const [summarizedCount, setSummarizedCount] = useState(0);

  async function send() {
    const text = draft.trim();
    if (text === "" || sending) return;

    const visibleMessages = messages.filter((message) => message !== OPENING[0]);
    const unsummarized = summary === null ? visibleMessages : visibleMessages.slice(summarizedCount);
    const history = unsummarized.map((message) => ({
      role: (message.from === "ai" ? "assistant" : "user") as ApiRole,
      content: message.text,
    }));

    setMessages((prev) => [...prev, { from: "user", text }]);
    setDraft("");
    setSending(true);
    setError("");

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text, category_slug: categorySlug, history, mode, summary }),
      });
      if (!response.ok) throw new Error(`Request failed: ${response.status}`);
      const data = await response.json();
      setMessages((prev) => [
        ...prev,
        {
          from: "ai",
          text: data.reply,
          productComparison: data.product_comparison ?? undefined,
          productRanking: data.product_ranking ?? undefined,
        },
      ]);
      if (data.summary && data.summary !== summary) {
        setSummary(data.summary);
        setSummarizedCount(Math.max(0, visibleMessages.length - KEEP_RECENT_MESSAGES));
      }
    } catch {
      setError(apiErrorMessage("Could not reach the assistant"));
    } finally {
      setSending(false);
    }
  }

  return { messages, draft, setDraft, sending, error, send };
}
