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
      className="rounded border border-gray-300 p-2 text-sm"
    >
      {models.map((model) => (
        <option key={model.key} value={model.key}>
          {model.display_name}
        </option>
      ))}
    </select>
  );
}
