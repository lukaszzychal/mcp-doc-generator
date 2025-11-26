# Git Hooks

This directory contains git hooks for the project.

## Installation

To install the hooks, run:

```bash
git config core.hooksPath .githooks
```

Or manually copy hooks to `.git/hooks/`:

```bash
cp .githooks/commit-msg .git/hooks/commit-msg
chmod +x .git/hooks/commit-msg
```

## Hooks

### commit-msg

Validates commit messages according to:
- Conventional Commits format
- English language requirement
- Maximum 72 characters for subject line

See [docs/COMMIT_RULES.md](../docs/COMMIT_RULES.md) for details.

