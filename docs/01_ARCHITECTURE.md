# Architecture

## System Shape

AI Flywheel Builder uses a thin mother skill, a state orchestrator, and stage-specific child skills.

```text
ai-flywheel-builder       # entry and routing
  -> flywheel-initializer # new-user initialization
  -> practice-designer    # next practice design
  -> practice-capture     # material intake and indexing
  -> practice-reviewer    # practice review and routing decision
  -> content-decomposer   # content package generation
  -> feedback-attributor  # feedback collection and attribution
  -> flywheel-orchestrator
  -> future content-producer
  -> future asset-builder
```

## Mother Skill

`ai-flywheel-builder` is a thin entry and routing skill.

It owns:

- entry classification
- state inspection
- routing to the correct module
- final sanity checks

It does not own detailed initialization, practice design, content drafting, asset building, or feedback integration.

## State Model

Use two state surfaces:

```text
flywheel-state.md  # machine scheduling state
current-focus.md   # human-readable focus summary
```

`flywheel-state.md` is authoritative for routing. `current-focus.md` must not be used as the machine state source.

### Fixed State Values

`current_stage` is a fixed enum. V0.1 allows only:

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

Each state file must include:

```text
current_stage
active_module
next_action
missing_requirements
```

If `next_action` is empty, the system is stuck. The orchestrator repairs state before giving advice.

## Initializer

`flywheel-initializer` owns the first-run experience:

```text
layered interview -> user model -> flywheel blueprint -> one confirmation -> batch initialization
```

It creates or updates:

- `flywheel-state.md`
- `current-focus.md`
- `user-flywheel-profile.md`
- `content-seed-library.md`
- `content-pillars.md`
- `artifact-registry.md`
- `feedback-log.md`
- `memory-rules.md`
- `activation-plan.md`

It must not generate content or self-check lists during initialization.

## Practice Designer

`practice-designer` runs after initialization when the state asks for the next practice.

It reads:

- `flywheel-state.md`
- `user-flywheel-profile.md`
- `content-seed-library.md`
- `content-pillars.md`
- `practice-pool.md`

It outputs:

- 1-3 candidate practices
- one recommended first practice
- execution steps
- completion criteria
- expected content potential
- expected asset potential

It updates `flywheel-state.md` to `practice_execution_waiting`.

Practice quality is judged mainly by clear input, clear action, observable result, reviewability, and ability to produce content or product direction. Time is only a rough estimate, not the sole gate.

## Practice Capture

`practice-capture` runs after a user submits any material for a designed practice.

It accepts messy submissions:

- process description
- file path
- directory path
- screenshot description
- AI conversation
- failure or stuck point
- draft
- feedback

It creates:

- `run_id`
- `workspace/{user}/runs/{run_id}/run.md`
- `workspace/{user}/runs/{run_id}/materials.md`
- `workspace/{user}/runs/{run_id}/capture-report.md`

It updates:

- `workspace/{user}/indexes/run-index.md`
- `workspace/{user}/indexes/material-index.md`
- `flywheel-state.md`

It does not generate content. It advances state to `practice_review`.

## Practice Reviewer

`practice-reviewer` runs after `practice-capture`.

It reads:

- `workspace/{user}/runs/{run_id}/capture-report.md`
- `workspace/{user}/runs/{run_id}/materials.md`
- `workspace/{user}/indexes/run-index.md`
- `workspace/{user}/indexes/material-index.md`
- `memory-rules.md`

It outputs:

- factual practice review
- practice quality conclusion
- friction and discoveries
- content seeds
- product opportunities
- long-term memory candidates
- one next route

It creates:

- `workspace/{user}/runs/{run_id}/review-report.md`

It updates:

- `workspace/{user}/indexes/content-seed-index.md`
- `workspace/{user}/indexes/output-index.md`
- `flywheel-state.md`
- `current-focus.md`

It does not write content or build products. It decides what should happen next.

## Long-Term Management

The flywheel stores practice material in three layers:

```text
raw material references -> structured run records -> durable memory candidates
```

Use this workspace structure:

```text
workspace/{user}/
  runs/
  materials/
  indexes/
  memory/
  outputs/
```

