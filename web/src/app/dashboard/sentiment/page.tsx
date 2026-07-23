import SentimentForm from "@/components/SentimentForm/SentimentForm";
import SentimentMetrics from "@/components/SentimentMetrics/SentimentMetrics";

export default function Sentiment() {
  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
      <SentimentForm />
      <SentimentMetrics />
    </div>
  );
}
