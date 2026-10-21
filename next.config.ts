import type { NextConfig } from "next";

// Название репозитория — GitHub Pages отдаёт проект по адресу
// https://<username>.github.io/<repo-name>/, поэтому в режиме
// статического экспорта сайту нужен соответствующий basePath.
const repoName = "yunusov.tj";
const isStaticExport = process.env.GITHUB_PAGES_EXPORT === "true";

const nextConfig: NextConfig = {
  // Изображения проектов уже оптимизированы (WebP) и отдаются статикой,
  // серверная оптимизация next/image не нужна — а в статическом экспорте
  // для GitHub Pages она и вовсе недоступна.
  images: { unoptimized: true },
  ...(isStaticExport
    ? {
        output: "export",
        basePath: `/${repoName}`,
        assetPrefix: `/${repoName}/`,
        trailingSlash: true,
      }
    : {}),
};

export default nextConfig;
