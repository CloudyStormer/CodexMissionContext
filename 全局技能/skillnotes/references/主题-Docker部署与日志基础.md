# 学习主题：Docker部署与日志基础

记录日期：2026-08-11
最近更新：2026-08-21

## 一句话回忆

Docker 用镜像封装应用环境并创建容器；应用通过 logger 输出日志，Docker 日志驱动捕获 stdout/stderr 并负责展示、轮换或转发。

## 核心结论

```text
Dockerfile -> Image -> Container -> Docker Engine
```

- 镜像包含 Python、依赖、代码和启动命令；容器是运行实例。
- 宿主机不必安装容器内相同版本 Python，但必须有兼容 Docker Engine 和足够资源。
- API Key、数据库地址等在启动时外部注入，不写入镜像。
- CI 负责测试和构建，CD 负责交付或部署；`docker pull` 不会自动替换旧容器。

## 日志链路

```text
logger.info/error
  -> Python Handler
  -> stdout/stderr或文件
  -> Docker日志驱动或文件系统
```

- `stdout` 是标准输出，`stderr` 是标准错误/诊断输出。
- `StreamHandler` 输出到流；`FileHandler` 追加写入文件。
- Docker 不会自动生成业务日志，代码仍需调用 logger。
- `docker logs` 不会自动读取任意 FileHandler 文件。
- 普通 FileHandler 默认不轮换；可按大小或时间轮换。
- Docker 日志应配置 `max-size/max-file` 或接入日志平台。

## 前端类比

- stdout/stderr 类似 Node.js 的 `process.stdout` / `process.stderr`。
- Python logger 类似 Pino/Winston，不只是散落的 `console.log`。
- Docker 日志驱动类似部署平台统一接收进程输出，但不是永久数据库。

## 关键互动问答

**问：`docker logs` 是否自动拥有所有日志？**
答：只显示日志驱动捕获的 stdout/stderr；业务日志仍由代码产生，文件日志需另行采集。

**问：日志默认永久存在吗？**
答：不保证。可能持续增长，但容器删除、磁盘故障或平台策略都可能导致丢失。

**问：容器名和服务名一样吗？**
答：`docker logs` 使用容器名/ID；`docker compose logs` 使用 Compose 服务名。

## 能力边界与误区

- 写入容器内部的日志文件若不挂载 volume，删除容器时通常丢失。
- 正式生产通常输出 stdout/stderr，再由 Docker、systemd 或日志平台管理。

## 下次回忆提示

代码负责产生日志，Handler 决定去向，Docker 负责捕获，日志平台负责长期检索和保留。
