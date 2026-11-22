# Builds the plugin-only tree published on the `directory` branch for the Claude directory.
# The directory accepts only Markdown, text, JSON, YAML and images from unverified
# organizations, so this edition leaves out the optional Python checker and the website.
# Copyright (c) 2026 nudarofficial. MIT License, see LICENSE.
# Usage, from the repository root: python3 tools/build_directory.py . OUTPUT_DIR
import re, shutil, sys
from pathlib import Path

root, out = Path(sys.argv[1]), Path(sys.argv[2])
REPO = 'https://github.com/nudarofficial/humanize'
RAW = 'https://raw.githubusercontent.com/nudarofficial/humanize/main/'
for child in out.iterdir() if out.exists() else []:
    if child.name != '.git':
        shutil.rmtree(child) if child.is_dir() else child.unlink()
out.mkdir(parents=True, exist_ok=True)
shutil.copytree(root / '.claude-plugin', out / '.claude-plugin')
shutil.copytree(root / 'skills', out / 'skills',
                ignore=shutil.ignore_patterns('scripts', '__pycache__', '*.py', '*.pyc'))
shutil.copy2(root / 'LICENSE', out / 'LICENSE')

def absolute(m):
    label, url = m.group(1), m.group(2)
    if re.match(r'(https?:|#|mailto:)', url) or url == 'LICENSE':
        return m.group(0)
    base = RAW if label.startswith('!') else REPO + '/blob/main/'
    return f'{label}({base}{url.lstrip("./")})'

readme = (root / 'README.md').read_text(encoding='utf-8')
readme = re.sub(r'(!?\[[^\]]*\])\(([^)\s]+)\)', absolute, readme)
readme = re.sub(r'src="(?!https?:)([^"]+)"', lambda m: f'src="{RAW}{m.group(1).lstrip("./")}"', readme)
(out / 'README.md').write_text(readme, encoding='utf-8')

skill_readme = out / 'skills' / 'humanize' / 'README.md'
text = skill_readme.read_text(encoding='utf-8')
text = re.sub(r'- scripts/check_patterns\.py:[^\n]*',
              f'- The optional pattern checker (scripts/check_patterns.py) is not included in this edition. Get it from {REPO}.',
              text)
skill_readme.write_text(text, encoding='utf-8')
print('built', out)
