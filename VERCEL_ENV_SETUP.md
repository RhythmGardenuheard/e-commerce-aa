# Vercel环境变量设置指南

## C) Vercel仪表板环境变量配置步骤

### 步骤1: 访问Vercel项目设置
1. 登录 https://vercel.com/dashboard
2. 选择项目: `e-commerce-frontend`
3. 点击 `Settings` → `Environment Variables`

### 步骤2: 添加NEXT_PUBLIC_API_URL
| 字段 | 值 |
|-----|-----|
| **Name** | `NEXT_PUBLIC_API_URL` |
| **Value** | `https://your-backend-domain.com` (生产环境) |
| **Environment** | Production, Preview, Development (全选) |

具体环境值：
```
生产环境 (Production):  https://api.yourdomain.com
预览环境 (Preview):     https://staging-api.yourdomain.com
开发环境 (Development): http://localhost:8000
```

### 步骤3: 验证环境变量
1. 点击 `Save` 后，触发重新部署
2. Vercel会自动重建项目，注入新环境变量

### 步骤4: 本地开发环境
在项目根目录创建 `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**重要**: 
- `NEXT_PUBLIC_`前缀变量在构建时注入（客户端、服务器都可访问）
- 不要在`.env.local`中提交密钥
- 重新启动开发服务器使变量生效：`npm run dev`

## 配置验证清单

### D) 部署前检查清单

#### 配置文件检查
- [ ] `vercel.json` 不包含 `env` 字段（改用Vercel仪表板）
- [ ] `vercel.json` 不包含 `functions` 字段（此项目无API路由）
- [ ] `vercel.json` 不包含冲突的rewrites（单一API代理规则）
- [ ] `next.config.ts` 的rewrites使用 `beforeFiles` 结构

#### 环境变量检查
- [ ] Vercel仪表板已设置 `NEXT_PUBLIC_API_URL`
- [ ] 值不包含末尾斜杠（正确: `https://api.example.com`）
- [ ] 三个环境都已配置（Production, Preview, Development）
- [ ] 本地 `.env.local` 包含开发环境值

#### 构建检查
- [ ] 本地构建成功: `npm run build`
- [ ] 无构建错误或警告
- [ ] `.next` 目录已生成

#### 运行时检查
- [ ] 本地启动成功: `npm run dev`
- [ ] API请求正确转发到后端（检查浏览器Network标签）
- [ ] 页面加载无CORS错误

#### Vercel部署检查
- [ ] 推送到GitHub后自动触发部署
- [ ] 部署日志无错误
- [ ] 预览URL可访问
- [ ] 生产URL正确解析API请求

#### 故障排查
如遇404错误：
1. 检查Vercel仪表板 → Deployments → 构建日志
2. 验证 `NEXT_PUBLIC_API_URL` 在运行时可访问
3. 检查后端API服务状态
4. 清除浏览器缓存: `Ctrl+Shift+Delete`
5. 检查 `next.config.ts` 的rewrites语法

如遇环境变量未注入：
1. Vercel仪表板重新部署: `Redeploy`
2. 确认环境变量 `Environment` 选项包含当前部署环境
3. 等待30秒使缓存失效
4. 在部署日志搜索 `NEXT_PUBLIC_API_URL`

## 推荐的部署流程

```bash
# 1. 本地验证
npm run build
npm run start

# 2. 提交代码
git add .
git commit -m "fix: resolve Vercel 404 and env var issues"
git push

# 3. Vercel自动部署（webhook触发）
# 等待 3-5 分钟

# 4. 验证预览URL
# 访问预览环境 Preview URL

# 5. 生产部署
# 合并到main分支后自动部署
```
