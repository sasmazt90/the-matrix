---
name: commit-style
description: |
  TRIGGER when: user asks Claude Code to commit changes (git commit).
  Enforces: Conventional Commits format with type/scope/imperative subject,
  body wrapping, and issue references.
  SKIP: when user explicitly provides a full commit message in quotes.
---

# Commit Style Enforcer

Whenever the user asks to commit changes, you must produce a commit message that follows Conventional Commits.

## Format

```
<type>(<scope>): <subject>

<optional body, wrapped at 72 chars>

<optional footer with issue refs>
```

## Allowed types

| Type | Use case |
|---|---|
| `feat` | new user-facing feature |
| `fix` | bug fix |
| `chore` | tooling, build, dependencies |
| `docs` | documentation only |
| `refactor` | code change without behavior change |
| `test` | adding or updating tests |
| `perf` | performance improvement |
| `style` | formatting, no logic change |

## Subject rules

- **< 70 characters**
- **Imperative present tense** (`add` not `added`, `fix` not `fixed`)
- **No period** at the end
- **Lowercase** first letter (after the type)
- **No emojis**

## Scope

- Use the package, module, or area name
- Examples: `auth`, `db`, `api`, `ui`, `deploy`

## Body

- Wrap lines at **72 characters**
- Explain **why**, not what (the diff shows what)
- Reference issues: `Closes #123` or `Refs #456`

## Examples

### ✓ Good

```
feat(auth): add Better Auth migration

Replaces Clerk with Better Auth for self-hosted control.
Sessions invalidate; users will need to log in again.

Closes #234
```

```
fix(db): handle null in user.email lookup
```

```
chore(deps): bump next from 16.0.0 to 16.0.5
```

### ✗ Bad

- `Updated stuff` (no type, vague)
- `feat: Added new feature.` (past tense, period)
- `feat(auth): adding the new better-auth integration that replaces clerk` (too long, present continuous)
- `feat: ✨ shiny new auth!` (emoji, vague)

## Process

1. Inspect the diff: `git diff --staged` (or unstaged if nothing staged)
2. Identify the dominant type and scope
3. Draft the message
4. Show it to the user before committing
5. After approval, run: `git commit -m "..."` (use heredoc for multiline)
