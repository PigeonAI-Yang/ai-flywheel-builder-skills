# 飞轮激活方案

## 当前母 skill

- `ai-flywheel-builder`：薄入口和路由

## 当前子 skill

| Skill | 用途 | 触发场景 |
|---|---|---|
| `flywheel-initializer` | 新用户初始化 | 没有 `flywheel-state.md`，或用户第一次建立飞轮 |
| `practice-designer` | 设计下一轮小实践 | `flywheel-state.md` 的阶段为 `practice_design` |
| `practice-capture` | 接收、归档和索引实践材料 | `flywheel-state.md` 的阶段为 `practice_execution_waiting` 且用户提交材料 |
| `practice-reviewer` | 复盘实践并决定下一步路由 | `flywheel-state.md` 的阶段为 `practice_review` |
| `flywheel-orchestrator` | 初始化后维护当前焦点 | 用户问下一步、流程卡住，或子 skill 可能导致跑偏 |
| `flywheel-memory` | 维护长期记忆 | 身份、边界、产物或规则需要长期保留 |
| `friction-capture` | 捕捉实践摩擦 | 用户描述真实工作、失败、反复困惑或 AI 协作痛点 |
| `artifact-designer` | 把摩擦转成小产物 | 摩擦重复出现、公开安全，并且 1-2 天内可做出产物 |
| `content-decomposer` | 把复盘后的实践或已有产物拆成内容包 | `flywheel-state.md` 的阶段为 `content_package`，且已有 `review-report.md` 或等价复盘材料 |
| `feedback-attributor` | 把反馈归因到迭代 | 用户收到评论、使用反馈、平台反馈或自我复盘 |
| `flywheel-gatekeeper` | 防止跑偏 | 想法太大、太虚、太敏感，或脱离真实实践 |

## 首次验证路径

1.
2.
3.

## 用户只需要做

-
