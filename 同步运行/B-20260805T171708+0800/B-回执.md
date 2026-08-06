# 设备 B 回执

- 运行 ID：`B-20260805T171708+0800`
- 设备：B
- 交接包协议版本：`1`
- 目标修订：`1`
- merged_package_file_sha256：`4f11185555411aa3f1cd2674f9da372dd069929ccc7cbe02782d1cf444c0601c`
- target_layout_version：`3`
- target_layout_sha256：`5310e24b57cfc72e401f56e2e6d775351fa701fd8fb0d1f451b62ca92cb5d81e`
- applied_layout_version：`3`（部分应用）
- applied_layout_sha256：`5310e24b57cfc72e401f56e2e6d775351fa701fd8fb0d1f451b62ca92cb5d81e`
- 回执时间：2026-08-06（Asia/Shanghai）
- 回执结论：39 个任务实体、标题、项目归属、非置顶状态和同版语义 SHA 已回读；共享任务顺序与项目布局未通过，Git 仍有冲突、脏现场、无 upstream 和网络不可达，故为部分回执。

expected_projects_pinned: mission-context,ai-workflow,vid-mat-lab
actual_projects_pinned: UNKNOWN
projects_pinned_verified: unknown
expected_projects_unpinned: aidrama-project,liquidity-watermark-assistant,liquidity-portrait,liquidity-bmi,canvas-garment,funhub-space,lottery,demo
actual_projects_unpinned: mission-context,ai-workflow,vid-mat-lab,aidrama-project,liquidity-watermark-assistant,liquidity-portrait,liquidity-bmi,demo,canvas-garment,funhub-space,lottery
projects_unpinned_verified: false
project_layout_verified: unknown

- expected_tasks_unpinned：mission-context-current-sync,mission-context-maintenance,ai-workflow-00-foreman,ai-workflow-01-market-researcher,ai-workflow-02-project-manager,ai-workflow-03-product-manager,ai-workflow-04-ui-ux-designer,ai-workflow-05-architect,ai-workflow-06-frontend-engineer,ai-workflow-07-backend-engineer,ai-workflow-08-data-engineer,ai-workflow-09-code-reviewer,ai-workflow-10-test-engineer,ai-workflow-11-devops-engineer,ai-workflow-retired-inline-letter-slots,vid-mat-lab-foreman,vid-mat-lab-foreman-2,aidrama-negative-review-reaper,aidrama-consultant,aidrama-worker-comeback,aidrama-ninth-lesson,watermark-foreman,watermark-frontend,watermark-backend,portrait-program-manager,portrait-foreman,portrait-frontend,portrait-backend,bmi-foreman,bmi-frontend,bmi-backend,canvas-garment-foreman,funhub-space-foreman,funhub-repair-computer,funhub-press-to-talk-fix,funhub-aime-frontend,funhub-aime-backend,lottery-foreman,demo-foreman
- actual_tasks_unpinned：vid-mat-lab-foreman-2,mission-context-current-sync,demo-foreman,lottery-foreman,funhub-aime-backend,funhub-aime-frontend,funhub-press-to-talk-fix,funhub-repair-computer,funhub-space-foreman,canvas-garment-foreman,bmi-backend,bmi-frontend,bmi-foreman,portrait-backend,portrait-frontend,portrait-foreman,portrait-program-manager,watermark-backend,watermark-frontend,watermark-foreman,aidrama-ninth-lesson,aidrama-worker-comeback,aidrama-consultant,aidrama-negative-review-reaper,vid-mat-lab-foreman,ai-workflow-retired-inline-letter-slots,ai-workflow-11-devops-engineer,ai-workflow-10-test-engineer,ai-workflow-09-code-reviewer,ai-workflow-08-data-engineer,ai-workflow-07-backend-engineer,ai-workflow-06-frontend-engineer,ai-workflow-05-architect,ai-workflow-04-ui-ux-designer,ai-workflow-03-product-manager,ai-workflow-02-project-manager,ai-workflow-01-market-researcher,ai-workflow-00-foreman,mission-context-maintenance
- task_layout_verified：false
- 任务正文验收：39/39；正式回读均找到本运行的 `[SYNC-CONTEXT v1]`、逻辑 ID、预期 SHA 与完整正文。

## `mission-context-current-sync`

logical_task_id: mission-context-current-sync
project_id: ef30d636-e54c-41df-8958-6e66834ca7d5
thread_id: 019fa8cf-205c-7c71-8350-e78edd3b712c
expected_title: 开始
actual_title: 开始
title_verified: true
expected_project_id: ef30d636-e54c-41df-8958-6e66834ca7d5
actual_project_id: ef30d636-e54c-41df-8958-6e66834ca7d5
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 2
shared_index_verified: false
expected_body_sha256: b1993e241cbb729e31d4daca7fc28b494a0155b949defba6b0b7a2c98abe98c6
actual_body_sha256: b1993e241cbb729e31d4daca7fc28b494a0155b949defba6b0b7a2c98abe98c6
body_sha256_verified: true

