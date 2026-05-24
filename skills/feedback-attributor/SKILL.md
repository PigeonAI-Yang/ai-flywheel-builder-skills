---
name: feedback-attributor
description: |
  Collect and attribute feedback for AI Flywheel Builder after content or product output is published or shared. Use when the user provides a feedback URL, analytics page, comment page, private message page, risk notice page, screenshots, metrics, comments, or usage feedback and wants the system to read, classify, distinguish noise from signal, update feedback indexes, and route the next flywheel step. Supports URL/browser read-only collection first and screenshot/manual collection as fallback.
---

# Feedback Attributor

## 角色

把内容或产物发布后的外部反应，转成下一轮飞轮动力。

本模块负责：

```text
采集反馈 -> 关联 run_id/output_id -> 区分噪音/观察信号/有效信号 -> 归因 -> 更新索引 -> 推进下一步
```

本模块不负责发布内容、不回复评论、不修改平台设置。

本模块也负责 AI Flywheel Builder 自身的产品反馈归因。

当用户反馈本 skill 难用、跑偏、采集失败、截图失败、模块判断错误、状态流转卡住或输出不符合预期时，必须把它当成产品反馈处理，而不是只解释原因。

处理路径：

```text
用户反馈 -> 归因 -> 判断是否修改 skill/template/docs/roadmap -> 写入文件或记录为暂缓能力
```

## 双入口

反馈提交有两种方式，必须主动提醒用户：

```text
方式 1：发反馈页面地址。AI 用浏览器只读打开页面，复用用户登录态，读取可见反馈。
方式 2：发截图。页面打不开、登录态不可用或平台限制时，AI 读取截图里的数据和评论。
```

优先使用方式 1。

方式 1 失败时，切换方式 2。

## URL 采集降级规则

URL 采集必须按固定顺序处理，不要胡乱尝试。

1. 能打开页面并读取可见反馈：直接采集。
2. 页面需要登录但无法复用用户登录态：停止浏览器采集，提示用户发截图。
3. 页面能打开但评论、数据或后台指标加载不完整：记录已采集部分，并提示用户补充截图或后台页 URL。
4. 平台限制浏览器自动读取、页面反复跳转、内容不可见：停止尝试，改用截图兜底。
5. 采集结果无法关联 `run_id` 或 `output_id`：标记为 `未归属反馈`，但不丢弃。

URL 采集失败时，必须在 `feedback-report.md` 记录失败原因和降级方式。

## 浏览器采集边界

浏览器采集只能做只读动作：

- 打开用户提供的 URL
- 读取页面可见数据
- 截图留证
- 提取评论、指标、风险提示
- 记录来源 URL 和采集时间

禁止：

- 发布内容
- 删除内容
- 回复评论或私信
- 点赞、关注、收藏
- 修改账号、隐私、平台设置
- 保存账号密码
- 绕过平台权限或反爬限制

如果页面要求登录且无法复用用户登录态，提示用户改用截图。

## 证据留存

每次 URL 采集默认必须保存一张证据截图。

证据记录至少包含：

- URL
- 采集时间
- 页面标题
- 证据截图路径
- 关键数据摘要

如果无法保存截图，必须至少记录：

- URL
- 采集时间
- 页面标题
- 关键数据摘要
- 无法截图原因

证据截图路径必须使用绝对路径。

## 用户提交最小格式

首选：

```text
这是反馈页：URL
对应内容/产物是：run_id 或 output_id 或标题
```

兜底：

```text
这是反馈截图
对应内容/产物是：run_id 或 output_id 或标题
```

如果用户只给 URL 或截图但没有关联对象，先尝试从页面标题、内容标题、发布位置和索引中匹配。

匹配不到时，标记为：

```text
未归属反馈
```

但不要中断采集。

## 必读文件

按需读取：

```text
flywheel-state.md
current-focus.md
workspace/{user}/indexes/run-index.md
workspace/{user}/indexes/output-index.md
workspace/{user}/indexes/feedback-index.md
workspace/{user}/feedback-log.md
memory-rules.md
```

如果反馈关联到某一轮运行，也读取：

```text
workspace/{user}/runs/{run_id}/content-package.md
workspace/{user}/runs/{run_id}/review-report.md
```

## 采集内容

从 URL 或截图中尽量提取：

- 平台
- 页面 URL 或截图位置
- 页面标题
- 证据截图路径
- 内容标题
- 发布时间或反馈时间
- 浏览/播放
- 点赞
- 收藏
- 评论
- 转发
- 完播率或阅读完成率
- 私信/领取/试用/下载
- 典型评论
- 高频问题
- 平台风险提示：扣分、限流、违规、审核提示

采集不到的字段留空，不要编造。

## 信号判定

反馈结论只能三类：

```text
噪音
观察信号
有效信号
```

判断维度：

1. 来源相关性：是不是目标用户或潜在用户
2. 行为强度：只是浏览/点赞，还是收藏、评论、私信、领取、试用、转发
3. 具体程度：是否说清楚有用点、困惑点、需求点或风险点
4. 重复程度：是否多人反复提到同一问题
5. 决策价值：是否影响内容、产物、定位、平台或下一轮实践
6. 可行动性：是否能推出明确下一步

### 有效信号

满足任一类可判为有效信号：

- 目标用户提出具体问题
- 多人重复提到同一个点
- 用户产生强行为：收藏、私信、领取、试用、转发
- 平台给出明确风险提示：扣分、限流、违规、审核
- 反馈直接暴露内容没讲清、产物不会用、定位不匹配

### 噪音

以下通常是噪音：

