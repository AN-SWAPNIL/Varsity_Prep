"""Inspect chapter destinations and render representative PDF pages for visual review."""
from pathlib import Path
import argparse
import json
import re
import fitz

parser = argparse.ArgumentParser()
parser.add_argument('pdf',type=Path)
args = parser.parse_args()
out = Path(__file__).resolve().parent / 'pdf_checks'
out.mkdir(exist_ok=True)
doc = fitz.open(args.pdf)
toc = doc.get_toc()
chapters = [entry for entry in toc if entry[0] == 1]
samples = {0,len(doc)-1}
samples.update(entry[2]-1 for entry in chapters)
needles = ['One buy, one later sell','PCA versus regression, with an actual',
           'LSTM — gates', 'Linear Diophantine equations',
           'Build-heap and heapsort are different','Runtime polymorphism',
           'Man in the middle: encryption', 'Subject Preparation']
hits = {}
body_start = chapters[1][2] - 1 if len(chapters) > 1 else 0
for i,page in enumerate(doc):
    text = page.get_text()
    for needle in needles:
        words = re.sub(r'[^a-z0-9]+',' ',needle.casefold()).strip()
        normalized = re.sub(r'[^a-z0-9]+',' ',text.casefold())
        if words in normalized and needle not in hits and i >= body_start:
            hits[needle] = i+1
            samples.update({i,min(i+1,len(doc)-1)})

for i in sorted(samples):
    doc[i].get_pixmap(matrix=fitz.Matrix(1.25,1.25),alpha=False).save(out/f'page-{i+1:04d}.png')
report = {'pdf':args.pdf.name,'pages':len(doc),'bookmarks':len(toc),
          'chapters':chapters,'topic_pages':hits,'preview_pages':[i+1 for i in sorted(samples)]}
(out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
