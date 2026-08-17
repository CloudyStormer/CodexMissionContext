# Codex 与 AppData 迁移到 E 盘

更新时间：2026-08-17（设备 B）

## 用户目标

- 将此前暂存于 `D:\C-Drive-Migration-Staging` 的 Codex 与可迁移 AppData 缓存最终迁入新 E 盘，今后同类数据也写入 E。
- 迁移后不保留 C/D 的数据副本或 E 内重复副本；迁移前后必须验证可用性与完整性。

## 当前已核验事实

- 当前 Codex 运行环境和用户级持久化变量均指向 D：
  - `CODEX_HOME` / `CODEX_SQLITE_HOME`：`D:\C-Drive-Migration-Staging\CodexHome`
  - npm、Yarn、pip、`TEMP` / `TMP`：`D:\C-Drive-Migration-Staging\AppData-Caches\...`
- D 的主数据当前仍在写入：`CodexHome` 最近写入为 2026-08-17；C 的旧 `.codex` 最后写入为 2026-08-13。
- D 主数据量：`CodexHome` 46.435 GiB，`AppData-Caches` 14.914 GiB；其中 6 个 Codex SQLite 数据库的 `PRAGMA quick_check` 均为 `ok`。
- `D:\C-Drive-Migration-Staging\C-Origin-Relocated` 是 38.404 GiB 的回退副本。其 `CodexHome` 中 942 个文件已逐文件 SHA-256 对照：941 个同哈希；唯一差异是 D 主副本中的同一历史会话追加了数据，且其前缀与旧文件的 SHA-256 一致。因此回退区没有发现独有的会话内容，但在最终切换验证前尚未删除。
- 当前 E 是不同于先前故障盘的新盘：`Lenovo L6`，序列号 `EE202512051033`，USB/GPT，状态 Healthy、未标记为 Dirty；`chkdsk E:` 已完成并报告无文件系统错误。512 MiB 随机写入、两次独立 SHA-256 读取一致，近 7 天无该盘存储错误事件。
- 但 E 当前为 **USB 外接盘 + exFAT**，并且已有约 214.7 GiB / 2,707 个既有文件。exFAT 不提供 NTFS 权限与日志保护，不适合承载 Codex 的实时 SQLite 状态；直接格式化会清空这些既有文件。

## 安全结论与下一步

- 不得将运行中的 `CODEX_HOME`、`CODEX_SQLITE_HOME` 或 `TEMP` 直接切到当前 exFAT E，以免断连、意外拔盘或异常关机导致状态库损坏。
- 推荐方案：先逐文件校验备份 E 现有内容至 D，格式化 E 为 NTFS，再进行 D -> E 的逐文件复制、哈希/SQLite 校验、路径切换、应用重启验证，最后才删除 C/D 的已确认重复源。
- 因格式化会清除 E 现有约 214.7 GiB 文件，必须取得用户对此不可逆操作的明确授权后执行。期间不得删除或覆盖 E、C 或 D 的用户数据。