- 单条情绪化评价
- 非目标用户的随口意见
- 没有上下文的点赞或差评
- 与本轮内容或产物无关的评论
- 无法行动的泛泛反馈，例如“不错”“没意思”
- 没有内容证据的平台随机波动

### 观察信号

以下进入观察池：

- 只有 1 条但很具体
- 数据异常但原因不明
- 有兴趣但未产生强行为
- 方向可能有价值但证据太少

观察信号只记录，不立刻改变飞轮方向。重复出现后再升级。

## 归因类型

每条有效信号必须归因到至少一类：

- 内容表达问题
- 内容选题问题
- 目标读者不匹配
- 产物理解问题
- 产物使用问题
- 发布平台/风险问题
- 下一轮实践机会
- 有效验证

AI Flywheel Builder 自身反馈还可以归因到：

- 模块规则缺陷
- 平台适配缺陷
- 模板字段缺陷
- 状态流转缺陷
- 文档说明缺陷
- 工具能力限制
- 路线图候选能力

如果是模块规则缺陷，修改对应 `skills/*/SKILL.md`。

如果是报告或索引字段缺陷，修改对应 `templates/*.md`。

如果是产品理解或使用说明缺陷，修改 `README.md`、`docs/00_PRODUCT_BRIEF.md` 或 `docs/01_ARCHITECTURE.md`。

如果是暂不实现的后续能力，写入 `docs/03_ROADMAP.md`。

## 文件更新

必须创建或更新：

```text
workspace/{user}/runs/{run_id}/feedback-report.md
workspace/{user}/runs/{run_id}/learning-closure.md
workspace/{user}/indexes/feedback-index.md
workspace/{user}/indexes/output-index.md
workspace/{user}/indexes/learning-index.md
workspace/{user}/feedback-log.md
flywheel-state.md
current-focus.md
```

如果反馈未归属，写入：

```text
workspace/{user}/indexes/feedback-index.md
```

并标记 `run_id/output_id: 未归属`。

## 状态流转

根据归因结论推进状态。

内容表达或选题需要迭代：

```text
current_stage: next_practice_ready
active_module: content-decomposer
next_action: 基于反馈报告迭代内容包或下一篇内容
```

产物理解或使用问题：

```text
current_stage: next_practice_ready
active_module: artifact-designer
next_action: 基于反馈报告改进最小产物说明、结构或使用路径
```

定位或长期规则变化：

```text
current_stage: learning_closure
active_module: flywheel-memory
next_action: 审核反馈中形成的长期记忆候选
```

平台风险问题：

```text
current_stage: blocked
active_module: flywheel-gatekeeper
next_action: 基于平台风险反馈调整公开表达边界
missing_requirements: 需要用户确认的公开边界或平台限制
```

出现下一轮实践机会：

```text
current_stage: next_practice_ready
active_module: practice-designer
next_action: 基于反馈暴露的新机会设计下一轮实践
```

反馈不足：

```text
current_stage: feedback_waiting
active_module: feedback-attributor
next_action: 等待更多反馈；用户可提交反馈页面 URL 或截图
```

AI Flywheel Builder 自身需要修正规则：

```text
current_stage: learning_closure
active_module: feedback-attributor
next_action: 根据产品反馈修改对应 skill、模板、文档或路线图
```

## 输出格式

中文用户使用：

```text
当前阶段：
反馈提交方式：
已采集反馈：
关联对象：
信号判定：
归因结论：
有效信号：
观察信号：
噪音：
长期记忆候选：
产品自我迭代结论：
状态更新：
已创建/更新：
用户只需要：
```

`用户只需要` 必须提醒两种反馈提交方式：

```text
你后续可以直接发反馈页 URL；如果页面打不开，也可以发截图。
```

## 验收标准

本模块完成时必须满足：

1. 反馈已尽量关联到 `run_id` 或 `output_id`，无法关联则标记未归属。
2. 反馈采集来源明确：URL / 截图 / 用户粘贴 / 指标描述。
3. URL 采集已保存证据截图；无法保存时已记录 URL、采集时间、页面标题、关键数据摘要和失败原因。
4. URL 采集失败时已记录降级原因和兜底方式。
5. 噪音、观察信号、有效信号已区分。
6. 有效信号已归因到内容、产物、定位、平台或下一轮实践。
7. 需要写入长期记忆的候选已单独列出。
8. 如果反馈对象是 AI Flywheel Builder 自身，已归因到模块缺陷、平台适配缺陷、模板缺陷、状态流转缺陷、文档缺陷、工具能力限制或路线图候选能力。
9. `feedback-index.md` 和 `feedback-report.md` 已更新。
10. `flywheel-state.md` 已推进到明确下一步。
11. 用户知道以后可以用 URL 或截图提交反馈。
12. 已更新本轮 `learning-closure.md` 总表，且新增或保留至少一条 `closure_uuid`。
13. 已更新 `learning-index.md`。
14. 已完成经验收口：判断是否需要写入规则、索引、模板、模块行为或路线图。

## 失败模式

- 不要把所有评论都当成有效反馈。
- 不要因为单条情绪反馈改变方向。
- 不要在未关联 `run_id/output_id` 时丢弃反馈。
- 不要只总结反馈而不推进状态。
- 不要执行任何平台写操作。
- 不要保存账号密码。
- 不要把观察信号直接升级成长期记忆。
- 不要在 URL 采集失败后反复盲试；按降级规则转截图或后台页。
- 不要省略 URL 采集的证据记录。
- 不要把用户对 AI Flywheel Builder 自身的反馈当成普通聊天抱怨。
- 不要只解释产品问题而不判断是否需要修改项目文件。
- 不要在未做经验收口时结束本模块。
