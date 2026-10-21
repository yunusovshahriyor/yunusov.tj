// next/image с { unoptimized: true } не добавляет basePath к src сам,
// поэтому для статичных путей из /public добавляем его вручную.
const basePath = process.env.GITHUB_PAGES_EXPORT === "true" ? "/yunusov.tj" : "";

export function assetPath(path: string) {
  return `${basePath}${path}`;
}
