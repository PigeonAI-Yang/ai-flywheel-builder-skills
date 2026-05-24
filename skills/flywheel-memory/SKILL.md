---
name: flywheel-memory
description: |
  Maintain long-term memory for a user's AI flywheel. Use when important identity, positioning, practice fields, artifacts, feedback, public boundaries, or validated rules should be saved, updated, or checked against prior memory. Trigger on "remember this for my flywheel", "update my flywheel memory", "what should be written into memory", or when a new durable rule emerges.
---

# Flywheel Memory

## Role

Keep only durable memory that improves future flywheel decisions.

Do not save chat logs. Do not summarize the conversation. Save only memory that will change future artifact, content, positioning, or boundary decisions.

## Memory Types

V0.1 only maintains four memory types:

1. Identity Memory
   - who the user is
   - what kind of creator/operator they want to become
   - their current main line

2. Boundary Memory
   - what can be public
   - what must stay private
   - how to abstract sensitive work into public-safe methods

3. Artifact Memory
   - active artifacts
   - artifact status
   - next step for each artifact

4. Rule Memory
   - validated long-term rules
   - evidence for the rule
   - when the rule applies

Ignore content history, feedback logs, and friction logs unless they create or update one of these four memory types.

## Default Memory Files

For the first user case, use:

```text
workspace/pigeon-yang/user-flywheel-profile.md
workspace/pigeon-yang/artifact-registry.md
```

Future optional files:

```text
workspace/pigeon-yang/friction-log.md
workspace/pigeon-yang/feedback-log.md
workspace/pigeon-yang/rules.md
```

## Decision Gate

Before writing memory, ask:

1. Will this still matter in 2 weeks?
2. Does this affect future artifact or content decisions?
3. Is it stable enough, or should it be marked as provisional?
4. Does it conflict with old memory?

If the answer is not clearly useful, return `ignore`.

## Conflict Handling

Do not silently overwrite old memory.

If new information conflicts with old memory:

1. quote or summarize the old memory
2. state the new information
3. mark the action as `conflict`
4. ask for confirmation before editing

## Workflow

### Step 1: Read Current Memory

Before proposing a write, read the relevant memory file if available.

### Step 2: Classify

Classify the new information as:

- identity
- boundary
- artifact
- rule
- ignore

### Step 3: Gate

Apply the four decision questions.

### Step 4: Propose

Output a memory update proposal. Do not edit files until the user confirms, unless the user explicitly asks you to update memory now.

### Step 5: Apply

When confirmed, update the target file with the smallest possible change.

## Output

Match the user's language in output. For Chinese users, use:

```text
记忆类型：
建议写入：
动作：新增 / 更新 / 冲突 / 忽略
目标文件：
为什么重要：
是否需要确认：是 / 否
```

For English users, use:

```text
Memory type:
Proposed entry:
Action: add / update / conflict / ignore
Target file:
Why it matters:
Needs confirmation: yes / no
```

## Failure Modes

- Do not write every interesting sentence into memory.
- Do not store raw chat history.
- Do not turn temporary emotions into stable identity.
- Do not overwrite boundaries casually.
- Do not expand beyond the four v0.1 memory types unless the user asks.
