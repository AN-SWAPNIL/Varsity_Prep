"""Prepare original TikZ figures and a Quarto reference template; render editable PPTX."""
from pathlib import Path
import argparse
import re
import subprocess
import zipfile
import copy
import io
import json
import posixpath
import xml.etree.ElementTree as ET
import fitz
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / 'build' / 'editable'
ASSETS = ROOT / 'editable_assets'
QUARTO = r'D:\Applications\Quarto\bin\quarto.exe'
P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
NS = {'p': P, 'a': A}
STEM = 'sonia_np_completeness_demo_editable'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
PKG = 'http://schemas.openxmlformats.org/package/2006/relationships'

# x, y, width, height in inches; final number is native text size in points.
# F = full-width source blocks; L/R = original source columns. Pictures fit
# their rectangle without stretching. These positions preserve the teaching
# layout while avoiding Pandoc's limited mixed-figure placeholder placement.
LAYOUT = {
 1:{'F0':(.55,2.15,8.9,4.2,20)},
 2:{'F0':(.45,1.30,9.1,1.5,18),'F1':(.6,3.05,8.8,1.25,21),'F2':(1.0,4.55,8,1.05,18),'F3':(.6,6.0,8.8,.55,15)},
 3:{'L0':(.4,1.05,4.45,1.3,18),'L1':(.75,2.5,3.6,1.7,18),'L2':(.4,4.55,4.45,2.25,17),'R0':(5.15,1.05,4.45,1.95,18),'R1':(5.95,3.1,2.85,1.65,18),'R2':(5.15,4.95,4.45,2.05,16)},
 4:{'L0':(.4,1.15,4.5,5.8,18),'R0':(5.15,1.5,4.4,3.25,18),'R1':(5.15,5.05,4.4,1.7,17)},
 5:{'F0':(.5,1.15,9,.85,18),'L0':(.4,2.3,4.45,4.6,18),'R0':(5.15,2.3,4.45,1.85,18),'R1':(5.15,4.45,4.45,1.1,16),'R2':(5.15,5.95,4.45,.95,16)},
 6:{'L0':(.4,1.2,4.45,2.8,19),'R0':(5.15,1.2,4.45,3.3,18),'F0':(1.2,4.7,7.6,1.55,18),'F1':(.5,6.55,9,.55,18)},
 7:{'L0':(.4,1.15,4.45,3.0,18),'R0':(5.15,1.15,4.45,2.5,19),'F0':(.8,4.3,8.4,1.55,18),'F1':(.5,6.05,9,.95,17)},
 8:{'L0':(.4,1.3,4.45,1.3,19),'L1':(.8,2.85,3.7,3.2,18),'R0':(5.15,1.3,4.45,1.2,19),'R1':(5.1,2.9,4.6,2.65,18),'R2':(5.15,6.05,4.45,.85,19)},
 9:{'L0':(.4,1.1,4.35,5.95,16),'R0':(4.95,1.35,4.65,3.95,18),'R1':(5.05,5.55,4.55,1.35,15)},
10:{'L0':(.4,1.15,4.45,1.7,18),'L1':(.5,3.0,4.2,.8,18),'L2':(.4,4.2,4.45,2.15,18),'R0':(5.15,1.15,4.45,1.65,18),'R1':(5.6,2.95,3.55,2.15,18),'R2':(5.15,5.6,4.45,1.2,14)},
11:{'F0':(.5,1.5,9,.8,21),'L0':(.4,2.85,4.45,3.65,20),'R0':(5.15,2.85,4.45,3.65,20)},
12:{'F0':(.9,1.2,8.2,5.4,18),'F1':(.45,6.85,9.1,.45,17)},
13:{'L0':(.4,1.15,4.45,2.8,18),'R0':(5.15,1.15,4.45,2.8,18),'F0':(.5,4.25,9,1.6,18),'F1':(.5,6.1,9,1.05,17)},
14:{'F0':(.5,1.05,9,1.15,19),'L0':(.4,2.45,4.45,4.45,18),'R0':(5.45,2.35,3.85,2.55,18),'R1':(5.15,5.25,4.45,1.65,16)},
15:{'F0':(.6,1.5,8.8,1.6,18),'F1':(.6,3.65,8.8,3.2,21)},
16:{'F0':(.55,1.6,8.9,4.9,21)},
}

