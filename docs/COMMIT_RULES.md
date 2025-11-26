# 📝 Commit Message Rules

## ✅ Requirements

1. **Language: English only** - All commit messages must be in English
2. **Format: Conventional Commits** - Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification
3. **Length: Max 72 characters** for subject line

## 📋 Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | A new feature | `feat(server): add C4 context diagram generation` |
| `fix` | A bug fix | `fix(tools): correct PlantUML container parsing` |
| `docs` | Documentation only changes | `docs(readme): update installation instructions` |
| `style` | Changes that do not affect the meaning of the code | `style(server): format code with black` |
| `refactor` | A code change that neither fixes a bug nor adds a feature | `refactor(client): simplify MCP request handling` |
| `perf` | A code change that improves performance | `perf(server): optimize PlantUML rendering` |
| `test` | Adding missing tests or correcting existing tests | `test(tools): add tests for C4 diagram generation` |
| `chore` | Changes to the build process or auxiliary tools | `chore(deps): update PlantUML to v1.2.0` |
| `ci` | Changes to CI configuration files and scripts | `ci(github): add automated testing workflow` |

### Scope (Optional)

Scope should be the area of the codebase affected:
- `server` - MCP server code
- `client` - MCP client code
- `tools` - Diagram generation tools
- `docs` - Documentation
- `examples` - Example files
- `scripts` - Utility scripts

### Subject

- Use **imperative, present tense**: "change" not "changed" nor "changes"
- Don't capitalize first letter
- No dot (.) at the end
- Maximum **72 characters**

### Body (Optional)

- Explain **WHAT** and **WHY** vs. HOW
- Wrap at 72 characters
- Can use multiple paragraphs
- Separate from subject with blank line

### Footer (Optional)

- Reference issues: `Closes #123`, `Fixes #456`
- Breaking changes: `BREAKING CHANGE: description`

## ✅ Good Examples

```bash
feat(server): add C4 context diagram generation

Add support for generating C4 Context diagrams using PlantUML.
The diagram shows system as single block without internal containers.

Closes #42
```

```bash
fix(tools): correct PlantUML container parsing

Fix bug where Context diagram was incorrectly showing containers
instead of single System block. Updated parser to use System()
for context diagrams.

Fixes #38
```

```bash
docs(readme): update installation instructions

Add Docker Compose setup instructions and clarify Python version
requirements.
```

```bash
refactor(client): simplify MCP request handling

Extract request parsing logic into separate function to improve
code readability and maintainability.
```

## ❌ Bad Examples

```bash
# ❌ Polish language
Naprawiono błąd w parsowaniu PlantUML

# ✅ Correct
fix(tools): correct PlantUML container parsing
```

```bash
# ❌ No type prefix
Add C4 context diagram generation

# ✅ Correct
feat(server): add C4 context diagram generation
```

```bash
# ❌ Past tense
Added C4 context diagram generation

# ✅ Correct
feat(server): add C4 context diagram generation
```

```bash
# ❌ Too long subject (over 72 characters)
feat(server): add comprehensive C4 context diagram generation with full support for all C4 model types including context, container, component and code levels

# ✅ Correct
feat(server): add C4 context diagram generation

Add support for generating C4 Context diagrams using PlantUML.
Supports all C4 model types: context, container, component, code.
```

## 🔧 Setup

### Automatic Template

Git is configured to use `.gitmessage` template:

```bash
git config commit.template .gitmessage
```

### Validation Hook

A `commit-msg` hook validates commit messages automatically:
- Checks Conventional Commits format
- Enforces English language (with warning for Polish)
- Validates subject length (max 72 characters)

The hook is located at: `.githooks/commit-msg`

**Installation:**

```bash
# Option 1: Use git config (recommended)
git config core.hooksPath .githooks

# Option 2: Manual copy
cp .githooks/commit-msg .git/hooks/commit-msg
chmod +x .git/hooks/commit-msg
```

### Manual Validation

You can test your commit message format:

```bash
echo "feat(server): add new feature" | .git/hooks/commit-msg /dev/stdin
```

## 📚 References

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Angular Commit Message Guidelines](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit)
- [Git Commit Best Practices](https://chris.beams.io/posts/git-commit/)

---

**Date:** 26 Listopada 2025  
**Status:** ✅ Active  
**Enforcement:** Git hook + manual review

