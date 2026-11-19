#!/usr/bin/env python3
"""Keep original course Markdown and downloadable teaching files byte-for-byte."""
import hashlib
import json
from pathlib import Path
import subprocess

PIN = '1d695c94ccafdce3f06d6b9dfe3e6f106097693a'
paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', PIN], text=True).splitlines()
checked = []
for name in paths:
    if not (name.endswith('.md') or name.startswith('static/files/')) or name == 'AGENTS.md':
        continue
    original = subprocess.check_output(['git', 'show', f'{PIN}:{name}'])
    current = Path(name).read_bytes()
    assert current == original, f'Original teaching content changed: {name}'
    checked.append({'path': name, 'sha256': hashlib.sha256(current).hexdigest()})
print(f'PASS: {len(checked)} original Markdown/download files unchanged against {PIN}')

subtitles = json.loads(Path('SUBTITLE_QA.json').read_text())
for item in subtitles['files']:
    source, translated = Path(item['source']), Path(item['translation'])
    assert hashlib.sha256(source.read_bytes()).hexdigest() == item['source_sha256']
    assert hashlib.sha256(translated.read_bytes()).hexdigest() == item['translation_sha256']
    original_cues = source.read_text().strip().split('\n\n')
    localized_cues = translated.read_text().strip().split('\n\n')
    assert len(original_cues) == len(localized_cues) == item['cues']
    assert [c.splitlines()[0] for c in original_cues] == [c.splitlines()[0] for c in localized_cues]
    assert all(len(c.splitlines()) >= 2 for c in localized_cues)
print(f"PASS: {subtitles['total_cues']} reviewed subtitle cues, timestamps/order and release hashes exact")