# September 8: split the two clause cases, add full construction, remove CLIQUE.
LAYOUT.update({
 17:LAYOUT[16], 16:LAYOUT[15], 15:LAYOUT[13], 13:LAYOUT[12],
 12:{'F0':(.5,1.2,9,.8,21),'L0':(.4,2.35,4.45,3.8,19),'R0':(5.15,2.35,4.45,4.7,18)},
 14:{'F0':(.45,1.02,9.1,5.55,18),'F1':(.45,6.65,9.1,.75,15)},
 10:{'L0':(.4,1.15,3.15,5.8,18),'R0':(3.85,1.2,5.75,4.9,18),'R1':(3.85,6.3,5.75,.45,14)},
 11:{'L0':(.4,1.15,3.15,5.5,17),'R0':(3.85,1.2,5.75,4.9,18),'R1':(3.85,6.3,5.75,.45,14),'F0':(.4,6.95,9.2,.42,14)},
})

def diagram_crops():
    """One visible-content crop for all reveals of a drawing; source PNGs stay intact.

    Beamer's invisible overlay paths can enlarge the PDF path bounding box.
    Crop only whitespace via native PowerPoint picture cropping, preserving
    identical node positions across reveals and all original drawing pixels.
    """
    result = {}
    groups = {}
    figure_counts=json.loads((ASSETS/'figure-counts.json').read_text())
    active=[ASSETS/f'diagram-{i:02d}-{phase}.png' for i,count in enumerate(figure_counts,1) for phase in range(1,count+1)]
    for path in active:
        groups.setdefault(path.stem.rsplit('-', 1)[0], []).append(path)
    for paths in groups.values():
        boxes = []
        for path in paths:
            with Image.open(path) as image:
                image = image.convert('RGB')
                width, height = image.size
                box = ImageChops.difference(image, Image.new('RGB', image.size, 'white')).getbbox()
                if box: boxes.append(box)
        assert boxes
        left=max(0,min(b[0] for b in boxes)-12)
        top=max(0,min(b[1] for b in boxes)-12)
        right=min(width,max(b[2] for b in boxes)+12)
        bottom=min(height,max(b[3] for b in boxes)+12)
        crop=dict(l=str(round(100000*left/width)),t=str(round(100000*top/height)),
                  r=str(round(100000*(width-right)/width)),b=str(round(100000*(height-bottom)/height)))
        for path in paths:result[path.name]=(crop,(right-left)/(bottom-top))
    return result

def native_style(shape, rect, kind='text', title=False, centered=False):
    x,y,w,h,size=rect
    if shape.tag==f'{{{P}}}graphicFrame':
        xf=shape.find(f'{{{P}}}xfrm')
        for child in list(xf): xf.remove(child)
        ET.SubElement(xf,f'{{{A}}}off',x=str(round(x*914400)),y=str(round(y*914400)))
        ET.SubElement(xf,f'{{{A}}}ext',cx=str(round(w*914400)),cy=str(round(h*914400)))
        grid=shape.find('.//a:tblGrid',NS)
        columns=list(grid); total=sum(int(c.get('w')) for c in columns)
        for c in columns: c.set('w',str(round(int(c.get('w'))/total*w*914400)))
        rows=shape.findall('.//a:tr',NS)
        for row in rows:row.set('h',str(round(h*914400/len(rows))))
    else:
        # Handles a native shape, image, or the native equation AlternateContent.
        targets=[shape] if shape.tag in (f'{{{P}}}sp',f'{{{P}}}pic') else shape.findall('.//p:sp',NS)
        for sp in targets:
            transform(sp,x,y,w,h)
            nv=sp.find('p:nvSpPr/p:nvPr',NS)
            if nv is not None:
                ph=nv.find('p:ph',NS)
                if ph is not None:nv.remove(ph)
    for body in shape.findall('.//a:bodyPr',NS):
        for key in ('lIns','rIns','tIns','bIns'):body.set(key,'0')
        body.set('anchor','t');body.set('wrap','square')
        for tag in ('normAutofit','spAutoFit','noAutofit'):
            for child in body.findall(f'{{{A}}}{tag}'):body.remove(child)
        ET.SubElement(body,f'{{{A}}}noAutofit')
    for tx in shape.findall('.//p:txBody',NS)+shape.findall('.//a:txBody',NS):
        lst=tx.find('a:lstStyle',NS)
        if lst is None:lst=ET.SubElement(tx,f'{{{A}}}lstStyle')
        for child in list(lst):lst.remove(child)
        for level in range(1,10):
            pr=ET.SubElement(lst,f'{{{A}}}lvl{level}pPr')
            rp=ET.SubElement(pr,f'{{{A}}}defRPr',sz=str(round(size*100)))
            ET.SubElement(rp,f'{{{A}}}latin',typeface='Times New Roman')
        for para in tx.findall('a:p',NS):
            pp=para.find('a:pPr',NS)
            if pp is None:pp=ET.Element(f'{{{A}}}pPr');para.insert(0,pp)
            if centered:pp.set('algn','ctr')
            for spacing in pp.findall('a:spcAft',NS):pp.remove(spacing)
            space=ET.Element(f'{{{A}}}spcAft')
            # DrawingML paragraph spacing precedes bullet/default-run properties.
            before=sum(c.tag in (f'{{{A}}}lnSpc',f'{{{A}}}spcBef') for c in pp)
            pp.insert(before,space)
            ET.SubElement(space,f'{{{A}}}spcPts',val='650' if size>=18 else '400')
    for rp in shape.findall('.//a:rPr',NS)+shape.findall('.//a:defRPr',NS)+shape.findall('.//a:endParaRPr',NS):
        rp.set('sz',str(round(size*100)))
        latin=rp.find('a:latin',NS)
        if latin is None:latin=ET.SubElement(rp,f'{{{A}}}latin')
        latin.set('typeface','Times New Roman')
        if title:
            rp.set('b','1')
            for fill in rp.findall('a:solidFill',NS):rp.remove(fill)
            fill=ET.Element(f'{{{A}}}solidFill')
            rp.insert(1 if rp.find(f'{{{A}}}ln') is not None else 0,fill)
            ET.SubElement(fill,f'{{{A}}}srgbClr',val='3333B2')

