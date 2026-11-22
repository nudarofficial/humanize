# Tests for the humanize skill. Copyright (c) 2026 nudarofficial. MIT License, see LICENSE.
# Run from the repository root: python3 -m unittest discover -s tests -v
import importlib.util
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / 'skills' / 'humanize'
FIXTURES = Path(__file__).resolve().parent / 'fixtures'

spec = importlib.util.spec_from_file_location('check_patterns', SKILL / 'scripts' / 'check_patterns.py')
cp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp)

CASES = json.loads((Path(__file__).resolve().parent / 'cases.json').read_text(encoding='utf-8'))
BY_ID = {c['id']: c for c in CASES}
DIGITS = re.compile(r'[0-9٠-٩][0-9٠-٩,.]*')


def tags(text):
    return [t for _, t, _ in cp.check(text)]


def hard(text):
    # Hits that are not marked (review): these must be fixed in finished output.
    return [t for t in tags(text) if '(review)' not in t]


class CheckerTests(unittest.TestCase):
    def test_human_paragraph_is_clean(self):
        self.assertEqual(tags((FIXTURES / 'en_human_paragraph.md').read_text(encoding='utf-8')), [])

    def test_structure_flags(self):
        found = tags((FIXTURES / 'structure.md').read_text(encoding='utf-8'))
        for expected in ('title-case heading', 'horizontal rule', 'bullet character', 'heading with only subheadings', 'small table'):
            self.assertTrue(any(expected in t for t in found), expected)

    def test_skipped_heading_level(self):
        self.assertIn('skipped heading level', tags('## Intro\n#### Detail\ntext'))

    def test_chatbot_markup(self):
        found = tags((FIXTURES / 'markup.txt').read_text(encoding='utf-8'))
        self.assertGreaterEqual(sum('chatbot-markup' in t for t in found), 2)

    def test_sentence_band(self):
        found = tags((FIXTURES / 'sentence_band.txt').read_text(encoding='utf-8'))
        self.assertTrue(any('8-20 word band' in t for t in found))

    def test_wasnt_just_parallelism(self):
        self.assertIn('parallelism', tags("It wasn't just a course. It was a reset."))

    def test_x_not_y(self):
        self.assertTrue(any('X, not Y' in t for t in tags('It is a strategy, not a trick.')))

    def test_arabic_neutral_checks(self):
        found = tags('هذا نص — فيه رمز \U0001F680 و [اسم الشركة]')
        for expected in ('em-dash', 'emoji', 'placeholder'):
            self.assertIn(expected, found)

    def test_cli_exit_codes(self):
        import subprocess, sys
        script = str(SKILL / 'scripts' / 'check_patterns.py')
        clean = subprocess.run([sys.executable, script], input='We met on Thursday.', capture_output=True, text=True)
        dirty = subprocess.run([sys.executable, script], input='This is a pivotal moment.', capture_output=True, text=True)
        self.assertEqual(clean.returncode, 0)
        self.assertEqual(dirty.returncode, 1)


class ModeTests(unittest.TestCase):
    def test_rewrite_and_write_cases(self):
        for case in CASES:
            if case['mode'] not in ('rewrite', 'write'):
                continue
            with self.subTest(case['id']):
                out = case['output']
                for fact in case['required_facts']:
                    self.assertIn(fact, out, 'fact lost: ' + fact)
                # No invented numbers: every number in the output must appear in the input.
                for num in DIGITS.findall(out):
                    self.assertIn(num.rstrip('.,'), case['input'], 'number not in input: ' + num)
                self.assertEqual(hard(out), [], 'unfixed patterns in output')
                if case['mode'] == 'rewrite':
                    self.assertTrue(hard(case['input']), 'input should contain AI patterns')

    def test_review_cases(self):
        for case in CASES:
            if case['mode'] != 'review':
                continue
            with self.subTest(case['id']):
                if 'input_from' in case:
                    text = BY_ID[case['input_from']]['input']
                else:
                    text = (FIXTURES / case['fixture']).read_text(encoding='utf-8')
                found = tags(text)
                for expected in case['expected_tags']:
                    self.assertTrue(any(t.startswith(expected) for t in found), 'missing ' + expected)
                if not case['expected_tags']:
                    self.assertEqual(found, [])


class SkillFileTests(unittest.TestCase):
    def test_zip_matches_skill_folder(self):
        import subprocess, sys, tempfile, zipfile
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'humanize.zip'
            subprocess.run([sys.executable, str(ROOT / 'tools' / 'build_zip.py'), str(ROOT), str(out)], check=True, capture_output=True)
            with zipfile.ZipFile(out) as z:
                packed = {n: z.read(n) for n in z.namelist()}
        disk = {'humanize/' + p.relative_to(SKILL).as_posix(): p.read_bytes()
                for p in SKILL.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
        self.assertEqual(packed, disk)
        self.assertIn('humanize/LICENSE', packed)
        self.assertIn('humanize/SKILL.md', packed)

    def test_frontmatter(self):
        text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        self.assertTrue(text.startswith('---\n'))
        front = text.split('---', 2)[1]
        name = re.search(r'^name: (.+)$', front, re.M).group(1).strip()
        desc = re.search(r'^description: (.+)$', front, re.M).group(1).strip()
        self.assertEqual(name, SKILL.name)
        self.assertRegex(name, r'^[a-z0-9]+(-[a-z0-9]+)*$')
        self.assertLessEqual(len(name), 64)
        self.assertLessEqual(len(desc), 200)  # claude.ai upload limit; the spec allows 1024
        self.assertNotIn('<', desc)
        self.assertLess(text.count('\n'), 500)

    def test_referenced_files_exist(self):
        text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        for ref in ('references/patterns.md', 'scripts/check_patterns.py', 'examples/examples.md'):
            self.assertIn(ref, text)
            self.assertTrue((SKILL / ref).exists(), ref)

    def test_license_ships_with_skill(self):
        self.assertEqual((SKILL / 'LICENSE').read_text(encoding='utf-8'), (ROOT / 'LICENSE').read_text(encoding='utf-8'))

    def test_examples_match_tested_cases(self):
        text = (SKILL / 'examples' / 'examples.md').read_text(encoding='utf-8')
        for case in CASES:
            if case['mode'] in ('rewrite', 'write'):
                for line in case['output'].split(chr(10)):
                    if line.strip():
                        self.assertIn(line, text, case['id'])

    def test_skill_prose_has_no_em_dash_or_curly_quotes(self):
        for path in (SKILL / 'SKILL.md', SKILL / 'README.md', SKILL / 'references' / 'patterns.md', ROOT / 'README.md'):
            if path.exists():
                text = path.read_text(encoding='utf-8')
                for ch in ('—', '‘', '’', '“', '”'):
                    self.assertNotIn(ch, text, str(path))


if __name__ == '__main__':
    unittest.main()
