import { Reveal } from "./Reveal";

export function SectionHeading({
  eyebrow,
  title,
  description,
  align = "left",
}: {
  eyebrow?: string;
  title: string;
  description?: string;
  align?: "left" | "center";
}) {
  const alignClass = align === "center" ? "text-center items-center" : "text-left items-start";

  return (
    <Reveal>
      <div className={`flex flex-col gap-4 ${alignClass}`}>
        {eyebrow && (
          <span className="text-sm font-medium tracking-wide text-accent uppercase">
            {eyebrow}
          </span>
        )}
        <h2 className="text-3xl sm:text-4xl font-semibold tracking-tight text-foreground text-balance">
          {title}
        </h2>
        {description && (
          <p
            className={`text-base sm:text-lg text-muted leading-relaxed ${
              align === "center" ? "max-w-2xl" : "max-w-xl"
            }`}
          >
            {description}
          </p>
        )}
      </div>
    </Reveal>
  );
}
