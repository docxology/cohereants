# docs/ — Project Documentation

> **Operational rulebook** for the `cohereants` biomimetic IR sensor engineering project

**Quick Reference:** [Agent Instructions](agent_instructions.md) | [Architecture](architecture.md) | [Testing](testing_philosophy.md) | [Rendering](rendering_pipeline.md) | [Style](style_guide.md) | [Syntax](syntax_guide.md) | [Index](AGENTS.md)

## Purpose

The `docs/` directory holds behavioral and architectural rules for modifying **cohereants** — a computational study of insect infra-red perception and biomimetic sensor design, adapted into the Research Project Template's two-layer architecture. Every document here is a hard constraint for agents and contributors working in the private project tree.

**Canonical source:** `path/to/cohereants/`

**Template symlink (WIP, passive):** `template/projects_in_progress/cohereants` → private `passive/cohereants`. The project is **not** in default `discover_projects()` scope while it remains passive; pipeline commands still use `--project cohereants` and `resolve_project_root()` finds the WIP tree when the symlink is present.

## Contents

| File | Purpose | Audience |
| --- | --- | --- |
| [`agent_instructions.md`](agent_instructions.md) | Hard rules for AI agents; verification checklist | AI agents, developers |
| [`architecture.md`](architecture.md) | Domain module map, layer boundaries, forbidden patterns | Developers |
| [`testing_philosophy.md`](testing_philosophy.md) | Zero-mock policy, coverage gate (≥90%), known upstream mock debt | Developers, testers |
| [`rendering_pipeline.md`](rendering_pipeline.md) | Analysis → variables → PDF; WIP path resolution | Content authors, developers |
| [`style_guide.md`](style_guide.md) | Understated engineering prose; thin orchestrator; show-not-tell | Developers, manuscript authors |
| [`syntax_guide.md`](syntax_guide.md) | `{{TOKEN}}` manuscript variables, `\Cref{fig:…}` figure protocol | Content authors |
| [`output_conventions.md`](output_conventions.md) | `output/figures`, `output/data`, registries, regeneration | Developers |
| [`troubleshooting.md`](troubleshooting.md) | Symptom-driven fixes for tests, analysis, render | Developers |
| [`quickstart.md`](quickstart.md) | Passive/WIP note; minimal commands with `--project cohereants` | New users |
| [`faq.md`](faq.md) | Recurring questions on architecture, testing, claims | All |
| [`AGENTS.md`](AGENTS.md) | Technical index of this `docs/` folder | Developers, agents |

## Quick Navigation

### Before Modifying Any Code

1. Read **[Agent Instructions](agent_instructions.md)**
2. Read **[Architecture](architecture.md)**
3. Read **[Testing Philosophy](testing_philosophy.md)**

### Before Editing Manuscript Files

1. Read **[Rendering Pipeline](rendering_pipeline.md)**
2. Read **[Syntax Guide](syntax_guide.md)**
3. Read **[../manuscript/AGENTS.md](../manuscript/AGENTS.md)** — figure tokens, VAR tokens, engineering claim policy

### Before Writing Source Code

1. Read **[Style Guide](style_guide.md)**

## Lifecycle and confidentiality

| Location | Role |
| --- | --- |
| `projects/passive/cohereants/` (private repo) | Canonical git history — commit here |
| `template/projects_in_progress/cohereants` | Symlink for local pipeline inspection |
| `projects/cohereants` under public `template/` | Must never be committed |

Promote to `active/` in the private lifecycle repo only when the project should enter default discovery and rendering.

## Verification Commands

From the **template** checkout (with symlink synced):

```bash
# Authoritative project test gate (90% on src/)
uv run python scripts/01_run_tests.py --project cohereants --project-only

# Direct gate inside the project tree
cd projects_in_progress/cohereants   # or passive/cohereants in private repo
MPLBACKEND=Agg .venv/bin/python -m pytest tests/ --cov=src --cov-fail-under=90 -q
```

## See Also

- [../AGENTS.md](../AGENTS.md) — Project-level agent guide
- [../README.md](../README.md) — Project overview and domain module table
- [../ISA.md](../ISA.md) — Ideal-State Artifact (system of record)
- [../manuscript/AGENTS.md](../manuscript/AGENTS.md) — Manuscript editing protocol
