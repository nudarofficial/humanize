# Changelog

## Unreleased

- humanize.zip is no longer kept in the repository; a workflow builds it and attaches it to each GitHub release.
- A plugin icon, and a `directory` branch with a plugin-only edition for the Claude directory, built automatically from main.
- SKILL.md treats the checker script as optional when it isn't bundled.
- Removed the shebang line from check_patterns.py; run it with python3 as documented.

## 1.1.1 (22 November 2026)

- The skill folder, and so humanize.zip, now includes the LICENSE file, so the MIT notice and the CC BY-SA 4.0 attribution travel with every copy.
- Copyright lines on the bundled pattern catalog and examples.
- Agensi listing link in the skill README.

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
