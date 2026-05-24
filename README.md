# AI Flywheel Builder

AI Flywheel Builder 是一个个性化 AI 内容创作飞轮 skill。

它帮助用户发现自己可以创作什么、哪些实践值得讲、下一步可以做什么 AI 实践，并把这些实践持续转成内容、产物、反馈和下一轮行动。

一句话：

> 不是让用户硬想选题，而是帮用户建立一套能持续长出选题的 AI 内容创作飞轮。

当前版本从 AI 实践型创作者场景切入。长期方向是通用内容创作飞轮：任何有真实实践的人，都可以把产品、项目、作品、服务、案例、实验、失败或经验交给系统，由系统判断什么值得讲、怎么讲、能沉淀什么产物、反馈如何进入下一轮实践。

## Product Status

- Version: `0.1.0`
- Stage: product skeleton
- Owner: PigeonAI / 鸽子杨的雾灯会
- Current goal: define the product architecture and first usable skill set

## Core Loop

```text
初始化：必要采访 -> 用户画像 -> 内容种子库 -> 内容主线 -> 产物方向 -> 反馈机制 -> 记忆更新规则
运行：实践设计 -> 实践过程 -> 发现/摩擦 -> 内容主题 -> 内容草稿/脚本 -> 可领取产物 -> 用户反馈 -> 下一轮实践
```

## 模块划分

### 模块 1：初始化

新用户第一次使用时，系统不产内容、不产清单、不要求用户提交实践。

初始化模块只做一件事：

```text
层层采访 -> 用户建模 -> 生成个性化内容创作飞轮 -> 用户确认 -> 批量初始化飞轮系统
```

初始化完成后，用户应该得到：

- 用户画像
- 内容种子库
- 内容主线
- 产物方向
- 反馈机制
- 记忆更新规则
- 当前焦点
- 下一步自动动作

### 模块 2：实践设计

初始化完成后，如果用户不知道下一步做什么，系统从飞轮里生成下一轮小实践。

实践设计模块才生成实践池和第一轮实践建议。

### 模块 3：实践处理

用户提交实践后，系统先接住材料、建立运行编号、归档资料、更新索引，再进入复盘和内容/产物处理。

材料可以是乱的。整理资料是 AI 的职责。

实践复盘模块负责判断本轮实践是否值得继续加工，并提取内容种子、产物机会、长期记忆候选和下一步路由。用户不需要自己判断“这东西值不值得讲”。

内容拆解模块不负责写完整产物本体。它负责把一次真实实践或已有产物拆成内容包，并产出首发稿、产物发布说明、证据清单和反馈入口。

反馈归因模块支持双入口：用户可以发反馈页面 URL，让 AI 用浏览器只读采集；也可以发截图作为兜底。反馈模块负责区分噪音、观察信号和有效信号，并把反馈推进到下一轮行动。

用户对 AI Flywheel Builder 本身的使用反馈，也必须进入飞轮。比如模块跑偏、截图失败、采集失败、状态卡住、输出不符合预期，都要归因到模块、模板、文档、平台适配、工具限制或路线图，而不是只停留在聊天解释。

每个模块结束前都必须做经验收口：判断本次是否暴露重复问题、新避坑规则、模板字段缺失、模块行为缺陷或未来能力。符合条件的经验必须写入规则、索引、模板、skill 或路线图，让系统下一次少犯同类错误。

每个真实运行目录都必须生成 `learning-closure.md`，并至少包含一条 `closure_uuid`。`learning-closure.md` 是本轮经验收口总表，可以有多条记录。即使本轮没有长期经验要写入，也要记录“本轮无长期经验写入”的原因。

标识规则：

- `run_id`：人类可读编号
- `run_uuid`：机器稳定运行 ID
- `closure_uuid`：单条经验收口记录 ID

所有经验收口记录还必须同步进入：

`J:/pigeonAI/AI-flywheel-Builder/workspace/{user}/indexes/learning-index.md`

## 固定状态与中控规则

初始化完成后，`flywheel-orchestrator` 拥有最高调度优先级。

用户问“下一步是什么”“怎么推进”“我该做什么”时，系统默认执行 `flywheel-state.md` 里的 `next_action`，而不是继续解释概念。

