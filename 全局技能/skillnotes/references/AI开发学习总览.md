# AI 开发学习总览

最近更新：2026-08-21

## 当前状态

- 背景：前端工程师，通过英语 AI 陪练学习 Python、后端和 AI 应用开发。
- 项目：`/Users/qichao/Documents/AI学习/english-ai-coach`。
- 模型：火山方舟 `doubao-seed-2-0-mini-260428`。
- 已完成：FastAPI 基础调用链、Pydantic、依赖注入、豆包完整响应、Prompt、结构化输出、Mock 测试、SSE 前端解析与取消。
- 正在学习：`AsyncIterator[str]`、异步生成器，以及豆包上游流到浏览器下游流的衔接。
- 下一步：给 `CoachService` 增加独立的 `stream_reply()`，先实现 Mock 和测试，再接豆包原生流。
- 验证基线：完整测试 `9 passed`；正常流日志 `completed=True`，中断流日志 `completed=False`。

## 学习路线

```text
Python/FastAPI基础                 已完成第一轮
豆包完整响应、Prompt、结构化输出    已完成
SSE、Fetch流、取消                 已完成第一轮
豆包原生流式输出                   进行中
多轮上下文、Token与评测             待学习
数据库、事务、迁移                 待学习
前端产品化、语音                   待学习
RAG、工具调用、Agent、MCP          待学习
Docker部署、监控、商业化            已了解概念，待实战
PyTorch、Transformer、SFT、LoRA    后期专项，不遗漏
```

## 项目调用链

```text
浏览器/Swagger
  -> Uvicorn监听HTTP
  -> FastAPI路由
  -> Pydantic把JSON校验成Python对象
  -> Depends注入CoachService
  -> MockCoachService或DoubaoCoachService
  -> 豆包Responses API
  -> Pydantic校验模型输出
  -> FastAPI序列化JSON
  -> 浏览器
```

关键文件：

```text
backend/app/main.py                    应用入口
backend/app/api/routes/practice.py     普通接口与SSE Demo
backend/app/api/dependencies.py        注入Mock或豆包Service
backend/app/services/coach.py          业务逻辑和模型调用
backend/app/schemas/practice.py        请求/响应模型
backend/app/prompts/english_coach.py   Prompt
backend/app/static/stream-lab.html     前端流式实验
backend/tests/                         自动化测试
```

## Python与前端对照

| Python/后端 | 前端类比 | 关键区别 |
|---|---|---|
| `dict` | 普通对象 | dict 是独立内置类型，键不限于字符串 |
| 类型标注 | TypeScript 类型 | Python 默认仍是动态类型 |
| Pydantic | Zod schema + 类型 | Pydantic 在运行时校验并创建对象 |
| `Protocol` | TypeScript `interface` | 描述服务应提供哪些方法 |
| `Depends()` | 服务端依赖注入 | 参数不来自用户 JSON |
| `async def/await` | `async function/await` | 概念相近，运行时不同 |
| `AsyncIterator[str]` | `AsyncIterable<string>` | 每次获取下一项可能需要等待 |
| `async for` | `for await...of` | 逐项消费异步生成器 |

## 高频代码

### 请求与依赖注入

文件：`backend/app/api/routes/practice.py`

```python
@router.post("/turn", response_model=PracticeTurnResponse)
async def create_practice_turn(
    request: PracticeTurnRequest,
    coach: Annotated[CoachService, Depends(get_coach_service)],
) -> PracticeTurnResponse:
    return await coach.create_turn(request)
```

- `request` 来自用户 JSON。
- `coach` 由 FastAPI 调用 `get_coach_service()` 创建。
- `await` 最终得到一个完整 `PracticeTurnResponse`。

### Pydantic请求模型

```python
class PracticeTurnRequest(BaseModel):
    message: str = Field(max_length=500)
    level: Literal["beginner", "intermediate", "advanced"] = "beginner"
```

不传 `level` 会补默认值；非法数据在进入业务函数前返回 `422`。

### 豆包完整响应

文件：`backend/app/services/coach.py`

```python
response = await client.post(
    "responses",
    json={
        "model": self._model,
        "instructions": build_coach_instructions(request.level),
        "input": request.message,
        "text": {"format": {"type": "json_schema"}},
    },
)

ark_response = ArkResponse.model_validate(response.json())
parsed = AIPracticeTurn.model_validate_json(ark_response.get_output_text())
```

`json=` 负责 HTTP 序列化；JSON Schema 负责约束模型输出；`model_validate_json()` 负责把模型 JSON 字符串变成 Pydantic 对象。

### 后端SSE生成器

```python
async def _demo_reply_stream(reply: str) -> AsyncIterator[str]:
    try:
        for chunk in chunks:
            yield _sse_event("delta", {"text": chunk})
            await asyncio.sleep(0.4)
        yield _sse_event("done", {"status": "completed"})
    finally:
        logger.info("Demo stream closed")
```