## `mission-context-maintenance`

logical_task_id: mission-context-maintenance
project_id: ef30d636-e54c-41df-8958-6e66834ca7d5
thread_id: 019fa8d5-32b4-7670-816e-b0dc862ee35c
expected_title: 双设备同步维护
actual_title: 双设备同步维护
title_verified: true
expected_project_id: ef30d636-e54c-41df-8958-6e66834ca7d5
actual_project_id: ef30d636-e54c-41df-8958-6e66834ca7d5
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 39
shared_index_verified: false
expected_body_sha256: b3abb2c4b91ec0a27bb363d39fc4a08e3f08930bfa34130344087f966443f755
actual_body_sha256: b3abb2c4b91ec0a27bb363d39fc4a08e3f08930bfa34130344087f966443f755
body_sha256_verified: true

## `ai-workflow-00-foreman`

logical_task_id: ai-workflow-00-foreman
project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
thread_id: 019fc330-2ae2-7eb2-a36f-51caf1fb5aaf
expected_title: 00 包工头
actual_title: 00 包工头
title_verified: true
expected_project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
actual_project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 38
shared_index_verified: false
expected_body_sha256: f0f0625a272e62ecbb93cb6f5fc41c72d783def0086a5b5b412945f2ab687579
actual_body_sha256: f0f0625a272e62ecbb93cb6f5fc41c72d783def0086a5b5b412945f2ab687579
body_sha256_verified: true

## `ai-workflow-01-market-researcher`

logical_task_id: ai-workflow-01-market-researcher
project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
thread_id: 019fc330-3222-74c0-984d-e1fe0fb86edd
expected_title: 01 市场调研员
actual_title: 01 市场调研员
title_verified: true
expected_project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
actual_project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 37
shared_index_verified: false
expected_body_sha256: ceed2af00336d6a035c338cc1bca885594a2401ad3761ed5ebafcb075c5287de
actual_body_sha256: ceed2af00336d6a035c338cc1bca885594a2401ad3761ed5ebafcb075c5287de
body_sha256_verified: true

## `ai-workflow-02-project-manager`

logical_task_id: ai-workflow-02-project-manager
project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
thread_id: 019fc330-3e7c-7f03-b37d-f075efa57c44
expected_title: 02 项目经理
actual_title: 02 项目经理
title_verified: true
expected_project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
actual_project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 36
shared_index_verified: false
expected_body_sha256: d64bcdf6e79027ccfe2ba5a2f60eb9348a5898a7e1b49cb8075b07ecb9ffb86a
actual_body_sha256: d64bcdf6e79027ccfe2ba5a2f60eb9348a5898a7e1b49cb8075b07ecb9ffb86a
body_sha256_verified: true

## `ai-workflow-03-product-manager`

logical_task_id: ai-workflow-03-product-manager
project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
thread_id: 019fc330-4c83-7aa3-9133-237254a5dd6d
expected_title: 03 产品经理
actual_title: 03 产品经理
title_verified: true
expected_project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
actual_project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 35
shared_index_verified: false
expected_body_sha256: f142311f399598a66ee66c36f56fc160582e7f9eb34e6782d08302e5c1c87847
actual_body_sha256: f142311f399598a66ee66c36f56fc160582e7f9eb34e6782d08302e5c1c87847
body_sha256_verified: true

## `ai-workflow-04-ui-ux-designer`

logical_task_id: ai-workflow-04-ui-ux-designer
project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
thread_id: 019fc330-5c23-7c20-9502-ab93a6945257
expected_title: 04 UI/UX设计师
actual_title: 04 UI/UX设计师
title_verified: true
expected_project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
actual_project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 34
shared_index_verified: false
expected_body_sha256: 6fc1da75bbfcc68495a071b444e4e7e49489f55d89c63e04332d95e5118e1c9a
actual_body_sha256: 6fc1da75bbfcc68495a071b444e4e7e49489f55d89c63e04332d95e5118e1c9a
body_sha256_verified: true

## `ai-workflow-05-architect`

logical_task_id: ai-workflow-05-architect
project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
thread_id: 019fc330-6c68-7920-ad1b-07ea30bdd399
expected_title: 05 架构师
actual_title: 05 架构师
title_verified: true
expected_project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
actual_project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 33
shared_index_verified: false
expected_body_sha256: 150ee5e9bcd8f8477f6cae2abff98f3aabb423eebf67ce309e17f1a54bef94bc
actual_body_sha256: 150ee5e9bcd8f8477f6cae2abff98f3aabb423eebf67ce309e17f1a54bef94bc
body_sha256_verified: true

