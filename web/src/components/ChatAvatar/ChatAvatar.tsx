import { ChatIcon, PersonIcon } from "@/components/AppShell/navIcons";

export default function ChatAvatar({ from }: { from: "user" | "ai" }) {
  if (from === "user") {
    return (
      <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-ink text-white ring-1 ring-ink/10">
        <PersonIcon className="h-4 w-4" />
      </span>
    );
  }

  return (
    <span className="relative flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary-soft text-primary ring-1 ring-primary/20">
      <ChatIcon className="h-4 w-4" />
      <span className="absolute -bottom-0.5 -right-0.5 h-2 w-2 animate-pulse-dot rounded-full bg-primary ring-2 ring-surface" />
    </span>
  );
}