每个 `yield` 是异步迭代器的一项。当前每项是一条完整 SSE，其中 `text` 是部分回答。

JavaScript 对照：

```javascript
async function* streamReply() {
  yield "Hel";
  yield "lo";
}

for await (const text of streamReply()) {
  console.log(text);
}
```

### 前端读取响应流

文件：`backend/app/static/stream-lab.html`

```javascript
const response = await fetch(url, options);
const reader = response.body.getReader();
const decoder = new TextDecoder();
let pendingText = "";

while (true) {
  const { done, value } = await reader.read();
  if (done) break;

  pendingText += decoder.decode(value, { stream: true });
  const frames = pendingText.split("\n\n");
  pendingText = frames.pop();

  for (const frame of frames) {
    const parsed = parseEvent(frame);
    if (parsed?.event === "delta") {
      replyOutput.textContent += parsed.data.text;
    }
  }
}
```

一次 `fetch()`，多次 `reader.read()`。`read()` 得到当前可用的 `Uint8Array`，不保证正好是一条 SSE。

### 取消链路

```text
AbortController.abort()
  -> 浏览器终止请求
  -> Uvicorn产生ASGI http.disconnect
  -> Starlette取消StreamingResponse任务
  -> Python异步生成器进入finally
```

`finally` 不是监听器；框架取消任务导致代码离开 `try`，所以执行清理。

## 关键互动问答

**问：一次 Fetch 流为什么会多次处理？**
答：请求和异步函数都只执行一次；同一个 `while` 循环多次调用 `reader.read()`。

**问：`read()` 是否每次正好拿到一条 SSE？**
答：不是。它拿到任意网络字节块；一次 SSE 可拆成多次 read，多条 SSE 也可合并在一次 read。

**问：残缺 JSON 为什么不会立刻报错？**
答：先追加到 `pendingText`，只有出现 `\n\n` 的完整 SSE 才进入 `parseEvent()` 和 `JSON.parse()`。

**问：`Uint8Array` 是否只有0和1？**
答：不是。每项占8 bit，值为0–255；`new Uint8Array(4)` 默认是四个0，不是随机数。

**问：`TextDecoder.decode(..., {stream:true})` 返回什么？**
答：返回 JavaScript 字符串；`stream:true` 让解码器暂存被拆开的多字节字符。

**问：`AsyncIterator` 是方法吗？**
答：不是，是标准库类型协议；`yield` 产出项目，`async for` 逐项消费。

**问：后端日志 `completed=False` 能否证明前端没收到 done？**
答：不能。它只证明生成器没继续执行到赋值位置，不能当作客户端送达回执。

**问：断网后已显示内容会怎样？**
答：已写入 DOM 的完整事件保留；残缺事件留在 `pendingText` 并丢失；当前 Fetch 不自动续传。

## 已纠正的误区

- SSE 的 `event:` 字段名是标准；`delta/done` 是项目自定义值。
- `\n\n` 是 SSE 事件边界，不是模型厂商随意约定。
- 当前 Mock 先生成完整回答再拆段，停止发送不能节省模型 Token。
- 后端一次 `yield` 不等于前端一次 `read()`。
- 完整回答由多个独立、完整 JSON 的 `delta` 事件追加形成。
- 结构化模型 JSON 的残缺 delta 不能直接 `JSON.parse()`，也不应直接显示给用户。

## Docker与日志速记

```text
Dockerfile -> Image -> Container -> Docker Engine
```

- 代码通过 logger 产生日志；Handler 决定输出到 stdout/stderr 或文件。
- Docker 捕获 stdout/stderr，但不会自动生成业务日志，也不读取任意 FileHandler 文件。
- `docker logs 容器名` 使用容器名；`docker compose logs 服务名` 使用 Compose 服务名。
- 日志默认不会永久可靠保存；应配置大小/时间轮换和生产日志平台。

## 下一步代码目标

```python
class CoachService(Protocol):
    def stream_reply(
        self,
        request: PracticeTurnRequest,
    ) -> AsyncIterator[str]:
        ...
```

实现顺序：

1. Mock `stream_reply()` 与测试。
2. 豆包 `httpx.AsyncClient.stream()` 上游流。
3. 路由把上游 delta 转换成内部 SSE。
4. 客户端取消时关闭豆包上游连接。
5. 再解决自然语言流与结构化纠错 JSON 的组合。

## 专题入口

- [FastAPI与豆包应用基础](主题-FastAPI与豆包应用基础.md)
- [SSE流式响应与前端解析](主题-SSE流式响应与前端解析.md)
- [Python异步生成器与流取消](主题-Python异步生成器与流取消.md)
- [Docker部署与日志基础](主题-Docker部署与日志基础.md)
