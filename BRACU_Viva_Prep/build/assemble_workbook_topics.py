"""Mechanically excerpt existing explanations for the seniors' XLSX topic list.

No full reference book is changed. Selection is explicit, heading-bounded,
fence-aware, and recorded with original line ranges and SHA-256 hashes.
"""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'BRACU_Viva_Prep'

# Course, workbook routing, UIU inclusion, [(source volume, heading patterns)].
SELECTION = [
 ('Structured programming: parameter passing', 'DSA B42; BRAC Ques Bank C9', True, [
  ('04', [r'^7\.1 ', r'^11\.1 ', r'^11\.3 ', r'^11\.4 ', r'^20\.2 '])]),
 ('Object-oriented programming', 'DSA B40/B42/B62–B72; Random Screenshots constructors, abstract classes, friends and inheritance; BRAC C37/C45', True, [
  ('03', [r'^Part I ', r'^Constructors$', r'^Lecture 3 ', r'^References$',
          r'^Lecture 5 ', r'^Lecture 7 ', r'^Lecture 10 ',
          r'^The pass-by-value correction$', r'^Overriding, hiding, and dispatch$',
          r'^Abstract classes and anonymous subclasses$', r'^Interfaces$',
          r'^Abstract class versus interface in Java$', r'^Workbook board supplement '])]),
 ('Discrete mathematics and number theory', 'Runtime Analysis number-theory screenshot; BRAC C5/C37; graph and hashing prerequisites', True, [
  ('10', [r'^106\. ', r'^107\. ', r'^110\. ', r'^111\. ', r'^112\. ', r'^113\. ', r"^Seniors' workbook supplement"]),
  ('01', [r'^15\.1 '])]),
 ('Data structures, searching, sorting and dynamic programming', 'DSA B7–B38/B58; Board B35/B37; Runtime Analysis sorting screenshot; BRAC array/list, circular array, DP, stock-profit and graph questions', True, [
  ('01', [r'^1\. ', r'^2\.1 ', r'^2\.2 ', r'^2\.5 ',
          r'^3\.2 ', r'^3\.3 ', r'^3\.6 ', r'^4\.1 ',
          r'^5\.1 ', r'^5\.2 ', r'^5\.3 ', r'^5\.4 ',
          r'^6\. ', r'^7\. ', r'^8\. ', r'^9\. ', r'^10\. ', r'^11\. ',
          r'^12\.1 ', r'^12\.3 ', r'^14\.1 ', r'^14\.2 ', r'^14\.3 ', r'^14\.5 ', r'^14\.12 ', r'^17\. '])]),
 ('Graph algorithms, hashing and amortized analysis', 'DSA B5/B44–B56; Board B9–B15; Runtime Analysis MST/shortest-path screenshots; hidden Niche Topics C4 (Johnson)', True, [
  ('02', [r'^3\.1 ', r'^3\.2 ', r'^3\.3 ', r'^3\.4 ', r'^3\.6 ',
          r'^4\. ', r'^5\.2 ', r'^5\.3 ', r'^13\.1 ', r'^13\.2 ', r'^13\.3 ',
          r'^13\.4 ', r'^13\.5 ', r'^17\. ', r'^21\. ::lead', r'^21\.5 ', r'^24\. '])]),
 ('Database topics from the interviews', 'DB tab is work-in-progress; BRAC C19 (ACID), C41 (NoSQL to SQL); Board B41 (SQL injection)', True, [
  ('05', [r'^1\.6 ', r'^2\.1 ', r'^2\.2 ', r'^18\.1 ', r'^18\.2 ', r'^26\. ']),
  ('13', [r'^11\.1 ', r'^19\.4 '])]),
 ('Software engineering', 'BRAC C5 (Agile versus waterfall); BRAC C11 professional ethics', True, [
  ('08', [r'^2\. ', r'^3\. ', r'^4\. ', r'^17\.4 '])]),
 ('Operating systems', 'OS B3–B15; BRAC C11/C13/C31/C37/C49: scheduling, deadlock, semaphores, page tables, replacement and context switching', True, [
  ('06', [r'^[1-6]\. ', r'^Workbook supplement ', r'^15\.1 ', r'^15\.2 ',
          r'^15\.5 ', r'^15\.6 ', r'^15\.8 ', r'^15\.10 ', r'^15\.11 ', r'^15\.12 ', r'^15\.13 '])]),
 ('Artificial intelligence', 'AI B4–B34; DSA BFS/DFS completeness claims; BRAC rationality, search, minimax and alpha-beta; ML horizon effect', True, [
  ('09', [r'^1\. ', r'^[3-9]\. ', r'^1[0-9]\. ', r'^20\. ',
          r'^2[5-8]\. ', r'^Workbook supplement '])]),
 ('Machine learning', 'Entire ML tab; classification/regression/ensemble screenshots; BRAC bias–variance, k-means, MLE/EM, XGBoost, AdaBoost, GD, LSTM, Transformers and LM/LLM', True, [
  ('11', [r'^[1-9]\. ', r'^1[0-2]\. ', r'^1[5-9]\. ', r'^24\. ',
          r'^34\. ', r'^3[7-9]\. ', r'^4[0-5]\. ', r'^46\. ',
          r'^5[1-8]\. ', r'^Workbook supplement '])]),
 ('Computer networking', 'Computer Network B3/C3 (OSI); Board B31; BRAC TCP/UDP, IPv4/IPv6, NAT/PAT, MAC/IP and loss handling', False, [
  ('07', [r'^The 30-second map of the course$', r'^Protocol[s]?, services, encapsulation$', r'^What the network layer provides$',
          r'^Same subnet versus remote subnet$', r'^ARP$', r'^IPv4 header$',
          r'^IPv4 addressing and CIDR$', r'^Public, private, loopback, and link-local IPv4$',
          r'^NAT and PAT$', r'^Ports, sockets, and the five-tuple$', r'^Part IX ',
          r'^Part X ', r'^Why IPv6$', r'^IPv4 versus IPv6$'])]),
 ('Security and cryptography', 'Things to Explain on Board: RSA/AES/MITM/spoofing/hijacking/Wi-Fi/cache poisoning/access/crypto/buffer overflow; BRAC CIA, hashing, salt, detection and hunting', False, [
  ('13', [r'^1\. ', r'^4\. ', r'^5\. ', r'^8\. ', r'^10\.1 ', r'^10\.5 ',
          r'^14\.5 ', r'^16\.2 ', r'^16\.3 ', r'^17\.1 ',
          r'^21\.1 ', r'^21\.2 ', r'^22\.1 ', r'^25\.1 ', r'^26\. '])]),
 ('Architecture and digital logic', 'Computer Archi B8/B10/B12; Random Screenshots Moore/Mealy; BRAC signed overflow, cache/memory, exponent bias, asynchronous circuits', False, [
  ('14', [r'^1\. ', r'^4\. ', r'^6\. ', r'^7\. ', r'^11\. ',
          r'^H[1-3]\. ', r'^23\.7 ', r'^25\.2 '])]),
 ('Computer graphics', 'BRAC C5 (RGB/CMYK), C7 (ray tracing), C51 (ambient and illumination)', False, [
  ('12', [r'^3[1-6]\. ', r'^38\. ', r'^39\. ', r'^41\. ', r'^44\. '])]),
 ('Theory of computation and compiler phases', 'Hidden Niche Topics C6 (Kleene); BRAC C45 (compiler phases)', False, [
  ('15', [r'^1\. ', r'^2\.1 ', r'^3\.1 ', r'^4\. ', r'^18\. '])]),
 ('Interview, research ownership and industry preparation', 'Industry Prep advice and BRAC question-bank prompts about thesis motivation, ownership, outcomes, research plans, CV and coding on paper', False, [
  ('00', [r'^1\.1 ', r'^2\.4 ', r'^3\. ']),
  ('17', [r'^1\. ', r'^11\. ', r'^12\.5 '])]),
]

