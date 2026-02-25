import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // 启用静态导出优化（Next.js 16推荐）
  reactStrictMode: true,

  // 公共环境变量 - 必须以NEXT_PUBLIC_前缀，在构建时注入
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },

  // 图片优化配置 - 允许外部来源
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**',
      },
      {
        protocol: 'http',
        hostname: 'localhost',
        port: '8000',
      },
    ],
  },

  // API代理rewrite - 在构建时处理，Vercel会保留此配置
  async rewrites() {
    return {
      beforeFiles: [
        {
          source: '/api/:path*',
          destination: `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/:path*`,
        },
      ],
    };
  },
};

export default nextConfig;
