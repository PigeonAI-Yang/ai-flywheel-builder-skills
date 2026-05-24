# Agent Rules

本仓库是一个准备发布到 Git 的产品仓库。所有改动必须服务于 AI Flywheel Builder 的产品化。

## 工作原则

1. 先读 `README.md`、`docs/00_PRODUCT_BRIEF.md`、`docs/01_ARCHITECTURE.md`。
2. 不要把本项目写成泛泛内容方法论。
3. 每个 skill 必须有清晰职责、触发场景、输入、输出和失败边界。
4. 保持母 skill 和子 skill 职责分离。
5. 不要把所有能力塞进一个巨大的 `SKILL.md`。
6. 优先做可验证的 v0.1，而不是设计大而全系统。
7. 新增文件必须能回答：它帮助产品发布、使用、验证或版本管理中的哪一环。

## 产品边界

AI Flywheel Builder 不是：

- 选题生成器
- 写作提示词合集
- 普通个人知识库
- 一次性咨询问卷

AI Flywheel Builder 是：

- 个性化 AI 飞轮生成器
- 长期记忆维护系统
- artifact 产品化系统
- 内容与反馈回流系统

## 版本规则

- 使用 SemVer：`MAJOR.MINOR.PATCH`。
- 当前初始版本为 `0.1.0`。
- 破坏 skill 触发语义或输出契约时，至少提升 MINOR。
- 文案、拼写、说明性修正提升 PATCH。
