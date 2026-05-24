---
name: flywheel-orchestrator
description: |
  Central orchestration skill for AI Flywheel Builder. Use after initialization when deciding what module should run next. It reads flywheel-state.md as the machine scheduling source, uses current-focus.md only as a human-readable summary, protects the active stage goal, chooses the correct child skill, and blocks locally reasonable actions that would distract from the current flywheel stage.
---

# Flywheel Orchestrator

## Role

Protect the current stage goal and route by machine state.

This skill exists because a local artifact can be reasonable while still distracting from the current flywheel objective.

Drive the flywheel workflow for the user after the flywheel has been initialized.

Do not use this skill as the first-run generator. If `flywheel-state.md` is missing or current_stage is `not_initialized` / `initializing`, route to `flywheel-initializer`.

The user should not have to think through the next step, which child skill to call, how to test it, or where memory should be written. The user provides confirmation, choices, and missing facts. The orchestrator handles stage focus, routing, and executable next actions.

Do not design artifacts directly unless that is the smallest safe action. Decide whether the next action supports the current focus, then execute it or route to the right child skill.

## Highest Priority

After initialization, this skill has highest routing priority.

Child skills are executors. They must not override `current_stage`, invent ad hoc stages, or ask the user to decide the next module when `flywheel-state.md` already defines `active_module` and `next_action`.

When a user asks "下一步是什么", "怎么推进", or "我该做什么", do not answer with a conceptual explanation. Execute the state-defined next action if it is safe.

Ask for confirmation only when the action:

- modifies product rules, skills, templates, docs, or roadmap outside the current run
- needs browser, network, login, or external platform access
- publishes, deletes, replies, likes, follows, or changes external data
- touches sensitive public/private boundaries
- requires a real user judgment that cannot be inferred

Creating or updating standard run files under `workspace/{user}/runs/{run_id}/`, `workspace/{user}/indexes/`, and `workspace/{user}/outputs/{run_id}/` is normal execution, not user homework.

## Required Input

Before recommending any action, read:

```text
workspace/{user}/flywheel-state.md
```

Then read only the supporting files required by the active module.

`current-focus.md` is human-readable. Do not use it as the authoritative routing source.

If `flywheel-state.md` is missing, do not create a piecemeal work package. Route to `flywheel-initializer` because the user needs initialization or state recovery.

## Fixed State Values

Only these `current_stage` values are valid:

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

If state contains another value, repair state before routing.

`next_action` and `missing_requirements` are mandatory. If `next_action` is empty, the flywheel is stuck and the orchestrator must repair it before advising the user.

## Input-State Relation

Before executing the old `next_action`, classify how the newest user input relates to current state.

Current state is a memory of the previous stop point. It is not allowed to override the user's newest concrete input without inspection.

Use five relation types:

```text
continue  新输入正好补齐当前状态所需材料
override  新输入给了更具体的新对象或新任务
branch    新输入有效，但用户没有要求打断当前主线
correct   用户指出当前判断、输出、状态或规则有问题
noise     情绪或无可执行信息
```

Decision rules:

- If relation is `continue`, execute the state-defined next action.
- If relation is `override`, route by the newest input, not by old state.
- If relation is `branch`, record it as a later queue unless the user says to do it now.
- If relation is `correct`, treat it as product self-feedback and update the relevant files when the user asks to fix it.
- If relation is `noise`, reduce variables and ask one smallest necessary question.

Concrete object rule:

If the newest input contains a usable object, the agent must first try to catch and process it:

```text
product
directory
skill
handbook
draft
tool
workflow
process description
screenshot
URL
feedback
error
stuck point
explicit user裁定
```

Do not say "current state is waiting for feedback" when the user has just submitted a product, directory, skill, draft, tool, workflow, or other processable object. In that case, mark relation as `override` and route to the smallest module that can produce a useful result.

Useful result rule:

If a useful result can be produced from the newest input, produce it. Only ask for more input when a specific missing fact blocks that result.

## Processed Object Reuse

When the newest input contains a processable object, check whether it already appears in:

```text
workspace/{user}/indexes/material-index.md
workspace/{user}/indexes/run-index.md
workspace/{user}/indexes/output-index.md
```

If it already exists, do not create a duplicate run unless the user explicitly asks for a new version, rewrite, new angle, new platform, or new run.

However, an already processed object still requires a useful response.

Return a minimum useful summary:

```text
产品一句话：
目标读者：
读者痛点：
对外主线：
正文能讲什么：
正文不能讲什么：
推荐首发形态：
已有主交付物：
下一步唯一动作：
```

Do not answer only with "this is already processed, send feedback next." That is a state-management answer, not a user-useful result.

If the existing output lacks these fields, synthesize the summary from `review-report.md`, `content-package.md`, and `content-flywheel-run.md` before asking for feedback.

Feedback may still be the next action, but only after the summary has made clear what the agent already produced from the user's object.

## Decision Levels

Classify the request as one of:

- Mainline: directly advances the current focus
- Supporting: helps the current focus but is not the core action
- Side branch: valid later, not now
- Drift: distracts or expands scope
- Noise: emotional overload; reduce variables first

## Routing

Use this routing table:

