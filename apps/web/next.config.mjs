/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  output: "standalone",
  experimental: {
    typedRoutes: true,
  },
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
