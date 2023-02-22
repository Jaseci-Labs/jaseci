/** @type {import('next').NextConfig} */
const nextConfig = {
  basePath: process.env.NEXT_PUBLIC_TAURI ? undefined : "/studio",
  reactStrictMode: true,
  swcMinify: true,
  images: {
    unoptimized: true,
  },
  // async redirects() {
  //   return [
  //     {
  //       source: "/",
  //       destination: "/studio",
  //       basePath: false,
  //       permanent: false,
  //     },
  //   ];
  // },
};

module.exports = nextConfig;
