function renderInlineNodes(text: string) {
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  return parts.map((part, index) =>
    part.startsWith("**") && part.endsWith("**") ? (
      <strong key={index} className="font-semibold text-ink">
        {part.slice(2, -2)}
      </strong>
    ) : (
      <span key={index}>{part}</span>
    ),
  );
}

function renderParagraph(text: string, key: number) {
  return (
    <p key={key} className="text-[15px] leading-relaxed text-ink-soft">
      {renderInlineNodes(text)}
    </p>
  );
}

export default function ArticleBody({ text }: { text: string }) {
  const lines = text.split("\n");
  const blocks: React.ReactNode[] = [];
  let listBuffer: string[] = [];

  function flushList(key: number) {
    if (listBuffer.length === 0) return;
    blocks.push(
      <ul key={`list-${key}`} className="flex list-none flex-col gap-1.5 border-l-2 border-primary/20 pl-4">
        {listBuffer.map((item, index) => (
          <li key={index} className="text-[15px] leading-relaxed text-ink-soft">
            {renderInlineNodes(item)}
          </li>
        ))}
      </ul>,
    );
    listBuffer = [];
  }

  lines.forEach((rawLine, index) => {
    const line = rawLine.trim();
    if (line.startsWith("#### ") || line.startsWith("### ")) {
      flushList(index);
      const level = line.startsWith("#### ") ? 4 : 3;
      const content = line.replace(/^#{3,4}\s+/, "");
      blocks.push(
        level === 3 ? (
          <h3 key={index} className="mt-2 text-lg font-semibold tracking-tight text-primary">
            {content}
          </h3>
        ) : (
          <h4 key={index} className="mt-1 font-mono text-xs font-semibold uppercase tracking-widest text-secondary">
            {content}
          </h4>
        ),
      );
    } else if (line.startsWith("- ")) {
      listBuffer.push(line.slice(2));
    } else if (line === "") {
      flushList(index);
    } else {
      flushList(index);
      blocks.push(renderParagraph(line, index));
    }
  });
  flushList(lines.length);

  return <div className="flex flex-col gap-3">{blocks}</div>;
}
