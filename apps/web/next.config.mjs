import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  output: "standalone",
  // Tell Next.js this is part of a monorepo so the standalone build traces
  // and copies files from the workspace root rather than just apps/web.
  outputFileTracingRoot: path.join(__dirname, "../.."),
  // typedRoutes moved out of `experimental` in Next.js 15.5.
  typedRoutes: true,
  // For dockerized SSR fetches: the internal URL the server uses to reach the API,
  // separate from NEXT_PUBLIC_API_URL which the browser uses.
  env: {
    INTERNAL_API_URL:
      process.env.INTERNAL_API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000",
  },
  async redirects() {
    return [{ source: "/api-docs", destination: "/docs", permanent: false }];
  },
};

export default nextConfig;
