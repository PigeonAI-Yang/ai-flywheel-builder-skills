---
name: practice-capture
description: |
  Practice capture module for AI Flywheel Builder. Use when an initialized user submits practice material after a recommended practice, including messy descriptions, file paths, screenshots, AI conversations, failures, product directories, drafts, or feedback. It creates a run id, archives and classifies materials, updates indexes, writes a capture report, then advances the flywheel state to practice review.
---

# Practice Capture

## 角色

接住用户提交的实践材料，并把杂乱材料整理成可长期管理、可复盘、可继续加工的飞轮记录。

本模块不直接产内容，不直接设计产物。

它只做：

```text
接收材料 -> 建立运行编号 -> 归档材料 -> 分类整理 -> 更新索引 -> 生成接收报告 -> 推进到实践复盘
```

## 触发边界

只有满足以下条件时运行：

```text
flywheel-state.md 存在
current_stage: practice_execution_waiting
用户提交了实践过程、结果、文件路径、截图说明、AI 对话、失败或卡住点中的任意一种材料
```

如果用户没有提交材料，只告诉用户当前等待什么，并允许用户随便提交，不要求填写表格。

## 用户可以乱提交

用户可以用任意形式提交材料：

- 一段过程描述
- 一个本地绝对路径
- 一个产品目录
- 一份草稿
- 一段 AI 对话
- 几张截图的说明
- 一个失败过程
- 一个卡住点
- 一段反馈

整理资料是 AI 的职责。

不要要求用户先按模板补全字段。

## 必读文件

按需读取：

```text
flywheel-state.md
current-focus.md
next-practice-brief.md
practice-pool.md
memory-rules.md
```

如果存在当前用户工作区，也读取：

```text
workspace/{user}/indexes/run-index.md
workspace/{user}/indexes/material-index.md
workspace/{user}/indexes/content-seed-index.md
workspace/{user}/indexes/output-index.md
```

## 工作区结构

用户工作区必须按长期管理设计。

默认结构：

```text
workspace/{user}/
  runs/
  materials/
  indexes/
  memory/
  outputs/
```

如果目录不存在，创建对应目录。

## 运行编号

每一轮实践必须创建唯一 `run_id`。

格式：

```text
YYYY-MM-DD-NNN-topic-slug
```

示例：

```text
2026-05-24-001-ai-flywheel-skill
```

规则：

- 日期使用当前日期。
- `NNN` 是当天序号，从 `001` 开始。
- `topic-slug` 来自本轮实践主题，使用短横线连接的英文或拼音稳定标识。
- 如果无法可靠生成主题标识，使用 `untitled-practice`，但要在报告中标记需要后续修正。

同时必须创建 `run_uuid`。

规则：

- `run_id` 是人类可读编号，用于目录和沟通。
- `run_uuid` 是机器稳定 ID，用于长期引用。
- `run_uuid` 必须是 UUID 格式。

## 每轮目录

每轮实践目录：

```text
workspace/{user}/runs/{run_id}/
```

必须创建或更新：

```text
run.md
materials.md
capture-report.md
learning-closure.md
outputs/
```

`learning-closure.md` 必须在创建本轮目录时同时创建，即使本轮暂时没有长期经验要写入。

每个 `learning-closure.md` 必须包含：

```text
run_id
run_uuid
经验收口记录总表
至少一条 closure_uuid
```

每条 `closure_uuid` 必须是 UUID 格式，用来追踪单条经验收口记录。

必须同步更新：

```text
workspace/{user}/indexes/learning-index.md
```

## 三层存储

### 1. 原始材料

原始材料尽量保留引用，不强行改写。

材料可以是：

- 文件路径
- 目录路径
- 用户粘贴文本
- 截图说明
- 对话片段
- 失败描述

如果是本地路径，记录绝对路径。

如果是用户粘贴内容，记录在本轮 `materials.md` 中。

### 2. 结构化记录

在 `capture-report.md` 中提取：

- 本轮实践对象
- 材料类型
- 已完成事实
- 可观察结果
- 失败或卡住点
- 暴露的摩擦
- 可复盘问题
- 可能进入内容或产物的线索

### 3. 长期记忆候选

只提出候选，不自动写入长期记忆。

长期记忆候选必须符合 `memory-rules.md`：

- 会影响未来判断
- 不是一次性情绪
- 不是未验证想法
- 不是原始聊天归档

## 索引机制

必须更新：

```text
workspace/{user}/indexes/run-index.md
workspace/{user}/indexes/material-index.md
```

按需更新：

```text
workspace/{user}/indexes/content-seed-index.md
workspace/{user}/indexes/output-index.md
```

索引只存可检索摘要，不存长正文。

## 状态流转

材料接收完成后，将 `flywheel-state.md` 更新为：

```text
current_stage: practice_review
active_module: practice-reviewer
next_action: 基于本轮 capture-report.md 进行实践复盘，判断可生成的内容主题、产物方向和长期记忆候选
required_inputs:
  - workspace/{user}/runs/{run_id}/capture-report.md
```

在 `routing_notes` 中记录本轮 `run_id` 和绝对路径。

## 输出格式

中文用户使用：

```text
当前阶段：
已接收材料：
本轮运行编号：
已创建/更新：
材料分类：
初步提取：
长期记忆候选：
状态更新：
用户只需要：
```

`用户只需要` 必须告诉用户下一步不是重新整理材料，而是等待系统复盘，或补充 AI 明确缺失的关键事实。

## 验收标准

本模块完成时必须满足：

1. 已创建本轮 `run_id`。
2. 已创建或更新本轮运行目录。
3. 已生成 `capture-report.md`。
4. 已生成或更新本轮 `learning-closure.md`，且包含 `closure_uuid`。
5. 已更新 `learning-index.md`。
6. 已更新 `run-index.md`。
7. 已更新 `material-index.md`。
8. 已更新 `flywheel-state.md` 到 `practice_review`。
9. 用户知道材料已被接住，下一步由系统进入复盘。
10. 已完成经验收口：判断是否需要写入规则、索引、模板、模块行为或路线图。

## 失败模式

- 不要要求用户按表格重新提交材料。
- 不要把原始聊天全文写进长期记忆。
- 不要跳过索引直接产内容。
- 不要把一次性材料当成长期规则。
- 不要在未接收和复盘前调用内容拆解。
- 不要只生成报告而不更新机器状态。
- 不要在未做经验收口时结束本模块。
