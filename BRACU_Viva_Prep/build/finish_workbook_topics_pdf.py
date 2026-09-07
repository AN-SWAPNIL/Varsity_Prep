"""Validate a focused workbook PDF, add chapter bookmarks and render samples."""
from pathlib import Path
import sys
import json
import fitz
from postprocess_pdf import headings_from_markdown, find_heading_pages

raw,output,source,work=map(Path,sys.argv[1:])
doc=fitz.open(raw)
assert len(doc)>30, 'Focused book unexpectedly short'
headings=headings_from_markdown([source])
toc=find_heading_pages(doc,headings)
# Flat chapter outline: title then course chapters (all H1 in source).
toc=[[1,title,page] for _,title,page in toc]
doc.set_toc(toc)
assert len(toc)>=10
meta=doc.metadata
meta.update(title=source.stem.replace('_',' '),author='Ahmmad Nur Swapnil',
            subject="Existing explanations selected for the seniors' topic workbook")
doc.set_metadata(meta)
doc.save(output,garbage=1,deflate=True)
assert output.stat().st_size>500000
preview=work/'preview'
preview.mkdir(exist_ok=True)
samples={0,len(doc)-1}
samples.update(page-1 for _,_,page in toc)
needles=['bias variance the precise answer','build heap and heapsort are different',
         'lstm gates memory path','man in the middle encryption','kleene s algorithm']
from postprocess_pdf import normalized
hits={}
for i,page in enumerate(doc):
    if i < toc[1][2]-1: continue
    text=normalized(page.get_text())
    for needle in needles:
        if needle in text and needle not in hits:
            hits[needle]=i+1
            samples.update({i,min(i+1,len(doc)-1)})
for i in sorted(samples):
    page=doc[i]
    assert page.get_text().strip(),f'Empty sample page {i+1}'
    page.get_pixmap(matrix=fitz.Matrix(1.15,1.15),alpha=False).save(preview/f'page-{i+1:04d}.png')
report=dict(pages=len(doc),bookmarks=toc,topic_pages=hits,preview_pages=[i+1 for i in sorted(samples)])
(work/'pdf_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'PDF verified: {len(doc)} pages; {len(toc)} chapter bookmarks; {output.stat().st_size/1048576:.1f} MiB.')
