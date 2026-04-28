## Objective
Set up a **complete, correct documentation structure** and **hierarchical AGENTS.md system** for this project based on `./dev/plans/0-init-plan.md` that we worked on together.

This ensures from day one:
- AI agents have precise, contextual instructions
- Documentation is complete and correctly structured
- The project scales without documentation debt
- Compatibility with all major AI coding assistants

---

## Todo now

### 1. Initialize Project Structure

### 2. Create Root-Level `AGENTS.md` FIRST

This is the foundational file. Create it **before writing any code**.

#### Required Sections:

```markdown
# AGENTS.md — Root Project Rules for [Project Name]

This is the canonical, repo-wide instruction file for AI agents working on **[Project Name]**.

## Hierarchical Context Model

Agents **must** follow this rule:

> When working inside a directory, load the nearest `AGENTS.md` file and merge it with parent `AGENTS.md` files up to root.  
> Local rules override global rules.

Context resolution order (highest priority first):
1. `AGENTS-[module].md` in module directories — module-specific context
2. `AGENTS.md` in current working directory (if present)
3. Root `AGENTS.md` — global project rules

---

## Project Overview

**[Project Name]** is [1-2 sentence description].

[Optional: longer description, goals, target audience]

---

## Language and Naming Conventions

---

## Tech Stack

---

## Coding Guidelines

1. **[Rule 1]** — [description]
2. **[Rule 2]** — [description]

## Documentation Standards

- **Every module must have a corresponding `AGENTS-[module].md` file.**
- **Every command must have documentation in `docs/man/[command].md`.**
- **Help text must include concrete examples.**
- **Options with restricted values MUST document all valid values.**

Format: `Example: --language fr` or `Example: -n 30,80`

---

## Commit Message Format

Use [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`

---

## What to Avoid

- Do not use [deprecated libraries]
- Do not add [unnecessary dependencies]
- Do not [anti-pattern 1]
- Do not [anti-pattern 2]

---

## Module-Level AGENTS Files

The following module-specific AGENTS files are located in their respective directories:

| Module | AGENTS File | Documentation |
|---|---|---|
| [module1] | `AGENTS-[module1].md` | `docs/man/[module1].md` |
| [module2] | `AGENTS-[module2].md` | `docs/man/[module2].md` |

(Update this table as new modules are added)

---


## Dependency and Inheritance Map

```
Root AGENTS.md (global rules)
    │
    │
    └── Future: AGENTS.md in any subdirectory (local context)
```

Local rules override global rules. Module-level files focus on domain-specific behavior, constraints, and invariants.
```


### 4. Module-Level AGENTS.md Template

template for creating module-level AGENTS.md files:

```markdown
# AGENTS-[module].md — [Module Name] Agent Instructions

## Summary
[1-2 sentence description of the module]

## Purpose and Expected Behavior
[What it does, subcommands, key behavior patterns]

## Constraints and Invariants
- [Database constraints, security rules, invariants]
- [Dependencies that must be present]
- [State management rules]

## Input/Output Expectations

## Documentation Reference

## Domain-Specific Rules for Agents
- [How to modify this module safely]
- [Patterns to follow]
- [Integration points with other modules]
- [Migration rules for schema changes, if applicable]
```

## Requirements

### A. Create AGENTS.md BEFORE Code
> The root `AGENTS.md` must be created **before** any substantial code is written.  
> This ensures the agent has context from the first line of code.

### B. Hierarchical Context Model
Specify in root-level ./AGENTS.md that agents must follow this rule:

> When working inside a directory, load the nearest `AGENTS.md` file and merge it with parent `AGENTS.md` files.  
> Local rules override global rules.  
> Most specific context wins.

### C. No Duplication
- Root AGENTS.md: Global rules only
- Module AGENTS files: Module-specific rules only
- No copying of global rules into module files

### E. Clarity and Determinism
All files must be:
- Declarative
- Concise
- Machine-readable
- Unambiguous
- Consistent in terminology

### F. Maximum Compatibility
The generated structure must work with:
- **GitHub Copilot** (reads AGENTS.md files automatically)
- **Claude / Cursor / Opencode** (hierarchical context loading)
- **MCP-based agents** (via context resolution protocol)
- **Any LLM-driven coding assistant**

---

## Deliverables

You must produce:

1. **Complete directory structure** — All folders created
2. **Root `AGENTS.md`** — Canonical project-wide instruction file
4. **Module-level `AGENTS-[module].md` templates** — Ready to fill for each module
6. **`.gitignore`** — Appropriate for the tech stack
7. **`README.md`** — Human-readable project overview
8. **Dependency and Inheritance Map** — ASCII diagram in root AGENTS.md