只有涉及修改产品规则或当前运行之外的项目文件、联网/浏览器/登录态、发布、删除、敏感边界或必须由用户判断的分叉时，才打断用户确认。

`flywheel-state.md` 的 `current_stage` 只能使用：

```text
not_initialized
initializing
practice_design
practice_execution_waiting
practice_capture
practice_review
content_package
feedback_waiting
feedback_attribution
learning_closure
next_practice_ready
blocked
```

状态文件必须包含 `next_action` 和 `missing_requirements`。如果 `next_action` 为空，说明飞轮卡住，中控必须先修复状态。

## 用户可见主交付物

每轮实践必须生成一个用户可见主交付物：

`J:/pigeonAI/AI-flywheel-Builder/workspace/{user}/outputs/{run_id}/content-flywheel-run.html`

Markdown 可以同时保留为后台源码版或可编辑草稿：

`J:/pigeonAI/AI-flywheel-Builder/workspace/{user}/outputs/{run_id}/content-flywheel-run.md`

后台索引、模板、接收报告、复盘报告和经验收口不能替代主交付物。

HTML 主交付物默认使用开源内置主题：

`J:/pigeonAI/AI-flywheel-Builder/themes/default-html-report/`

如果用户明确指定本地设计 skill 或主题，系统可以使用对应主题。PigeonAI / 雾灯会设计范式是作者本机可选主题，不是开源核心依赖；没有该私有主题时，系统必须回退到默认 HTML 主题。

主交付物最低包含：

- 本轮实践一句话
- 为什么值得讲
- 可发布内容草稿
- 配套可领取产物
- 证据与边界
- 反馈入口
- 下一轮实践

V0.1 整体验收使用真实实践：

`J:/pigeonAI/AI-flywheel-Builder/`

验收标准：

1. 用户不用追问“然后呢”。
2. 有一个绝对路径的主交付物。
3. run 目录、索引、经验收口全部闭环。

## 它解决什么问题

AI 重度使用者和潜在创作者常见的问题是：

- 不知道自己到底能创作什么
- 不知道哪些经历、问题、失败或 AI 使用方式值得讲
- 不知道下一步可以做什么小实践
- 即使做了实践，也不知道怎么拆成内容
- 不知道哪个部分能公开
- 不知道能配套什么可领取产物
- 不知道反馈怎么回到下一轮实践

AI Flywheel Builder 的职责是把这些判断系统化。

## 用户提交什么

新用户可以什么都没有。系统会先进入初始化模块，通过分层采访建立个性化飞轮。

如果已经有材料，也可以提交真实实践对象，例如：

- 一个 app 或产品目录
- 一个 skill
- 一份手册草稿
- 一个工作流
- 一段调试过程
- 一次失败案例
- 一段用户反馈
- 一个对话记录

## 系统返回什么

初始化阶段返回的是飞轮系统，不是内容成品：

1. 用户画像
2. 内容种子库
3. 内容主线
4. 产物方向
5. 反馈机制
6. 记忆更新规则
7. 当前焦点
8. 下一步自动动作

实践处理阶段才返回：

1. 内容种子
2. 实践复盘
3. 第一轮最小实践
4. 本轮内容主题
5. 若干内容选题
6. 一篇内容草稿或短视频脚本
7. 一个配套可领取产物
8. 反馈回流方式
9. 下一轮实践动作

并且必须生成或更新一个可见交付文件，例如：

`J:/pigeonAI/AI-flywheel-Builder/workspace/pigeon-yang/content-flywheel-run-v0.1.md`

`J:/pigeonAI/AI-flywheel-Builder/templates/practice-submission.md` 和 `J:/pigeonAI/AI-flywheel-Builder/templates/reverse-validation-report.md` 只能作为后台记录和收口，不能替代主交付物。

## 像 Nuwa 一样使用

用户不需要反复追问概念。

新用户缺少飞轮时，系统先做分层采访并初始化飞轮；初始化完成后，才进入实践设计或内容生成。

```text
$ai-flywheel-builder 我想建立自己的 AI 内容创作飞轮，但我不知道该创作什么，也不知道自己有什么实践值得讲。
```

系统应该直接返回并写入：