def scan(text):
    lines = text.splitlines(keepends=True)
    headings, fence = [], None
    for i,line in enumerate(lines):
        marker = re.match(r'^\s*(`{3,}|~{3,})',line)
        if marker:
            run=marker.group(1)
            if fence is None: fence=run
            elif run[0]==fence[0] and len(run)>=len(fence): fence=None
            continue
        match=re.match(r'^(#{1,6})\s+(.+?)\s*$',line)
        if match and fence is None:
            headings.append(dict(start=i,level=len(match[1]),title=match[2]))
    assert fence is None, 'Unclosed code fence in source'
    for pos,h in enumerate(headings):
        h['end']=next((n['start'] for n in headings[pos+1:] if n['level']<=h['level']),len(lines))
    return lines,headings

def excerpts(prefix, patterns):
    files=list(SOURCE.glob(prefix+'_*.md'))
    assert len(files)==1,(prefix,files)
    source=files[0]
    text=source.read_text(encoding='utf-8')
    lines,headings=scan(text)
    selected={}
    for pattern in patterns:
        lead_only=pattern.endswith('::lead')
        if lead_only: pattern=pattern.removesuffix('::lead')
        matches=[h for h in headings if re.search(pattern,h['title'])]
        assert matches,(source.name,pattern)
        for h in matches:
            h=dict(h)
            if lead_only: h['end']=next((n['start'] for n in headings if n['start']>h['start']),len(lines))
            selected[h['start']]=h
    retained=[]
    for h in sorted(selected.values(),key=lambda x:x['start']):
        if retained and h['start']<retained[-1]['end']: continue
        retained.append(h)
    output=[]
    for h in retained:
        original=''.join(lines[h['start']:h['end']]).strip()
        # Only heading depth is changed; code, math, diagrams and prose stay intact.
        excerpt_lines,local_headings=scan(original)
        for child in local_headings:
            depth=min(6,2+child['level']-h['level'])
            excerpt_lines[child['start']]='#'*depth+' '+child['title']+'\n'
        body=''.join(excerpt_lines).strip()
        assert scan(body)[0],h['title']
        record=dict(file=source.name,title=h['title'],first_line=h['start']+1,last_line=h['end'],
                    source_sha256=hashlib.sha256(original.encode()).hexdigest(),characters=len(original))
        body+=f"\n\n*Excerpt source: `{source.name}`, original lines {h['start']+1}–{h['end']}. Original section numbers are retained.*\n"
        output.append((body,record))
    return output

