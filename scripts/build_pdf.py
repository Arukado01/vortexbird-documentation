from pathlib import Path
import re, html, textwrap
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, CondPageBreak, Image, Preformatted, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output'/'pdf'; OUT.mkdir(parents=True,exist_ok=True)
FONTDIR=Path('C:/Windows/Fonts') if Path('C:/Windows/Fonts').exists() else Path('/usr/share/fonts/truetype/dejavu')
win=FONTDIR.name.lower()=='fonts'
for name,file in [('Body','arial.ttf' if win else 'DejaVuSans.ttf'),('Bold','arialbd.ttf' if win else 'DejaVuSans-Bold.ttf'),('Mono','consola.ttf' if win else 'DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONTDIR/file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Body',boldItalic='Bold')
NAVY=colors.HexColor('#09263E'); TEAL=colors.HexColor('#087F8C'); INK=colors.HexColor('#243F50')
W,H=A4; M=43; CONTENT=W-2*M
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Text',fontName='Body',fontSize=9.1,leading=13.5,textColor=INK,spaceAfter=6))
styles.add(ParagraphStyle(name='SmallText',parent=styles['Text'],fontSize=8.2,leading=11.4,spaceAfter=0))
styles.add(ParagraphStyle(name='TableHead',parent=styles['SmallText'],fontName='Bold',textColor=colors.white))
styles.add(ParagraphStyle(name='TitleVB',fontName='Bold',fontSize=29,leading=35,textColor=NAVY,spaceAfter=16))
styles.add(ParagraphStyle(name='H2VB',fontName='Bold',fontSize=20,leading=25,textColor=NAVY,spaceBefore=15,spaceAfter=16,keepWithNext=True))
styles.add(ParagraphStyle(name='H3VB',fontName='Bold',fontSize=12.4,leading=17,textColor=TEAL,spaceBefore=12,spaceAfter=8,keepWithNext=True))
styles.add(ParagraphStyle(name='CodeVB',fontName='Mono',fontSize=7.3,leading=10,textColor=NAVY,backColor=colors.HexColor('#F1F6F8'),borderPadding=10,spaceAfter=11))
styles.add(ParagraphStyle(name='BulletVB',parent=styles['Text'],leftIndent=13,firstLineIndent=-9))
styles.add(ParagraphStyle(name='CaptionVB',parent=styles['Text'],fontSize=8.1,leading=11,textColor=colors.HexColor('#607887'),spaceAfter=12))

def rich(t):
    t=t.replace('—','-').replace('–','-').replace('‑','-')
    t=html.escape(t)
    t=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',t)
    t=re.sub(r'`([^`]+)`',r'<font name="Mono">\1</font>',t)
    t=re.sub(r'\[([^]]+)\]\((https?://[^)]+)\)',r'<link href="\2" color="#087F8C">\1</link>',t)
    return t

def para(t,style='Text'):return Paragraph(rich(t),styles[style])

def table(rows):
    count=len(rows[0]); lengths=[]
    for col in range(count):
        mean=sum(min(len(r[col]),180) for r in rows)/len(rows)
        lengths.append(max(5,mean**.65))
    if rows[0][0]=='ID': weights=[.08,.49,.43]
    elif rows[0][0]=='Riesgo': weights=[.22,.20,.13,.45]
    elif rows[0][0]=='Amenaza': weights=[.19,.24,.36,.21]
    elif rows[0][0]=='Dato': weights=[.21,.26,.16,.37]
    elif rows[0][0]=='Semana': weights=[.10,.47,.43]
    elif count==3: weights=[.23,.36,.41]
    elif count==4: weights=[.22,.26,.26,.26]
    elif count==5: weights=[1/count]*count
    else: weights=[x/sum(lengths) for x in lengths]
    widths=[CONTENT*x for x in weights]
    data=[[para(cell,'TableHead' if i==0 else 'SmallText') for cell in row] for i,row in enumerate(rows)]
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F3F7F9')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),1,TEAL),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#D8E3E8'))]))
    return [t,Spacer(1,10)]

story=[]; lines=(ROOT/'vortexbird-architecture-assessment.md').read_text(encoding='utf-8').splitlines(); i=0
while i<len(lines):
    line=lines[i].strip()
    if not line:i+=1;continue
    if line.startswith('# '):
        story.extend([Spacer(1,42),para('ARQUITECTURA / INTEROPERABILIDAD','H3VB'),para(line[2:],'TitleVB')]);i+=1;continue
    if re.match(r'## \d+\.',line):
        story.extend([PageBreak() if line.startswith('## 1.') else CondPageBreak(260),para(line[3:],'H2VB')]);i+=1;continue
    if line.startswith('### '):story.append(para(line[4:],'H3VB'));i+=1;continue
    if line.startswith('```'):
        i+=1; code=[]
        while i<len(lines) and not lines[i].startswith('```'):
            for chunk in textwrap.wrap(lines[i],width=91,replace_whitespace=False,drop_whitespace=False) or ['']:code.append(chunk)
            i+=1
        story.append(Preformatted('\n'.join(code),styles['CodeVB']));i+=1;continue
    if line.startswith('|'):
        rows=[]
        while i<len(lines) and lines[i].strip().startswith('|'):
            row=[c.strip() for c in lines[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r'[:\- ]+',c or '-') for c in row):rows.append(row)
            i+=1
        story.extend(table(rows));continue
    match=re.match(r'!\[([^]]+)\]\(([^)]+)\)',line)
    if match:
        path=ROOT/match.group(2)
        with PILImage.open(path) as image: iw,ih=image.size
        width=CONTENT; height=width*ih/iw
        if height>450:height=450;width=height*iw/ih
        story.extend([Image(str(path),width=width,height=height),para(match.group(1),'CaptionVB')]);i+=1;continue
    if line.startswith('- '):story.append(para('• '+line[2:],'BulletVB'));i+=1;continue
    if re.match(r'^\d+\. ',line):story.append(para(line,'BulletVB'));i+=1;continue
    p=[line];i+=1
    while i<len(lines) and lines[i].strip() and not re.match(r'^(#|\||```|!\[|- |\d+\. )',lines[i].strip()):p.append(lines[i].strip());i+=1
    story.append(para(' '.join(p)))

def page(canvas,doc):
    canvas.saveState();canvas.setStrokeColor(TEAL);canvas.setLineWidth(1.5);canvas.line(M,H-32,W-M,H-32)
    canvas.setFont('Bold',7.6);canvas.setFillColor(NAVY);canvas.drawString(M,H-24,'VORTEXBIRD  /  INTEGRATION PLATFORM')
    canvas.setFont('Body',7);canvas.setFillColor(colors.HexColor('#607887'))
    canvas.drawString(M,25,'AndesRetail · Assessment de arquitectura · 13 noviembre 2026')
    canvas.drawRightString(W-M,25,str(doc.page));canvas.restoreState()

dest=OUT/'vortexbird-architecture-assessment.pdf'
doc=SimpleDocTemplate(str(dest),pagesize=A4,leftMargin=M,rightMargin=M,topMargin=52,bottomMargin=43,title='VortexBird Integration Platform - Assessment de arquitectura',author='Propuesta técnica para sustentación',pageCompression=1)
doc.build(story,onFirstPage=page,onLaterPages=page)
reader=PdfReader(dest)
assert len(reader.pages)>=9
extracted='\n'.join(p.extract_text() or '' for p in reader.pages)
assert all(title in extracted for title in ('Resumen ejecutivo','Cultura y liderazgo','Seguridad','Observabilidad'))
print(f'PDF generated: {dest}; {len(reader.pages)} pages; text checks passed')
