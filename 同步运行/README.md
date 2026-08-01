# “开始同步”运行交接

本目录保存四字口令“开始同步”的跨设备运行级精准交接，不保存原始聊天、附件、本地数据库、session、凭据或代码副本。

每次运行使用唯一目录：

```text
同步运行/<A或B>-<YYYYMMDDTHHMMSS+0800或Z>/
├── A-任务快照.md
├── B-任务快照.md
├── 合并任务包.md
├── A-回执.md
└── B-回执.md
```

所有运行文件都要记录：运行 ID、交接包协议版本、目标修订与规范化顺序 SHA、任务清单版本、开始时有效布局版本及其 SHA、开始时上下文提交。A/B 快照先生成，因此不记录尚不存在的合并包 SHA；`合并任务包.md` 记录两份快照文件 SHA，A/B 回执再记录最终合并任务包文件 SHA。不同运行或不同目标修订的快照与回执禁止混用。

快照文件、合并任务包文件的 SHA 均按整文件规范化字节计算：UTF-8 无 BOM、Unicode NFC、LF、移除行尾空白、末尾恰好一个换行。文件不在自身正文中记录自己的 SHA，避免自引用。

## 写入责任

- A 只创建或更新 `A-任务快照.md`、`A-回执.md`。
- B 只创建或更新 `B-任务快照.md`、`B-回执.md`。
- 发起端在取得两端快照后生成 `合并任务包.md`；另一端只读取并应用，不重新生成另一份正文。
- 同一运行目录中的既有设备快照和回执不由对方覆盖。发现冲突时保留双方文件并停止完成判定。

顺序必须分阶段：A/B 完整任务快照和合并包是发布下一布局候选的输入；候选按两阶段协议晋升为“有效”后，两端才应用该顺序并填写 `shared_index_verified`。不得要求尚未存在的新布局回执作为候选发布前提，也不得在候选晋升前按候选顺序重排。

## 任务快照最小字段

每台设备的快照必须按交接包目标顺序列出全部逻辑任务，每个 ID 恰好一次；不能只列本机已有项。每项记录：

```text
logical_task_id:
entity_state: PRESENT | MISSING | UNAVAILABLE
semantic_state: PRESENT | MISSING | UNAVAILABLE
title:
logical_project_id:
local_thread_id:
pinned:
visible_shared_index:
semantic_body_sha256:
semantic_body:
```

实体不存在时使用字面量 `MISSING`；实体列表工具或来源不可达时使用 `UNAVAILABLE`。不得使用空值、`null` 或直接省略字段。`entity_state` 不是 `PRESENT` 时，`local_thread_id`、`pinned`、`visible_shared_index` 使用同一哨兵值。`semantic_state` 单独表示精确正文是否可读：实体存在但正文读取能力缺失时写 `UNAVAILABLE`，并把 `semantic_body_sha256`、`semantic_body` 写为 `UNAVAILABLE`；实体缺失时两者写 `MISSING`。

语义正文按 `同步清单/完全对齐交接包.md` 的八节结构规范化。只读足以恢复当前状态的摘要和最近轮次，不复制原始消息全文。

正文 SHA 只覆盖八节正文，不含上述字段或消息头；规范化必须使用 UTF-8 无 BOM、Unicode NFC、LF、移除行尾空白并保留恰好一个末尾换行。`原设备与更新时间` 是语义来源时间，不因重复投递而变化。

## 合并任务包最小字段

文件元数据先记录 `snapshot_file_sha256_a`、`snapshot_file_sha256_b`。随后对交接包当前全部逻辑任务逐项记录：

```text
logical_task_id:
merge_state: READY | BLOCKED_MISSING | BLOCKED_UNAVAILABLE | CONFLICT
merged_body_sha256:
source_body_sha256_a:
source_body_sha256_b:
conflict: false | true | unknown
merge_rationale:
merged_body:
```

`source_body_sha256_a/b` 只表示该设备此任务的八节正文 SHA，不表示整份快照；缺失或不可达时分别使用 `MISSING`、`UNAVAILABLE`。合并包完成后计算整文件 SHA，但只把该值写入设备回执，不回写合并包自身。

合并状态必须按下列确定性规则填写，不得留空或凭推测补正文：

