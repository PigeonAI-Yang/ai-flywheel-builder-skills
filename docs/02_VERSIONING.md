# Versioning

AI Flywheel Builder uses semantic versioning.

```text
MAJOR.MINOR.PATCH
```

## Current Version

`0.1.0`

## Version Rules

### PATCH

Use PATCH for:

- typo fixes
- clearer wording
- non-breaking doc edits
- small examples

### MINOR

Use MINOR for:

- new child skill
- new template
- new workflow section
- non-breaking skill behavior expansion

### MAJOR

Use MAJOR for:

- changing the mother skill contract
- changing the core loop
- removing or renaming child skills
- changing memory schema incompatibly

## Release Checklist

Before a Git release:

1. Update `VERSION`.
2. Update `CHANGELOG.md`.
3. Update `docs/03_ROADMAP.md` if planned or deferred capabilities changed.
4. Validate all `skills/*/SKILL.md` frontmatter.
5. Run `python J:/pigeonAI/AI-flywheel-Builder/scripts/verify_learning_closure.py`.
6. Run `python J:/pigeonAI/AI-flywheel-Builder/scripts/verify_v01_acceptance.py`.
7. Check README architecture matches actual folders.
8. Tag release as `vX.Y.Z`.

## Planning Documents

- Completed changes: `J:/pigeonAI/AI-flywheel-Builder/CHANGELOG.md`
- Version rules: `J:/pigeonAI/AI-flywheel-Builder/docs/02_VERSIONING.md`
- Future roadmap and deferred capabilities: `J:/pigeonAI/AI-flywheel-Builder/docs/03_ROADMAP.md`
