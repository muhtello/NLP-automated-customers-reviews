export type ChatMode = "recommender" | "anti_recommender";

const MODES: { value: ChatMode; label: string }[] = [
  { value: "recommender", label: "Recommender" },
  { value: "anti_recommender", label: "Anti-recommender" },
];

export default function ChatModeToggle({ mode, onChange }: { mode: ChatMode; onChange: (mode: ChatMode) => void }) {
  return (
    <div className="mb-3 flex rounded-full border border-line bg-surface p-1 text-xs">
      {MODES.map((option) => (
        <button
          key={option.value}
          onClick={() => onChange(option.value)}
          className={`flex-1 rounded-full px-2 py-1.5 font-medium transition-colors ${
            mode === option.value ? "bg-primary text-white" : "text-ink-soft hover:text-primary"
          }`}
        >
          {option.label}
        </button>
      ))}
    </div>
  );
}
