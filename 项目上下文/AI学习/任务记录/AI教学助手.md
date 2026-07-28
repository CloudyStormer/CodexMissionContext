# 长期任务：AI 教学助手

## 元数据

- 逻辑任务 ID：`ai-learning-teacher`
- 设备 A 线程 ID：`019ed1b3-b59f-7d52-96a0-641e80d71b57`
- 所属项目：AI学习
- 原工作目录：`/Users/qichao/Documents/AI学习`
- 主要代码目录：`/Users/qichao/Documents/AI学习/english-ai-coach`
- 状态：进行中

## 目标

以“英语 AI 陪练”为实战项目，按专业顺序带用户从前端开发逐步进入 Python 后端、大模型应用、Agent、部署和模型训练。

## 教学要求

- 一次只讲一个概念，完成并验证后再进入下一步。
- 使用中文、前端类比和逐行拆解。
- 介绍代码时给出真实文件和行号链接，不只贴孤立代码块。
- Python、AI 应用、Agent、Prompt、模型训练和服务器部署均不得遗漏。
- 使用豆包/火山方舟，不要求 OpenAI。
- 代码、配置、测试和启动由 Codex 完成；用户只在安全位置提供 API Key。
- 密钥不能发到聊天、截图或 Git。
- 用户明确说“记笔记”时，交给独立的 AI 笔记助手。

## 已确认理解

- 主链路：`Uvicorn → FastAPI app → 路由汇总 → POST /api/v1/practice/turn → Service → 响应模型 → JSON`。
- 请求链：`JSON bytes → dict → PracticeTurnRequest → 业务逻辑 → PracticeTurnResponse → JSON bytes`。
- `request` 来自用户 JSON；`coach` 来自 `Depends(get_coach_service)`。
- `CoachService(Protocol)` 类似 TypeScript `interface`；Mock 与 Doubao 是具体实现。
- `.env` 保存环境差异值，不保存业务算法；配置修改后通常需要重启。
- 用户已经学习类、类型、实例、变量、`dict`、Pydantic、`None/null`、`async/await/return`、路由前缀和常见 HTTP 错误。

## 已完成

- FastAPI 英语陪练后端已建立并跑通。
- 已验证健康检查、等级列表、陪练请求、Pydantic 校验和 Swagger。
- Mock 阶段和豆包真实调用阶段测试均达到 `7 passed`。
- 真实模型使用 `doubao-seed-2-0-mini-260428`。
- 使用 HTTPX 调用火山方舟 Responses API。
- 使用 JSON Schema 约束 `reply`、`corrected_sentence`、`tip`。
- 移除了方舟不支持的 `metadata`，关闭非必要深度思考。
- API Key 已迁入被 Git 忽略的 `.env`。

## 关键文件

- `english-ai-coach/README.md`
- `english-ai-coach/LEARNING_PATH.md`
- `english-ai-coach/backend/app/main.py`
- `english-ai-coach/backend/app/api/router.py`
- `english-ai-coach/backend/app/api/routes/practice.py`
- `english-ai-coach/backend/app/api/dependencies.py`
- `english-ai-coach/backend/app/core/config.py`
- `english-ai-coach/backend/app/schemas/practice.py`
- `english-ai-coach/backend/app/schemas/ark.py`
- `english-ai-coach/backend/app/services/coach.py`
- `english-ai-coach/backend/app/prompts/english_coach.py`
- `english-ai-coach/backend/tests/test_doubao_coach.py`

## 精确下一步

从 `coach.py` 中的 `build_coach_instructions(request.level)` 开始讲 Prompt 如何按英语等级生成；随后依次讲完整请求体、方舟响应解析、结构化输出和错误处理。

## 设备 B 导入提示

```text
读取 AI教学助手.md，把它视为已经确认的教学进度。不要自动进入下一课，只回复“教学上下文已导入，等待继续”。
```

## 安全检查

- 摘要未包含真实 API Key。
- `.env` 不得进入 Git。