def compose():
    info=json.loads((BUILD/'elements.json').read_text())
    crops=diagram_crops()
    for prefix,uri in [('p',P),('a',A),('r',R),('a14','http://schemas.microsoft.com/office/drawing/2010/main'),('m','http://schemas.openxmlformats.org/officeDocument/2006/math'),('mc','http://schemas.openxmlformats.org/markup-compatibility/2006')]:ET.register_namespace(prefix,uri)
    fragment_path=BUILD/'fragments.pptx'
    with zipfile.ZipFile(fragment_path) as src:
        fragments=[f for f in src.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',f)]
        assert len(fragments)==info['fragments'], (len(fragments),info['fragments'])
        output={};used_notes={};new_ids=[]
        for slide_no,record in enumerate(info['slides'],1):
            frame=record['frame']
            tid=record['title']
            root=ET.fromstring(src.read(f'ppt/slides/slide{tid}.xml'))
            tree=root.find('p:cSld/p:spTree',NS)
            for child in list(tree):
                if child.tag not in (f'{{{P}}}nvGrpSpPr',f'{{{P}}}grpSpPr'):tree.remove(child)
            relationships=ET.Element(f'{{{PKG}}}Relationships')
            def addrel(rel):
                for existing in relationships:
                    if all(existing.get(k)==rel.get(k) for k in ('Type','Target','TargetMode')):return existing.get('Id')
                new=copy.deepcopy(rel);new.set('Id',f'rId{len(relationships)+1}');relationships.append(new);return new.get('Id')
            def load(fragment):
                slide=ET.fromstring(src.read(f'ppt/slides/slide{fragment}.xml'))
                rels=ET.fromstring(src.read(f'ppt/slides/_rels/slide{fragment}.xml.rels'))
                return slide,{r.get('Id'):r for r in rels}
            title_slide,title_rels=load(tid)
            for rel in title_rels.values():
                if rel.get('Type').endswith('/slideLayout'):addrel(rel)
                if rel.get('Type').endswith('/notesSlide'):
                    addrel(rel)
                    name=posixpath.normpath(posixpath.join('ppt/slides',rel.get('Target')))
                    used_notes[name]=(tid,slide_no)
            def transfer(node,rels):
                node=copy.deepcopy(node)
                for elem in node.iter():
                    for name,value in list(elem.attrib.items()):
                        if name.startswith('{'+R+'}') and value in rels:elem.set(name,addrel(rels[value]))
                tree.append(node)
                return node
            for child in title_slide.find('p:cSld/p:spTree',NS):
                if child.tag==f'{{{P}}}sp' and child.find('p:nvSpPr/p:nvPr/p:ph',NS) is not None:
                    ph=child.find('p:nvSpPr/p:nvPr/p:ph',NS)
                    if ph.get('type') in ('title','ctrTitle'):
                        n=transfer(child,title_rels)
                        native_style(n,(.25,1.0,9.5,.9,25) if frame==1 else (.25,.14,9.5,.78,23.5),title=True,centered=frame==1)
            for element in record['elements']:
                slide,rels=load(element['fragment'])
                rect=LAYOUT[frame][element['key']]
                found=[]
                for child in slide.find('p:cSld/p:spTree',NS):
                    if child.tag in (f'{{{P}}}nvGrpSpPr',f'{{{P}}}grpSpPr'):continue
                    ph=child.find('p:nvSpPr/p:nvPr/p:ph',NS)
                    if ph is not None and ph.get('type') in ('title','ctrTitle'):continue
                    found.append(child)
                assert len(found)==1,(frame,element['key'],element['kind'],len(found))
                child=found[0]
                if element['kind']=='image':
                    blip=child.find('.//a:blip',NS);rel=rels[blip.get(f'{{{R}}}embed')]
                    img_path=posixpath.normpath(posixpath.join('ppt/slides',rel.get('Target')))
                    with Image.open(io.BytesIO(src.read(img_path))) as im:ratio=im.width/im.height
                    description=child.find('p:nvPicPr/p:cNvPr',NS).get('descr','')
                    key=posixpath.basename(description)
                    if key in crops:
                        attrs,ratio=crops[key]
                        fill=child.find('p:blipFill',NS)
                        for old in fill.findall('a:srcRect',NS):fill.remove(old)
                        fill.insert(1,ET.Element(f'{{{A}}}srcRect',attrs))
                    x,y,w,h,size=rect;fw=min(w,h*ratio);fh=fw/ratio
                    rect=(x+(w-fw)/2,y+(h-fh)/2,fw,fh,size)
                n=transfer(child,rels)
                native_style(n,rect,element['kind'],centered=frame==1)
            # Give every native object a unique id within this final slide.
            for uid,cn in enumerate(tree.findall('.//p:cNvPr',NS),1):cn.set('id',str(uid))
            output[f'ppt/slides/slide{slide_no}.xml']=ET.tostring(root,encoding='utf-8',xml_declaration=True)
            output[f'ppt/slides/_rels/slide{slide_no}.xml.rels']=ET.tostring(relationships,encoding='utf-8',xml_declaration=True)
            new_ids.append(slide_no)
        pres=ET.fromstring(src.read('ppt/presentation.xml'));lst=pres.find(f'{{{P}}}sldIdLst')
        for child in list(lst):lst.remove(child)
        pr=ET.fromstring(src.read('ppt/_rels/presentation.xml.rels'))
        for rel in list(pr):
            if rel.get('Type').endswith('/slide'):pr.remove(rel)
        for number in new_ids:
            rid=f'rIdEditable{number}'
            ET.SubElement(lst,f'{{{P}}}sldId',id=str(255+number),attrib={f'{{{R}}}id':rid})
            ET.SubElement(pr,f'{{{PKG}}}Relationship',Id=rid,Type=R+'/slide',Target=f'slides/slide{number}.xml')
        output['ppt/presentation.xml']=ET.tostring(pres,encoding='utf-8',xml_declaration=True)
        output['ppt/_rels/presentation.xml.rels']=ET.tostring(pr,encoding='utf-8',xml_declaration=True)
        content=ET.fromstring(src.read('[Content_Types].xml'));CT='http://schemas.openxmlformats.org/package/2006/content-types'
        for child in list(content):
            name=child.get('PartName','').lstrip('/')
            if name.startswith('ppt/slides/') or (name.startswith('ppt/notesSlides/') and name not in used_notes):content.remove(child)
        for number in new_ids:ET.SubElement(content,f'{{{CT}}}Override',PartName=f'/ppt/slides/slide{number}.xml',ContentType='application/vnd.openxmlformats-officedocument.presentationml.slide+xml')
        output['[Content_Types].xml']=ET.tostring(content,encoding='utf-8',xml_declaration=True)
        with zipfile.ZipFile(ROOT/f'{STEM}.pptx','w',zipfile.ZIP_DEFLATED) as dst:
            for item in src.infolist():
                name=item.filename
                if name in output or name.startswith('ppt/slides/'):continue
                if name.startswith('ppt/notesSlides/'):
                    if '/_rels/' in name:
                        note=name.replace('/_rels/','/').removesuffix('.rels')
                        if note not in used_notes:continue
                        data=ET.fromstring(src.read(name))
                        for rel in data:
                            if rel.get('Type').endswith('/slide'):rel.set('Target',f'../slides/slide{used_notes[note][1]}.xml')
                        dst.writestr(item,ET.tostring(data,encoding='utf-8',xml_declaration=True));continue
                    if name not in used_notes:continue
                dst.writestr(item,src.read(name))
            for name,data in output.items():dst.writestr(name,data)
    print(f'Assembled {len(new_ids)} slides with native editable text, equations and tables.')

def run(args):
    p = subprocess.run([str(a) for a in args], cwd=ROOT, text=True,
                       capture_output=True, errors='replace')
    if p.returncode:
        raise RuntimeError(p.stdout[-5000:] + p.stderr[-5000:])
    return p.stdout

def figures():
    source = (ROOT/'sonia_np_completeness_demo_stepwise.tex').read_text(encoding='utf-8')
    preamble = source.split(r'\begin{document}')[0]
    pictures = re.findall(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}', source, re.S)
    assert len(pictures) == 17
    document = preamble + '\n\\setbeamertemplate{footline}{}\n\\begin{document}\n'
    for picture in pictures:
        document += '\\begin{frame}[plain]\n\\centering\n' + picture + '\n\\end{frame}\n'
    document += '\\end{document}\n'
    path = BUILD/'figures.tex'
    path.write_text(document, encoding='utf-8')
    for i in (1,2):
        print(f'Rendering original TikZ figures, pass {i}/2', flush=True)
        run(['xelatex','-interaction=nonstopmode','-halt-on-error',f'-output-directory={BUILD}',path])
    ranges = [(int(a),int(b)) for a,b in re.findall(r'\\beamer@framepages\s*\{(\d+)\}\{(\d+)\}',(BUILD/'figures.nav').read_text())]
    assert len(ranges)==17
    (ASSETS/'figure-counts.json').write_text(json.dumps([last-first+1 for first,last in ranges]))
    pdf=fitz.open(BUILD/'figures.pdf')
    for diagram,(first,last) in enumerate(ranges,1):
        bbox=fitz.Rect()
        for page in pdf[first-1:last]:
            for kind, bounds in page.get_bboxlog():
                r=fitz.Rect(bounds)
                if kind=='fill-path' and r.width>=page.rect.width-1 and r.height>=page.rect.height-1:
                    continue  # Beamer's white page background.
                if kind!='ignore-text':
                    bbox |= r
        bbox=(bbox+(-2,-2,2,2)) & pdf[first-1].rect
        assert 0<bbox.width<363 and 0<bbox.height<273, (diagram,bbox)
        for phase,page_number in enumerate(range(first,last+1),1):
            pdf[page_number-1].get_pixmap(matrix=fitz.Matrix(6,6),clip=bbox,alpha=False).save(ASSETS/f'diagram-{diagram:02d}-{phase}.png')
    print('Extracted all 17 original TikZ drawings, including their reveals.',flush=True)

def transform(sp, x,y,w,h):
    pr=sp.find('p:spPr',NS)
    old=pr.find('a:xfrm',NS)
    if old is not None: pr.remove(old)
    # xfrm MUST precede geometry/fills; PowerPoint can silently hide pictures
    # when a transform is appended after prstGeom/ln despite a valid ZIP.
    xf=ET.Element(f'{{{A}}}xfrm');pr.insert(0,xf)
    ET.SubElement(xf,f'{{{A}}}off',x=str(round(x*914400)),y=str(round(y*914400)))
    ET.SubElement(xf,f'{{{A}}}ext',cx=str(round(w*914400)),cy=str(round(h*914400)))

def template():
    original=BUILD/'default.pptx'
    run([QUARTO,'pandoc','-o',original,'--print-default-data-file','reference.pptx'])
    for prefix,uri in [('p',P),('a',A),('r','http://schemas.openxmlformats.org/officeDocument/2006/relationships')]:
        ET.register_namespace(prefix,uri)
    with zipfile.ZipFile(original) as src, zipfile.ZipFile(ASSETS/'editable-reference.pptx','w',zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            data=src.read(item.filename)
            if item.filename=='ppt/presentation.xml':
                data=re.sub(rb'<p:sldSz\b[^>]*/>',b'<p:sldSz cx="9144000" cy="6858000" type="screen4x3"/>',data)
            elif item.filename.startswith(('ppt/slideMasters/','ppt/slideLayouts/')) and item.filename.endswith('.xml'):
                root=ET.fromstring(data)
                cs=root.find('p:cSld',NS)
                layout_name=cs.get('name','') if cs is not None else ''
                for sp in root.findall('.//p:sp',NS):
                    ph=sp.find('p:nvSpPr/p:nvPr/p:ph',NS)
                    if ph is None: continue
                    role=ph.get('type','obj'); idx=ph.get('idx','0')
                    if role in ('title','ctrTitle'):
                        transform(sp,.25,.12,9.5,.70)
                    elif role in ('body','obj','subTitle'):
                        if layout_name in ('Two Content','Comparison'):
                            right=idx in ('2','4')
                            transform(sp,5.13 if right else .38,1.04,4.49,5.95)
                        else:
                            transform(sp,.38,1.04,9.24,5.95)
                    elif role in ('dt','ftr','sldNum'):
                        transform(sp,.4 if role!='sldNum' else 8.8,7.13,1 if role=='sldNum' else 7.5,.20)
                    tx=sp.find('p:txBody',NS)
                    if tx is not None:
                        body=tx.find('a:bodyPr',NS)
                        body.set('anchor','t'); body.set('lIns','0'); body.set('rIns','0')
                        body.set('tIns','0'); body.set('bIns','0')
                        lst=tx.find('a:lstStyle',NS)
                        if lst is not None:
                            for child in list(lst): lst.remove(child)
                            for level in range(1,10):
                                para=ET.SubElement(lst,f'{{{A}}}lvl{level}pPr',algn='l')
                                rp=ET.SubElement(para,f'{{{A}}}defRPr',sz='2350' if role in ('title','ctrTitle') else '1800')
                                if role in ('title','ctrTitle'):
                                    rp.set('b','1'); fill=ET.SubElement(rp,f'{{{A}}}solidFill'); ET.SubElement(fill,f'{{{A}}}srgbClr',val='3333B2')
                                ET.SubElement(rp,f'{{{A}}}latin',typeface='Times New Roman')
                for style in root.findall('.//p:txStyles/*',NS):
                    for rp in style.findall('.//a:defRPr',NS):
                        rp.set('sz','2350' if style.tag.endswith('titleStyle') else '1800')
                    for para in list(style):
                        for space in para.findall('a:spcBef',NS):
                            para.remove(space)
                        spacing=ET.SubElement(para,f'{{{A}}}spcBef'); ET.SubElement(spacing,f'{{{A}}}spcPts',val='500')
                data=ET.tostring(root,encoding='utf-8',xml_declaration=True)
            elif item.filename.startswith('ppt/theme/') and item.filename.endswith('.xml'):
                root=ET.fromstring(data)
                for latin in root.findall('.//a:fontScheme/*/a:latin',NS): latin.set('typeface','Times New Roman')
                data=ET.tostring(root,encoding='utf-8',xml_declaration=True)
            dst.writestr(item,data)

def verify():
    with zipfile.ZipFile(ROOT/f'{STEM}.pptx') as z:
        slides=sorted((n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)),key=lambda n:int(re.search(r'(\d+)\.xml',n).group(1)))
        expected=len(json.loads((BUILD/'elements.json').read_text())['slides'])
        assert len(slides)==expected==42, len(slides)
        counts={'slides':len(slides),'text_runs':0,'native_equations':0,'pictures':0,'tables':0}
        for f in slides:
            r=ET.fromstring(z.read(f))
            assert r.find('p:cSld/p:bg',NS) is None, 'Unexpected slide screenshot background'
            text=r.findall('.//a:t',NS)
            assert text, f+' contains no editable text'
            counts['text_runs']+=len(text)
            counts['pictures']+=len(r.findall('.//p:pic',NS))
            counts['tables']+=len(r.findall('.//a:tbl',NS))
            counts['native_equations']+=len(r.findall('.//{http://schemas.openxmlformats.org/officeDocument/2006/math}oMath'))
            for pic in r.findall('.//p:pic',NS):
                assert list(pic.find('p:spPr',NS))[0].tag==f'{{{A}}}xfrm', 'Picture transform must come first'
        assert counts['native_equations']>50
        print(counts)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--skip-figures',action='store_true')
    parser.add_argument('--prepare-only',action='store_true')
    args=parser.parse_args()
    BUILD.mkdir(parents=True,exist_ok=True); ASSETS.mkdir(exist_ok=True)
    if not args.skip_figures: figures()
    template()
    if args.prepare_only:return
    print(run([QUARTO,'render',f'{STEM}.qmd','--to','pptx','--output-dir','build/editable','--output','fragments.pptx']))
    compose()
    verify()

if __name__=='__main__': main()
