# humanize

An Agent Skill that rewrites robotic, AI-generated text into natural human writing without changing the facts. It works in Claude Code, the Claude apps and other agents that read SKILL.md files.

What it does:

- Rewrite: paste a draft and get it back in plain, specific language with every fact, number and name kept.
- Write: give the facts and get new text that avoids AI writing patterns from the start.
- Review: ask whether a draft sounds AI-generated and get the exact phrases, the pattern each one matches and how strong the signal is.

Files:

- SKILL.md: the workflow, output format and rules.
- references/patterns.md: the full pattern catalog, adapted from Wikipedia's Signs of AI writing guide (November 2026).
- examples/examples.md: finished rewrites and a review, in English and Arabic.
- scripts/check_patterns.py: an optional checker that flags AI writing patterns in a draft. Python 3, no dependencies, no network access. Run: python3 scripts/check_patterns.py draft.txt

Languages: full support for English. Other languages, Arabic included, get the language-independent rules (keeping facts, cutting inflated claims, removing chatbot leftovers and formatting habits).

Source code, tests and issues: https://github.com/nudarofficial/humanize

Copyright © 2026 nudarofficial. Skill text and references are licensed CC BY-SA 4.0 (adapted from Wikipedia, CC BY-SA 4.0); the script is MIT. See the LICENSE file in the repository.
