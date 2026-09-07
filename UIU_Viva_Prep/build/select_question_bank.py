"""Copy complete in-scope chapters from the BRACU question bank, retaining sources."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
source = root.parent / 'BRACU_Viva_Prep' / '19_CORE_COURSES_COMMON_INTERVIEW_QA.md'
text = source.read_text(encoding='utf-8')
matches = list(re.finditer(r'^# (\d+)\. (.+)$', text, re.M))
sections = {int(m.group(1)): text[m.start():matches[i+1].start() if i+1<len(matches) else len(text)].strip()
            for i,m in enumerate(matches)}
selected = [4, 3, 1, 8, 6, 10, 9, 2]
intro = '''# Bismillah.

# UIU Relevant Common Interview Questions and Detailed Answers

This is a scope-selected copy of the existing BRACU cross-university question
bank. The eight chapters below retain their complete answers, code, diagrams,
source references, and follow-ups. Chapter order follows UIU's domains where
possible. Structured C programming is covered by volume 04 and the UIU demo
guide; DSA covers both Data Structures and Algorithms. AI includes ML here,
as requested. Networking and standalone security chapters are excluded.

This is a practice bank, not a prediction of UIU's random topic or actual questions.
Consult the detailed subject books for the full slide-grounded explanations.

For algorithms, practise: contract, idea, trace, invariant, complexity, code,
and edge cases. For equations, define every variable and assumption before
substitution. For systems, explain mechanism, example, trade-off, and failure case.

Original bank: `../BRACU_Viva_Prep/19_CORE_COURSES_COMMON_INTERVIEW_QA.md`.
See `README.md` for the mapping to the copied academic notes.
'''
parts = [intro]
for new_number, old_number in enumerate(selected, 1):
    chapter = sections[old_number]
    chapter = re.sub(r'^# \d+\.', f'# {new_number}.', chapter, count=1)
    parts.append(chapter)
cross = sections[11].split('## 11.4')[0]
cross = cross.replace('# 11.', '# 9.', 1)
cross = re.sub(r'^## 11\.', '## 9.', cross, flags=re.M)
parts.append(cross)
target = root / '19_UIU_RELEVANT_COMMON_INTERVIEW_QA.md'
target.write_text('\n\n'.join(parts).rstrip()+'\n', encoding='utf-8')
print(f'Selected 8 subject chapters and general follow-up drills: {target.name}')
