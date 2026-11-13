from pathlib import Path
import re

root=Path(__file__).resolve().parents[1]
text=(root/'vortexbird-architecture-assessment.md').read_text(encoding='utf-8')
sections=re.findall(r'^## (\d+)\. (.+)$',text,re.M)
assert [int(n) for n,_ in sections]==list(range(1,10)), sections
assert len(list((root/'diagrams').glob('*.mmd')))==10
assert len(list((root/'adr').glob('*.md')))>=5
assert len(re.findall(r'^\| Q\d+',text,re.M))>=8
assert len(re.findall(r'^\| A\d+',text,re.M))>=8
for name in ('presentation-guide.md','implementation-status.md','README.md'):
    assert (root/name).stat().st_size>100
for image in re.findall(r'!\[[^]]*\]\(([^)]+)\)',text):
    assert (root/image).is_file(), image
print('PASS: nine sections, questions, assumptions, ten diagrams, ADRs and linked images')
