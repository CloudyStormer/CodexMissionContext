# 学习主题：FastAPI与豆包应用基础

记录日期：2026-08-21
最近更新：2026-08-21

## 一句话回忆

FastAPI 接收 HTTP JSON，Pydantic 将其校验为 Python 对象，依赖注入选择 Mock 或豆包 Service，Service 调用 Responses API 并把结构化模型输出变成业务响应。

## 核心结论

- Uvicorn 监听端口并运行 ASGI 应用；FastAPI 负责路由、校验、依赖注入和响应。
- Pydantic 默认值会补齐缺失字段，非法数据通常在进入业务函数前返回 `422`。
- Python 内部操作 Python 对象；FastAPI 在响应阶段序列化 JSON。
- `Depends(get_coach_service)` 创建服务实例，不读取用户 JSON。
- `COACH_MODE` 决定使用 Mock 还是豆包。
- Prompt 的 `instructions` 可以使用中文，且应与用户输入分开。
- `json=` 负责 HTTP 序列化；JSON Schema 负责约束模型输出。
- `model_validate_json()` 是 Pydantic 方法，用来校验模型返回的 JSON 字符串。
- `httpx.MockTransport` 可以验证豆包调用映射，不消耗 Token。

## 前端类比

```text
Pydantic BaseModel   类似 Zod schema + 类型
Protocol             类似 TypeScript interface
Depends              类似服务端依赖容器
httpx AsyncClient    类似服务端 fetch/axios
```

区别：TypeScript 类型通常不在运行时校验；Pydantic 会在 Python 运行时校验并创建对象。

## 代码案例

```python
@router.post("/turn", response_model=PracticeTurnResponse)
async def create_practice_turn(
    request: PracticeTurnRequest,
    coach: Annotated[CoachService, Depends(get_coach_service)],
) -> PracticeTurnResponse:
    return await coach.create_turn(request)
```

```text
请求JSON -> PracticeTurnRequest -> CoachService -> PracticeTurnResponse -> JSON
```

## 关键互动问答

**问：`Annotated[CoachService, Depends(...)]` 是否要求用户多传一个参数？**
答：不要求。用户只传请求 JSON；FastAPI 在服务器内部生成 `coach`。

**问：JSON Schema 和 `httpx json=` 是否重复？**
答：不重复。前者约束内容结构，后者负责把 Python 数据编码成 HTTP JSON。

**问：`model_validate_json` 是自定义方法吗？**
答：不是，是 Pydantic `BaseModel` 提供的方法。

## 能力边界与误区

- FastAPI 是 Web 框架，路由只是其中一部分。
- `response_model` 约束业务响应，不代表模型厂商返回天然合法。
- API Key 只能放在后端环境变量，不进入前端、仓库、日志和笔记。

## 已验证记录

- 普通接口：`POST /api/v1/practice/turn`。
- Swagger：`http://127.0.0.1:8000/docs`。
- 模型：`doubao-seed-2-0-mini-260428`。

## 下次回忆提示

从用户 JSON 开始，按“Pydantic -> Depends -> Service -> 豆包 -> Pydantic -> JSON”复述一次。
