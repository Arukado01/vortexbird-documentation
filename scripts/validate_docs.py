from pathlib import Path
import re

root=Path(__file__).resolve().parents[1]
text=(root/'vortexbird-architecture-assessment.md').read_text(encoding='utf-8')
sections=re.findall(r'^## (\d+)\. (.+)$',text,re.M)
assert [int(n) for n,_ in sections]==list(range(1,10)), sections
assert len(list((root/'diagrams').glob('*.mmd')))==14
assert len(list((root/'adr').glob('*.md')))>=5
assert len(re.findall(r'^\| Q\d+',text,re.M))>=8
assert len(re.findall(r'^\| A\d+',text,re.M))>=8
for name in ('presentation-guide.md','implementation-status.md','README.md'):
    assert (root/name).stat().st_size>100
for image in re.findall(r'!\[[^]]*\]\(([^)]+)\)',text):
    assert (root/image).is_file(), image
import json
from xml.etree import ElementTree
manifest=json.loads((root/'diagrams/vector/manifest.json').read_text(encoding='utf-8'))
assert len(manifest)==14
assert [f['number'] for f in manifest]==list(range(1,15))
for figure in manifest:
    path=root/'diagrams/vector'/figure['file']
    svg=ElementTree.parse(path)
    assert svg.getroot().tag.endswith('svg')
    assert path.stat().st_size>1000
for name in ('audit-matrix.md','closure-report.md','operation-runbook.md','manual-inventory.md','execution-evidence.json'):
    assert (root/name).stat().st_size>100
evidence=json.loads((root/'execution-evidence.json').read_text(encoding='utf-8'))
assert evidence['date']=='2026-11-17'
assert 'No desplegado' in evidence['aws_status']
assert len(evidence['tests'])>=5
assert (root/'output/presentation/VortexBird_AndesRetail_Executive.pptx').is_file()
print('PASS: nine technical sections, fourteen valid SVG figures, current reports, evidence and executive deck')
