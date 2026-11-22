#!/usr/bin/env python3
# check_patterns.py: flags AI-writing tells listed on Wikipedia's Signs of AI writing page (November 2026).
# Part of the humanize skill. Copyright (c) 2026 nudarofficial. MIT License, see LICENSE.
# Usage: python3 check_patterns.py draft.txt   (or pipe text in). Exits 1 if anything is flagged.
# Hits marked (review) are often fine in context: judge them instead of deleting on sight.
# The word and phrase lists are English. For other languages (Arabic included) only the
# language-neutral checks apply: punctuation, emoji, formatting, chatbot markup and placeholders.
import sys

APOS = chr(39)
EM, BULLET, ARROW = chr(0x2014), chr(0x2022), chr(0x21A9)
CURLY = chr(0x2018) + chr(0x2019) + chr(0x201C) + chr(0x201D)
AR_COMMA, AR_SEMI, AR_QMARK = chr(0x060C), chr(0x061B), chr(0x061F)

WORDS = '''additionally|align with|aligns with|boasts|bolstered|crucial|deep dive|delve|delves|delving|
emphasizing|enduring|enhance|enhances|enhanced|enhancing|foster|fosters|fostering|garner|garnered|
highlight|highlights|highlighted|highlighting|interplay|intricate|intricacies|landscape|meticulous|
meticulously|pivotal|robust|showcase|showcases|showcased|showcasing|tapestry|testament|underscore|
underscores|underscored|underscoring|valuable|vibrant|leverage|leveraging|multifaceted|quietly|
universally|echoed|dependable|seamless|seamlessly|transformative|game-changer|game-changing|synergy|
unlock|unlocks|unlocking|elevate|elevates|elevating|realm|myriad|plethora|ever-evolving|embark|
nestled|groundbreaking|renowned|profound|exemplifies|resonate with|resonates with'''
SOFT = '''challenge|challenges|clearer|matters|practical|prioritize|prioritise|steady|key|causal|
empirical|correlate|notably|moreover|furthermore'''

PHRASES = {
 'significance': '''stands as|serves as|served as|is a testament|a testament to|is a reminder|crucial role|
pivotal role|vital role|significant role|key role|pivotal moment|crucial moment|key moment|
underscores its importance|highlights its importance|underscores the importance|highlights the importance|
underscored the importance|highlighted the importance|underscoring the importance|highlighting the importance|
reflects broader|reflects the broader|symbolizing|setting the stage|marks a shift|marking a shift|
represents a shift|turning point|evolving landscape|focal point|indelible mark|deeply rooted|
forms part of the wider|distinction matters because|shaped conversations|shaped discussions|
shaped the debate|generated debate|sparked debate|prompted broader reflection|wider discussions about''',
 'promotional': '''in the heart of|natural beauty|diverse array|commitment to|rich cultural heritage''',
 'notability': '''independent coverage|media outlets|trade publications|tech outlets|business outlets|
music outlets|featured in|profiled in|cited in|extensively documented''',
 'identifies-as': '''identifies him as|identifies her as|identifies them as|identified him as|
identified her as|lists him as|lists her as|describes him as|describes her as|was identified by|
is listed in|profile lists''',
 'online-presence': '''social media presence|digital presence|online presence''',
 'ing-tail': ''', highlighting|, underscoring|, emphasizing|, ensuring|, reflecting|, symbolizing|
, contributing to|, cultivating|, fostering|, encompassing|, enhancing|, showcasing|, demonstrating|
, cementing|, solidifying|, reinforcing|valuable insight''',
 'vague-link': '''associated with|connected with|connected to|in connection with|in association with|
ventured into''',
 'weasel': '''industry reports|observers have cited|observers have noted|experts argue|experts say|
experts agree|experts suggest|some critics|some experts|some observers|some analysts|several sources|
several publications|numerous sources|various sources|described in scholarship|many believe''',
 'challenges-formula': '''faces several challenges|faces challenges|despite these challenges|
despite its challenges|future outlook|future prospects|challenges and legacy|awards and recognition''',
 'is-has-dodge': '''functions as|operates as|represents a|represents an|boasts a|boasts an|features a|
features an|refers to|holds the distinction''',
 'parallelism': '''not only|not just|'t just|not merely|'t merely|not simply|rather than|no longer''',
 'source-hedge': '''details are limited|details are scarce|details remain limited|not widely available|
not widely documented|not widely disclosed|not widely known|in the provided sources|
in the available sources|in the search results|based on available information|
based on the available information|should be treated as|should be presented as|
should be understood as|should be viewed as|should be read as|does not by itself|
should not be confused with|low profile|personal life private|personal details private|
important to note|worth noting|worth mentioning|it should be noted''',
 'chatbot': '''i hope this helps|of course!|certainly!|absolutely!|you're absolutely right|would you like|
is there anything else|let me know|detailed breakdown|here is a |here's a |here is an |here's an |
great question|feel free to|happy to help|as an ai|language model|my last knowledge update|
my last training update|i'm sorry, but|wikipedia-style''',
 'placeholder': '''xx-xx|example.com|insert_|add your|insert your|(if available)|lorem ipsum''',
 'chatbot-markup': '''oaicite|contentreference|oai_citation|turn0search|attributableindex|[cite:|
start_span|end_span|<mark>|grok_card|grok-card|grok_render|[attached_file:|[web:|ppl-ai-file-upload|
:::writing|utm_source=chatgpt|utm_source=openai|utm_source=copilot|referrer=grok''',
 'summary-ending': '''in summary|in conclusion|to sum up|to summarize|all in all|in essence''',
 'change-note': '''improved clarity|improved the clarity|improved flow|improved the flow|
improved readability|refined the tone|refined tone|refined the language|streamlined|while preserving|
while retaining|ensured that|ensured neutrality|for clarity|for better clarity|for better flow|
in compliance with|sourced content|verified content|sourced information|reviewer feedback''',
 'service-voice': '''carefully reviewed|apologize for any inconvenience|apologise for any inconvenience|
if there are specific issues|if there are any specific issues|unsubstantiated speculation''',
 'stiff-word': '''authored|relocated|utilize|utilizes|utilized|utilizing|utilization|utilise|utilised|
attempted|passed away''',
 'social-hook (talk page)': '''here's the thing|the truth is|here's the best part|here's the crazy part|
part nobody tells you|part no one tells you|no one talks about|nobody talks about''',
}
REVIEW = {'vague-link', 'notability', 'identifies-as', 'is-has-dodge', 'summary-ending', 'change-note', 'stiff-word'}
SMALL = {'a', 'an', 'the', 'and', 'or', 'of', 'in', 'on', 'to', 'for', 'with', 'at', 'by', 'vs', 'from'}
SUBJECTS = {'i', 'we', 'you', 'they', 'he', 'she', 'it', 'then'}