## `ai-workflow-06-frontend-engineer`

logical_task_id: ai-workflow-06-frontend-engineer
project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
thread_id: 019fc330-7bc3-75b1-a302-0e30fa80e228
expected_title: 06 前端工程师
actual_title: 06 前端工程师
title_verified: true
expected_project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
actual_project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 32
shared_index_verified: false
expected_body_sha256: 819ac89d7c266bcf2820e2ff6d83c5ecbdacc7b1ab3910965a0f36786d53a3d4
actual_body_sha256: 819ac89d7c266bcf2820e2ff6d83c5ecbdacc7b1ab3910965a0f36786d53a3d4
body_sha256_verified: true

## `ai-workflow-07-backend-engineer`

logical_task_id: ai-workflow-07-backend-engineer
project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
thread_id: 019fc330-8a0d-7541-b1a5-cba59193a63b
expected_title: 07 后端工程师
actual_title: 07 后端工程师
title_verified: true
expected_project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
actual_project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 31
shared_index_verified: false
expected_body_sha256: 90f95d300c854761db494382a9492bb6bb5ec0a76887f99a470fafe26bcb6c8e
actual_body_sha256: 90f95d300c854761db494382a9492bb6bb5ec0a76887f99a470fafe26bcb6c8e
body_sha256_verified: true

## `ai-workflow-08-data-engineer`

logical_task_id: ai-workflow-08-data-engineer
project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
thread_id: 019fc330-9979-7392-8400-09561715be8e
expected_title: 08 数据工程师
actual_title: 08 数据工程师
title_verified: true
expected_project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
actual_project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 30
shared_index_verified: false
expected_body_sha256: b2b60708a01adf2f2d7de1d860ea1990cb1d0aa588da1b40e48c7eac11940fc8
actual_body_sha256: b2b60708a01adf2f2d7de1d860ea1990cb1d0aa588da1b40e48c7eac11940fc8
body_sha256_verified: true

## `ai-workflow-09-code-reviewer`

logical_task_id: ai-workflow-09-code-reviewer
project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
thread_id: 019fc330-a713-7f90-9f36-6d74a4dbe941
expected_title: 09 代码审查员
actual_title: 09 代码审查员
title_verified: true
expected_project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
actual_project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 29
shared_index_verified: false
expected_body_sha256: 7af2900a4a184f03673d172c42e62ccc909828db37ff9409f9f4bc477b7938f0
actual_body_sha256: 7af2900a4a184f03673d172c42e62ccc909828db37ff9409f9f4bc477b7938f0
body_sha256_verified: true

## `ai-workflow-10-test-engineer`

logical_task_id: ai-workflow-10-test-engineer
project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
thread_id: 019fc330-b74d-75e0-8d97-cddc5690427a
expected_title: 10 测试工程师
actual_title: 10 测试工程师
title_verified: true
expected_project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
actual_project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 28
shared_index_verified: false
expected_body_sha256: 3fcd7aaed4f35f91e95ff107e8bb7a21c99752e69906ae62095d3e431b08aa0b
actual_body_sha256: 3fcd7aaed4f35f91e95ff107e8bb7a21c99752e69906ae62095d3e431b08aa0b
body_sha256_verified: true

## `ai-workflow-11-devops-engineer`

logical_task_id: ai-workflow-11-devops-engineer
project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
thread_id: 019fc330-c74d-72f3-93bd-a52194903e2d
expected_title: 11 DevOps工程师
actual_title: 11 DevOps工程师
title_verified: true
expected_project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
actual_project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 27
shared_index_verified: false
expected_body_sha256: 8d5b5ca191a40b051f7289c0e228ad2fc1c220e832c0ce5c663f9a2427e075cf
actual_body_sha256: 8d5b5ca191a40b051f7289c0e228ad2fc1c220e832c0ce5c663f9a2427e075cf
body_sha256_verified: true

## `ai-workflow-retired-inline-letter-slots`

logical_task_id: ai-workflow-retired-inline-letter-slots
project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
thread_id: 019fc330-d8a9-73e3-88b2-8c96fcaf065b
expected_title: AI English Learning｜产品变更：行内字母槽填空
actual_title: AI English Learning｜产品变更：行内字母槽填空
title_verified: true
expected_project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
actual_project_id: e7d65417-ea9a-47b3-8e2f-87da309b8406
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 26
shared_index_verified: false
expected_body_sha256: 6e2be3a67fe214c9f3ebe90d14c76417315af88a8270def348535669cadd8a26
actual_body_sha256: 6e2be3a67fe214c9f3ebe90d14c76417315af88a8270def348535669cadd8a26
body_sha256_verified: true

## `vid-mat-lab-foreman`

