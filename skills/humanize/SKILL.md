---
name: humanize
description: Use when asked to humanize AI text, make writing sound natural or less like ChatGPT, rewrite or polish a draft, or check if text sounds AI-generated. Keeps every fact.
license: Instructions and references CC-BY-SA-4.0; scripts MIT. See LICENSE.
metadata:
  author: nudarofficial
  version: "1.1.1"
  repository: https://github.com/nudarofficial/humanize
---

Use this skill to make text read as if a person wrote it. Apply it to any text meant for a reader, and don't comment on it unless asked.

The rules come from Wikipedia's "Signs of AI writing" advice page (WP:AISIGNS, kept by WikiProject AI Cleanup) and its Style and Markup subpages, read in full on 22 November 2026. Editors keep revising that page as models change, so some signs fade and new ones appear. If this skill and the live page disagree, the page wins.

Files in this skill:

- references/patterns.md is the full pattern catalog. Read it when rewriting or reviewing anything longer than a short paragraph, or when you're unsure whether something counts.
- scripts/check_patterns.py flags the surface patterns in a draft. It needs Python 3 and nothing else.
- examples/examples.md shows finished rewrites and a review in English and Arabic. Read it when you want to see the expected output.

## Why it works this way

Language models predict the most statistically likely text, so they drift toward the safe, generic version of everything. The page's example: "inventor of the first train-coupling device" turns into "a revolutionary titan of industry". The subject ends up less specific and more exaggerated at the same time.

The page also warns that the surface signs point to deeper problems (vague claims, invented or missing sources), and that fixing only the surface just makes weak text harder to spot. So the work has two layers. First, say something specific and true in plain words. Then check the surface patterns.

Over-correcting creates new tells. Models built to avoid em dashes now lean so hard on commas and periods that the page lists flat punctuation as a sign too (that line is tagged "citation needed"). Swapping "delve" for "dig into" in every draft would become a tell of its own. The page says its word lists should be read literally: a flagged word doesn't make its synonyms suspect. The fix is usually to say the plain thing.

## Modes

Rewrite (the user gives you text):

1. Read for meaning first. Note the point, the audience, the register, and every fact, number, name and claim. All of them stay.
2. Add nothing the author didn't supply: no facts, numbers, quotes, sources or examples. If a vague passage needs a detail you don't have, keep it modest and mention the gap in one line after the text, or ask.
3. Rewrite in plain, specific language in the author's voice. If the user has shared a sample of their writing, copy its sentence length, contractions, punctuation habits and vocabulary. Otherwise follow the default voice below.
4. Check. If you can run code, save the draft to a file and run `python3 scripts/check_patterns.py draft.txt` from this skill's directory. Fix every hit or confirm it's legitimate (a quotation, a name, a literal use like a landscape photo, a real list of three things). Then reread for what a script can't see: inflated significance, vague attribution, synonym cycling, a wrap-up ending, lists rounded up to three, and a sentence rhythm that never changes.
5. Deliver the text without commentary on what you changed. If the user asks what changed, name the actual edits ("cut the last paragraph", "swapped 'utilize' for 'use'"). Canned change notes like "refined the tone and improved flow while preserving your voice" are one of the listed tells.

Write (new text): the same process without steps 1 and 2, though the ban on invented facts still applies. Write plainly from the start and run the checker on anything over about 150 words. For quick chat replies, keep the patterns in mind and skip the script.

Review ("does this sound like AI?"): quote the specific phrases that match the catalog and say how strong each signal is. A cluster of signs is strong evidence; one sign alone is weak, since people write all of these sometimes. Don't rewrite unless asked, and never claim certainty. The page cites studies showing people are poor at telling AI text from human text, and detectors have real error rates.

## Output format

Rewrite and Write: return only the finished text, in the same format as the input (an email stays an email, Markdown stays Markdown). If a fact was missing or a claim needs a source, add one short line after the text that says so. Add no preamble and no list of changes unless the user asks.

Review: list each problem as a bullet in this form: the quoted phrase, then the pattern it matches, then how strong the signal is (strong, medium or weak). After the list, give a one-sentence overall read, for example "Several strong signs; this reads as AI-assisted." If you find nothing, say so plainly.

## Default voice

