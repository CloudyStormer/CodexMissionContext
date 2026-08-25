# 学习主题：Python异步生成器与流取消

记录日期：2026-08-21
最近更新：2026-08-21

## 一句话回忆

带 `yield` 的 `async def` 是异步生成器，每次产出一项供 `async for` 消费；客户端断开会取消流任务，并通过 `finally` 清理资源。

## 核心结论

- `AsyncIterator` 是标准库类型协议，不是方法。
- `AsyncIterator[str]` 表示每项是字符串，获取下一项可能需要异步等待。
- 一个 `yield` 对应一项；这一项不一定是不完整字符串。
- 普通异步函数使用 `result = await fn()` 得到一个结果。
- 异步生成器使用 `async for item in fn()` 得到多个结果。
- `await asyncio.sleep()` 只暂停当前协程，不阻塞整个服务器。
- 取消后不会从下一个 chunk 自动恢复；重新连接是新请求。
- `finally` 不是监听器，而是退出 `try` 时执行的清理块。

## 前端类比

```python
async def stream_reply() -> AsyncIterator[str]:
    yield "Hel"
    yield "lo"

async for text in stream_reply():
    print(text)
```

```javascript
async function* streamReply() {
  yield "Hel";
  yield "lo";
}

for await (const text of streamReply()) {
  console.log(text);
}
```

## 关键互动问答

**问：逐项消费是否就是每次拿一个残缺字符串？**
答：一个 `yield` 是一项，但项可以是部分文字、完整句子、对象或完整 SSE。

**问：`yield done` 后 `completed=False` 是否矛盾？**
答：不矛盾。`yield` 会暂停生成器；数据可能已交出，但生成器尚未恢复执行下一行。

**问：怎么确认前端真的处理完成？**
答：普通聊天以服务端持久化为事实；必须确认时才设计 ACK。

## 流取消链路

```text
AbortController.abort()
  -> 浏览器终止请求
  -> Uvicorn通知ASGI http.disconnect
  -> Starlette取消StreamingResponse任务
  -> 生成器finally执行
```

未来双流：

```text
豆包 -> Python      上游流
Python -> 浏览器    下游流
```

`async with client.stream(...)` 用于在正常、异常或取消时关闭上游 HTTP 资源。

## 已验证记录

- 正常 Demo：`completed=True`。
- 中途断开：只收到第一条 SSE，`completed=False`。
- 完整测试：`9 passed`。

## 下次回忆提示

记住：`await` 等一个结果，`async for` 等很多项，`finally` 只保证清理，不保证客户端送达。
