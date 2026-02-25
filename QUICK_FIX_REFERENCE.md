# 快速参考卡片 - Vercel 404修复

## 已修复的问题

### ✅ 问题1: Rewrite循环冲突
- **原因:** vercel.json中的 `/api/(.*) → /api/$1` 自引用
- **修复:** 已移除该rewrite配置
- **保留:** next.config.ts中的API代理规则

### ✅ 问题2: 无效API Routes配置
- **原因:** `functions` 配置指向不存在的路径
- **修复:** 已删除functions字段（此项目无托管API）

### ✅ 问题3: 环境变量传递失败
- **原因:** vercel.json配置过时，未能正确传递变量
- **修复:** 改用Vercel仪表板管理，添加fallback值

---

## 立即执行的步骤

### 第一步: 验证本地构建 (5分钟)
```bash
cd e-commerce-frontend
npm run build
npm start
# 访问 http://localhost:3000
# 在浏览器Network标签验证API请求成功
```

### 第二步: 设置Vercel环境变量 (5分钟)
1. 访问 https://vercel.com/dashboard
2. 选择项目，进入 Settings → Environment Variables
3. 新增变量：
   ```
   Name: NEXT_PUBLIC_API_URL
   Values:
     - Production:  https://your-api.com
     - Preview:     https://staging-api.com
     - Development: http://localhost:8000
   ```
4. 保存并触发Redeploy

### 第三步: 部署 (2分钟)
```bash
git add .
git commit -m "fix: resolve Vercel 404 errors"
git push origin main
# 等待Vercel自动部署 (3-5分钟)
```

### 第四步: 验证部署 (3分钟)
- [ ] 访问预览URL
- [ ] 检查控制台无错误
- [ ] API请求成功转发

---

## 配置代码对照

### vercel.json (已简化)
```json
{
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "installCommand": "npm install",
  "devCommand": "npm run dev"
}
```

### next.config.ts (已优化)
```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: '**' },
      { protocol: 'http', hostname: 'localhost', port: '8000' },
    ],
  },
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
```

### .env.local (本地开发)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 常见问题排查

| 问题 | 解决方案 |
|-----|--------|
| 仍然出现404 | 检查Vercel部署日志，确认环境变量已注入 |
| 环境变量为undefined | Vercel仪表板已保存？Redeploy后无效？检查缓存 |
| 本地正常，远程出错 | API URL配置错误或后端未启动 |
| 浏览器CORS错误 | 检查后端CORS配置，不是Vercel问题 |

---

## 验证清单 (部署前)

- [ ] `vercel.json` 不含env、functions、rewrites
- [ ] `next.config.ts` 使用beforeFiles结构
- [ ] 本地构建成功: `npm run build`
- [ ] 本地运行正常: `npm start`
- [ ] `.env.local` 已创建
- [ ] Vercel仪表板环境变量已设置
- [ ] 三个环境都已配置 (Prod/Preview/Dev)
- [ ] 本地API请求成功转发

---

## 相关文档

- 详细指南: [VERCEL_404_FIX_GUIDE.md](VERCEL_404_FIX_GUIDE.md)
- 环境变量步骤: [VERCEL_ENV_SETUP.md](VERCEL_ENV_SETUP.md)
- 已修改文件:
  - `e-commerce-frontend/vercel.json`
  - `e-commerce-frontend/next.config.ts`

---

## 技术细节

**兼容性:** Next.js 16.1.6 ✅  
**标准:** Vercel最佳实践 ✅  
**重复配置:** 已移除 ✅  
**环境变量:** Vercel仪表板管理 ✅  

---

**修复完成时间:** 2026-02-25  
**预期效果:** 404错误解决，环境变量正确传递，API请求成功转发
