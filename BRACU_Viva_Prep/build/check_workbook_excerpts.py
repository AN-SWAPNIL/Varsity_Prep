"""Check every manifest excerpt against its source and generated focused Markdown."""
from pathlib import Path
import hashlib
import json
import re
from assemble_workbook_topics import ROOT, SOURCE, scan

def without_headings(text):
    lines,headings=scan(text)
    skip={h['start'] for h in headings}
    return ''.join(line for i,line in enumerate(lines) if i not in skip).strip()

for pack in ('BRACU','UIU'):
    folder=ROOT/(pack+'_Viva_Prep')
    entries=json.loads((folder/'build/workbook_topics/selection.json').read_text(encoding='utf-8'))
    book=(folder/(pack+'_Seniors_Workbook_Topics_Explained.md')).read_text(encoding='utf-8')
    normalized=without_headings(book)
    files={entry['file'] for entry in entries}
    cached={name:(SOURCE/name).read_text(encoding='utf-8').splitlines(keepends=True) for name in files}
    for entry in entries:
        original=''.join(cached[entry['file']][entry['first_line']-1:entry['last_line']]).strip()
        assert hashlib.sha256(original.encode()).hexdigest()==entry['source_sha256'],entry
        assert without_headings(original) in normalized,entry
    assert 'W7. LSTM' in book and '7. Bias' in book and 'N10.' in book
    assert 'Kleene' in book if pack=='BRACU' else '## 4.3 Kleene' not in book
    print(f'{pack}: all {len(entries)} excerpts match source prose/code/math/diagrams; heading depths only adjusted.')
