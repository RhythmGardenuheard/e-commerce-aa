# Vercel 环境变量配置指南

## 问题
您的 Next.js 应用因缺少 `NEXT_PUBLIC_API_URL` 环境变量而返回 404，导致 API 调用失败。

## 解决方案

### 方式 1: Vercel 仪表板配置（推荐）

1. **登录 Vercel**: https://vercel.com/dashboard
2. **选择项目**: `e-commerce-aa`
3. **进入设置**: Settings → Environment Variables
4. **添加变量**:
   ```
   名称: NEXT_PUBLIC_API_URL
   值: https://your-railway-backend-url.com (替换为实际URL)
   ```
5. **选择环境** (推荐全部选中):
   - ✅ Production
   - ✅ Preview  
   - ✅ Development
6. **保存**: 点击 "Save"
7. **重新部署**: 进入 Deployments，点击最新部署旁的 "Redeploy"

### 方式 2: 本地测试（可选）

创建 `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

运行开发环境:
```bash
npm run dev
```

### 方式 3: vercel.json 中硬编码（不推荐用于生产）

```json
{
  "env": {
    "NEXT_PUBLIC_API_URL": "@next_public_api_url"
  }
}
```

## 验证

部署完成后，访问您的应用并检查：

1. **浏览器控制台**:
   ```javascript
   // 打开开发者工具 (F12) → Console 输入：
   console.log(process.env.NEXT_PUBLIC_API_URL)
   ```

2. **检查 API 调用**:
   - 打开 Network 标签
   - 调用任何 API 端点
   - 确认请求发送到正确的后端 URL

3. **检查构建输出**:
   - Vercel Deployments → 选择最新部署
   - 查看 Build 阶段日志
   - 确认环境变量已注入

## 常见问题

**Q: 为什么我设置了环境变量但仍然返回 404?**
A: 可能需要重新部署。点击 "Redeploy" 按钮触发新的构建过程。

**Q: 我不知道我的后端 URL 是什么?**
A: 如果部署在 Railway，访问 https://railway.app/dashboard，点击项目，查看 Service URL。

**Q: 本地开发时环境变量未生效?**
A: 确保创建了 `.env.local` 文件并重启 `npm run dev`。