const ICONS: Record<string, React.ReactNode> = {
  "e-readers-e-books": (
    <>
      <path d="M4 4.5h9a3 3 0 0 1 3 3v13a2.5 2.5 0 0 0-2.5-2.5H4z" />
      <path d="M4 4.5v13.5" />
      <path d="M8 9h4M8 12h4" />
    </>
  ),
  "entertainment-tablets-media-devices": (
    <>
      <rect x="5" y="3" width="14" height="18" rx="1.5" />
      <path d="M9 18.5h6" />
      <path d="M10.5 9.5l4 2.5-4 2.5z" />
    </>
  ),
  "non-electronics-office-pets": (
    <>
      <path d="M4 8l3-3h6l3 3v11a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1z" />
      <path d="M4 8h16" />
      <path d="M10 5v3M14 5v3" />
    </>
  ),
  "smart-home-audio-systems": (
    <>
      <rect x="7" y="3" width="10" height="18" rx="3" />
      <circle cx="12" cy="9" r="2.2" />
      <circle cx="12" cy="16" r="1" />
    </>
  ),
  "tech-accessories-everyday-electronics": (
    <>
      <path d="M8 4v4M16 4v4" />
      <rect x="6" y="8" width="12" height="9" rx="2" />
      <path d="M10 20h4" />
    </>
  ),
};

export default function CategoryIcon({ slug, className = "h-6 w-6" }: { slug: string; className?: string }) {
  const paths = ICONS[slug];
  if (!paths) return null;
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" className={className}>
      {paths}
    </svg>
  );
}
