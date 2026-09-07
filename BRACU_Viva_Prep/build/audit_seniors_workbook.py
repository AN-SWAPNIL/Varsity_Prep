"""Extract the supplied XLSX's cells, links, and embedded screenshots without dependencies."""
from pathlib import Path
import json
import posixpath
import xml.etree.ElementTree as ET
import zipfile

workspace=Path(__file__).resolve().parents[2]
source=workspace/'Varsity_Topics_List_In Memory of Masud.xlsx'
out=Path(__file__).resolve().parent/'seniors_audit'
out.mkdir(exist_ok=True)
S='http://schemas.openxmlformats.org/spreadsheetml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
XDR='http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing'
A='http://schemas.openxmlformats.org/drawingml/2006/main'
def rels(z,path):
    relpath=posixpath.join(posixpath.dirname(path),'_rels',posixpath.basename(path)+'.rels')
    if relpath not in z.namelist():return {}
    return {r.get('Id'):{'target':r.get('Target'),'mode':r.get('TargetMode')} for r in ET.fromstring(z.read(relpath))}
def resolve(path,target):return posixpath.normpath(posixpath.join(posixpath.dirname(path),target)).lstrip('/')
report=[]
with zipfile.ZipFile(source) as z:
    shared=[''.join(si.itertext()) for si in []]
    if 'xl/sharedStrings.xml' in z.namelist():
        shared=[''.join(t.text or '' for t in si.iter(f'{{{S}}}t')) for si in ET.fromstring(z.read('xl/sharedStrings.xml'))]
    book=ET.fromstring(z.read('xl/workbook.xml'));br=rels(z,'xl/workbook.xml')
    for idx,sheet in enumerate(book.find(f'{{{S}}}sheets'),1):
        path=resolve('xl/workbook.xml',br[sheet.get(f'{{{R}}}id')]['target'])
        xml=ET.fromstring(z.read(path));sr=rels(z,path)
        data={'index':idx,'name':sheet.get('name'),'state':sheet.get('state'),'cells':[],'links':[],'images':[]}
        for c in xml.iter(f'{{{S}}}c'):
            v=c.find(f'{{{S}}}v');value=v.text if v is not None else ''
            if c.get('t')=='s':value=shared[int(value)] if value else ''
            elif c.get('t')=='inlineStr':value=''.join(t.text or '' for t in c.iter(f'{{{S}}}t'))
            formula=c.find(f'{{{S}}}f')
            if value or formula is not None:data['cells'].append({'cell':c.get('r'),'text':value,'formula':formula.text if formula is not None else None})
        for h in xml.iter(f'{{{S}}}hyperlink'):
            rid=h.get(f'{{{R}}}id');data['links'].append({'cell':h.get('ref'),'target':sr[rid]['target'] if rid in sr else h.get('location')})
        for drawing in xml.iter(f'{{{S}}}drawing'):
            dp=resolve(path,sr[drawing.get(f'{{{R}}}id')]['target']);dr=rels(z,dp)
            for anchor in ET.fromstring(z.read(dp)):
                start=anchor.find(f'{{{XDR}}}from');row=start.find(f'{{{XDR}}}row').text if start is not None else None
                for blip in anchor.iter(f'{{{A}}}blip'):
                    rid=blip.get(f'{{{R}}}embed')
                    if rid not in dr:continue
                    ip=resolve(dp,dr[rid]['target']);name=f'sheet-{idx:02d}-{Path(ip).name}'
                    (out/name).write_bytes(z.read(ip));data['images'].append({'file':name,'row':int(row)+1 if row else None})
        report.append(data)
(out/'workbook.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
for s in report:
    lines=[f"# {s['index']}. {s['name']} ({s['state']})",'']
    lines += [f"{c['cell']}: {c['text']}" for c in s['cells']]
    lines += ['', 'LINKS']+[f"{l['cell']}: {l['target']}" for l in s['links']]
    lines += ['', 'IMAGES']+[str(i) for i in s['images']]
    (out/f"sheet-{s['index']:02d}.txt").write_text('\n'.join(lines),encoding='utf-8')
    print(f"{s['index']:02d} {s['name']}: {len(s['cells'])} cells, {len(s['links'])} links, {len(s['images'])} images")
