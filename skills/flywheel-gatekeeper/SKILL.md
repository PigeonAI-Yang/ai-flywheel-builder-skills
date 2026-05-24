---
name: flywheel-gatekeeper
description: |
  Guard a user's AI flywheel from drift. Use when the user proposes a new idea, product, content direction, or system and needs to decide whether it belongs in the flywheel. The skill checks if it is grounded in practice, small enough, public-safe, artifact-shaped, and aligned with the user's main line.
---

# Flywheel Gatekeeper

## Role

Decide whether a new idea should enter the flywheel.

The goal is not to kill ideas. The goal is to shrink or redirect them until they can become a useful artifact.

This skill is a local gate, not the global orchestrator. Before using it, check `flywheel-orchestrator` or the current focus. A locally valid artifact can still be `Park for later` if it distracts from the active stage.

## Gate

Ask:

1. Is this grounded in real practice?
2. Can it become a small artifact?
3. Can v0.1 ship in 1-2 days?
4. Is it public-safe?
5. Does it support the user's main line?
6. Can it produce at least 3 content angles?
7. Does it advance the current focus right now?

## Output

Match the user's language in output.

For Chinese users, return one of:

- 进入飞轮
- 先缩小
- 暂停，稍后再做
- 拒绝

For English users, return one of:

- Enter flywheel
- Shrink first
- Park for later
- Reject

Always include the next smallest action.

If an idea is valid but not aligned with the current focus, return `Park for later`.
