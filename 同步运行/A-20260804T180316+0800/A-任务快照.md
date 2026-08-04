# 设备 A 任务快照

- 运行 ID：`A-20260804T180316+0800`
- 设备：A
- 交接包协议版本：`1`
- 目标修订：`1`
- 规范化目标顺序 SHA-256：`5310e24b57cfc72e401f56e2e6d775351fa701fd8fb0d1f451b62ca92cb5d81e`
- 任务清单版本：`5`
- 开始时有效布局版本：`3`
- 开始时有效布局 SHA-256：`5310e24b57cfc72e401f56e2e6d775351fa701fd8fb0d1f451b62ca92cb5d81e`
- 开始时上下文提交：`1ef92c089c3f1afbc5c13a3fd8ef5ee897fd55d2`
- 快照时间：2026-08-04 18:12（Asia/Shanghai）
- 正式任务来源：Codex `list_threads(limit=50)` 与目标线程定向回读；`unavailableHosts=[]`、`unavailableSources=[]`
- 快照结论：目标仍为 39 项，没有第 40 项；A 端 PRESENT 38 项、MISSING 1 项（`demo-foreman`），38 项均非置顶。两个先前不可见但可读取的目标任务已恢复可见。当前共享任务实际子序列因近期业务活动已偏离有效布局版本 3；B 本运行不可达，尚未生成 B 快照、唯一合并包或双端回执。

## `mission-context-current-sync`

logical_task_id: mission-context-current-sync
entity_state: PRESENT
semantic_state: PRESENT
title: 开始
logical_project_id: mission-context
local_thread_id: 019fc25a-b5c4-7082-a9bc-7c7049928335
pinned: false
visible_shared_index: 10
semantic_body_sha256: dd7fd62004a6dc9d3bfa9c7fda74e2b10e30bf0afd3ee97a194b6959db6c79f1
semantic_body: |
  ## 当前目标
  作为 CodexMissionContext 的“开始”入口保存双设备同步语义；只在用户明确触发时执行。

  ## 已完成
  用户确认 AIWorkflow 项目已手动创建且另一端已同步。A 已启动运行 A-20260804T180316+0800、拉取上下文至 1ef92c0，并把本任务恢复为可见。

  ## 关键决定与原因
  每次四字口令建立新运行；只有同一运行 ID 的 A/B 快照、唯一合并包和双端回执齐全才能报双端完成。镜像不自动执行旧需求。

  ## 文件与命令
  同步清单/完全对齐交接包.md、同步运行/README.md、全局技能/check-projects/SKILL.md、脚本/同步上下文.sh 开始。

  ## 验证
  A 正式列表未发现第 40 项；本任务定向读取成功，标题和项目路径未变。

  ## 失败与风险
  B 维护线程本轮返回 No Codex thread found；当前没有 B 快照或回执。Demo 无 HEAD，两个 funhub 来源不可达。

  ## 下一步
  等待用户继续；B 下次执行“开始同步”时拉取本运行记录并生成本端新快照，不能复用旧运行验收。

  ## 原设备与更新时间
  设备 A，2026-08-04 18:12（Asia/Shanghai）。

## `mission-context-maintenance`

logical_task_id: mission-context-maintenance
entity_state: PRESENT
semantic_state: PRESENT
title: 双设备同步维护
logical_project_id: mission-context
local_thread_id: 019fa7e2-1ca2-7453-aadf-bbbb23d633f3
pinned: false
visible_shared_index: 1
semantic_body_sha256: 1ea5d5c6b98f0a3b7abc7ddde9c197c90a10f464e1266461ed59d0e289307bc0
semantic_body: |
  ## 当前目标
  完成运行 A-20260804T180316+0800 的双设备项目、代码、39 个任务语义和共享布局同步。

  ## 已完成
  A 拉取上下文至 1ef92c0；18 个现存业务仓库均 fetch。funhub-taro 与证件照前端各快进 1 个远端提交；两个不可见目标任务已恢复可见。

  ## 关键决定与原因
  AI English Learning 的 6 项未提交前端现场被项目工作流冻结，禁止测试、提交或夹带。B 当前轮不可达时只发布 A 快照和未完成运行状态，不猜测合并包或任何正式回执。

  ## 文件与命令
  同步运行/A-20260804T180316+0800、check-projects/scripts/inspect-project-repos.sh、脚本/同步上下文.sh。

  ## 验证
  A 有 38/39 个目标实体、全部非置顶且无第 40 项。18 个业务仓中 17 个 clean 0/0；AIWorkFlow 为 a35316d、0/0、工作树 6 项冻结改动。Demo 两远端无 refs，两个 funhub 来源返回 Repository not found。

  ## 失败与风险
  B 唯一唤醒失败；A 仍缺 Demo 与 demo-foreman。近期活动使共享任务实际顺序偏离布局版本 3；项目布局仍无完整正式回读。

  ## 下一步
  发布 A 快照、未完成运行状态和交接；等待 B 拉取本运行并生成 B 快照。AIWorkflow 冻结现场由原固定角色在审批门后继续。

  ## 原设备与更新时间
  设备 A，2026-08-04 18:12（Asia/Shanghai）。

## `ai-workflow-00-foreman`

