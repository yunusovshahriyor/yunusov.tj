import type { NextConfig } from "next";

// Название репозитория — GitHub Pages отдаёт проект по адресу
// https://<username>.github.io/<repo-name>/, поэтому в режиме
// статического экспорта сайту нужен соответствующий basePath.
const repoName = "yunusov.tj";
const isStaticExport = process.env.GITHUB_PAGES_EXPORT === "true";

const nextConfig: NextConfig = {
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