logical_task_id: vid-mat-lab-foreman
project_id: local-d048fcddd193ac828b23b524d4434940
thread_id: 019f596c-f12d-7702-9b7e-85d4b536b514
expected_title: 包工头
actual_title: 包工头
title_verified: true
expected_project_id: local-d048fcddd193ac828b23b524d4434940
actual_project_id: local-d048fcddd193ac828b23b524d4434940
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 25
shared_index_verified: false
expected_body_sha256: 7ed9a6441fe8bdc1bb72f615a3cc60338a7fd8da7743ffa950dc4dfe2c3f82ee
actual_body_sha256: 7ed9a6441fe8bdc1bb72f615a3cc60338a7fd8da7743ffa950dc4dfe2c3f82ee
body_sha256_verified: true

## `vid-mat-lab-foreman-2`

logical_task_id: vid-mat-lab-foreman-2
project_id: local-d048fcddd193ac828b23b524d4434940
thread_id: 019fc2a5-a242-7401-a3e5-dcacecc55016
expected_title: 包工头 (2)
actual_title: 包工头 (2)
title_verified: true
expected_project_id: local-d048fcddd193ac828b23b524d4434940
actual_project_id: local-d048fcddd193ac828b23b524d4434940
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 1
shared_index_verified: false
expected_body_sha256: 324eafb6e3972410ee1722331528d18787efb5d3e6e80ed8e1a25d3fd6f423aa
actual_body_sha256: 324eafb6e3972410ee1722331528d18787efb5d3e6e80ed8e1a25d3fd6f423aa
body_sha256_verified: true

## `aidrama-negative-review-reaper`

logical_task_id: aidrama-negative-review-reaper
project_id: 098b2f95-b291-4a54-a4dc-943f6b3e0de4
thread_id: 019fb5b8-e8fd-7380-bc6f-ee5a7e6055f0
expected_title: 差评死神
actual_title: 差评死神
title_verified: true
expected_project_id: 098b2f95-b291-4a54-a4dc-943f6b3e0de4
actual_project_id: 098b2f95-b291-4a54-a4dc-943f6b3e0de4
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 24
shared_index_verified: false
expected_body_sha256: 41298a96fa228d18d531411557c2cfc35adf1c1f72be9ce7174506aff8315b25
actual_body_sha256: 41298a96fa228d18d531411557c2cfc35adf1c1f72be9ce7174506aff8315b25
body_sha256_verified: true

## `aidrama-consultant`

logical_task_id: aidrama-consultant
project_id: 098b2f95-b291-4a54-a4dc-943f6b3e0de4
thread_id: 019f9ed0-bc3f-7bb1-a687-57ed6e802c60
expected_title: 咨询专家
actual_title: 咨询专家
title_verified: true
expected_project_id: 098b2f95-b291-4a54-a4dc-943f6b3e0de4
actual_project_id: 098b2f95-b291-4a54-a4dc-943f6b3e0de4
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 23
shared_index_verified: false
expected_body_sha256: ae17f580b0f7d303721438754f28b877ee855b5bef28b345c1bffadbf820146a
actual_body_sha256: ae17f580b0f7d303721438754f28b877ee855b5bef28b345c1bffadbf820146a
body_sha256_verified: true

## `aidrama-worker-comeback`

logical_task_id: aidrama-worker-comeback
project_id: 098b2f95-b291-4a54-a4dc-943f6b3e0de4
thread_id: 019f97f2-349a-7243-9b31-35ecd4982890
expected_title: 打工人逆袭
actual_title: 打工人逆袭
title_verified: true
expected_project_id: 098b2f95-b291-4a54-a4dc-943f6b3e0de4
actual_project_id: 098b2f95-b291-4a54-a4dc-943f6b3e0de4
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 22
shared_index_verified: false
expected_body_sha256: dbb8fb6e326bb05350813126897509f2d4fac0f7712e558d3f522b58d01cc4c2
actual_body_sha256: dbb8fb6e326bb05350813126897509f2d4fac0f7712e558d3f522b58d01cc4c2
body_sha256_verified: true

## `aidrama-ninth-lesson`

logical_task_id: aidrama-ninth-lesson
project_id: 098b2f95-b291-4a54-a4dc-943f6b3e0de4
thread_id: 019f97d8-fbe7-7312-8358-9a0047abba7a
expected_title: 第九节课
actual_title: 第九节课
title_verified: true
expected_project_id: 098b2f95-b291-4a54-a4dc-943f6b3e0de4
actual_project_id: 098b2f95-b291-4a54-a4dc-943f6b3e0de4
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 21
shared_index_verified: false
expected_body_sha256: 17b5fa70ba1edb267a6071f2b666eeccd4546e411e7dcfea359a64a7883581e4
actual_body_sha256: 17b5fa70ba1edb267a6071f2b666eeccd4546e411e7dcfea359a64a7883581e4
body_sha256_verified: true

