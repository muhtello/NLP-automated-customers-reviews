import ChatAvatar from "@/components/ChatAvatar/ChatAvatar";
import ProductComparisonTable, { type ProductComparison } from "@/components/ProductComparisonTable/ProductComparisonTable";
import ProductRankingList, { type ProductRanking } from "@/components/ProductRankingList/ProductRankingList";

export type ChatMessage = {
  from: "user" | "ai";
  text: string;
  productComparison?: ProductComparison;
  productRanking?: ProductRanking;
};

export default function ChatMessageBubble({ message }: { message: ChatMessage }) {
  return (
    <div className={`flex flex-col gap-2 ${message.from === "user" ? "items-end" : "items-start"}`}>
      <div className={`flex items-end gap-2 ${message.from === "user" ? "flex-row-reverse text-right" : ""}`}>
        <ChatAvatar from={message.from} />
        <p
          className={`max-w-[80%] rounded-lg p-3 text-sm shadow-sm ${
            message.from === "ai" ? "glass-panel rounded-bl-none text-ink" : "rounded-br-none bg-primary text-white"
          }`}
        >
          {message.text}
        </p>
      </div>
      {message.productComparison && <ProductComparisonTable comparison={message.productComparison} />}
      {message.productRanking && <ProductRankingList ranking={message.productRanking} />}
    </div>
  );
}
