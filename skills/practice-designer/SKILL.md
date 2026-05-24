---
name: practice-designer
description: |
  Practice design module for AI Flywheel Builder. Use after a user's flywheel has been initialized and the next stage is choosing what small AI practice to run. It reads flywheel state, user profile, content seed library, and content pillars, then designs 1-3 concrete practices and recommends the first one.
---

# Practice Designer

## 角色

为已经完成初始化的用户设计下一轮具体 AI 实践。

本模块只处理初始化之后的“下一步实践设计”。

它回答：

```text
下一轮做什么实践，为什么做，怎么做，完成标准是什么，这个实践预计能长出什么内容和产物。
```

## 触发边界

只有同时满足以下条件时，才运行本模块：

```text
flywheel-state.md 存在
current_stage: practice_design
```

如果 `flywheel-state.md` 缺失，路由回 `flywheel-initializer`。

如果用户飞轮尚未初始化，不设计实践。

## 必读文件

按需读取：

```text
flywheel-state.md
user-flywheel-profile.md
content-seed-library.md
content-pillars.md
practice-pool.md
current-focus.md
```

`flywheel-state.md` 是机器调度依据。

`current-focus.md` 只作为人类可读摘要，不作为路由依据。

## 用户输入信号

用户可能会说：

```text
下一步做什么？
我不知道做什么实践。
帮我设计下一轮实践。
```

不要让用户自己发明实践选项。

## 实践生成方法

从以下路径生成实践：

```text
内容种子 -> 可观察小动作 -> 可验证结果 -> 可复盘材料 -> 可生成内容/产物
```

默认生成 1-3 个候选实践，并推荐其中 1 个作为第一实践。

不要默认生成 5 个候选，除非用户明确要求更多选择。

## 合格实践标准

合格实践必须同时满足：

- 有明确输入
- 有明确动作
- 有可观察结果
- 完成后能复盘
- 能长出内容主题或产物方向
- 颗粒度足够小，适合先做完再进入内容生成

时间只做粗略估算，不作为唯一硬门槛。

写法：

```text
预计用时：粗估 30-120 分钟；以实际执行复杂度为准。
```

如果 AI 无法可靠估算时间，必须说明：

```text
时间只是粗估，本实践是否合格主要看动作是否清楚、结果是否可观察。
```

拒绝以下实践：

- 太大
- 太虚
- 主要追热点
- 不来自用户画像、内容种子或内容主线
- 结果不可观察
- 无法复盘
- 与当前焦点无关

## 推荐规则

AI 必须给出默认推荐，不要把选择负担丢回用户。

用户可以回复：

```text
就做这个
换一个
缩小一点
换成更偏内容/更偏产品/更偏研究
```

不要问：

```text
你想选哪个？
```

## 输出格式

中文用户使用：

```text
当前阶段：
读取依据：
候选实践：
推荐第一实践：
为什么先做它：
执行步骤：
完成标准：
预计能长出的内容：
预计能沉淀的产物：
用户只需要：
状态更新：
```

候选实践格式：

```text
实践名：
预计用时：
输入：
动作：
可观察结果：
内容潜力：
产物潜力：
风险：
```

## 文件更新

必须更新：

```text
practice-pool.md
flywheel-state.md
```

必须创建或更新：

```text
next-practice-brief.md
```

建议同步更新：

```text
current-focus.md
```

## 状态流转

推荐第一实践后，将 `flywheel-state.md` 更新为：

```text
current_stage: practice_execution_waiting
active_module: practice-capture
next_action: 等待用户提交实践过程或结果，然后进入实践捕捉/复盘
required_inputs:
  - 过程描述
  - 结果截图
  - 生成的文件路径
  - AI 对话记录
  - 失败或卡住的地方
```

用户不需要一次性提交全部材料，有什么交什么。

材料提交后由 `practice-capture` 负责整理、归档和建立索引。不要要求用户先整理材料。

## 验收标准

本模块完成时必须满足：

1. `practice-pool.md` 已更新。
2. `next-practice-brief.md` 已生成或更新。
3. `flywheel-state.md` 已进入 `practice_execution_waiting`。
4. 用户清楚知道现在做什么、怎么做、完成后提交什么。
5. 已完成经验收口：判断是否需要写入规则、索引、模板、模块行为或路线图。

## 失败模式

- 不要在实践存在前生成内容草稿。
- 不要在实践复盘前生成可公开主张的产物。
- 不要给用户空白自检清单。
- 不要在状态已经要求实践设计时问“你想做什么实践”。
- 不要忽略 `flywheel-state.md`。
- 不要把时间估算当成判断实践是否合格的唯一依据。
- 不要在未做经验收口时结束本模块。