def split(block):
    return [p for p in block.replace(chr(10), '').split('|') if p]


def has(low, phrase):
    i = low.find(phrase)
    while i != -1:
        j = i + len(phrase)
        left = i == 0 or not phrase[0].isalnum() or not low[i - 1].isalnum()
        right = j == len(low) or not phrase[-1].isalnum() or not low[j].isalnum()
        if left and right:
            return True
        i = low.find(phrase, i + 1)
    return False


def sentences(text):
    out, cur = [], ''
    for ch in text:
        cur += ch
        if ch in '.!?' + AR_QMARK:
            out.append(cur.strip())
            cur = ''
    if cur.strip():
        out.append(cur.strip())
    return [s for s in out if s]


def triple(sent):
    t = sent.replace(AR_COMMA, ',').replace(',', ' , ').split()
    for i, w in enumerate(t):
        if w.lower() not in ('and', 'or') or i + 1 >= len(t):
            continue
        nxt = t[i + 1].lower()
        if nxt in SUBJECTS or nxt.startswith('i' + APOS):
            continue
        j = i - 1
        if j >= 0 and t[j] == ',':
            j -= 1
        k = j
        while k >= 0 and t[k] != ',' and j - k < 2:
            k -= 1
        if k < 1 or t[k] != ',' or k == j:
            continue
        if t[k - 1] != ',':
            return True
    return False


def bullet_rest(s):
    if s[:2] in ('- ', '* ') or s[:1] == BULLET:
        return s[1:].strip()
    tok = s.split(' ', 1)
    if len(tok) == 2 and tok[0][:-1].isdigit() and tok[0][-1:] in '.)':
        return tok[1].strip()
    return None