- 内容种子
- 内容主线
- 产物方向
- 反馈机制
- 当前焦点
- 下一步自动动作

## 成果处理的位置

已有成果处理不是产品主线，只是内容飞轮的一环。

当用户提交已有 app、skill、手册、工作流或产品目录时，系统会把它处理成：

- 可讲的真实实践故事
- 可发布的内容草稿或脚本
- 可领取、可复用、可维护的产物
- 可收集反馈的入口
- 可推动下一轮实践的问题清单

## 路径规则

面向用户交付文件、报告更新结果或提示下一步时，必须提供绝对路径。

示例：

- 正确：`J:/pigeonAI/AI-flywheel-Builder/templates/practice-submission.md`
- 错误：`templates/practice-submission.md`

## Core Product Principle

用户不负责推进流程，AI 负责推进流程。

用户只负责三件事：

- 确认判断是否正确
- 在真实分叉处做选择
- 提供 AI 不知道的事实、经历、边界和反馈

系统必须负责：

- 首次初始化时生成完整飞轮蓝图
- 用户确认后批量创建或更新必要文件
- 维护当前阶段目标
- 判断下一步
- 选择该调用的子 skill
- 执行能安全执行的最小动作
- 只在需要用户判断或授权时打断用户

## 决策固化规则

凡是用户已经裁定的模块边界、状态流转、文件职责、输出标准、命名规则或验收标准，不能只停留在聊天里。

必须写入对应项目文件：

- 影响运行行为：写入对应 `J:/pigeonAI/AI-flywheel-Builder/skills/*/SKILL.md`
- 影响产品理解：写入 `J:/pigeonAI/AI-flywheel-Builder/README.md`、`J:/pigeonAI/AI-flywheel-Builder/docs/00_PRODUCT_BRIEF.md` 或 `J:/pigeonAI/AI-flywheel-Builder/docs/01_ARCHITECTURE.md`
- 影响生成文件结构：写入 `J:/pigeonAI/AI-flywheel-Builder/templates/*.md`

没有写入文件的设计决策，不算完成。

## 经验收口规则

AI Flywheel Builder 的目标不是只完成当前任务，而是让下一次类似任务更容易、更准确、更少踩坑。

每个模块完成前，系统必须内部检查：

- 本次有没有暴露重复问题？
- 本次有没有新增避坑规则？
- 本次有没有模板字段缺失？
- 本次有没有模块行为需要改？
- 本次有没有未来能力，暂时不能做但应该进 roadmap？

只有满足以下至少一项，才升级为长期经验：

- 问题重复出现
- 用户明确裁定
- 造成流程中断
- 影响下一次判断
- 暴露模板或模块缺陷
- 属于平台或工具限制

写入位置：

- 规则：`J:/pigeonAI/AI-flywheel-Builder/templates/memory-rules.md`
- 索引：`J:/pigeonAI/AI-flywheel-Builder/templates/run-index.md`、`J:/pigeonAI/AI-flywheel-Builder/templates/material-index.md`、`J:/pigeonAI/AI-flywheel-Builder/templates/feedback-index.md`
- 经验索引：`J:/pigeonAI/AI-flywheel-Builder/templates/learning-index.md`
- 模板字段：`J:/pigeonAI/AI-flywheel-Builder/templates/*.md`
- 模块行为：`J:/pigeonAI/AI-flywheel-Builder/skills/*/SKILL.md`
- 未来能力：`J:/pigeonAI/AI-flywheel-Builder/docs/03_ROADMAP.md`

硬校验脚本：

`python J:/pigeonAI/AI-flywheel-Builder/scripts/verify_learning_closure.py`

V0.1 规则验收脚本：

`python J:/pigeonAI/AI-flywheel-Builder/scripts/verify_v01_acceptance.py`

检查某个真实运行目录：

`python J:/pigeonAI/AI-flywheel-Builder/scripts/verify_learning_closure.py --run-dir J:/pigeonAI/AI-flywheel-Builder/workspace/{user}/runs/{run_id}`

`python J:/pigeonAI/AI-flywheel-Builder/scripts/verify_v01_acceptance.py --run-dir J:/pigeonAI/AI-flywheel-Builder/workspace/{user}/runs/{run_id}`