| Need | Route |
|---|---|
| Missing state or initialization stage | `flywheel-initializer` |
| current_stage: practice_design | `practice-designer` |
| current_stage: practice_execution_waiting and material is present | `practice-capture` |
| current_stage: practice_execution_waiting and no material is present | tell the user what material can be submitted, without asking them to fill a form |
| current_stage: practice_capture | `practice-capture` |
| current_stage: practice_review | `practice-reviewer` |
| current_stage: content_package | `content-decomposer` |
| current_stage: feedback_waiting and feedback is not present | remind the user they can submit a feedback URL or screenshot |
| current_stage: feedback_waiting and feedback URL or screenshot is present | `feedback-attributor` |
| current_stage: feedback_waiting but newest input is a processable object, not feedback | classify relation as `override` and route by newest input |
| newest processable object already exists in indexes | return processed object summary before giving next action |
| current_stage: feedback_attribution | `feedback-attributor` |
| current_stage: learning_closure | complete `learning-closure.md` and sync `learning-index.md` |
| current_stage: next_practice_ready | execute `next_action` or route to `practice-designer` |
| current_stage: blocked | ask only for `missing_requirements` |
| Define or repair machine state | stay in orchestrator |
| Update durable memory | `flywheel-memory` |
| Capture real work friction | `friction-capture` |
| Design a small artifact | `artifact-designer` |
| Decompose reviewed practice or artifact into content package | `content-decomposer` only after `review-report.md` exists or an equivalent reviewed artifact is provided |
| Attribute feedback | `feedback-attributor` |
| Judge whether an idea can enter flywheel | `flywheel-gatekeeper`, but only after checking current focus |

## Autopilot Work Package

When an initialized user says they do not know what to do, feel the process is hard to push forward, or asks "what should I do next", read `flywheel-state.md` and execute `next_action` through the correct module.

If `flywheel-state.md` already contains `next_action` and `active_module`, do not explain the workflow again. Execute or route to that module.

If the flywheel has not been initialized, do not create a work package. Route to `flywheel-initializer`.

A work package must contain:

For Chinese users:

```text
工作包：
目标：
为什么现在做：
输入：
AI 将执行：
用户只需要：
完成标准：
阻塞条件：
```

For English users:

```text
Work package:
Goal:
Why this now:
Inputs:
Actions the agent will do:
User only needs to:
Done when:
Blocked if:
```

Rules:

- Keep exactly one active work package.
- The agent owns the actions.
- The user only confirms, chooses between real options, or supplies missing facts.
- If the next action is known, execute it immediately after stating the work package.
- Do not expose internal child-skill choreography as user homework.
- The run is not complete until `flywheel-state.md` has been updated.
- Also update `current-focus.md` as a human-readable summary.

## Output

Match the user's language in output.

For Chinese users, use:

```text
当前焦点：
机器阶段：
请求分类：主线 / 支撑 / 支线 / 跑偏 / 噪音
判断：
路由：
下一步最小动作：
为什么现在做：
现在不做什么：
```

If creating a work package, append:

```text
当前工作包：
AI 将执行：
用户只需要：
完成标准：
```

For English users, use:

```text
Current focus:
Request classification: Mainline / Supporting / Side branch / Drift / Noise
Decision:
Route:
Next smallest action:
Why now:
What not to do:
```

If creating a work package, append:

```text
Active work package:
Agent will do:
User only needs to:
Done when:
```

## Rules

- Treat "what next" as a command to advance the workflow, not as a request for advice.
- Before obeying old state, classify the newest input relation as continue / override / branch / correct / noise.
- Treat "I do not know what to do" or "this feels hard to push forward" as a product failure signal. If the flywheel is already initialized, repair the workflow by executing the state-defined next action. If not, route to `flywheel-initializer`.
- When the user asks "what next", do not hand back a prompt for the user to send if the next action can be executed by the agent. Execute the smallest safe action directly.
- If the next step is a test, construct the test input yourself from current project facts, run the relevant child skill logic, and report the result.
- If the user resubmits an already processed object, return the existing processed result summary instead of only asking for feedback.
- If the user submits messy practice material, route to `practice-capture`; do not ask the user to clean, classify, or reformat it first.
- If captured material exists and state is `practice_review`, route to `practice-reviewer`; do not ask the user to decide whether it is worth writing about.
- If reviewed material exists and state is `content_package`, route to `content-decomposer`; do not ask the user to invent the content package.
- If the user submits a feedback URL or screenshot, route to `feedback-attributor`; do not ask the user to manually summarize platform feedback first.
- Ask the user only when a real choice, confirmation, or external permission is required.
- Do not let content work start during initialization.
- Do not let content work start before a practice exists or has been reviewed.
- Do not let content work start before submitted practice material has been captured and indexed.
- Do not let `content-decomposer` write the full product artifact body; route unfinished products to `artifact-designer` or a future product-building module.
- Do not let `feedback-attributor` perform platform write actions; feedback collection is read-only.
- Do not let community design overtake core product validation.
- Do not let Git/release work start before the product flow works once.
- Do not call `content-decomposer` just because an artifact exists; first ask whether content supports the current focus.
- If the user says the system has drifted, update `flywheel-state.md` first, then update `current-focus.md`.