## `watermark-foreman`

logical_task_id: watermark-foreman
project_id: local-d4627f88c2af08ced6276dcfcd552616
thread_id: 019f1c3c-e9f2-7981-9e63-27982e981323
expected_title: 包工头
actual_title: 包工头
title_verified: true
expected_project_id: local-d4627f88c2af08ced6276dcfcd552616
actual_project_id: local-d4627f88c2af08ced6276dcfcd552616
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 20
shared_index_verified: false
expected_body_sha256: 57f9362f0696788d51ea526b03b77f43506f2d38d1fc296c8be2ec5f8aaaf948
actual_body_sha256: 57f9362f0696788d51ea526b03b77f43506f2d38d1fc296c8be2ec5f8aaaf948
body_sha256_verified: true

## `watermark-frontend`

logical_task_id: watermark-frontend
project_id: local-d4627f88c2af08ced6276dcfcd552616
thread_id: 019f1be7-31c0-7863-92e0-45e07b1337a8
expected_title: 前端部分
actual_title: 前端部分
title_verified: true
expected_project_id: local-d4627f88c2af08ced6276dcfcd552616
actual_project_id: local-d4627f88c2af08ced6276dcfcd552616
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 19
shared_index_verified: false
expected_body_sha256: 424b7d96359728d4fc3ee47631189c9317722e61123ea50cb0b94a8575f7810c
actual_body_sha256: 424b7d96359728d4fc3ee47631189c9317722e61123ea50cb0b94a8575f7810c
body_sha256_verified: true

## `watermark-backend`

logical_task_id: watermark-backend
project_id: local-d4627f88c2af08ced6276dcfcd552616
thread_id: 019f1bea-5f1d-7040-a656-484733ca3fe7
expected_title: 后端部分
actual_title: 后端部分
title_verified: true
expected_project_id: local-d4627f88c2af08ced6276dcfcd552616
actual_project_id: local-d4627f88c2af08ced6276dcfcd552616
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 18
shared_index_verified: false
expected_body_sha256: 547c5549f61c1ababb946ed70156599fde5cf154bdd78a348a95c1f003d47b53
actual_body_sha256: 547c5549f61c1ababb946ed70156599fde5cf154bdd78a348a95c1f003d47b53
body_sha256_verified: true

## `portrait-program-manager`

logical_task_id: portrait-program-manager
project_id: local-238c34aaf0e8d91bc25db82a4ea4cba7
thread_id: 019f4a2d-1ca0-74e2-92a3-6b996bdbbbcf
expected_title: 总包（项目经理）
actual_title: 总包（项目经理）
title_verified: true
expected_project_id: local-238c34aaf0e8d91bc25db82a4ea4cba7
actual_project_id: local-238c34aaf0e8d91bc25db82a4ea4cba7
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 17
shared_index_verified: false
expected_body_sha256: 112e3739c35f3bd6701003ccaf5ed44ebdbf085e3b99c04b6033756e63703013
actual_body_sha256: 112e3739c35f3bd6701003ccaf5ed44ebdbf085e3b99c04b6033756e63703013
body_sha256_verified: true

## `portrait-foreman`

logical_task_id: portrait-foreman
project_id: local-238c34aaf0e8d91bc25db82a4ea4cba7
thread_id: 019f1cce-d8ed-7b20-83cf-0617527307d3
expected_title: 包工头
actual_title: 包工头
title_verified: true
expected_project_id: local-238c34aaf0e8d91bc25db82a4ea4cba7
actual_project_id: local-238c34aaf0e8d91bc25db82a4ea4cba7
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 16
shared_index_verified: false
expected_body_sha256: e6d7a0d54004e669082f499f536922c23366a34684d0fd27f96f153b30fbb911
actual_body_sha256: e6d7a0d54004e669082f499f536922c23366a34684d0fd27f96f153b30fbb911
body_sha256_verified: true

## `portrait-frontend`

logical_task_id: portrait-frontend
project_id: local-238c34aaf0e8d91bc25db82a4ea4cba7
thread_id: 019f1ccb-6552-7983-9719-ddd86e4435a1
expected_title: 前端部分
actual_title: 前端部分
title_verified: true
expected_project_id: local-238c34aaf0e8d91bc25db82a4ea4cba7
actual_project_id: local-238c34aaf0e8d91bc25db82a4ea4cba7
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 15
shared_index_verified: false
expected_body_sha256: 689695044b7912cb8b7e6fe5277ebb6a10849f131e833ea73cc37049ebcd7252
actual_body_sha256: 689695044b7912cb8b7e6fe5277ebb6a10849f131e833ea73cc37049ebcd7252
body_sha256_verified: true

## `portrait-backend`