## Skill System

```text
skills/
  ai-flywheel-builder/     # 薄母 skill：入口、状态检查、路由
  flywheel-initializer/    # 初始化模块：分层采访、用户建模、飞轮蓝图、批量初始化
  practice-designer/       # 实践设计模块：根据状态生成下一轮小实践
  practice-capture/        # 实践接收模块：接材料、建 run_id、归档、索引、推进复盘
  practice-reviewer/       # 实践复盘模块：判断价值、提取种子、机会和下一步路由
  content-decomposer/      # 内容拆解模块：内容包、首发稿、发布说明、证据和反馈入口
  feedback-attributor/     # 反馈归因模块：URL/截图采集、信号判断、归因和下一步路由
  flywheel-orchestrator/   # 中控 skill：读取 flywheel-state.md，保护阶段目标与路由
  flywheel-memory/         # 子 skill：长期记忆维护
  friction-capture/        # 子 skill：实践摩擦采集
  artifact-designer/       # 子 skill：小产物设计
  flywheel-gatekeeper/     # 子 skill：飞轮守门
```

## Repository Layout

```text
docs/
  00_PRODUCT_BRIEF.md
  01_ARCHITECTURE.md
  02_VERSIONING.md
  03_ROADMAP.md
templates/
  user-flywheel-profile.md
  flywheel-state.md
  artifact-registry.md
  friction-log.md
  feedback-log.md
  current-focus.md
  activation-plan.md
  practice-submission.md
  reverse-validation-report.md
  run-index.md
  material-index.md
  content-seed-index.md
  output-index.md
  feedback-index.md
  learning-index.md
  run.md
  materials.md
  capture-report.md
  review-report.md
  content-package.md
  feedback-report.md
  learning-closure.md
skills/
  */SKILL.md
scripts/
  verify_learning_closure.py
themes/
  default-html-report/     # 开源默认 HTML 主交付物主题
  pigeonai-ff-optional/    # PigeonAI / 雾灯会可选主题适配说明，不是硬依赖
```

## 长期管理结构

用户工作区必须按轮次和索引管理：

```text
J:/pigeonAI/AI-flywheel-Builder/workspace/{user}/
  runs/
  materials/
  indexes/
  memory/
  outputs/
```

每一轮实践使用 `YYYY-MM-DD-NNN-topic-slug` 作为 `run_id`，例如：

`J:/pigeonAI/AI-flywheel-Builder/workspace/pigeon-yang/runs/2026-05-24-001-ai-flywheel-skill/`

索引文件负责让系统越用越好：

- `J:/pigeonAI/AI-flywheel-Builder/workspace/{user}/indexes/run-index.md`
- `J:/pigeonAI/AI-flywheel-Builder/workspace/{user}/indexes/material-index.md`
- `J:/pigeonAI/AI-flywheel-Builder/workspace/{user}/indexes/content-seed-index.md`
- `J:/pigeonAI/AI-flywheel-Builder/workspace/{user}/indexes/output-index.md`
- `J:/pigeonAI/AI-flywheel-Builder/workspace/{user}/indexes/feedback-index.md`

## 状态文件职责

`J:/pigeonAI/AI-flywheel-Builder/templates/flywheel-state.md` 是机器调度状态，给 skill 判断当前阶段、下一步动作和要调用的模块。

`J:/pigeonAI/AI-flywheel-Builder/templates/current-focus.md` 是人类可读摘要，给用户理解当前目标和下一步。

路由以 `flywheel-state.md` 为准，不以 `current-focus.md` 为准。

## First Product Principle

先用这个系统解决鸽子杨自己的痛点，再抽象成能帮助其他人的产品。

当前验证场景：

- 用户想做 AI 实践型创作者和内容飞轮产品主理人。
- 用户手上有复杂 AI 产品实践，但粒度太大、太敏感、难公开。
- 系统要帮助用户从复杂实践中拆出可公开、可复用、可迭代的内容和小产物。

## 版本规划

版本规划统一记录在：

`J:/pigeonAI/AI-flywheel-Builder/docs/03_ROADMAP.md`

已完成变化记录在：

`J:/pigeonAI/AI-flywheel-Builder/CHANGELOG.md`
