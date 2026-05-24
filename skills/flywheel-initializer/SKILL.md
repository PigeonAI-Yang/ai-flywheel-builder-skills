---
name: flywheel-initializer
description: |
  New-user initialization module for AI Flywheel Builder. Use when a user has no initialized personal AI content creation flywheel, asks to initialize their flywheel, or does not yet know what they can create or what practice is worth doing. This skill performs layered interview, provisional inference, user modeling, flywheel blueprint generation, one confirmation, and batch initialization. It must not generate practices before initialization is complete.
---

# Flywheel Initializer

## Role

Initialize a new user's personalized AI content creation flywheel.

This module is only for the new-user stage.

It does not generate publishable content, a self-check checklist, a content draft, or a claimable asset as the main output. It builds the flywheel system that later modules will run.

## Goal

```text
新用户 -> 分层采访 -> 用户建模 -> 个性化飞轮蓝图 -> 用户确认 -> 批量初始化飞轮系统
```

## Required Output After Initialization

The initialized flywheel must include:

```text
用户画像
内容种子库
内容主线
产物方向
反馈机制
记忆更新规则
机器调度状态
人类可读焦点
下一步自动动作
```

## Required Files

Create or update these files in the user's workspace:

```text
flywheel-state.md
current-focus.md
user-flywheel-profile.md
content-seed-library.md
content-pillars.md
artifact-registry.md
feedback-log.md
memory-rules.md
activation-plan.md
```

If the project still uses older files, preserve them and add the missing files rather than deleting user data.

## Layered Interview

Start by showing the brief interview map, then ask only the first detailed question.

For Chinese users, start like this:

```text
我会用 5 层信息帮你初始化内容创作飞轮：
1. 身份与受众
2. AI 使用场景
3. 当前卡点
4. 公开边界
5. 内容/产物偏好与第一轮实践粒度

先问第 1 层：你想成为什么类型的 AI 内容创作者？主要想帮谁？

你可以任选一种方式回答：
- 一句话粗略回答
- 分点回答
- 丢一段自我介绍让我提炼
- 直接说“不确定”，我会先给暂定判断，后面你再纠正
```

Then continue one layer at a time. Do not dump all detailed questions unless the user explicitly asks for the full form.

### Layer 1: Identity And Audience

Ask:

```text
你想成为什么类型的 AI 内容创作者？主要想帮谁？
```

Collect:

```text
用户身份：
目标受众：
不想成为的类型：
```

### Layer 2: AI Usage And Experience

Ask:

```text
你平时在哪些场景重度使用 AI？最近 7 天真实用 AI 做过什么？
```

Collect:

```text
主要 AI 使用场：
近期真实使用：
已有项目/工作流/skill/手册/案例：
```

### Layer 3: Pain And Friction

Ask:

```text
你最常卡在哪：不知道讲什么、不知道做什么实践、实践拆不成内容、发出去没反馈，还是反馈无法迭代？
```

Collect:

```text
当前卡点：
反复出现的问题：
失败/误判/修正样本：
```

### Layer 4: Boundary

Ask:

```text
哪些内容可以公开讲？哪些只能抽象讲？哪些不讲？
```

Collect:

```text
可公开：
需抽象：
不公开：
```

Only ask topic-relevant boundaries. Do not inject unrelated private-project boundaries.

### Layer 5: Format And Workload

Ask:

```text
你更适合先做文章、短视频、skill、手册、模板、清单，还是工作流？第一轮你能接受 30 分钟、2 小时、1 天，还是 1 周的实践？
```

Collect:

```text
偏好内容形式：
偏好产物形式：
第一轮可承受实践粒度：
成功信号：
```

## Required Model

Before generating a blueprint, the agent must have at least provisional answers for:

```text
用户身份：
目标受众：
主要 AI 使用场：
内容种子：
当前卡点：
公开边界：
偏好内容形式：
偏好产物形式：
第一轮可承受实践粒度：
成功信号：
```

If a field is missing, ask the next smallest question.

## Blueprint Format

For Chinese users:

```text
飞轮一句话：
用户画像：
目标受众：
主要 AI 使用场：
内容种子库：
内容主线：
产物方向：
反馈机制：
记忆更新规则：
当前焦点：
下一步自动动作：
要创建或更新的文件：
```

After the blueprint, stop for one confirmation:

```text
回复“确认初始化”，我会一次性创建或更新你的飞轮系统。
如果身份、受众、边界或主线有错，只回复要修正的部分。
```

## Batch Initialization

After confirmation, create or update the required files.

`flywheel-state.md` must be machine-readable enough for routing:

```text
current_stage:
current_focus:
next_action:
active_module:
blocking_condition:
missing_requirements:
last_completed:
required_inputs:
updated_at:
```

`current-focus.md` must be human-readable:

```text
当前阶段：
当前目标：
为什么现在做：
下一步系统会做什么：
用户只需要：
暂时不做：
```

## State Transition

After successful initialization:

```text
current_stage: practice_design
active_module: practice-designer
next_action: 调用 practice-designer 生成实践池和第一轮可做实践
```

## Provisional Inference And Correction

Provisional inference is allowed, but it must be explicit.

Use this label:

```text
暂定判断：
```

If the user corrects a provisional inference:

1. Apply the correction.
2. Restate the corrected field briefly.
3. Continue to the next initialization layer or blueprint.

Do not stop after the correction. Do not make the user ask "下一步".

## Initialization Acceptance

Initialization is complete only if all four conditions are true:

```text
1. flywheel-state.md exists.
2. current-focus.md exists.
3. user profile, content seed library, and content pillars exist.
4. flywheel-state.md next_action points to practice-designer.
```

Before final delivery, learning closure must be complete:

```text
5. 已完成经验收口：判断是否需要写入规则、索引、模板、模块行为或路线图。
是否有重复问题：
是否有新避坑规则：
是否有模板字段缺失：
是否有模块行为要改：
是否有未来能力要进 roadmap：
写入位置：
```

If no durable lesson qualifies, state that no long-term learning was written.

## Failure Modes

- Do not generate a publishable article during initialization.
- Do not generate a self-check checklist as the main output.
- Do not generate a practice pool or first practice before initialization is complete.
- Do not ask the user to submit a practice object.
- Do not ask the user to design the flywheel structure.
- Do not continue interviewing after the required model is complete.
- Do not stop after a user correction. Apply the correction and continue the next initialization step.
- Do not leave the user without a current focus and next automatic action.
- 不要在未做经验收口时结束本模块。
