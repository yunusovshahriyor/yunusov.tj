// Ёфтани калимаи рамзӣ дар матни шарҳ.

export type Keyword = {
  id: string;
  words: string[];
  url: string;
  message: string;
  button: string;
};

type RawKeyword = {
  id: unknown;
  words: unknown;
  url: unknown;
  message?: unknown;
  button?: unknown;
};

// Payload-и deep-link (t.me/bot?start=...) танҳо A-Z, a-z, 0-9, _ ва - -ро қабул мекунад.
const ID_RE = /^[A-Za-z0-9_-]{1,64}$/;

export function parseKeywords(data: unknown): Keyword[] {
  if (!Array.isArray(data) || data.length === 0) {
    throw new Error("keywords бояд рӯйхати ғайриихолӣ бошад");
  }
  const seen = new Set<string>();
  return data.map((item: RawKeyword) => {
    const id = String(item.id).trim();
    if (!ID_RE.test(id)) {
      throw new Error(`id «${id}» нодуруст аст: танҳо ҳарфҳои лотинӣ, рақам, _ ва -`);
    }
    if (seen.has(id)) throw new Error(`id «${id}» такрор шудааст`);
    seen.add(id);

    const words = Array.isArray(item.words)
      ? item.words.map((w) => String(w).trim()).filter(Boolean)
      : [];
    if (words.length === 0) throw new Error(`барои «${id}» калимаи рамзӣ нест`);

    return {
      id,
      words,
      url: String(item.url).trim(),
      message: typeof item.message === "string" ? item.message : "Ана маводи ваъдашуда 👇\n{url}",
      button: typeof item.button === "string" ? item.button : "📥 Кушодан",
    };
  });
}

export function normalize(text: string): string {
  return text.toLowerCase().replaceAll("ё", "е").split(/\s+/).filter(Boolean).join(" ");
}

function escapeRegExp(text: string): string {
  return text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

// Калима бояд алоҳида бошад: «гайд» дар «гайдҳо» ҳисоб намешавад,
// вале «Гайд!», «гайд 🔥» ва «мехоҳам гайд» ҳисоб мешаванд.
function pattern(word: string): RegExp {
  return new RegExp(`(?<![\\p{L}\\p{N}_])${escapeRegExp(normalize(word))}(?![\\p{L}\\p{N}_])`, "u");
}

export class KeywordMatcher {
  private readonly items: Array<[Keyword, RegExp[]]>;

  constructor(keywords: Keyword[]) {
    this.items = keywords.map((k) => [k, k.words.map(pattern)]);
  }

  match(text: string | undefined | null): Keyword | null {
    if (!text) return null;
    const normalized = normalize(text);
    for (const [keyword, patterns] of this.items) {
      if (patterns.some((p) => p.test(normalized))) return keyword;
    }
    return null;
  }
}