When there's no sample, write direct, plain and conversational prose with contractions where they sound natural. Match the register the piece needs: a cover letter is more formal than a caption, and an essay keeps its academic tone. For social content, put the hook first. Use no emojis unless the user's own text or request includes them.

If the user states standing preferences (banned words, a house style, a tone), they outrank these defaults. People who install this skill for themselves can add their own rules in a section at the end of this file.

## Write it this way instead

- Use plain verbs. "Is" and "has" beat "serves as", "stands as", "boasts" and "features".
- State relationships directly ("was CEO of", "taught violin at"). Avoid "associated with", "connected to", "in connection with" and "ventured into".
- Prefer specifics to praise. A date, a number, a name or a concrete detail does more than "significant" or "vibrant".
- Name the source or drop the claim. Never invent a source, quote, statistic or trend to make text sound specific; if a claim needs a source you don't have, flag it.
- Say each thing once and stop on the last useful sentence. No wrap-up paragraph.
- Use as many items as the content has. Two is fine. Four is fine.
- Repeat a word when it's the right word instead of cycling through synonyms.
- In informational writing, cut scene-setting and hype, and drop claims about how a topic fits a bigger picture.
- Cut meta-commentary such as "it's worth noting" and state the thing.
- Punctuate like a person. Don't use em dashes. Use commas and periods, and also colons, semicolons, parentheses and question marks where they fit, so the rhythm doesn't go flat. Write ranges with "to" (2019 to 2023). Use straight quotes.
- Vary sentence length. Mix short sentences with longer ones; a long run of sentences that all land between 8 and 20 words is a 2026 tell.
- Write in paragraphs. Use a list only when the content is a list, and never start bullets with a bold label and a colon.
- Use sentence case for headings and skip them on short pieces. Don't open with a title heading, and don't separate sections with horizontal rules. Put two or three facts in a sentence instead of a table.
- Keep the things people naturally write, like "there is" and "it has", plain words like "wrote" and "used", superlatives when they're true ("the first", "the only"), and qualifiers like "very" or "perhaps". AI text tends to strip these out.
- Leave in some rough edges when they fit the voice: a fragment, a sentence that starts with "And" or "But", a contraction, a short aside in parentheses. Don't add fake typos.

## The strongest signs, in brief

The catalog has the full lists. These come up most often in 2026 text:

- Inflated importance ("a pivotal moment", "reflects broader trends", "an indelible mark") and shallow "-ing" tails ("..., highlighting its significance").
- Vague links and attribution ("associated with", "experts argue", "several sources" when there's one), and stressing how records "identify" someone.
- Negative parallelisms ("it's not X, it's Y") and the reversed "Y rather than X", plus corrective disclaimers ("should be treated as X rather than Y", "does not by itself establish").
- Clusters of AI vocabulary: delve, tapestry, testament, underscore, pivotal, showcase, vibrant, and since mid-2026 words like leverage, multifaceted, quietly and steady.
- Chatbot leftovers ("I hope this helps", "Would you like...", placeholders like [Name]), leaked citation code (oaicite, turn0search0, utm_source=chatgpt.com) and invented sources.
- Formatting habits: bold-label bullets, title case headings, emoji bullets, curly quotes, em dashes.

## Other languages

The catalog describes English text. In other languages, Arabic included, apply the language-independent rules: keep every fact and the author's meaning, prefer specifics to praise, drop inflated significance and vague attribution, remove chatbot leftovers and placeholders, avoid decorative formatting and emoji, and follow the punctuation norms of that language. Write in the language the user wrote in. Don't translate English stock phrases into "AI vocabulary" lists for other languages; the page doesn't provide them. The checker's word lists are English, so for other languages it only checks punctuation, emoji, formatting, markup and placeholders.

## Guardrails

- Preserve meaning. Facts, figures, names and the author's position stay intact.
- Leave quotations, code, citations, legal wording and formulas untouched.
- This improves writing. It doesn't guarantee any detector result, so never promise one.
- If the user says a school, journal, employer or platform requires disclosing AI help, that disclosure is theirs to make, and this skill shouldn't be used to hide it. Wikipedia's WP:LLM guideline bans LLM-written article content (since March 2026, according to WikiProject AI Cleanup), so point that out before drafting article text for Wikipedia.
- Don't lecture about the patterns or list what you removed unless asked.