def check(text):
    hits, lines = [], text.splitlines()
    vocab, soft = split(WORDS), split(SOFT)
    phrases = {tag: split(block) for tag, block in PHRASES.items()}
    soft_seen, heads, table, prose = set(), [], [], []
    for n, line in enumerate(lines, 1):
        s = line.strip()
        low = line.lower().replace(chr(0x2019), APOS)
        add = lambda tag: hits.append((n, tag, s))
        if EM in line: add('em-dash')
        if ' -- ' in line: add('double-hyphen dash')
        if any(c in line for c in CURLY): add('curly quotes')
        if any(0x1F300 <= ord(c) <= 0x1FAFF or 0x2600 <= ord(c) <= 0x27BF or ord(c) in (0x2B50, 0x2705, 0x274C) for c in line):
            add('emoji')
        if line.count('**') >= 2 or line.count('__') >= 2: add('bold')
        if ARROW in line or (chr(0x3010) in line and chr(0x2020) in line): add('chatbot-markup')
        if s[:1] == BULLET: add('bullet character')
        if len(s) >= 3 and set(s) <= set('-*_'): add('horizontal rule')
        rest = bullet_rest(s)
        if rest is not None:
            head = rest.split(':', 1)[0]
            if rest.startswith('**') and ':' in rest[:60]: add('bold-label bullet')
            elif ':' in rest[:42] and rest[:1].isupper() and len(head.split()) <= 5 and '.' not in head:
                add('label-colon bullet (review)')
        if s.startswith('|'):
            table.append(n)
            continue
        if table:
            if len(table) <= 4: hits.append((table[0], 'small table (review: would prose do?)', ''))
            table = []
        if s.startswith('#'):
            level = len(s) - len(s.lstrip('#'))
            title = s.lstrip('#').strip()
            heads.append((n, level))
            words = [w for w in title.split() if w[:1].isalpha()]
            body = [w for w in words[1:] if w.lower() not in SMALL]
            if len(body) >= 2 and all(w[0].isupper() for w in body): add('title-case heading')
            if ' and ' in title.lower(): add('X-and-Y heading (review)')
        elif s and rest is None:
            prose.append(s)
        for w in vocab:
            if has(low, w): add('ai-vocab: ' + w)
        soft_seen.update(w for w in soft if has(low, w))
        for tag, plist in phrases.items():
            if any(has(low, p) for p in plist):
                add(tag + (' (review)' if tag in REVIEW else ''))
        for i in range(len(line)):
            if line[i] == '[':
                j = line.find(']', i)
                inner = line[i + 1:j] if j != -1 else ''
                if 2 <= len(inner) <= 40 and (inner[0].isupper() or not inner[0].isascii()) and all(c.isalpha() or c in ' ' + APOS for c in inner) and line[j + 1:j + 2] != '(':
                    add('placeholder')
                    break
        if any(triple(x) for x in sentences(s)): add('three-item list (review)')
    if table and len(table) <= 4: hits.append((table[0], 'small table (review: would prose do?)', ''))
    first = next((l.strip() for l in lines if l.strip()), '')
    if first.startswith('# '): hits.append((1, 'title heading at top (review)', first))
    for (n1, l1), (n2, l2) in zip(heads, heads[1:]):
        if l2 > l1 + 1: hits.append((n2, 'skipped heading level', lines[n2 - 1].strip()))
        if l2 > l1 and not any(x.strip() for x in lines[n1:n2 - 1]):
            hits.append((n1, 'heading with only subheadings', lines[n1 - 1].strip()))
    if len(soft_seen) >= 3: hits.append((0, '2026 vocab cluster: ' + ', '.join(sorted(soft_seen)), ''))
    sents = sentences(' '.join(prose))
    lows = [x.lower().replace(chr(0x2019), APOS) for x in sents]
    for a, x in enumerate(lows):
        if x.startswith(('overall,', 'ultimately,')): hits.append((0, 'summary-ending (review)', sents[a]))
        if (x.startswith(('it' + APOS + 's not ', 'it is not ', 'this is not ', 'that' + APOS + 's not ', 'it isn' + APOS + 't '))
                and any(m in x for m in (', it' + APOS + 's ', '; it' + APOS + 's ', ', but '))):
            hits.append((0, 'parallelism', sents[a]))
        cut = x.rfind(', not ')
        if cut != -1 and len(x[cut + 6:].split()) <= 4: hits.append((0, 'parallelism (X, not Y)', sents[a]))
        if x.startswith('here' + APOS + 's the') and ':' in x: hits.append((0, 'social-hook (colon reveal)', sents[a]))
        if a >= 2 and lows[a - 2].startswith('no ') and lows[a - 1].startswith('no ') and x.startswith(('just ', 'only ')):
            hits.append((0, 'parallelism (No X. No Y. Just Z.)', sents[a]))
    lens = [len(x.split()) for x in sents]
    if len(lens) >= 8 and max(lens) <= 25 and sum(8 <= k <= 20 for k in lens) / len(lens) >= 0.9:
        hits.append((0, 'sentences all sit in the 8-20 word band (review: vary length)', ''))
    joined = ' '.join(prose)
    if len(text.split()) >= 150 and not any(c in joined for c in ':;()?' + AR_SEMI + AR_QMARK):
        hits.append((0, 'flat punctuation, only commas and periods (review)', ''))
    return hits


if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding='utf-8') as fh:
            src = fh.read()
    else:
        src = sys.stdin.read()
    found = check(src)
    for n, tag, s in found:
        print('L' + str(n).ljust(4), '[' + tag + ']', s[:100])
    print()
    print(str(len(found)) + ' hits.' if found else 'No hits. Reread for inflated significance, vague claims and synonym cycling.')
    sys.exit(1 if found else 0)