- 两端正文均为 `PRESENT` 且 SHA 相同：`merge_state: READY`，采用该正文与 SHA，`conflict: false`，`merge_rationale` 写 `EXACT_MATCH`。
- 一端正文为 `PRESENT`、另一端为 `MISSING`：`merge_state: READY`，采用存在端的正文与 SHA，`conflict: false`，`merge_rationale` 写 `SINGLE_SOURCE_A` 或 `SINGLE_SOURCE_B`；缺失端仍须创建镜像并回读验收。这里的来源 SHA 哨兵 `MISSING` 是补镜像的正常输入，不会阻止 READY 合并包进入候选。
- 两端正文均为 `PRESENT`、SHA 不同但事实兼容：发起端去重并完整合并双方的用户要求、决定原因、证据、失败、风险和下一步，生成一份新的规范化八节正文；`merge_state: READY`，`merged_body_sha256` 使用新正文 SHA，`conflict: false`，`merge_rationale` 以 `COMPATIBLE_MERGE:` 开头并引用两个来源 SHA、说明合并依据。不能只按时间戳选一端，也不能丢掉任一端仍有效的语义。
- 两端正文均为 `MISSING`：`merge_state: BLOCKED_MISSING`，`merged_body_sha256` 与 `merged_body` 都写字面量 `MISSING`，`conflict: false`，`merge_rationale` 写 `NO_SOURCE`。
- 任一端正文为 `UNAVAILABLE`：`merge_state: BLOCKED_UNAVAILABLE`，`merged_body_sha256` 与 `merged_body` 都写字面量 `UNAVAILABLE`，`conflict: unknown`，`merge_rationale` 写 `SOURCE_UNAVAILABLE`；即使另一端有正文也不得猜测两端一致。
- 两端正文均为 `PRESENT` 且存在不能同时成立的事实、互斥决定或无法安全消解的要求：`merge_state: CONFLICT`，`merged_body_sha256` 与 `merged_body` 都写字面量 `CONFLICT`，`conflict: true`，`merge_rationale` 写 `CONFLICT`，另加 `conflict_details` 精确引用两端来源 SHA 和矛盾摘要；原正文保留在两份快照中。

只有当前全部逻辑任务的 `merge_state` 均为 `READY`，合并包才具备进入“完整任务并集迁移”布局候选阶段的资格。`READY` 记录中的单端来源 SHA `MISSING` 可以保留，表示待补镜像，不是候选阻塞；任何 `merge_state` 非 `READY`、缺项、重复项或来源快照文件校验失败都会阻塞候选、本轮内容一致判定和“两端全部同步”。修复后使用新快照和新运行 ID 重建，不得就地把阻塞哨兵改写成猜测正文。

## 设备回执最小字段

每份回执的文件元数据记录 `target_layout_version`、`target_layout_sha256`、`applied_layout_version`、`applied_layout_sha256`；两组值必须指向顺序验收所依据的同一有效布局。项目布局再以逻辑 ID 列表记录：

```text
expected_projects_pinned:
actual_projects_pinned:
projects_pinned_verified:
expected_projects_unpinned:
actual_projects_unpinned:
projects_unpinned_verified:
project_layout_verified:
```

`project_layout_verified` 只有在两组 expected/actual 项目子序列逐项完全相同，且置顶状态均已通过正式 API 或用户可见界面回读时才能为 `true`；缺少项目排序、置顶或回读能力时写 `unknown`，并将本轮标记为部分应用。随后逐任务记录：

```text
logical_task_id:
project_id:
thread_id:
expected_title:
actual_title:
title_verified:
expected_project_id:
actual_project_id:
project_verified:
expected_pinned:
actual_pinned:
pinned_verified:
expected_shared_index:
actual_shared_index:
shared_index_verified:
expected_body_sha256:
actual_body_sha256:
body_sha256_verified:
```

`body_sha256_verified` 只能在正式读取任务中的 `[SYNC-CONTEXT v1]` 正文、重新规范化并计算 SHA 后写为真；发送接口返回成功不能替代回读。无法取得精确正文时写为未知并阻塞完成判定。

回执文件元数据还要记录 `merged_package_file_sha256`。回执还必须记录全部 Git 仓库最终 `HEAD`、upstream、ahead/behind、工作树、验证和 push 结果。只有 A、B 回执都存在、项目布局机器回执为真、应用的有效布局版本及 SHA 相同，且六个分量全部通过，才可声称“两端全部同步”。

## 运行中发现新任务

若任一快照发现交接包之外的新同步范围任务，本轮不得继续用旧目标发布布局候选或声称完成：先把新任务加入任务清单、提升清单版本，更新交接包目标顺序、数量和规范化 SHA 并推送；两端拉取同一新修订后，为新的运行 ID 重新生成完整快照。已经完成的只增不减实体补齐和安全语义摘录可以保留，但旧运行只能记为“目标已过期、未完成”。

未完成运行目录永久保留，状态写为“未完成”并列出阻塞；不得删除它来掩盖失败。成功运行也保留为审计入口，后续运行只写新增目录。
