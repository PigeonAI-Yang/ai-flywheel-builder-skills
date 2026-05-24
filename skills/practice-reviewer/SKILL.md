---
name: practice-reviewer
description: |
  Practice review module for AI Flywheel Builder. Use after practice-capture has created a run folder and capture-report.md. It reads captured practice materials, judges practice quality, extracts friction, discoveries, content seeds, product opportunities, long-term memory candidates, updates indexes, writes review-report.md, and routes the next flywheel step.
---

# Practice Reviewer

## 角色

把已经接收和索引的实践材料复盘成下一步可执行判断。

本模块是飞轮的判断器。

它回答：

```text
这轮实践有没有内容价值、产物价值、长期记忆价值，以及下一步该走哪条路。
```

本模块不接收原始材料，不直接写文章，不直接设计产物。

## 触发边界

只有满足以下条件时运行：

```text
flywheel-state.md 存在
current_stage: practice_review
capture-report.md 存在
```

如果材料尚未接收和索引，路由回 `practice-capture`。

如果用户只提交了新材料但还没有 capture-report，先接收材料，不要直接复盘。

## 必读文件

按需读取：

```text
flywheel-state.md
current-focus.md
memory-rules.md
workspace/{user}/runs/{run_id}/capture-report.md
workspace/{user}/runs/{run_id}/materials.md
workspace/{user}/runs/{run_id}/run.md
workspace/{user}/indexes/run-index.md
workspace/{user}/indexes/material-index.md
workspace/{user}/indexes/content-seed-index.md
workspace/{user}/indexes/output-index.md
```

`run_id` 从 `flywheel-state.md` 的 `routing_notes` 或当前运行目录中读取。

## 复盘流程

### 1. 事实复盘

只基于已接收材料，不补脑。

提取：

- 实践目标
- 用户实际做了什么
- 已完成结果
- 未完成部分
- 证据材料

如果证据不足，标记为“需要补充关键事实”，不要假装完成。

### 2. 实践质量判断

判断本轮实践是否足够进入后续加工：

- 是否有明确动作
- 是否有可观察结果
- 是否暴露真实问题
- 是否能复盘
- 是否能公开表达

质量结论只能三选一：

```text
可进入内容/产物处理
需要补充关键事实
实践质量不足，返回 practice-designer 重新设计
```

### 3. 摩擦与发现提取

提取飞轮核心材料：

```text
用户原本以为：
实际发生了：
卡住点：
AI 没帮上的地方：
用户手动解决了什么：
这暴露的普遍问题：
```

没有真实摩擦或发现时，不要硬造内容价值。

### 4. 内容种子提取

生成可追溯内容种子，不直接写内容稿。

每个内容种子必须包含：

- 内容种子
- 来源证据
- 适合平台
- 核心主张
- 为什么别人会关心
- 是否需要补证据

必须更新：

```text
workspace/{user}/indexes/content-seed-index.md
```

内容种子必须能追溯到 `run_id`。

### 5. 产物机会提取

判断本轮实践是否能沉淀成：

- skill
- 模板
- 清单
- 手册
- 案例库
- 脚本
- 工作流
- 小工具

每个产物机会必须回答：

- 解决什么痛点
- 用户为什么需要
- 最小版本是什么
- 是否已有证据
- 下一步交给哪个模块

如果只是想法，没有实践证据，标记为“待验证”，不要推进到产物设计。

### 6. 长期记忆候选

只提出候选，不自动写入长期记忆。

长期记忆候选必须符合 `memory-rules.md`。

候选类型：

- 身份/定位
- 公开边界
- 内容主线
- 已验证有效模式
- 已验证无效模式
- 反复出现的用户卡点

### 7. 路由决策

复盘结束必须给出下一步路由。

可选路由：

```text
content-decomposer     有明确内容种子
artifact-designer      有明确小产物机会
flywheel-memory        有长期记忆候选需要写入
practice-designer      本轮实践质量不足，需要重新设计
feedback-attributor    材料本身是外部反馈
```

如果多个路由都成立，只选择一个当前最小动作，并把其他动作列为后续队列。

如果用户提交的是已有产品、skill、手册、模板、工具、工作流或目录，并且可以进入内容处理，复盘结论必须同时给出“对外内容主线判断”：

```text
产品一句话：
目标读者：
读者痛点：
对外主线：
正文能讲什么：
正文不能讲什么：
推荐首发形态：
```

不要只复述“我理解这是一个什么产品”。如果信息足够，直接把这组判断交给 `content-decomposer` 生成发布前内容判断卡和内容包。

内部验收、目录、脚本、索引、状态流转、运行记录只能作为证据，不能成为对外内容主线。

## 文件更新

必须创建或更新：

```text
workspace/{user}/runs/{run_id}/review-report.md
workspace/{user}/runs/{run_id}/learning-closure.md
workspace/{user}/indexes/content-seed-index.md
workspace/{user}/indexes/output-index.md
workspace/{user}/indexes/learning-index.md
flywheel-state.md
current-focus.md
```

按需更新：

```text
workspace/{user}/indexes/run-index.md
```

## 状态流转

根据复盘结论更新 `flywheel-state.md`。

如果可进入内容处理：

```text
current_stage: content_package
active_module: content-decomposer
next_action: 基于本轮 review-report.md 生成内容包、首发稿、产物发布说明、证据清单和反馈入口
```

如果可进入产物设计：

```text
current_stage: content_package
active_module: artifact-designer
next_action: 基于本轮 review-report.md 设计最小可领取产物；完成后回到内容包生成
```

如果需要写长期记忆：

```text
current_stage: learning_closure
active_module: flywheel-memory
next_action: 审核并写入本轮长期记忆候选
```

如果需要补充关键事实：

```text
current_stage: blocked
active_module: practice-reviewer
next_action: 等待用户补充复盘所需的关键事实
missing_requirements: 列出唯一必要事实，不要让用户填长表
```

如果实践质量不足：

```text
current_stage: practice_design
active_module: practice-designer
next_action: 基于本轮失败原因重新设计下一轮实践
```

## 输出格式

中文用户使用：

```text
当前阶段：
本轮运行编号：
事实复盘：
实践质量结论：
摩擦与发现：
内容种子：
产物机会：
长期记忆候选：
路由决策：
对外内容主线判断：
已创建/更新：
用户只需要：
```

不要让用户自己判断“这东西值不值得讲”。这是本模块的职责。

## 验收标准

本模块完成时必须满足：

1. `review-report.md` 已生成。
2. 本轮实践质量有明确结论。
3. 内容种子、产物机会、长期记忆候选分开处理。
4. 至少给出一个下一步路由。
5. 如果不能推进，明确缺少哪些关键事实。
6. 如果本轮对象是已有产品或产物，已给出对外内容主线判断。
7. `flywheel-state.md` 已更新到下一阶段。
8. 用户知道下一步由系统推进什么。
9. 已更新本轮 `learning-closure.md` 总表，且新增或保留至少一条 `closure_uuid`。
10. 已更新 `learning-index.md`。
11. 已完成经验收口：判断是否需要写入规则、索引、模板、模块行为或路线图。

## 失败模式

- 不要在未读取 `capture-report.md` 时复盘。
- 不要把内容种子写成内容草稿。
- 不要把产物机会直接当成已完成产物。
- 不要把一次性发现写入长期记忆。
- 不要输出一堆选项后停住。
- 不要把产品理解和对外内容主线判断拆成两轮重复确认。
- 不要要求用户自己判断材料价值。
- 不要复盘后不更新状态。
- 不要在未做经验收口时结束本模块。