logical_task_id: portrait-backend
project_id: local-238c34aaf0e8d91bc25db82a4ea4cba7
thread_id: 019f1ccf-0207-7c02-8ba7-883fc2d9fea7
expected_title: 后端部分
actual_title: 后端部分
title_verified: true
expected_project_id: local-238c34aaf0e8d91bc25db82a4ea4cba7
actual_project_id: local-238c34aaf0e8d91bc25db82a4ea4cba7
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 14
shared_index_verified: false
expected_body_sha256: 9a90966541559df08c827f47313149b496c9dbd191897cd971fee216f1c5cf16
actual_body_sha256: 9a90966541559df08c827f47313149b496c9dbd191897cd971fee216f1c5cf16
body_sha256_verified: true

## `bmi-foreman`

logical_task_id: bmi-foreman
project_id: local-7eb1bd946cc1aa79f873e8566b9dd627
thread_id: 019f2c80-b9f6-7181-acdc-69e1a95fde36
expected_title: 包工头
actual_title: 包工头
title_verified: true
expected_project_id: local-7eb1bd946cc1aa79f873e8566b9dd627
actual_project_id: local-7eb1bd946cc1aa79f873e8566b9dd627
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 13
shared_index_verified: false
expected_body_sha256: c68418319feb898864a6638f054ef058c0509438ced324b0f780c5de17f31092
actual_body_sha256: c68418319feb898864a6638f054ef058c0509438ced324b0f780c5de17f31092
body_sha256_verified: true

## `bmi-frontend`

logical_task_id: bmi-frontend
project_id: local-7eb1bd946cc1aa79f873e8566b9dd627
thread_id: 019f423e-85a0-7662-8e59-4323e8212f7b
expected_title: 前端部分
actual_title: 前端部分
title_verified: true
expected_project_id: local-7eb1bd946cc1aa79f873e8566b9dd627
actual_project_id: local-7eb1bd946cc1aa79f873e8566b9dd627
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 12
shared_index_verified: false
expected_body_sha256: 8f64a84091bfe5bffe28a269791b458b4bd5e377225acf8bfe5bd657a12036c4
actual_body_sha256: 8f64a84091bfe5bffe28a269791b458b4bd5e377225acf8bfe5bd657a12036c4
body_sha256_verified: true

## `bmi-backend`

logical_task_id: bmi-backend
project_id: local-7eb1bd946cc1aa79f873e8566b9dd627
thread_id: 019f423e-b33c-7b30-b389-4f4187354350
expected_title: 后端部分
actual_title: 后端部分
title_verified: true
expected_project_id: local-7eb1bd946cc1aa79f873e8566b9dd627
actual_project_id: local-7eb1bd946cc1aa79f873e8566b9dd627
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 11
shared_index_verified: false
expected_body_sha256: fbe6030a1da9d59685977c855070c47af0695eaf685ae662092ac3a4292e200c
actual_body_sha256: fbe6030a1da9d59685977c855070c47af0695eaf685ae662092ac3a4292e200c
body_sha256_verified: true

## `canvas-garment-foreman`

logical_task_id: canvas-garment-foreman
project_id: local-5e4aef3ccc2d50379cefaca5e397ebef
thread_id: 019f5034-234e-77e3-a2b8-c6a76b72e414
expected_title: 包工头
actual_title: 包工头
title_verified: true
expected_project_id: local-5e4aef3ccc2d50379cefaca5e397ebef
actual_project_id: local-5e4aef3ccc2d50379cefaca5e397ebef
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 10
shared_index_verified: false
expected_body_sha256: 5fb611fb7a230222d4092c7edf32930d54fcbee25c0e0fa3b4e21d0ee755ffa2
actual_body_sha256: 5fb611fb7a230222d4092c7edf32930d54fcbee25c0e0fa3b4e21d0ee755ffa2
body_sha256_verified: true

## `funhub-space-foreman`

logical_task_id: funhub-space-foreman
project_id: local-90e565842c3b3296df299d30317505ec
thread_id: 019f4ff8-0d79-70f0-80db-29323d49858d
expected_title: 包工头
actual_title: 包工头
title_verified: true
expected_project_id: local-90e565842c3b3296df299d30317505ec
actual_project_id: local-90e565842c3b3296df299d30317505ec
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 9
shared_index_verified: false
expected_body_sha256: 65ad7cf25ca473fe10988c7d7de8e6aefe8d26d13a58e3f1ccfb24ba1b93e5f2
actual_body_sha256: 65ad7cf25ca473fe10988c7d7de8e6aefe8d26d13a58e3f1ccfb24ba1b93e5f2
body_sha256_verified: true

## `funhub-repair-computer`

