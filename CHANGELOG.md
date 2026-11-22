# Changelog

## 1.1.0 (22 November 2026)

- Trigger-based skill description ("Use when asked to...") that fits claude.ai's 200-character limit.
- New output format section for the rewrite, write and review modes.
- New examples/examples.md with finished rewrites and a review in English and Arabic, generated from the tested cases.
- README.md inside the skill folder, for marketplaces that show the skill on its own.

## 1.0.0 (22 November 2026)

First public release.

- Skill instructions with three modes: rewrite, write and review.
- Pattern catalog adapted from Wikipedia's Signs of AI writing guide and its Style and Markup subpages, read on 22 November 2026, including the 2026 additions.
- `check_patterns.py`, a dependency-free Python checker for AI writing patterns, with Arabic punctuation support for its language-neutral checks.
- Claude Code plugin and marketplace manifests, a ZIP package for the Claude apps, unit tests and a GitHub Actions workflow.