def main():
    collected=[]
    for course,routing,uiu,sources in SELECTION:
        chunks=[]
        for prefix,patterns in sources: chunks.extend(excerpts(prefix,patterns))
        collected.append((course,routing,uiu,chunks))
    for pack in ('BRACU','UIU'):
        groups=[g for g in collected if pack=='BRACU' or g[2]]
        title=f"{pack} — Seniors' Workbook Topics Explained"
        intro=f"""Bismillah.

# {title}

Focused companion to `Varsity_Topics_List_In Memory of Masud.xlsx`.
This book **copies existing explanations**, including their worked examples,
equations, code and diagrams. It is not another copy of the entire course pack.
The workbook's substantive topics across its subject tabs, interview questions,
embedded screenshots and hidden Niche Topics tab determine the selection.

{'This edition covers all identifiable technical topics in the workbook, plus its general research/interview preparation prompts.' if pack=='BRACU' else 'This edition filters those workbook topics to UIU-listed courses: structured programming, OOP, discrete mathematics, data structures, algorithms, DBMS, SWE, OS, AI and ML. SQL injection is retained as a database topic; standalone networking/security/hardware/graphics/TOC and personal research chapters are excluded.'}

Sections are copied whole so definitions and code prerequisites are not reduced
to isolated answers. Original section numbers, source labels, and cross-references
are retained; a reference to a section not reproduced here points back to the
named full book in `BRACU_Viva_Prep`. These are corrected explanations, not an
endorsement of inaccurate shorthand in the spreadsheet.

The DB tab says only “Work in progress”; database prompts elsewhere in the
workbook are included. Resource links, dedication artwork, and unidentified
questions have no technical explanation to copy; linked external collections
are not silently treated as read or solved. See the existing
`20_SENIORS_WORKBOOK_COVERAGE_AUDIT.md` for the cell-by-cell audit and screenshot
ledger. The original reference books and PDFs remain unchanged.

## Workbook-to-chapter map

| Chapter | Workbook topic routing |
|---|---|
"""
        intro+='\n'.join(f'| {i}. {g[0]} | {g[1]} |' for i,g in enumerate(groups,1))+'\n'
        parts=[intro]
        manifest=[]
        for i,(course,routing,uiu,chunks) in enumerate(groups,1):
            parts.append(f'\n<div class="volume-break"></div>\n\n# {i}. {course}\n\nWorkbook coverage: {routing}.\n')
            for body,record in chunks:
                parts.append(body)
                manifest.append(dict(chapter=course,**record))
        folder=ROOT/(pack+'_Viva_Prep')
        path=folder/(pack+'_Seniors_Workbook_Topics_Explained.md')
        path.write_text('\n\n'.join(parts).rstrip()+'\n',encoding='utf-8')
        target=folder/'build'/'workbook_topics'
        target.mkdir(exist_ok=True)
        (target/'selection.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
        # Every selected excerpt is present and every fenced block is balanced.
        scan(path.read_text(encoding='utf-8'))
        print(f'{pack}: {len(groups)} chapters, {len(manifest)} excerpts, {path.stat().st_size:,} bytes; {path.name}')

if __name__=='__main__': main()
