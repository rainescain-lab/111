# TikTok 选品决策系统（MVP）

一个可直接部署到 Vercel 的 Next.js 14 App Router 项目，通过 5 问答生成选品画像，并用 Supabase 规则引擎输出 4 层选品池。

## 技术栈
- Next.js 14 + TypeScript + App Router
- TailwindCSS
- @supabase/supabase-js

## 环境变量
> **注意：任何 key 都不能写在代码或文档示例中。**

在根目录创建 `.env.local`：

```
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
```

项目启动时会校验缺失变量并抛出清晰错误提示。

## Supabase 建表（SQL）
在 Supabase SQL Editor 执行：

```sql
-- 见 supabase/schema.sql
```

`supabase/schema.sql` 内容包含：
- products / product_cards / rules 表结构
- RLS 只读策略（前端仅 SELECT）

## 导入 seed 数据
执行以下 SQL 或导入 `supabase/seed.sql`：

```sql
-- 见 supabase/seed.sql
```

Seed 包含：
- 至少 10 个产品
- 对应产品卡片
- 规则配置（含 4 层池）

## 本地运行
```bash
pnpm install
pnpm dev
```

访问：
- `http://localhost:3000/`
- `http://localhost:3000/quiz`
- `http://localhost:3000/result`
- `http://localhost:3000/product/[id]`

## Vercel 部署
1. 将项目推送到 GitHub。
2. 在 Vercel 新建项目，选择该仓库。
3. 在 Vercel 环境变量配置中添加：
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
4. 一键部署即可。

## 目录结构
```
src/
  app/(routes)/
  components/
  lib/
  styles/
```

## 只读策略说明
- 前端仅 SELECT：products / product_cards / rules
- 未开启任何写入策略，匿名用户不可 INSERT/UPDATE/DELETE
- 答题结果存 localStorage，不落库
