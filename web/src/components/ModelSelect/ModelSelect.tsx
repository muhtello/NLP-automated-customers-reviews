import type { ModelInfo } from "@/lib/useModels";

type ModelSelectProps = {
  models: ModelInfo[];
  value: string;
  onChange: (modelKey: string) => void;
};

export default function ModelSelect({ models, value, onChange }: ModelSelectProps) {
  return (
    <select
      value={value}
      onChange={(event) => onChange(event.target.value)}
      className="rounded border border-line bg-surface px-3 py-2 text-sm text-ink outline-none transition-colors focus:border-2 focus:border-primary"
    >
      {models.map((model) => (
        <option key={model.key} value={model.key}>
          {model.display_name}
        </option>
      ))}
    </select>
  );
}
