# Vercel 404错误修复方案总结

## 问题诊断

### 问题1: vercel.json中的Rewrite循环冲突
**原始配置:**
```json
"rewrites": [
  {
    "source": "/api/(.*)",
    "destination": "/api/$1"
  }
]
```
**问题:** 自引用循环 - 请求 `/api/users` 被转发到 `/api/users`，导致本地404
**原因:** Vercel层和Next.js层都定义了API代理规则，造成冲突

**修复:** 
✅ 移除vercel.json中的整个`rewrites`字段
✅ 保留next.config.ts中的rewrite配置（在构建时处理）

---

### 问题2: 无效的API Routes运行时配置
**原始配置:**
```json
"functions": {
  "src/app/api/**/*.ts": {
    "runtime": "nodejs18.x"
  }
}
```
**问题:** 该项目无API路由（src/app下无api文件夹），配置指向不存在的路径
**原因:** 复制的样板文件，但此项目采用外部后端架构

**修复:**
✅ 移除`functions`字段（不需要Vercel托管API）
✅ API请求通过next.config.ts的rewrites转发到后端

---

### 问题3: 环境变量传递失败
**原始配置:**
```json
"env": {
  "NEXT_PUBLIC_API_URL": "@next_public_api_url"
}
```
**问题:** 
- vercel.json的env配置已过时（Vercel推荐用仪表板管理）
- `@next_public_api_url` 需要在Vercel中预先定义引用
- next.config.ts直接访问process.env可能获取到undefined

**修复:**
✅ 移除vercel.json中的env字段
✅ 在Vercel仪表板设置环境变量
✅ next.config.ts添加fallback: `process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'`

---

## A) 修复后的vercel.json

**路径:** `e-commerce-frontend/vercel.json`

```json
{
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "installCommand": "npm install",
  "devCommand": "npm run dev"
}
```

**关键变化:**
- 移除 `env` 字段 → 改用Vercel仪表板配置
- 移除 `functions` 字段 → 项目无托管API路由
- 移除 `rewrites` 字段 → 避免与next.config.ts冲突

**与Next.js 16.1.6兼容性:** ✅ 完全兼容
**Vercel最佳实践:** ✅ 遵循最小化原则

---

## B) 修复后的next.config.ts

**路径:** `e-commerce-frontend/next.config.ts`

```typescript
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
```

**关键变化:**
- 移除 `serverExternalPackages: []` → 无必要的空配置
- 改用 `beforeFiles` rewrites结构 → Next.js 16标准做法
- 添加 `reactStrictMode: true` → 启用严格模式检查
- 添加Fallback值 → 环境变量未定义时使用localhost

**环境变量访问方式:**
- 客户端: `process.env.NEXT_PUBLIC_API_URL`
- 构建时: 注入实际值
- 运行时: Vercel仪表板值替换

**与Next.js 16.1.6兼容性:** ✅ 完全兼容
**备注:** `beforeFiles` 是标准高性能rewrite配置

---

## C) Vercel仪表板环境变量配置步骤

详见 [VERCEL_ENV_SETUP.md](VERCEL_ENV_SETUP.md) 的"C) Vercel仪表板环境变量配置步骤"

**快速步骤:**
1. 登录 https://vercel.com/dashboard
2. 进入项目 → Settings → Environment Variables
3. 添加变量 `NEXT_PUBLIC_API_URL`
4. 设置三个环境的值 (Production / Preview / Development)
5. 触发重新部署

---

## D) 验证检查清单

详见 [VERCEL_ENV_SETUP.md](VERCEL_ENV_SETUP.md) 的"D) 部署前检查清单"

**关键检查点:**
- [ ] 本地构建成功: `npm run build`
- [ ] 本地运行正常: `npm run dev`
- [ ] Vercel仪表板已设置环境变量
- [ ] `.env.local` 包含开发值
- [ ] API请求成功转发 (浏览器控制台无错误)
- [ ] Vercel部署日志无构建错误

---

## 应用修复的步骤

```bash
# 1. 确保修改已生效
git status  # 应显示vercel.json和next.config.ts已修改

# 2. 本地测试
npm run build
npm start

# 3. 在浏览器测试API调用
# - 打开 http://localhost:3000
# - 检查 Network 标签，验证 /api/* 请求转发到后端

# 4. 配置Vercel环境变量
# - 访问 Vercel 仪表板
# - Project Settings → Environment Variables
# - 添加 NEXT_PUBLIC_API_URL

# 5. 部署
git add .
git commit -m "fix: resolve Vercel 404 errors - remove rewrite conflicts and invalid configs"
git push

# 6. 验证部署
# - 等待Vercel自动部署 (3-5分钟)
# - 访问预览URL验证功能
```

---

## 文件修改总结

| 文件 | 修改类型 | 详细内容 |
|-----|--------|---------|
| `vercel.json` | ✂️ 删除3项 | 移除env、functions、rewrites配置 |
| `next.config.ts` | 📝 优化 | 简化结构、添加注释、改进rewrite配置 |
| `.env.local` | 📝 需创建 | 添加: `NEXT_PUBLIC_API_URL=http://localhost:8000` |

---

## 预期结果

### 修复前
- ❌ Vercel部署404错误
- ❌ API请求循环转发
- ❌ 环境变量未正确传递
- ❌ 本地和远程行为不一致

### 修复后
- ✅ 404错误解决
- ✅ API请求直接转发到后端
- ✅ 环境变量正确注入
- ✅ 本地开发和Vercel部署表现一致
- ✅ 完全符合Vercel最佳实践
- ✅ Next.js 16.1.6完全兼容