Indexes are mandatory because the product should become easier to use over time. Each run, material, content seed, and output must be traceable by `run_id`.

## Learning Closure

Every module run must end with a learning closure check.

Every real `run_id` directory must contain:

```text
workspace/{user}/runs/{run_id}/learning-closure.md
```

Each `learning-closure.md` is a per-run closure table. It can contain multiple closure records, and each record must have a `closure_uuid` in UUID format.

Use three identifiers:

```text
run_id       # human-readable run identifier
run_uuid     # stable machine identifier for the run
closure_uuid # stable identifier for one learning closure record
```

Even when no durable lesson is written, the file must exist, contain a `closure_uuid`, and explain why no long-term learning was stored.

Every closure record must also be indexed in:

```text
workspace/{user}/indexes/learning-index.md
```

Purpose:

```text
Each practice, failure, feedback item, and correction should reduce future repeated mistakes.
```

The agent asks internally:

1. Did this run expose a repeated problem?
2. Did this run create a new avoidance rule?
3. Did this run reveal a missing template field?
4. Did this run require module behavior to change?
5. Did this run reveal a valuable future capability that should enter the roadmap?

The agent persists lessons only when at least one gate is true:

- problem repeated
- user explicitly裁定 it
- workflow was blocked
- future judgment changes
- template or module defect appeared
- platform or tool limitation appeared

Write targets:

- durable rule -> `memory-rules.md`
- searchable case -> `run-index.md`, `material-index.md`, or `feedback-index.md`
- learning closure index -> `learning-index.md`
- missing field -> `templates/*.md`
- module behavior -> `skills/*/SKILL.md`
- deferred capability -> `docs/03_ROADMAP.md`

If no lesson qualifies, the module may state that no durable learning was written. Conversation-only learning is not enough.

## Content Flywheel Principle

The main loop is:

```text
初始化：用户画像 -> 内容种子库 -> 内容主线 -> 产物方向 -> 反馈机制 -> 记忆更新规则 -> 机器状态
运行：实践设计 -> 实践过程 -> 内容 -> 产物 -> 反馈 -> 状态更新 -> 下一轮实践
```

Existing results such as apps, skills, handbooks, workflows, or product directories are not the whole product. They are practice objects that can become:

- content material
- claimable assets
- feedback entry points
- next-version questions

## Orchestration Principle

The user does not drive the workflow. The system drives the workflow.

The user provides confirmation, choices, and missing facts. The orchestrator reads `flywheel-state.md`, chooses the next child skill, executes safe next actions, and asks the user only when judgment or permission is required.

After initialization, `flywheel-orchestrator` has highest routing priority. Child skills execute local work; they do not override machine state or invent new stages.

When the user asks "what next", the default behavior is to execute the state-defined next action. Ask for confirmation only when an action changes product rules or files outside the current run, needs external access, publishes or deletes data, touches sensitive boundaries, or requires a real user judgment.

## Visible Delivery

Each practice run must create a user-visible main delivery:

```text
workspace/{user}/outputs/{run_id}/content-flywheel-run.html
```

Markdown may still exist as an editable source or backstage draft:

```text
workspace/{user}/outputs/{run_id}/content-flywheel-run.md
```

Backstage files, indexes, and templates cannot replace this main delivery.

The HTML delivery uses a pluggable theme policy:

```text
default theme -> workspace-safe HTML output
optional local design skill/theme -> user-specified branded output
fallback -> default theme
```

The bundled default theme lives at:

```text
J:/pigeonAI/AI-flywheel-Builder/themes/default-html-report/
```

PigeonAI / 雾灯会 presentation design is an optional author theme, not a core open-source dependency. If that local design skill is unavailable, the system must still generate `content-flywheel-run.html` with the default theme.

The minimum sections are:

- 本轮实践一句话
- 为什么值得讲
- 可发布内容草稿
- 配套可领取产物
- 证据与边界
- 反馈入口
- 下一轮实践

V0.1 acceptance uses three checks:

1. The user does not need to ask "then what?"
2. There is one absolute-path main delivery.
3. The run directory, indexes, and learning closure are all closed.

## Decision Persistence

