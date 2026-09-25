import { SVGProps } from "react";

export function TelegramIcon(props: SVGProps<SVGSVGElement>) {
  return (
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" {...props}>
      <path
        d="M21.05 3.87 2.98 10.9c-1.23.49-1.22 1.17-.22 1.47l4.63 1.45 1.78 5.42c.22.6.37.84.75.84.35 0 .5-.16.7-.36l1.7-1.65 4.68 3.46c.86.48 1.47.23 1.69-.8l3.06-14.42c.32-1.26-.48-1.83-1.7-1.44Zm-11.9 10.9-1.13-3.64 8.74-5.5c.4-.24.77-.11.47.15l-8.08 8.99Z"
        fill="currentColor"
      />
    </svg>
  );
}

export function InstagramIcon(props: SVGProps<SVGSVGElement>) {
  return (
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" {...props}>
      <rect x="3" y="3" width="18" height="18" rx="5" stroke="currentColor" strokeWidth="1.6" />
      <circle cx="12" cy="12" r="4.2" stroke="currentColor" strokeWidth="1.6" />
      <circle cx="17.3" cy="6.7" r="1.1" fill="currentColor" />
    </svg>
  );
}

export function YoutubeIcon(props: SVGProps<SVGSVGElement>) {
  return (
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" {...props}>
      <rect x="2.5" y="5.5" width="19" height="13" rx="3.5" stroke="currentColor" strokeWidth="1.6" />
      <path d="M10.3 9.2v5.6l4.9-2.8-4.9-2.8Z" fill="currentColor" />
    </svg>
  );
}

export function EmailIcon(props: SVGProps<SVGSVGElement>) {
  return (
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" {...props}>
      <rect x="2.5" y="4.5" width="19" height="15" rx="2.5" stroke="currentColor" strokeWidth="1.6" />
      <path d="m3.5 6 8.5 6.5L20.5 6" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}
