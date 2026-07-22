"use client";

import { useState } from "react";

import CategoryIcon from "@/components/CategoryIcon/CategoryIcon";

export default function ProductThumb({
  imageUrl,
  categorySlug,
  alt,
  size = "md",
}: {
  imageUrl: string | null | undefined;
  categorySlug: string;
  alt: string;
  size?: "sm" | "md";
}) {
  const [failed, setFailed] = useState(false);
  const dimension = size === "sm" ? "h-10 w-10" : "h-14 w-14";

  if (!imageUrl || failed) {
    return (
      <div className={`flex ${dimension} shrink-0 items-center justify-center border border-line bg-paper`}>
        <CategoryIcon slug={categorySlug} className="h-1/2 w-1/2 text-ledger-soft" />
      </div>
    );
  }

  return (
    // eslint-disable-next-line @next/next/no-img-element
    <img
      src={imageUrl}
      alt={alt}
      className={`${dimension} shrink-0 border border-line bg-paper object-contain p-1`}
      onError={() => setFailed(true)}
    />
  );
}