Accepted design decisions must be written into the project.

If the user裁定 a module boundary, state transition, file responsibility, output standard, naming rule, or acceptance standard, the decision must be recorded in at least one relevant file:

- runtime behavior -> corresponding `skills/*/SKILL.md`
- product understanding -> `README.md`, `docs/00_PRODUCT_BRIEF.md`, or `docs/01_ARCHITECTURE.md`
- generated file shape -> `templates/*.md`

Conversation-only decisions are not durable and must not be treated as finished product work.

## Child Skills

### flywheel-orchestrator

Runs after the user's flywheel has been initialized. It reads machine state and routes work before child skills run:

- reads `flywheel-state.md`
- updates `current-focus.md` only as a human-readable summary
- classifies requests as mainline/supporting/side branch/drift/noise
- blocks locally reasonable actions that distract from current product validation
- decides which child skill should run next

All child skills should be treated as local executors. The orchestrator owns sequencing.

The orchestrator is not the first-run generator. If `flywheel-state.md` is missing or points to initialization, route to `flywheel-initializer`.

### flywheel-memory

Maintains long-term memory:

- identity
- public boundaries
- output registry
- validated rules

V0.1 stores only durable memory that affects future decisions. It does not archive chat logs or general content history.

### friction-capture

Extracts usable material from daily practice:

- repeated pain
- failure modes
- AI mistakes
- manual workflows
- public-safe angles

### artifact-designer

Turns one friction into a small product:

- skill
- handbook
- checklist
- template
- script
- case library

### content-decomposer

Turns one reviewed practice or existing product asset into a content package:

- primary content theme
- 3-5 alternative topics
- first publishable draft
- product launch or claim note
- proof list
- pre-publish risk check
- feedback questions

It does not write the full product artifact itself. If the product body is not ready, route to `artifact-designer` or a future product-building module first.

It runs when:

```text
current_stage: content_package
active_module: content-decomposer
```

It requires `review-report.md` or an equivalent reviewed artifact. It must not run directly on raw unreviewed material.

### feedback-attributor

Collects and attributes feedback after content or product output is published or shared.

It supports two input modes:

- URL first: use browser read-only collection on a user-provided feedback, analytics, comment, private message, or risk notice page.
- Screenshot fallback: read screenshots when URL access fails, login state is unavailable, or platform restrictions block collection.

URL collection has a fixed fallback path:

1. Read visible feedback when the page opens.
2. If login state is unavailable, ask for screenshots.
3. If comments or metrics are incomplete, record partial data and ask for screenshots or a backend URL.
4. If platform restrictions block reading, stop trying and fall back to screenshots.
5. If feedback cannot be associated with `run_id` or `output_id`, mark it as unassigned.

Every URL collection should keep an evidence screenshot. If screenshot capture is not possible, record URL, collection time, page title, key data summary, and failure reason.

It classifies feedback into:

- noise
- observation signal
- valid signal

It attributes valid signals to:

- content expression
- content topic
- target reader mismatch
- product understanding
- product usage
- platform/risk issue
- next practice opportunity
- useful validation

It must associate feedback with `run_id` or `output_id` when possible. If not possible, mark it as unassigned instead of dropping it.

It is read-only. It must not post, delete, reply, like, follow, or change platform settings.

### flywheel-gatekeeper

Prevents drift:

- idea too large
- idea too vague
- idea too sensitive
- idea not based on practice
- no concrete output

## Memory Files

Use templates in `templates/` as the first local memory format:

- `user-flywheel-profile.md`
- `flywheel-state.md`
- `content-seed-library.md`
- `content-pillars.md`
- `artifact-registry.md`
- `current-focus.md`
- `memory-rules.md`
- `friction-log.md`
- `feedback-log.md`
- `activation-plan.md`
- `practice-submission.md`
- `reverse-validation-report.md`
- `run-index.md`
- `material-index.md`
- `content-seed-index.md`
- `output-index.md`
- `feedback-index.md`
- `learning-index.md`
- `run.md`
- `materials.md`
- `capture-report.md`
- `review-report.md`
- `content-package.md`
- `feedback-report.md`
- `learning-closure.md`
