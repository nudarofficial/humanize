# Rebuilds dist/humanize.zip from skills/humanize. Copyright (c) 2026 nudarofficial. MIT License, see LICENSE.
# Usage, from the repository root: python3 tools/build_zip.py .
import sys, zipfile
from pathlib import Path
root = Path(sys.argv[1]); skill = root / 'skills' / 'humanize'; out = root / 'dist' / 'humanize.zip'
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in sorted(skill.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts:
            info = zipfile.ZipInfo('humanize/' + p.relative_to(skill).as_posix(), date_time=(2026, 11, 22, 0, 0, 0))
            info.external_attr = (0o755 if p.suffix == '.py' else 0o644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, p.read_bytes())
print(out, out.stat().st_size)
