export function PhotoPlaceholder({ className = "" }: { className?: string }) {
  return (
    <div
      className={`flex flex-col items-center justify-center gap-3 bg-surface ${className}`}
      role="img"
      aria-label="Фотография Shahriyor Yunusov — будет добавлена"
    >
      <svg viewBox="0 0 24 24" fill="none" className="h-14 w-14 text-muted/60" aria-hidden="true">
        <circle cx="12" cy="8.5" r="3.5" stroke="currentColor" strokeWidth="1.5" />
        <path
          d="M4.5 19.5c1.4-3.2 4.3-5 7.5-5s6.1 1.8 7.5 5"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
        />
      </svg>
      <span className="text-xs text-muted">[Добавить фото]</span>
    </div>
  );
}