logical_task_id: funhub-repair-computer
project_id: local-90e565842c3b3296df299d30317505ec
thread_id: 019e3586-f21e-70a1-89e4-b4323d4e57c6
expected_title: 修电脑的
actual_title: 修电脑的
title_verified: true
expected_project_id: local-90e565842c3b3296df299d30317505ec
actual_project_id: local-90e565842c3b3296df299d30317505ec
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 8
shared_index_verified: false
expected_body_sha256: dd4503ee551f46788329e9122640d80b436e2eaa3cdf39fce0d1b01c5b5b4369
actual_body_sha256: dd4503ee551f46788329e9122640d80b436e2eaa3cdf39fce0d1b01c5b5b4369
body_sha256_verified: true

## `funhub-press-to-talk-fix`

logical_task_id: funhub-press-to-talk-fix
project_id: local-90e565842c3b3296df299d30317505ec
thread_id: 019e48c0-4547-7ce2-b3ca-0e1e589ee4e5
expected_title: 修复按住说话误弹窗
actual_title: 修复按住说话误弹窗
title_verified: true
expected_project_id: local-90e565842c3b3296df299d30317505ec
actual_project_id: local-90e565842c3b3296df299d30317505ec
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 7
shared_index_verified: false
expected_body_sha256: e5ecbb0d1aec8a3b53d782b1f1aed626dfdbf6ae7519612062e06381fa8978e2
actual_body_sha256: e5ecbb0d1aec8a3b53d782b1f1aed626dfdbf6ae7519612062e06381fa8978e2
body_sha256_verified: true

## `funhub-aime-frontend`

logical_task_id: funhub-aime-frontend
project_id: local-90e565842c3b3296df299d30317505ec
thread_id: 019e411b-9f7b-7802-aa9c-5a3ef22da7d1
expected_title: 开发极简聊天界面
actual_title: 开发极简聊天界面
title_verified: true
expected_project_id: local-90e565842c3b3296df299d30317505ec
actual_project_id: local-90e565842c3b3296df299d30317505ec
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 6
shared_index_verified: false
expected_body_sha256: fe488376e602ac382407d2a15e728f138460450fc2bcbdd0fc54137b96df3458
actual_body_sha256: fe488376e602ac382407d2a15e728f138460450fc2bcbdd0fc54137b96df3458
body_sha256_verified: true

## `funhub-aime-backend`

logical_task_id: funhub-aime-backend
project_id: local-90e565842c3b3296df299d30317505ec
thread_id: 019e411b-c333-7e82-a6bc-00a373fbc978
expected_title: 对齐 FunHub AI 服务
actual_title: 对齐 FunHub AI 服务
title_verified: true
expected_project_id: local-90e565842c3b3296df299d30317505ec
actual_project_id: local-90e565842c3b3296df299d30317505ec
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 5
shared_index_verified: false
expected_body_sha256: e6230230541d7924275c6e910d6d59ee866c8844a7ed3f45a4c8e2d90f9f71f1
actual_body_sha256: e6230230541d7924275c6e910d6d59ee866c8844a7ed3f45a4c8e2d90f9f71f1
body_sha256_verified: true

## `lottery-foreman`

logical_task_id: lottery-foreman
project_id: 71d16a40-79b9-4034-97b4-74d54bc0c500
thread_id: 019fbdee-4ee1-73b0-bd39-e9d2837a7370
expected_title: 包工头
actual_title: 包工头
title_verified: true
expected_project_id: 71d16a40-79b9-4034-97b4-74d54bc0c500
actual_project_id: 71d16a40-79b9-4034-97b4-74d54bc0c500
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 4
shared_index_verified: false
expected_body_sha256: 24d215f7d4ce079bf0cc7c47a726e9ac7707d1baccb546a420090e3d2b8c1211
actual_body_sha256: 24d215f7d4ce079bf0cc7c47a726e9ac7707d1baccb546a420090e3d2b8c1211
body_sha256_verified: true

## `demo-foreman`

logical_task_id: demo-foreman
project_id: local-81d8c01b7837e883f7b7ea9a01f3a3dc
thread_id: 019f4a32-a579-77b1-be24-5c600bd937cd
expected_title: 包工头
actual_title: 包工头
title_verified: true
expected_project_id: local-81d8c01b7837e883f7b7ea9a01f3a3dc
actual_project_id: local-81d8c01b7837e883f7b7ea9a01f3a3dc
project_verified: true
expected_pinned: false
actual_pinned: false
pinned_verified: true
expected_shared_index: undefined
actual_shared_index: 3
shared_index_verified: false
expected_body_sha256: a421e2e6cb921a45a3aa9ecacef865ab1241c7ac52a8025c9d18123d0228839d
actual_body_sha256: a421e2e6cb921a45a3aa9ecacef865ab1241c7ac52a8025c9d18123d0228839d
body_sha256_verified: true

## Git 仓库终态

