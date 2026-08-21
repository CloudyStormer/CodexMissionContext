# 学习主题：SSE流式响应与前端解析

记录日期：2026-08-20
最近更新：2026-08-20

## 一句话回忆

一次 Fetch 请求可以持续读取同一个 HTTP 响应体；`reader.read()` 得到任意大小的网络字节块，前端必须先解码、缓冲并按 `\n\n` 找到完整 SSE 事件，再解析其中的 JSON。

## 为什么重要

大模型文字生成通常不是等待完整答案后一次返回，而是持续产生文本片段。理解字节流、SSE 事件和业务文本的边界，才能正确处理流式显示、断网、取消和半包数据。

## 核心结论

### 一次请求，多次读取

- `fetch()` 只发起一次请求，外层异步函数也只执行一次。
- Fetch 在响应头到达后得到 `Response`，此时响应体可能仍在持续到达。
- 同一个函数通过循环多次调用 `await reader.read()` 消费响应体。
- `await` 是暂停并恢复同一次函数执行，不是重新触发整个函数。
- `reader.read()` 的 `done: true` 表示 HTTP 响应体关闭；项目自定义的 `event: done` 表示业务回答完成，二者不是一回事。

### 三种“段”不能混淆

1. 回答片段：如 `"Hello "`、`"World"`，由业务或模型决定。
2. SSE 事件：每个回答片段被包装成一条完整事件，每条 `data:` 都包含独立、完整的 JSON。
3. 网络读取块：Fetch 本次交给 `reader.read()` 的一批字节，边界由网络、系统和浏览器缓冲决定。

后端一次 `yield` 不保证对应前端一次 `read()`：一次事件可能被拆成多次读取，多条事件也可能合并在一次读取中。

### SSE 约定

- SSE 全称 `Server-Sent Events`，中文通常称“服务器发送事件”。
- `event:`、`data:`、`id:`、`retry:` 是标准字段。
- `\n\n` 是标准事件结束分隔符。
- `delta`、`done` 等事件名由项目自行定义，没有固定数量。
- 不写 `event:` 时，原生 `EventSource` 通常按 `message` 事件处理。
- SSE 常用于大模型文字流，但不是唯一方案；还可以使用 WebSocket、NDJSON 或自定义 Fetch 流。

### 字节、解码和缓冲

- Fetch 的 `response.body.getReader().read()` 在当前场景返回 `{ done, value }`。
- `value` 是 `Uint8Array`；读取结束时通常是 `undefined`。
- `Uint8Array` 每个元素占 8 bit，取值为 0–255，共 256 种，不是只有 0 和 1。
- `new Uint8Array(4)` 默认得到 `[0, 0, 0, 0]`，不会产生随机数。
- `ArrayBuffer` 是原始二进制内存；`Uint8Array` 是按每个 8 bit 无符号整数访问该内存的视图。
- `TextDecoder.decode(value, { stream: true })` 返回普通 JavaScript 字符串。
- `stream: true` 表示后续还有字节，使解码器可以暂存被拆开的多字节 UTF-8 字符；它不表示返回一个流。
- `TextDecoder` 解决“一个字符的字节被拆开”；`pendingText` 解决“一条 SSE 事件的文字被拆开”。

### 为什么残缺 JSON 不会立即解析

前端不是 `read()` 后立刻执行 `JSON.parse()`，而是：

```javascript
pendingText += decoder.decode(value, { stream: true });
const frames = pendingText.split("\n\n");
pendingText = frames.pop();

for (const frame of frames) {
  const parsed = parseEvent(frame);
}
```

- 没有 `\n\n` 时，残缺内容被 `frames.pop()` 放回 `pendingText`，`frames` 为空，不会解析。
- 下一批字节到达后继续拼接。
- 出现 `\n\n` 后，才把完整 SSE 事件送入 `parseEvent()`。
- `parseEvent()` 是项目自定义函数，不是浏览器原生 API。
- `JSON.parse()` 只解析 `data:` 后面的 JSON 字符串，不解析整个 SSE 文本。
- 如果服务器错误地在残缺 JSON 后发送 `\n\n`，前端才会错误地认为事件完整并发生 JSON 解析异常。

## 怎么使用

项目当前前端流式读取链路：

```text
一次fetch
  -> Response.body.getReader()
  -> 多次reader.read()
  -> Uint8Array
  -> TextDecoder转成JS字符串
  -> pendingText暂存和拼接
  -> 按\n\n提取完整SSE事件
  -> parseEvent提取event/data
  -> JSON.parse(data)
  -> 将delta文本追加到页面
```

当前项目使用 `fetch + POST + 手动解析 SSE`，因为传统原生 `EventSource` 主要用于 GET，不方便携带当前练习请求的 JSON body。

## 能力边界与误区

- TCP 保证正常连接上的字节可靠、有序，但不保存 SSE 或 `yield` 的业务边界。
- `pendingText` 只能处理同一连接中的分块，不能实现断线续传。
- 第一、第二条完整 SSE 已显示后，即使第三条中途断开，前两条仍然有效。
- 第三条只到达半条时会留在 `pendingText`，不会被解析；连接失败后这部分会丢失。
- 当前 Fetch 实现不会自动重连。断线续传需要额外设计事件 ID、服务端保存和重连位置。
- 当前 Demo 是 Mock 先产生完整回答，再由 Python 人为拆段发送；它还不是真实模型原生流式生成。

## 已验证记录

- 项目流式接口：`POST /api/v1/practice/turn/demo-stream`。
- 前端实验页：`http://127.0.0.1:8000/demo/stream-lab.html`。
- 页面源文件：`backend/app/static/stream-lab.html`。
- 后端源文件：`backend/app/api/routes/practice.py`。
- 已观察到正常流包含多条 `delta` 和一条 `done`；中途取消只收到前面的部分事件。

## 下次回忆提示

先问自己：`reader.read()` 读取的是完整 SSE，还是当前可用的任意网络字节？如果回答“任意网络字节”，再回忆 `TextDecoder -> pendingText -> \n\n -> parseEvent -> JSON.parse` 这条链。
