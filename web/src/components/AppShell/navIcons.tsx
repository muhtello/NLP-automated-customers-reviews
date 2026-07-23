type IconProps = { className?: string };

function base(paths: React.ReactNode, className = "h-5 w-5") {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" className={className}>
      {paths}
    </svg>
  );
}

export function DashboardIcon({ className }: IconProps) {
  return base(
    <>
      <rect x="4" y="4" width="7" height="7" rx="1.2" />
      <rect x="13" y="4" width="7" height="4" rx="1.2" />
      <rect x="13" y="11" width="7" height="9" rx="1.2" />
      <rect x="4" y="14" width="7" height="6" rx="1.2" />
    </>,
    className,
  );
}

export function SentimentIcon({ className }: IconProps) {
  return base(
    <>
      <path d="M4 18V9M9 18V4M14 18v-6M19 18v-3" />
    </>,
    className,
  );
}

export function ClusteringIcon({ className }: IconProps) {
  return base(
    <>
      <circle cx="7" cy="7" r="3" />
      <circle cx="17" cy="8" r="2.2" />
      <circle cx="10" cy="17" r="3.5" />
      <path d="M9 9l2 5.5M9.5 6.8l5.7 1.6" />
    </>,
    className,
  );
}

export function SearchIcon({ className }: IconProps) {
  return base(
    <>
      <circle cx="10.5" cy="10.5" r="6.5" />
      <path d="M20 20l-4.8-4.8" />
    </>,
    className,
  );
}

export function ChatIcon({ className }: IconProps) {
  return base(
    <>
      <path d="M12 3.5l1.4 3 3.3.5-2.4 2.3.6 3.3-3-1.6-3 1.6.6-3.3-2.4-2.3 3.3-.5z" />
    </>,
    className,
  );
}