logical_task_id: ai-workflow-00-foreman
entity_state: PRESENT
semantic_state: PRESENT
title: 00 包工头
logical_project_id: ai-workflow
local_thread_id: 019fb746-5875-77b3-809a-08a16100d950
pinned: false
visible_shared_index: 6
semantic_body_sha256: fe7e77ccc15efc4c1077b233555890f7df2694713091cc5515ae7a9d37e127f3
semantic_body: |
  ## 当前目标
  以 12 个固定角色推进 English、AI Model Radar、Frontend Career Radar 和 Control Center，不新建项目专属任务。

  ## 已完成
  初始化 Career 子项目；固化“一次通过只前进唯一一站”、角色本人汇报、UI 资产放 ui/、浏览器内容优先和完整简体中文。最新根仓 HEAD 为 a35316d。

  ## 关键决定与原因
  项目隔离依靠 project.yaml、项目 Skill 和 workflow，不新增第 40 个任务。高风险动作和用户本轮指定的两份架构即使通过也不自动路由。

  ## 文件与命令
  根 AGENTS.md、skill/、projects/*/workflow/、control-center/workflow/；治理提交含 30ff229、45211c5、519557b、9e6a2aa。

  ## 验证
  单根 Git 边界、Skill 漂移、YAML/JSONL、Markdown 和项目验证通过；a35316d 与 origin/main 一致。

  ## 失败与风险
  English 新产品变更使固定 06 的 6 项未提交现场冻结；真实数据接入和生产部署未授权。

  ## 下一步
  等待用户审核 English PRD v1.3、两份架构和 Control Center 前端；未通过前不自动继续。

  ## 原设备与更新时间
  设备 A，2026-08-04 17:45（Asia/Shanghai）。

## `ai-workflow-01-market-researcher`

logical_task_id: ai-workflow-01-market-researcher
entity_state: PRESENT
semantic_state: PRESENT
title: 01 市场调研员
logical_project_id: ai-workflow
local_thread_id: 019fb799-5686-7571-ab7f-25bf816128b0
pinned: false
visible_shared_index: 9
semantic_body_sha256: 7ff3e3c0a84c4330fffef1de4a82d20e3aea12107394f98679f801a79ccc5924
semantic_body: |
  ## 当前目标
  完成 Frontend Career Radar 的市场、用户和证据研究。

  ## 已完成
  交付 docs/00-market-research.md，提交 c8ffa9e；用户已批准，审批与固定 02 路由提交 4efde47 已推送。

  ## 关键决定与原因
  Career Radar 留在 AIWorkflow 根仓子项目；先按职业方向，再展开技术栈，所有结论保留可追溯证据。

  ## 文件与命令
  projects/market-analysis-dev/docs/00-market-research.md 与 workflow/ 四件套。

  ## 验证
  结构、工作流状态、调研 SHA、Git 边界和提交均验证并推送。

  ## 失败与风险
  真实持续采集和生产数据尚未接入；调研通过不等于授权全部实施。

  ## 下一步
  本角色本轮完成；范围或证据变化时再入场。

  ## 原设备与更新时间
  设备 A，2026-08-03 17:54（Asia/Shanghai）。

## `ai-workflow-02-project-manager`

logical_task_id: ai-workflow-02-project-manager
entity_state: PRESENT
semantic_state: PRESENT
title: 02 项目经理
logical_project_id: ai-workflow
local_thread_id: 019fb738-5706-7552-849f-35c8a124e2f0
pinned: false
visible_shared_index: 8
semantic_body_sha256: 23f942fc3d73fb98d4e9924960faafcbe30f1f4b39c069ce1170a3b48162ba6c
semantic_body: |
  ## 当前目标
  分别制定 AI Model Radar 与 Frontend Career Radar 项目计划。

  ## 已完成
  Model Radar 项目计划提交 d2ecc08，Career 计划提交 ca6f791；两份均获批，审批与固定 03 顺序路由提交 ad7dfa2 已推送。

  ## 关键决定与原因
  Web 内容优先，真实采集、后端和部署后置；两项目互不串改，固定 03 按 Career 先、Model Radar 后串行。

  ## 文件与命令
  两项目 docs/01-project-plan.md 与各自 workflow/。

  ## 验证
  结构、边界、状态文件、精确提交和推送通过。

  ## 失败与风险
  计划不等于授权实施；后续角色仍须逐站审批。

  ## 下一步
  计划阶段完成；只有架构获批且用户允许时再拆首批任务。

  ## 原设备与更新时间
  设备 A，2026-08-04 11:26（Asia/Shanghai）。

## `ai-workflow-03-product-manager`

logical_task_id: ai-workflow-03-product-manager
entity_state: PRESENT
semantic_state: PRESENT
title: 03 产品经理
logical_project_id: ai-workflow
local_thread_id: 019fb74a-9dbd-7e13-823f-80584d8ac1b7
pinned: false
visible_shared_index: 4
semantic_body_sha256: b4935f13c00ada55487064b678f233ba0d8bc01c402a1f0f9cb22c33bcb9afdf
semantic_body: |
  ## 当前目标
  维护 Career、AI Model Radar 与 English 产品定义；当前等待 English 记忆曲线 PRD v1.3 审核。

  ## 已完成
  Career PRD v1.1、Model Radar PRD v1.0 和 English“查看答案”PRD v1.2 已批准。English PRD v1.3 的 SHA 为 0b065ec4ffb4881d6893ec23a1d9c4ec57627fe173f43ada73cdf5c3f4b02385，提交 cb705c4 已推送并停在 product-change-review。

  ## 关键决定与原因
  查看答案即登记薄弱词；当天随机复现，跨日 D+1/D+3/D+7/D+14，D+30 维护；在不同学习日独立拼写成功并满足掌握规则后退出。产品变化先冻结下游。

  ## 文件与命令
  三个项目 docs/01-prd.md 或 docs/02-prd.md 与 workflow/；新增 AC-SR-01..36，保留 AC-RA-01..20。

  ## 验证
  YAML/JSONL、验收编号、边界、Markdown、Git 边界和精确提交通过。

  ## 失败与风险
  English 固定 06 的 reveal-answer 未提交现场已冻结，不能继续测试或提交。

  ## 下一步
  等待用户审核 PRD v1.3；通过只授权固定 04 修订提示词。

  ## 原设备与更新时间
  设备 A，2026-08-04 17:02（Asia/Shanghai）。

## `ai-workflow-04-ui-ux-designer`

logical_task_id: ai-workflow-04-ui-ux-designer
entity_state: PRESENT
semantic_state: PRESENT
title: 04 UI/UX设计师
logical_project_id: ai-workflow
local_thread_id: 019fb74a-9f5f-7433-999e-2e30012296a0
pinned: false
visible_shared_index: 7
semantic_body_sha256: dfa1c3e753969c1440a7b65ecd3ce8037b8bbae419780019eea3d51e375f126d
semantic_body: |
  ## 当前目标
  在已批准 PRD 上交付 UI 提示词并登记用户视觉基线。

  ## 已完成
  English Prompt v1.2 已批；Career Prompt v1.0 与 10 张基线已批；Model Radar Prompt v1.0 与 9 张基线已批；Control Center Prompt v1.0.1 与 9 张基线已批。另交付四份纯出图提示词。

  ## 关键决定与原因
  用户图片是视觉基线，但中文、数据真实性和 PRD 规则优先。Model Radar 即“AI 市场新闻”；仓库只有四个真实 UI 项目，不能虚构第五个。

  ## 文件与命令
  各项目 ui/README.md、ui/03-ui-prompt.md 或 English docs/03-ui-prompt.md、workflow/。

  ## 验证
  Prompt SHA、资产数量、Skill 漂移和状态检查通过；提示词提取未修改文件。

  ## 失败与风险
  部分基线缺平板、深色和全状态覆盖。English PRD v1.3 未通过，旧 Prompt 不足以指导新闭环。

  ## 下一步
  PRD v1.3 通过后修订 English 提示词；若用户提供第五个真实项目名，再补提示词。

  ## 原设备与更新时间
  设备 A，2026-08-04 16:41（Asia/Shanghai）。

## `ai-workflow-05-architect`

logical_task_id: ai-workflow-05-architect
entity_state: PRESENT
semantic_state: PRESENT
title: 05 架构师
logical_project_id: ai-workflow
local_thread_id: 019fb74a-a1a4-7a90-9a35-ebb4f3d9d6db
pinned: false
visible_shared_index: 5
semantic_body_sha256: f3eb53405de3c4f7a8ae7f78ddf846e5ba0e00a8a61e12fe7d818115214a90f0
semantic_body: |
  ## 当前目标
  依次完成 Career 与 AI Model Radar 架构，并分别等待 architecture-review。

  ## 已完成
  Career 架构 SHA bcc782409ebde28e003c9e4a1c20d45ddcb3b787f8a2de020c451ef05957d144，提交 93fedbb；Model Radar 架构 SHA 155e734351c753cd9a51878f9b1549f0d7aaf4db18872c35f8763ff39903db04，提交 7b2c756。均已推送。

  ## 关键决定与原因
  Career 固定“职业方向 → 技术栈”，采用静态证据内容与浏览器内隐私工作台；Model Radar 固定静态人工快照 Web，真实采集、后端、数据库和部署后置。

  ## 文件与命令
  两项目 docs/04-architecture.md 与 workflow/。

  ## 验证
  项目结构、Git 边界、Skill 漂移、YAML/JSONL、Markdown 和 scoped diff 均通过。

  ## 失败与风险
  未接真实来源、后端、数据库或生产部署；视觉实时状态只能视为占位。

  ## 下一步
  用户分别审核两份架构；即使通过也不自动拆任务或开发。

  ## 原设备与更新时间
  设备 A，2026-08-04 17:12（Asia/Shanghai）。

## `ai-workflow-06-frontend-engineer`

logical_task_id: ai-workflow-06-frontend-engineer
entity_state: PRESENT
semantic_state: PRESENT
title: 06 前端工程师
logical_project_id: ai-workflow
local_thread_id: 019fb74a-a427-7101-9941-442c34b157e3
pinned: false
visible_shared_index: 3
semantic_body_sha256: 989e7e6149c1bf04c4540c5add29ebe2e2087515e4946e6b2bfd9283d34f967a
semantic_body: |
  ## 当前目标
  交付获批浏览器前端，同时服从 English 产品冻结。

  ## 已完成
  English 行内字母槽提交 479090f 并通过 QA；reveal-answer 增量冻结保留。Control Center 六个简体中文视图、交互和 design-qa 完成，提交 a35316d，停在 frontend-delivery-review。

  ## 关键决定与原因
  所有项目必须有完整简体中文版，非实时信息标记“演示 / 待接入”。English 新逻辑输入不足，不能越过固定 03/04。

  ## 文件与命令
  English Word.tsx、App.css、verify-inline-cloze.mjs、revealAnswer.ts 与两张截图；Control Center dashboard 代码和 design-qa.md。

  ## 验证
  Control Center lint、build、3/3 测试和六页浏览器巡检通过；根仓 a35316d 与 upstream 0/0。

  ## 失败与风险
  English 有 3 个跟踪修改和 3 个未跟踪文件，共 6 项冻结现场；本轮不得测试、提交或冒充可交付。

  ## 下一步
  English 等 PRD v1.3 与固定 04 Prompt 批准后再恢复；Control Center 等用户审核后才进入固定 09。

  ## 原设备与更新时间
  设备 A，2026-08-04 17:45（Asia/Shanghai）。

## `ai-workflow-07-backend-engineer`

logical_task_id: ai-workflow-07-backend-engineer
entity_state: PRESENT
semantic_state: PRESENT
title: 07 后端工程师
logical_project_id: ai-workflow
local_thread_id: 019fb74a-a6f7-7e31-826f-799d3e713642
pinned: false
visible_shared_index: 11
semantic_body_sha256: dbb73d8cf7049baa35e915c24d2f9dfb73934e55d27e83f75ff4e596f21c0cef
semantic_body: |
  ## 当前目标
  作为固定后端工程师负责 API、业务逻辑、数据访问和认证集成。
  ## 已完成
  角色模板与边界已初始化。
  ## 关键决定与原因
  只处理已批准并由项目流程派发的后端工作。
  ## 文件与命令
  AIWorkFlow 根仓；本轮无后端业务文件。
  ## 验证
  任务实体、标题和项目归属已回读。
  ## 失败与风险
  没有新的已批准后端交付。
  ## 下一步
  等待明确派发。
  ## 原设备与更新时间
  设备 A，语义更新至 2026-08-01。

## `ai-workflow-08-data-engineer`

logical_task_id: ai-workflow-08-data-engineer
entity_state: PRESENT
semantic_state: PRESENT
title: 08 数据工程师
logical_project_id: ai-workflow
local_thread_id: 019fb74a-a99a-7731-9f95-ecaac1e96e99
pinned: false
visible_shared_index: 12
semantic_body_sha256: b8ad2ad1e567f37e29c1b9e36f2877f7193d733ded4b895919f217538302e2d9
semantic_body: |
  ## 当前目标
  作为固定数据工程师负责数据模型、迁移、SQL、缓存和数据管道。
  ## 已完成
  角色模板与边界已初始化。
  ## 关键决定与原因
  不在缺少架构与业务审批时自行变更数据层。
  ## 文件与命令
  AIWorkFlow 根仓；本轮无数据文件。
  ## 验证
  任务实体、标题和项目归属已回读。
  ## 失败与风险
  没有新的已批准数据交付。
  ## 下一步
  等待明确派发。
  ## 原设备与更新时间
  设备 A，语义更新至 2026-08-01。

## `ai-workflow-09-code-reviewer`

logical_task_id: ai-workflow-09-code-reviewer
entity_state: PRESENT
semantic_state: PRESENT
title: 09 代码审查员
logical_project_id: ai-workflow
local_thread_id: 019fb74a-b82f-76c3-ae1c-bef178d2939b
pinned: false
visible_shared_index: 13
semantic_body_sha256: 7c3067df4cb17768acf129b9981183881870da50f571f479378e5467a4272b67
semantic_body: |
  ## 当前目标
  作为固定代码审查员检查质量、缺陷、安全、性能和架构合规。
  ## 已完成
  角色模板与边界已初始化。
  ## 关键决定与原因
  只审查真实差异并按严重级别给出证据，不替代实现者。
  ## 文件与命令
  AIWorkFlow 根仓；本轮无待审查新差异。
  ## 验证
  任务实体、标题和项目归属已回读。
  ## 失败与风险
  当前没有新的审查任务。
  ## 下一步
  等待提交或明确审查请求。
  ## 原设备与更新时间
  设备 A，语义更新至 2026-08-01。

## `ai-workflow-10-test-engineer`

logical_task_id: ai-workflow-10-test-engineer
entity_state: PRESENT
semantic_state: PRESENT
title: 10 测试工程师
logical_project_id: ai-workflow
local_thread_id: 019fb74a-acbb-7442-ae63-5e61246a26f5
pinned: false
visible_shared_index: 14
semantic_body_sha256: 462b6313393f46cc6b93670553857b6d0f4e8cb3e038991a1b59ef51a67072e9
semantic_body: |
  ## 当前目标
  作为固定测试工程师负责测试计划、用例、回归和上线建议。
  ## 已完成
  角色模板与边界已初始化。
  ## 关键决定与原因
  测试依据已批准需求与真实实现，不伪造通过。
  ## 文件与命令
  AIWorkFlow 根仓；本轮无新测试交付。
  ## 验证
  任务实体、标题和项目归属已回读。
  ## 失败与风险
  当前没有新的已批准测试范围。
  ## 下一步
  等待实现和验收标准就绪。
  ## 原设备与更新时间
  设备 A，语义更新至 2026-08-01。

## `ai-workflow-11-devops-engineer`

logical_task_id: ai-workflow-11-devops-engineer
entity_state: PRESENT
semantic_state: PRESENT
title: 11 DevOps工程师
logical_project_id: ai-workflow
local_thread_id: 019fb74a-b067-76d0-8954-20aa6354d5b2
pinned: false
visible_shared_index: 15
semantic_body_sha256: 43b873cc45dbf4bbabd09091d0da09812d28a169c87d767ac1b4286179041102
semantic_body: |
  ## 当前目标
  作为固定 DevOps 工程师负责 CI/CD、部署、环境、监控和回滚。
  ## 已完成
  角色模板与边界已初始化。
  ## 关键决定与原因
  只对已验证版本和明确环境执行部署，不泄露凭据。
  ## 文件与命令
  AIWorkFlow 根仓；本轮无部署文件。
  ## 验证
  任务实体、标题和项目归属已回读。
  ## 失败与风险
  当前没有新的部署授权。
  ## 下一步
  等待明确发布任务。
  ## 原设备与更新时间
  设备 A，语义更新至 2026-08-01。

## `ai-workflow-retired-inline-letter-slots`

logical_task_id: ai-workflow-retired-inline-letter-slots
entity_state: PRESENT
semantic_state: PRESENT
title: AI English Learning｜产品变更：行内字母槽填空
logical_project_id: ai-workflow
local_thread_id: 019fb892-8981-74f0-a396-11a21b018c43
pinned: false
visible_shared_index: 16
semantic_body_sha256: 120a987797e664e55f18547e6c3694d41f2eb603d61a0d7cf808068ae473c99c
semantic_body: |
  ## 当前目标
  只保留 AI English Learning“行内字母槽填空”的历史停用任务语义；本任务不再承担当前产品审核、路由或开发。
  ## 已完成
  历史 PRD v1.1 曾明确移除独立答案框，答案直接输入句中缺词字母槽，对应提交 a1d0444 已推送。当前产品基线已由固定 `03 产品经理` 更新为 PRD v1.3，提交 cb705c4 已推送并停在 `product-change-review`。
  ## 关键决定与原因
  所有当前产品职责只由固定 `03 产品经理` 续接；历史停用镜像不得发起审核决策或把旧 v1.1 路由到 UI，避免与 v1.3 当前审批门分叉。
  ## 文件与命令
  历史与当前文件均在 `projects/ai-english-learning/docs/01-prd.md` 和 `workflow/approvals.yaml`、`artifacts.yaml`、`events.jsonl`、`state.yaml`；当前以固定 03 任务与提交 cb705c4 为准。
  ## 验证
  历史 v1.1 自查和 YAML/JSONL/文档哈希检查已通过。当前 v1.3 包含 D+1/D+3/D+7/D+14、D+30 和 36 条验收标准，已推送并等待固定 03 任务的用户审核。
  ## 失败与风险
  此任务不是第 13 个固定角色；若在这里继续旧 v1.1 审核或下游路由，会与固定 03 的 v1.3 当前状态冲突。
  ## 下一步
  保持可见作为历史镜像，不在本任务采取当前业务动作。PRD v1.3 的“通过 / 修改 / 打回”只在固定 `03 产品经理` 任务处理。
  ## 原设备与更新时间
  原设备 A；历史语义至 2026-08-01，当前路由校正至 2026-08-04。

## `vid-mat-lab-foreman`

logical_task_id: vid-mat-lab-foreman
entity_state: PRESENT
semantic_state: PRESENT
title: 包工头
logical_project_id: vid-mat-lab
local_thread_id: 019fb114-130d-7e50-aacd-f6a26b403b91
pinned: false
visible_shared_index: 2
semantic_body_sha256: e0a2440bff3c304c5e7df3e86eeb38fca0933f4053b0f0c5a909c5c46beaeff3
semantic_body: |
  ## 当前目标
  把 22 秒外耗型草稿制成第 013 集完整生产包，并建立小耗儿创作 Skill。

  ## 已完成
  第 013 集目录、17 张 941×1672 关键帧、17 镜 22 秒分镜、11 条对白加 6 条环境声提示词、口播/SRT/剪辑/声音/发布资料已完成；项目提交 2b199d5 已推送，全局 xiaoneihao-video-creator Skill 已发布。

  ## 关键决定与原因
  所有 clip 必须有声音，同角色固定真实声音资产；内部 VO 编号不得冒充平台 Voice ID。未知“小八/吉伊”改用原创小欧/小伏。

  ## 文件与命令
  episodes/013-return-the-problem/、video-prompts-v1.md、voice-anchor-register-v1.md、全局技能/xiaoneihao-video-creator/。

  ## 验证
  17 镜总长 22.0 秒、17 图可开、SRT 到 22 秒、Skill valid，vid 仓库 2b199d5 与 upstream 0/0。

  ## 失败与风险
  三角色真实干声锚点、17 条动态、剪映工程、BGM/音效和最终成片尚未生成。

  ## 下一步
  先锁定三条 6—10 秒干声锚点，再试 001—003，确认后批量生成与剪辑。

  ## 原设备与更新时间
  设备 A，2026-08-04 17:39（Asia/Shanghai）。

## `vid-mat-lab-foreman-2`

logical_task_id: vid-mat-lab-foreman-2
entity_state: PRESENT
semantic_state: PRESENT
title: 包工头 (2)
logical_project_id: vid-mat-lab
local_thread_id: 019fc25f-c000-78a2-9f5e-c3a953e1ebf9
pinned: false
visible_shared_index: 17
semantic_body_sha256: fbc40ab91387c6c6944630e7e59c7941e4626a169ca6b9b11e8eff79119fc006
semantic_body: |
  ## 当前目标
  承接 vid-mat-lab 的短视频与素材制作；这是 B 端旧 C 盘 worktree 任务，A 镜像必须使用正式项目。
  ## 已完成
  已知历史提交包括 cb82d20、697db9f、6b65ffe；绿发星灵 108×108 眼睛增强拼豆图已推送为 9f773f2，设备 A 已拉取。项目随后完成第 013 集并推送为 2b199d5。
  ## 关键决定与原因
  共同项目只使用正式权威仓库；固定 IP“小内耗”的身体结构、脸型、五官比例、四肢比例和核心标志不得改变。
  ## 文件与命令
  相关目录 episodes/010-photo-to-perler-pattern、episodes/012-dance-off-the-stress；永久底稿 assets/brand/resistor-mascot-identity-master-original.jpg。
  ## 验证
  第 012 集关键帧及配套材料已归档；A 当前 HEAD 与 upstream 均为 2b199d5，工作树干净。
  ## 失败与风险
  不得继续使用旧 C 盘工作树；第 002—004 集曾有未确认内容，不能混入无关提交。
  ## 下一步
  在正式项目等待用户继续；若继续第 012 集，按既定关键帧生成 5 秒舞蹈动态并逐帧检查角色结构。
  ## 原设备与更新时间
  原设备 B；任务级事实至 2026-08-01，项目级补充至 2026-08-04。

## `aidrama-negative-review-reaper`

logical_task_id: aidrama-negative-review-reaper
entity_state: PRESENT
semantic_state: PRESENT
title: 差评死神
logical_project_id: aidrama-project
local_thread_id: 019fb94b-0199-7c32-8a8c-e521082eb33f
pinned: false
visible_shared_index: 18
semantic_body_sha256: 57ef84d8e7726cfbae8a01661f96da9908ee694fbcdfb832ac7c324c163055bc
semantic_body: |
  ## 当前目标
  保留《差评死神》双设备长期任务语义并等待继续。
  ## 已完成
  已导入项目概览和任务记录，没有执行遗留工作。
  ## 关键决定与原因
  不得在 6 集现实悬疑版与 8 集早期赛博版之间自行选择。
  ## 文件与命令
  项目上下文/aidrama/项目概览.md、项目上下文/aidrama/任务记录/差评死神.md。
  ## 验证
  Aidrama main/3baedae Git 与 LFS 完整且 upstream 一致。
  ## 失败与风险
  剧本版本方向仍需用户决定；同仓其他剧目内容不得触碰。
  ## 下一步
  等待用户明确继续和版本方向。
  ## 原设备与更新时间
  设备 A，语义更新至 2026-08-01。

## `aidrama-consultant`

logical_task_id: aidrama-consultant
entity_state: PRESENT
semantic_state: PRESENT
title: 咨询专家
logical_project_id: aidrama-project
local_thread_id: 019fc25f-bcbb-7d80-9249-8c731b4cb3d9
pinned: false
visible_shared_index: 19
semantic_body_sha256: d9003441c690cf8a7dade3e44212a13b9d7a58d0341a0100a8c495cc7d946f56
semantic_body: |
  ## 当前目标
  审阅 AI 漫剧批量生产 PDF，并形成可执行的批量生产方案。
  ## 已完成
  方向已收敛为“稳定单集生产单元 + 3—5 集小批次队列”；用户发送“继续”后尚未形成最终交付。
  ## 关键决定与原因
  先稳定单集生产单元，再以 3—5 集小批次排队；具体取舍原因未进一步保存。
  ## 文件与命令
  被审阅 PDF 的精确文件名、路径及所用命令未记录；项目仓库为 Aidrama。
  ## 验证
  未记录最终交付或验收结果；只能确认上述方向已在 2026-08-01 日报和维护记录中重复登记。
  ## 失败与风险
  最终交付未形成；原线程更细的 PDF 内容、需求和审阅意见未知；不得覆盖同仓其他未确认内容。
  ## 下一步
  等待用户继续；如继续，重新定位原 PDF 和最近审阅产物，基于既定方向完成方案并验收。
  ## 原设备与更新时间
  原设备 B；已知语义更新时间 2026-08-01。

## `aidrama-worker-comeback`

logical_task_id: aidrama-worker-comeback
entity_state: PRESENT
semantic_state: PRESENT
title: 打工人逆袭
logical_project_id: aidrama-project
local_thread_id: 019fc25f-b8a6-7c63-b85e-d8669c517bd2
pinned: false
visible_shared_index: 20
semantic_body_sha256: e5854bb3fcae0af731833126961e1e423f320357b9b27bd40b4137386d71b018
semantic_body: |
  ## 当前目标
  与《打工人逆袭》漫剧相关的原任务目标；除精确标题外，具体需求未记录。
  ## 已完成
  完成内容未知；已知 B 端 Aidrama 工作树曾存在位于 AI漫剧_打工人逆袭爽剧 的既存未提交内容，其他任务明确未触碰。
  ## 关键决定与原因
  必须与《差评死神》等同仓其他漫剧隔离处理，避免跨任务覆盖或提交未经确认的改动。
  ## 文件与命令
  已知目录：AI漫剧_打工人逆袭爽剧；具体文件、命令和提交未知。
  ## 验证
  仅验证到该目录曾有既存未提交内容；正确性、完整性和所有权未验证。
  ## 失败与风险
  原对话语义不足；不可把项目级 Git 状态当作本任务完成。
  ## 下一步
  等待用户继续；先确认目标、已有产物和所有权，再只在本剧目范围内继续。
  ## 原设备与更新时间
  原设备 B；实体和相关工作树事实记录于 2026-08-01，原对话精确更新时间未知。

## `aidrama-ninth-lesson`

logical_task_id: aidrama-ninth-lesson
entity_state: PRESENT
semantic_state: PRESENT
title: 第九节课
logical_project_id: aidrama-project
local_thread_id: 019fc25f-c319-7a90-a39e-ca2f3212ea56
pinned: false
visible_shared_index: 21
semantic_body_sha256: d7b1dd0b931bc6fb34fcc2a313629d56ecb9d1e22b4d7632c6eb49548a53d022
semantic_body: |
  ## 当前目标
  “第九节课”原任务具体目标未知；目前只确认标题、项目归属和 B 端实体。
  ## 已完成
  未知。
  ## 关键决定与原因
  不得依据标题臆测课程内容、剧目、集数或交付形式。
  ## 文件与命令
  未知。
  ## 验证
  未找到独立记录、文件证据、命令或验收结果。
  ## 失败与风险
  语义来源不足；Aidrama 同仓包含多个剧目和未确认内容，错误推断可能串项目。
  ## 下一步
  等待用户继续；届时先确认对应剧目、目标和已有文件，再读取最小必要上下文。
  ## 原设备与更新时间
  原设备 B；实体于 2026-08-01 确认可见，原对话精确更新时间未知。

## `watermark-foreman`

logical_task_id: watermark-foreman
entity_state: PRESENT
semantic_state: PRESENT
title: 包工头
logical_project_id: liquidity-watermark-assistant
local_thread_id: 019fc260-d4b8-7b02-b987-68e81dd3e7c1
pinned: false
visible_shared_index: 22
semantic_body_sha256: 90f91baa29dc8774c307c57db1825b59daa91600e5a81c0e5efe04a4ca5f2e41
semantic_body: |
  ## 当前目标
  统筹去水印前后端项目；原任务具体产品需求和验收标准未保存。
  ## 已完成
  B 形成的后端提交 5ad0017 和前端提交 6a8f6ac 已于 2026-08-02 安全推送；A 当前两仓分别为 5ad0017、6a8f6ac，工作树干净且与 upstream 均为 0/0。
  ## 关键决定与原因
  前后端独立仓维护；已上线提交不再重复提交或推送，后续业务变更仍须按范围验证。
  ## 文件与命令
  仓库 liquidity-watermark-assistant-backend、liquidity-watermark-assistant-frontend；具体业务文件和原命令未知。
  ## 验证
  后端 33 项测试与 Ruff 通过；前端 typecheck 与 build 通过；A 本轮 fetch 后两仓干净、0/0。
  ## 失败与风险
  原任务具体产品语义和独立 UI/API 验收记录仍不完整；这不影响当前 Git 同步已完成的事实。
  ## 下一步
  等待用户新业务需求；B 下次只需 fetch 已上线的两个提交并验证 0/0，不重复推送。
  ## 原设备与更新时间
  原设备 B；项目级同步事实由设备 A 补充至 2026-08-04。

## `watermark-frontend`

logical_task_id: watermark-frontend
entity_state: PRESENT
semantic_state: PRESENT
title: 前端部分
logical_project_id: liquidity-watermark-assistant
local_thread_id: 019fc260-d83a-7b72-abfd-dff7150de37b
pinned: false
visible_shared_index: 23
semantic_body_sha256: b53ec1791f066105a74bf8f5037372aa1d690ea3c1aed2d9118ddc64455fbc99
semantic_body: |
  ## 当前目标
  负责去水印项目前端部分；具体功能需求未保存。
  ## 已完成
  前端提交 6a8f6ac 已推送到远端；A 当前 HEAD 为 6a8f6ac，工作树干净且与 upstream 为 0/0。
  ## 关键决定与原因
  不仅凭提交号推断原功能范围；已上线提交不重做、不重复推送。
  ## 文件与命令
  仓库 liquidity-watermark-assistant-frontend；具体变更文件和命令未知。
  ## 验证
  TypeScript/typecheck 与 build 已通过；A 本轮 fetch 后干净、0/0。
  ## 失败与风险
  原需求、功能流程与 UI 验收记录仍缺失；当前没有 Git 上传缺口。
  ## 下一步
  等待用户新业务需求；B 下次 fetch 6a8f6ac 并验证 0/0，不重复提交。
  ## 原设备与更新时间
  原设备 B；项目级同步事实由设备 A 补充至 2026-08-04。

## `watermark-backend`

logical_task_id: watermark-backend
entity_state: PRESENT
semantic_state: PRESENT
title: 后端部分
logical_project_id: liquidity-watermark-assistant
local_thread_id: 019fc260-e86b-71b1-8c30-7356eca4b441
pinned: false
visible_shared_index: 24
semantic_body_sha256: 2c1532127eee1fc1a0412cae3ead0be33f423b38c9c563634da5774680badbcf
semantic_body: |
  ## 当前目标
  负责去水印项目后端部分；具体接口或业务需求未保存。
  ## 已完成
  后端提交 5ad0017 已推送到远端；A 当前 HEAD 为 5ad0017，工作树干净且与 upstream 为 0/0。
  ## 关键决定与原因
  不仅凭提交号推断原功能范围；已上线提交不重做、不重复推送。
  ## 文件与命令
  仓库 liquidity-watermark-assistant-backend；具体文件和命令未知。
  ## 验证
  33 项测试和 Ruff 已通过；A 本轮 fetch 后干净、0/0。
  ## 失败与风险
  原接口、业务需求与独立验收语义仍缺失；当前没有 Git 上传缺口。
  ## 下一步
  等待用户新业务需求；B 下次 fetch 5ad0017 并验证 0/0，不重复提交。
  ## 原设备与更新时间
  原设备 B；项目级同步事实由设备 A 补充至 2026-08-04。

## `portrait-program-manager`

logical_task_id: portrait-program-manager
entity_state: PRESENT
semantic_state: PRESENT
title: 总包（项目经理）
logical_project_id: liquidity-portrait
local_thread_id: 019fc260-e522-7f72-adb1-852f821458f3
pinned: false
visible_shared_index: 25
semantic_body_sha256: 1d2349e3d38c53260b5adec17cc62bc2d38d7d4ee2cbb7d95333a2e0df71ad14
semantic_body: |
  ## 当前目标
  统筹证件照项目前后端交付；原任务具体范围、计划和验收标准未保存。
  ## 已完成
  后端提交 02560c1 已上线；B 后续将前端审查后提交并推送为 4f1290d。A 本轮已取得两仓，工作树干净且均为 0/0。
  ## 关键决定与原因
  前后端分仓、分验收处理；已上线提交不重复提交。历史风险只作审查背景，不再冒充当前未推送状态。
  ## 文件与命令
  仓库 liquidity-portrait-backend、liquidity-portrait-frontend；具体文件和命令未知。
  ## 验证
  后端 39 项测试通过；前端提交前 typecheck 通过；A 本轮两仓 fetch 后干净、0/0。
  ## 失败与风险
  原总包任务的完整产品范围、浏览器流程和端到端验收记录仍不完整；当前没有 Git 上传缺口。
  ## 下一步
  等待用户新业务需求；B 下次 fetch 02560c1 和 4f1290d 并验证 0/0，不重复推送。
  ## 原设备与更新时间
  原设备 B；项目级同步事实由设备 A 补充至 2026-08-04。

## `portrait-foreman`

logical_task_id: portrait-foreman
entity_state: PRESENT
semantic_state: PRESENT
title: 包工头
logical_project_id: liquidity-portrait
local_thread_id: 019fc260-e20a-7d53-a37f-6039de59dedf
pinned: false
visible_shared_index: 26
semantic_body_sha256: 036eb56fd3c7856e78690939404fe656868796b9958e90268c39d197517c9896
semantic_body: |
  ## 当前目标
  协调证件照项目实施；原任务更具体业务目标未知。
  ## 已完成
  后端 02560c1 和前端 4f1290d 均已推送；A 本轮已取得两仓，工作树干净且均为 0/0。
  ## 关键决定与原因
  前后端分别验收，避免混合不同成熟度改动；历史未提交风险不再作为当前 Git 阻塞。
  ## 文件与命令
  仓库 liquidity-portrait-backend、liquidity-portrait-frontend；具体业务文件和原命令未知。
  ## 验证
  后端 39 项测试通过；前端提交前 typecheck 通过；A 本轮两仓 fetch 后干净、0/0。
  ## 失败与风险
  原任务更具体业务目标和端到端验收未保存；当前没有 Git 上传缺口。
  ## 下一步
  等待用户新业务需求；B 下次 fetch 两个已上线提交并分仓验证 0/0。
  ## 原设备与更新时间
  原设备 B；项目级同步事实由设备 A 补充至 2026-08-04。

## `portrait-frontend`

logical_task_id: portrait-frontend
entity_state: PRESENT
semantic_state: PRESENT
title: 前端部分
logical_project_id: liquidity-portrait
local_thread_id: 019fc260-de73-73a1-b7b8-2d8268c524aa
pinned: false
visible_shared_index: 27
semantic_body_sha256: ad7ec0185f860f985340c5ab1439665fd45204bdbb1e417b6d479495c3e764e6
semantic_body: |
  ## 当前目标
  负责证件照项目前端部分；具体页面或功能需求未知。
  ## 已完成
  B 已在 typecheck 通过后创建并推送前端提交 4f1290d；A 本轮快进至该提交，工作树干净且与 upstream 为 0/0。
  ## 关键决定与原因
  前端与后端分仓验收；历史风险需作后续回归背景，但不再把已上线提交记为“未提交”。
  ## 文件与命令
  仓库 liquidity-portrait-frontend；当前 HEAD 4f1290d；具体原任务文件和命令未完整保存。
  ## 验证
  提交前 typecheck 通过；A 本轮 fetch 后干净、0/0。
  ## 失败与风险
  原业务流程、浏览器回归和产品验收记录仍不完整；当前没有 Git 上传缺口。
  ## 下一步
  等待用户新业务需求；B 下次 fetch 4f1290d 并验证 0/0，如继续业务再补完整流程回归。
  ## 原设备与更新时间
  原设备 B；项目级同步事实由设备 A 补充至 2026-08-04。

## `portrait-backend`

logical_task_id: portrait-backend
entity_state: PRESENT
semantic_state: PRESENT
title: 后端部分
logical_project_id: liquidity-portrait
local_thread_id: 019fc260-db6d-72c2-bfec-f608a1a5587f
pinned: false
visible_shared_index: 28
semantic_body_sha256: 661d93d0a6996eecabffe80849d349893f3be7d8b3747463577d7d4b2b31a82b
semantic_body: |
  ## 当前目标
  负责证件照项目后端部分；具体接口和业务要求未知。
  ## 已完成
  后端提交 02560c1 已推送到远端；A 当前 HEAD 为 02560c1，工作树干净且与 upstream 为 0/0。
  ## 关键决定与原因
  已上线提交不重复提交或推送；后续变更仍需单独审查差异和安全性。
  ## 文件与命令
  仓库 liquidity-portrait-backend；具体文件和命令未知。
  ## 验证
  后端测试 39 passed。
  ## 失败与风险
  原接口和业务验收语义仍不完整；当前没有 Git 上传缺口。
  ## 下一步
  等待用户新业务需求；B 下次 fetch 02560c1 并验证 0/0，不重复提交。
  ## 原设备与更新时间
  原设备 B；项目级同步事实由设备 A 补充至 2026-08-04。

## `bmi-foreman`

logical_task_id: bmi-foreman
entity_state: PRESENT
semantic_state: PRESENT
title: 包工头
logical_project_id: liquidity-bmi
local_thread_id: 019fc261-8649-7912-8ecc-c62a28fbf2ae
pinned: false
visible_shared_index: 29
semantic_body_sha256: b4e1a0242b5eba6afe92038d42755721c966cc0eb3e67465420de7ed3b8a5880
semantic_body: |
  ## 当前目标
  统筹 BMI 前后端项目；原任务具体产品需求和验收标准未知。
  ## 已完成
  后端提交 37ee234 和前端提交 7a0caf6 已安全推送；A 当前两仓分别为 37ee234、7a0caf6，工作树干净且与 upstream 均为 0/0。
  ## 关键决定与原因
  密钥与环境文件不得提交；前后端分仓验收，已上线提交不重复提交或推送。
  ## 文件与命令
  仓库 liquidity-bmi-backend、liquidity-bmi-frontend；具体业务文件和命令未知。
  ## 验证
  后端 14 项测试通过；前端 typecheck 与 build 通过；A 本轮两仓 fetch 后干净、0/0。
  ## 失败与风险
  原任务具体产品语义与端到端验收记录仍不完整；当前没有 Git 上传缺口。
  ## 下一步
  等待用户新业务需求；B 下次 fetch 37ee234 和 7a0caf6 并验证 0/0，不重复推送。
  ## 原设备与更新时间
  原设备 B；项目级同步事实由设备 A 补充至 2026-08-04。

## `bmi-frontend`

logical_task_id: bmi-frontend
entity_state: PRESENT
semantic_state: PRESENT
title: 前端部分
logical_project_id: liquidity-bmi
local_thread_id: 019fc261-8a0e-7913-8246-294d282fd702
pinned: false
visible_shared_index: 30
semantic_body_sha256: e2fa49ab9d0cf5ad4f6a75de77b54d17fd4e11f95c9f4a3054663fed6684ecb0
semantic_body: |
  ## 当前目标
  负责 BMI 项目前端部分；具体页面和业务需求未保存。
  ## 已完成
  前端提交 7a0caf6 已推送到远端；A 当前 HEAD 为 7a0caf6，工作树干净且与 upstream 为 0/0。
  ## 关键决定与原因
  环境文件和密钥不得进入提交；不仅凭提交号推断原功能范围，已上线提交不重复推送。
  ## 文件与命令
  仓库 liquidity-bmi-frontend；具体文件和命令未知。
  ## 验证
  TypeScript/typecheck 与 build 已通过；A 本轮 fetch 后干净、0/0。
  ## 失败与风险
  原功能需求、浏览器流程和 UI 验收记录仍缺失；当前没有 Git 上传缺口。
  ## 下一步
  等待用户新业务需求；B 下次 fetch 7a0caf6 并验证 0/0，不重复提交。
  ## 原设备与更新时间
  原设备 B；项目级同步事实由设备 A 补充至 2026-08-04。

## `bmi-backend`

logical_task_id: bmi-backend
entity_state: PRESENT
semantic_state: PRESENT
title: 后端部分
logical_project_id: liquidity-bmi
local_thread_id: 019fc261-8ce2-7ca2-b0ce-e0415a602468
pinned: false
visible_shared_index: 31
semantic_body_sha256: a6b798059a43083bca21a045b405b16b73628d7d5c0dbebe3c2a2dedb8d1d4f0
semantic_body: |
  ## 当前目标
  负责 BMI 项目后端部分；具体接口和业务需求未保存。
  ## 已完成
  后端提交 37ee234 已推送到远端；A 当前 HEAD 为 37ee234，工作树干净且与 upstream 为 0/0。
  ## 关键决定与原因
  密钥与环境文件不得提交；已上线提交不重复提交或推送，后续变更仍须重跑相称测试。
  ## 文件与命令
  仓库 liquidity-bmi-backend；具体文件和命令未知。
  ## 验证
  14 项后端测试已通过；A 本轮 fetch 后干净、0/0。
  ## 失败与风险
  原接口、业务需求和完整测试覆盖语义仍不足；当前没有 Git 上传缺口。
  ## 下一步
  等待用户新业务需求；B 下次 fetch 37ee234 并验证 0/0，不重复提交。
  ## 原设备与更新时间
  原设备 B；项目级同步事实由设备 A 补充至 2026-08-04。

## `canvas-garment-foreman`

logical_task_id: canvas-garment-foreman
entity_state: PRESENT
semantic_state: PRESENT
title: 包工头
logical_project_id: canvas-garment
local_thread_id: 019fc25f-c6ec-7fb0-9520-f47cba762dd1
pinned: false
visible_shared_index: 32
semantic_body_sha256: d81b0ab365c6d517046e917179d7024ec7d0639f83c4dfb5590d2cdd25614dbc
semantic_body: |
  ## 当前目标
  统筹服装品牌、印花及成衣项目；原任务具体业务需求未保存。
  ## 已完成
  项目级记录显示正式图片、脚本、预览和 XLSX 曾通过检查；A 已克隆并登记，远端基线 main/093d896。
  ## 关键决定与原因
  未确认内容由原业务任务确认后处理；node_modules Junction 和检查缓存必须排除。
  ## 文件与命令
  仓库 canvas-garment；具体业务文件和命令未知。
  ## 验证
  项目级检查覆盖正式图片、脚本、预览和 XLSX；发现约 298 MB node_modules Junction 与缓存；A 当前工作树干净且 0/0。
  ## 失败与风险
  B 端大量本地内容的业务归属与当前状态未知，不能由 A 推断或覆盖。
  ## 下一步
  等待用户继续；先盘点原现场差异、排除依赖缓存、确认交付语义并验证后再提交。
  ## 原设备与更新时间
  原设备 B；实体和项目级状态于 2026-08-01 确认，原对话精确更新时间未知。

## `funhub-space-foreman`

logical_task_id: funhub-space-foreman
entity_state: PRESENT
semantic_state: PRESENT
title: 包工头
logical_project_id: funhub-space
local_thread_id: 019fc261-9036-79b1-890d-3f478fb6b172
pinned: false
visible_shared_index: 33
semantic_body_sha256: 1cf011de0d9b04ffd9c878cc2eb63047b89f49bfa16d04fe09d50f9400daa76c
semantic_body: |
  ## 当前目标
  统筹花果山社区及衍生应用的八个独立 Git 仓库；原任务更具体业务目标未知。
  ## 已完成
  A 可访问的 6 仓均已 fetch 并与 upstream 为 0/0；funhub 两个旧本地提交已以 5111563 上线，funhub-taro 已以 ba8fb21 上线并移除当前代码的前端硬编码凭据。
  ## 关键决定与原因
  八仓独立取得、审查和验证；一个仓库阻塞不覆盖其他仓库。敏感 .env 和历史凭据需先轮换并停止跟踪。
  ## 文件与命令
  八仓包括 aime-bridge-backend、funhub、funhub-CandyArt、funhub-taro、funhub-WordSmiths、funhub-WordSmiths-backend、english-talk-trainer、MountainFruitCottage。
  ## 验证
  A 六个可访问仓库干净且 0/0；funhub 已记录 build，taro 已记录微信小程序构建，WordSmiths 后端本地提交 f562c49 已记录 8 项测试通过。
  ## 失败与风险
  两个来源仍为 Repository not found；B 的 aime 保护 stash 恢复在 `app/services/chat_store.py` 仍有冲突且 stash 保留；WordSmiths 后端 f562c49 因 GitHub 443 失败尚未推送。A 远端版本仍跟踪敏感 `.env` 与运行时会话数据。
  ## 下一步
  修复两个远端来源；B 安全解决 aime 冲突，网络恢复后非强制推送 f562c49；轮换凭据、停止跟踪环境文件和会话数据，然后逐仓验证。
  ## 原设备与更新时间
  原设备 B；项目级同步事实由设备 A 补充至 2026-08-04。

## `funhub-repair-computer`

logical_task_id: funhub-repair-computer
entity_state: PRESENT
semantic_state: PRESENT
title: 修电脑的
logical_project_id: funhub-space
local_thread_id: 019fc261-9a6e-7b12-9fc3-86e8ed7ac364
pinned: false
visible_shared_index: 34
semantic_body_sha256: 442a17d62a1600b150eddc20a05da0c3e5d855ec070233843049efff25c0b322
semantic_body: |
  ## 当前目标
  “修电脑的”原任务具体目标未知；目前只确认标题、项目归属和 B 端实体。
  ## 已完成
  原任务完成内容未知；项目级已知 A 的 6/8 可访问仓均干净、0/0，B 仍有 aime stash 恢复冲突和 WordSmiths 后端 f562c49 未推送。
  ## 关键决定与原因
  不得仅凭标题推断设备、软件、仓库或故障，必须先恢复原需求边界。
  ## 文件与命令
  未知；无法从现有记录唯一映射到某个组成仓库。
  ## 验证
  没有独立测试、命令、文件或验收记录。
  ## 失败与风险
  语义不足；两个来源不可达，B 还有一处冲突和一个未推送提交，并存在凭据风险。错误映射可能触碰错误现场。
  ## 下一步
  等待用户继续；先确认具体故障、目标仓库和期望结果，再读取最小必要现场。
  ## 原设备与更新时间
  原设备 B；原对话语义仍未知，项目级同步事实由设备 A 补充至 2026-08-04。

## `funhub-press-to-talk-fix`

logical_task_id: funhub-press-to-talk-fix
entity_state: PRESENT
semantic_state: PRESENT
title: 修复按住说话误弹窗
logical_project_id: funhub-space
local_thread_id: 019fc261-9310-7ed0-9b27-e6be5f48ed56
pinned: false
visible_shared_index: 35
semantic_body_sha256: 0c1eac362ffe2ad6119de09b0149d403e52db78a53c39297c2c655f046fd97ed
semantic_body: |
  ## 当前目标
  按标题修复“按住说话”交互触发误弹窗；触发条件、平台、目标仓库和验收标准未保存。
  ## 已完成
  原缺陷是否修复仍未知；项目级已知 A 的 6/8 可访问仓均干净、0/0，但没有提交可唯一归属到本任务。
  ## 关键决定与原因
  只能把标题视为已知需求，不臆测弹窗类型、根因或实现位置；应先复现。
  ## 文件与命令
  未知；不能唯一映射到 funhub、funhub-taro 或其他仓库。
  ## 验证
  未记录复现步骤、自动化测试、设备验证或验收结果。
  ## 失败与风险
  语义不足且项目有多仓、两个不可达来源、B 保留冲突与未推送提交，并有敏感配置风险。
  ## 下一步
  等待用户继续；确认客户端、表现和复现步骤，定位正确仓库，补回归用例后修复验证。
  ## 原设备与更新时间
  原设备 B；原对话语义仍未知，项目级同步事实由设备 A 补充至 2026-08-04。

## `funhub-aime-frontend`

logical_task_id: funhub-aime-frontend
entity_state: PRESENT
semantic_state: PRESENT
title: 开发极简聊天界面
logical_project_id: funhub-space
local_thread_id: 019fc261-96f2-7aa1-bdbf-cb0acdb31162
pinned: false
visible_shared_index: 36
semantic_body_sha256: b599610771feeac7c9670a7ef59b006289d35b38260ac30bcae784390ddb7fea
semantic_body: |
  ## 当前目标
  按标题开发极简聊天界面；页面范围、设计稿、技术栈、接口和验收标准未保存。
  ## 已完成
  原界面完成情况未知；项目级已知 A 的 6/8 可访问仓均干净、0/0，funhub-taro 已上线 ba8fb21，但无证据将该提交归属到本任务。
  ## 关键决定与原因
  不得仅凭项目级状态推断界面已实现，也不得在未确认接口和目标仓库前编码。
  ## 文件与命令
  未知；不能唯一确定对应 funhub、funhub-taro、funhub-WordSmiths 或其他前端仓库。
  ## 验证
  未记录 UI、TypeScript、构建、浏览器或真机验收。
  ## 失败与风险
  原需求不足，多前端仓库并存；两个来源不可达，B 仍有与其他仓相关的冲突和未推送提交。
  ## 下一步
  等待用户继续；确认目标端、仓库、界面范围、设计与 API 契约，再盘点代码实施验证。
  ## 原设备与更新时间
  原设备 B；原对话语义仍未知，项目级同步事实由设备 A 补充至 2026-08-04。

## `funhub-aime-backend`

logical_task_id: funhub-aime-backend
entity_state: PRESENT
semantic_state: PRESENT
title: 对齐 FunHub AI 服务
logical_project_id: funhub-space
local_thread_id: 019fc261-9e07-7ec0-b9b5-b4dbb646ce3e
pinned: false
visible_shared_index: 37
semantic_body_sha256: d255c5ff0305eb7594f96a7dec14826f53a8bc483037413630db1303a3158139
semantic_body: |
  ## 当前目标
  按标题对齐 FunHub AI 服务；具体协议、接口差异和验收标准未保存；可能相关仓库为 aime-bridge-backend，但未明确绑定。
  ## 已完成
  A 端 aime-bridge-backend 为 703f0c1，工作树干净且与 upstream 为 0/0。B 对本地改动做保护 stash 后已取得远端，但恢复时 `app/services/chat_store.py` 产生冲突，stash 仍保留。
  ## 关键决定与原因
  B 冲突现场必须保留 stash 并人工审查后解决，不强行覆盖；敏感 `.env` 不得提交或复述。
  ## 文件与命令
  候选仓库 aime-bridge-backend；具体文件、接口和命令未知。
  ## 验证
  项目级曾记录 31 项测试通过；A 本轮远端状态干净、0/0，但这不直接证明原任务已完成。
  ## 失败与风险
  B 当前有保护 stash 恢复冲突，不能由 A 远端干净状态代替解决。`.env` 仍被远端跟踪，当前敏感字段为空但历史曾有非空值，须轮换并停止跟踪。
  ## 下一步
  先确认原任务目标 API；B 保留 stash 后解决 `chat_store.py` 冲突、审查和复测，再轮换凭据并停止跟踪环境文件。
  ## 原设备与更新时间
  原设备 B；B 现场事实至 2026-08-03，A 远端复核至 2026-08-04。

## `lottery-foreman`

logical_task_id: lottery-foreman
entity_state: PRESENT
semantic_state: PRESENT
title: 包工头
logical_project_id: lottery
local_thread_id: 019f4af1-d1fd-78a3-a1e2-77f1ffdf1536
pinned: false
visible_shared_index: 38
semantic_body_sha256: 91c0d85de531d0565bdc88fefe49b6a589b03b9ea873c01f5e66205b9d8e4089
semantic_body: |
  ## 当前目标
  统筹彩票前后端项目并保持算法与界面可续接。
  ## 已完成
  历史已把候选算法改为合法组合空间等概率抽样并完成前端视觉升级。
  ## 关键决定与原因
  前后端独立仓库管理；不得把概率等价性与玄学解释混淆。
  ## 文件与命令
  lottery-calculation-backend、lottery-calculation-frontend。
  ## 验证
  后端 e2675e5、前端 ea3f326，均 clean、0/0。
  ## 失败与风险
  当前没有新待办或未推送内容；原线程路径为旧路径但实体仍保留。
  ## 下一步
  等待用户继续业务需求。
  ## 原设备与更新时间
  设备 A，语义更新至 2026-08-01。

## `demo-foreman`

logical_task_id: demo-foreman
entity_state: MISSING
semantic_state: MISSING
title: 包工头
logical_project_id: demo
local_thread_id: MISSING
pinned: MISSING
visible_shared_index: MISSING
semantic_body_sha256: MISSING
semantic_body: MISSING
