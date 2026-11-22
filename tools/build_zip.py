# Builds dist/humanize.zip from skills/humanize (attached to each GitHub release). Copyright (c) 2026 nudarofficial. MIT License, see LICENSE.
# Usage, from the repository root: python3 tools/build_zip.py . [output.zip]
import sys, zipfile
from pathlib import Path
root = Path(sys.argv[1]); skill = root / 'skills' / 'humanize'; out = Path(sys.argv[2]) if len(sys.argv) > 2 else root / 'dist' / 'humanize.zip'
out.parent.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in sorted(skill.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts:
            info = zipfile.ZipInfo('humanize/' + p.relative_to(skill).as_posix(), date_time=(2026, 11, 22, 0, 0, 0))
            info.external_attr = (0o755 if p.suffix == '.py' else 0o644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, p.read_bytes())
print(out, out.stat().st_size)