| 仓库 | 分支 | HEAD | upstream | dirty | ahead/behind | conflicts |
|---|---|---|---|---:|---|---:|
| `D:\.aaProject-Bruce\CodexMissionContext` | `main` | `ec8471ed579a` | `origin/main` | 2 | 0/0 | 0 |
| `D:\.aaProject-Bruce\AIWorkFlow` | `main` | `54e6d21198f6` | `origin/main` | 0 | 0/0 | 0 |
| `D:\.aaProject-Bruce\lottery\lottery-calculation-backend` | `master` | `e2675e5a0884` | `origin/master` | 0 | 0/0 | 0 |
| `D:\.aaProject-Bruce\lottery\lottery-calculation-frontend` | `master` | `ea3f326016d0` | `origin/master` | 0 | 0/0 | 0 |
| `D:\.aaProject-Bruce\vid-mat-lab` | `main` | `fc494e5f2493` | `origin/main` | 27 | 0/0 | 0 |
| `D:\.aaProject-Bruce\Aidrama` | `main` | `3baedae5d3bb` | `origin/main` | 72 | 0/0 | 0 |
| `D:\.aaProject-Bruce\canvas-garment` | `main` | `093d8967ff71` | `origin/main` | 7718 | 0/0 | 0 |
| `D:\.aaProject-Bruce\funhub-space\aime-bridge-backend` | `main` | `703f0c16d7bc` | `origin/main` | 18 | 0/0 | 1 |
| `D:\.aaProject-Bruce\funhub-space\english-talk-trainer` | `main` | `5effdf57fd36` | `origin/main` | 0 | 0/0 | 0 |
| `D:\.aaProject-Bruce\funhub-space\funhub` | `Feature/funhub-taro-migration-1.0` | `511156300714` | `origin/Feature/funhub-taro-migration-1.0` | 0 | 0/0 | 0 |
| `D:\.aaProject-Bruce\funhub-space\funhub-CandyArt` | `main` | `53eba8fd7042` | `origin/main` | 1 | 0/0 | 0 |
| `D:\.aaProject-Bruce\funhub-space\funhub-taro` | `main` | `ba8fb2134178` | `origin/main` | 0 | 0/0 | 0 |
| `D:\.aaProject-Bruce\funhub-space\funhub-WordSmiths` | `main` | `c9802350a87c` | `origin/main` | 0 | 0/0 | 0 |
| `D:\.aaProject-Bruce\funhub-space\funhub-WordSmiths-backend` | `main` | `f562c49ee9bc` | `origin/main` | 0 | 0/0 | 0 |
| `D:\.aaProject-Bruce\funhub-space\MountainFruitCottage` | `main` | `e5376419149c` | `origin/main` | 0 | 0/0 | 0 |
| `D:\.aaProject-Bruce\Demo\demo-for-course-backend` | `main` | `NO_HEAD` | `-` | 215 | - - | 0 |
| `D:\.aaProject-Bruce\Demo\demo-for-course-frontend` | `main` | `NO_HEAD` | `-` | 98 | - - | 0 |
| `D:\.aaProject-Bruce\liquidity-bmi\liquidity-bmi-backend` | `main` | `37ee234f0e23` | `origin/main` | 0 | 0/0 | 0 |
| `D:\.aaProject-Bruce\liquidity-bmi\liquidity-bmi-frontend` | `main` | `7a0caf6fbe4b` | `origin/main` | 0 | 0/0 | 0 |
| `D:\.aaProject-Bruce\liquidity-portrait\liquidity-portrait-backend` | `main` | `02560c1f9a3b` | `origin/main` | 1 | 0/0 | 0 |
| `D:\.aaProject-Bruce\liquidity-portrait\liquidity-portrait-frontend` | `main` | `4f1290da864c` | `origin/main` | 90 | 0/0 | 0 |
| `D:\.aaProject-Bruce\liquidity-watermark-assistant\liquidity-watermark-assistant-backend` | `main` | `5ad0017685c0` | `origin/main` | 18 | 0/0 | 0 |
| `D:\.aaProject-Bruce\liquidity-watermark-assistant\liquidity-watermark-assistant-frontend` | `main` | `6a8f6ace8035` | `origin/main` | 0 | 0/0 | 0 |

- 第一阶段远端取得：上下文、AIWorkflow、lottery、vid-mat-lab、Aidrama、canvas-garment、证件照和去水印仓库已取得或已有 0/0 事实；GitHub HTTPS 随后统一出现 443 连接失败，FunHub 与 BMI 的实时 fetch 结果不能完整确认。
- 安全快进：AIWorkflow `a35316d→54e6d21`；vid-mat-lab 使用保留式 stash 后 `16694cf→fc494e5`，恢复本地现场无冲突，保护 stash 保留。
- 阻塞：Aime 后端 1 个真实冲突；Demo 两仓无 HEAD/upstream；多个仓库存在未审查的大批量素材、缓存或普通改动；本轮不盲目提交。
