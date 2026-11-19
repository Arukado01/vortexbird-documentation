"""Build the complete assessment with an editorial layout and native vector atlas."""
from pathlib import Path
import re, html, json, textwrap
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    Table, TableStyle, PageBreak, NextPageTemplate, KeepTogether, Image, Flowable, CondPageBreak)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics import renderPDF
from pypdf import PdfReader
from vector_atlas import export

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'output'/'pdf'; OUT.mkdir(parents=True,exist_ok=True)
DATA=json.loads((ROOT/'execution-evidence.json').read_text(encoding='utf-8'))
FONT=Path('C:/Windows/Fonts')
for n,f in [('Body','arial.ttf'),('Bold','arialbd.ttf'),('Mono','consola.ttf')]:
    pdfmetrics.registerFont(TTFont(n,str(FONT/f)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Body',boldItalic='Bold')
NAVY=colors.HexColor('#102A43'); TEAL=colors.HexColor('#087F8C'); INK=colors.HexColor('#243F50'); MUTED=colors.HexColor('#526D82')
PW,PH=A4; LW,LH=landscape(A4); M=43; CW=PW-2*M
ST={
 'body':ParagraphStyle('body',fontName='Body',fontSize=10.1,leading=14.8,textColor=INK,spaceAfter=8),
 'small':ParagraphStyle('small',fontName='Body',fontSize=8.7,leading=12.2,textColor=INK,spaceAfter=0),
 'head':ParagraphStyle('head',fontName='Bold',fontSize=8.7,leading=12.2,textColor=colors.white),
 'h1':ParagraphStyle('h1',fontName='Bold',fontSize=25,leading=30,textColor=NAVY,spaceBefore=8,spaceAfter=18,keepWithNext=True),
 'h2':ParagraphStyle('h2',fontName='Bold',fontSize=13.5,leading=18,textColor=TEAL,spaceBefore=15,spaceAfter=9,keepWithNext=True),
 'caption':ParagraphStyle('caption',fontName='Body',fontSize=9.4,leading=13.8,textColor=MUTED,spaceAfter=9),
 'code':ParagraphStyle('code',fontName='Mono',fontSize=8,leading=11.5,textColor=NAVY,backColor=colors.HexColor('#F1F6F8'),borderPadding=9,spaceAfter=10),
 'bullet':ParagraphStyle('bullet',fontName='Body',fontSize=10.1,leading=14.8,textColor=INK,leftIndent=12,firstLineIndent=-10,spaceAfter=6),
 'coverTitle':ParagraphStyle('coverTitle',fontName='Bold',fontSize=38,leading=43,textColor=NAVY,spaceAfter=20),
 'coverSub':ParagraphStyle('coverSub',fontName='Body',fontSize=19,leading=26,textColor=MUTED,spaceAfter=18),
}

def rich(t):
    t=t.replace('—','-').replace('–','-').replace('‑','-')
    t=html.escape(t)
    t=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',t)
    t=re.sub(r'`([^`]+)`',r'<font name="Mono">\1</font>',t)
    t=re.sub(r'\[([^]]+)\]\((https?://[^)]+)\)',r'<link href="\2" color="#087F8C">\1</link>',t)
    t=re.sub(r'\[([^]]+)\]\(([^)]+)\)',r'\1',t)
    return t
def p(t,style='body'):return Paragraph(rich(t),ST[style])

def table(rows,width=CW):
    n=len(rows[0]); weights={2:[.27,.73],3:[.24,.32,.44],4:[.21,.23,.27,.29],5:[.13,.23,.20,.20,.24]}.get(n,[1/n]*n)
    if rows[0][0] in ['ID','Semana']: weights=[.09,.46,.45]
    if rows[0][0]=='Riesgo':weights=[.24,.20,.13,.43]
    data=[[p(c,'head' if i==0 else 'small') for c in r] for i,r in enumerate(rows)]
    t=Table(data,colWidths=[width*x for x in weights],repeatRows=1,hAlign='LEFT',splitByRow=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F3F7FA')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,0),(-1,0),1.2,TEAL),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#D6E2EA'))]))
    return [t,Spacer(1,10)]

class VectorFigure(Flowable):
    def __init__(self,drawing,width):
        Flowable.__init__(self); self.drawing=drawing; self.scale=width/drawing.width; self.width=width; self.height=drawing.height*self.scale
    def draw(self):
        self.canv.saveState();self.canv.scale(self.scale,self.scale);renderPDF.draw(self.drawing,self.canv,0,0);self.canv.restoreState()

def chrome(canvas,doc):
    w,h=canvas._pagesize
    if doc.page==1:
        canvas.setFillColor(TEAL);canvas.rect(0,h-12,w,12,fill=1,stroke=0)
    else:
        canvas.setStrokeColor(colors.HexColor('#C6D8E4'));canvas.line(M,h-31,w-M,h-31)
        canvas.setFont('Bold',7.5);canvas.setFillColor(NAVY);canvas.drawString(M,h-24,'VORTEXBIRD / ANDESRETAIL')
        canvas.setFont('Body',7.5);canvas.drawRightString(w-M,h-24,'Arquitectura y estado de validación')
    canvas.setFillColor(MUTED);canvas.setFont('Body',7.5)
    canvas.drawString(M,23,'17 noviembre 2026  |  Validación parcial. AWS pendiente.')
    canvas.drawRightString(w-M,23,f'{doc.page:02d}')

class Document(BaseDocTemplate):
    def afterFlowable(self,f):
        if isinstance(f,Paragraph) and f.style.name=='h1':
            title=f.getPlainText();key='s'+str(self.seq.nextf('heading'));self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(title,key,0,False)
            if title!='Índice':self.notify('TOCEntry',(0,title,self.page,key))

figures=export(); story=[]
story.extend([Spacer(1,65),p('ANDESRETAIL','h2'),p('VortexBird','coverTitle'),p('Plataforma de interoperabilidad','coverSub'),p('Arquitectura, validación y operación','coverSub'),Spacer(1,33)])
story.extend(table([['Estado de esta revisión','Alcance'],['Validación parcial','Código, pruebas acotadas, documentación viva y arquitectura ECS revisados.'],['Servicios conectados','El entorno bloquea loopback. El arranque de procesos no demuestra comunicación integral.'],['AWS pendiente','Sin infraestructura provisionada por esta ejecución. Falta superar la puerta local y aprobar un plan con costos.']]))
story.extend([Spacer(1,35),p('Assessment técnico y atlas vectorial','h2'),p('Edición de entrega · 17 de noviembre de 2026','caption'),p('Fuentes: repositorios de VortexBird, evidencia local y encargo Texto pegado(9).txt. Los simuladores, verificaciones aisladas y servicios desplegados se identifican por separado.','caption'),PageBreak()])
story.append(p('Índice','h1'))
toc=TableOfContents();toc.levelStyles=[ParagraphStyle('toc',fontName='Body',fontSize=10.5,leading=17,spaceBefore=8,textColor=NAVY)]
story.extend([toc,Spacer(1,20),p('El atlas reúne catorce diagramas vectoriales de lectura independiente. Las referencias del texto remiten a sus títulos.','caption'),PageBreak()])
story.append(p('Estado de la entrega','h1'))
story.append(p('La evidencia determina el estado'))
story.extend(table([['Área','Resultado observado'],['Entorno local',DATA['local_blocker']],['Despliegue AWS',DATA['aws_status']],['Costos',DATA['cost']]]))
story.append(p('Pruebas de esta ejecución','h2'))
if DATA['tests']:
    rows=[['Prueba','Resultado','Entorno y límite']]+[[t['name'],t['result'],t['limit']] for t in DATA['tests']]
    story.extend(table(rows))
else: story.append(p('El registro de comandos se conserva en el informe de cierre. Los resultados históricos se mantienen identificados por fecha y no se presentan como repetidos en esta sesión.'))
story.append(p('Dependencias para completar la aceptación','h2'))
for t in DATA['external_pending']:story.append(p('• '+t,'bullet'))

lines=(ROOT/'vortexbird-architecture-assessment.md').read_text(encoding='utf-8').splitlines();i=0;started=False
while i<len(lines):
    line=lines[i].strip()
    if re.match(r'## 1\.',line):started=True
    if not started or not line:i+=1;continue
    if re.match(r'## \d+\.',line):story.extend([CondPageBreak(340),Spacer(1,12),p(line[3:],'h1')]);i+=1;continue
    if line.startswith('### '):story.append(p(line[4:],'h2'));i+=1;continue
    if line.startswith('!['):
        caption=re.match(r'!\[([^]]+)\]',line).group(1)
        story.append(p('Referencia visual: '+caption+' Consulte el atlas vectorial al final.','caption'));i+=1;continue
    if line.startswith('```'):
        i+=1;code=[]
        while i<len(lines) and not lines[i].startswith('```'):
            code.extend(textwrap.wrap(lines[i],width=88,replace_whitespace=False,drop_whitespace=False) or ['']);i+=1
        for j in range(0,len(code),22):story.append(Paragraph('<br/>'.join(html.escape(l).replace(' ','&#160;') for l in code[j:j+22]),ST['code']))
        i+=1;continue
    if line.startswith('|'):
        rows=[]
        while i<len(lines) and lines[i].strip().startswith('|'):
            row=[c.strip() for c in lines[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r'[:\- ]+',c or '-') for c in row):rows.append(row)
            i+=1
        story.extend(table(rows));continue
    if line.startswith('- '):story.append(p('• '+line[2:],'bullet'));i+=1;continue
    if re.match(r'^\d+\. ',line):story.append(p(line,'bullet'));i+=1;continue
    paragraph=[line];i+=1
    while i<len(lines) and lines[i].strip() and not re.match(r'^(#|\||```|!\[|- |\d+\. )',lines[i].strip()):paragraph.append(lines[i].strip());i+=1
    story.append(p(' '.join(paragraph)))

story.extend([PageBreak(),p('Atlas de arquitectura','h1'),p('Catorce figuras vectoriales','h2'),p('Los diagramas representan relaciones verificadas en el código o el diseño objetivo indicado en cada figura. Ninguno acredita por sí mismo el funcionamiento de un entorno conectado.'),Spacer(1,12)])
story.extend(table([['Figura','Contenido']]+[[f"{f['number']:02d}",f['title']] for f in figures]))
for f in figures:
    story.extend([NextPageTemplate('landscape'),PageBreak(),VectorFigure(f['drawing'],LW-2*M),Spacer(1,6),p(f['caption'],'caption')])

if DATA['screenshots']:
    story.extend([NextPageTemplate('portrait'),PageBreak(),p('Pantallas y alcance de evidencia','h1')])
    for s in DATA['screenshots']:
        path=Path(s['path']);path=path if path.is_absolute() else ROOT/path
        if not path.exists():continue
        from PIL import Image as PILImage
        im=PILImage.open(path); width=CW;height=width*im.height/im.width
        story.extend([p(s['title'],'h2'),Image(str(path),width=width,height=height),p(s['caption'],'caption')])

dest=OUT/'vortexbird-architecture-assessment.pdf'
doc=Document(str(dest),pagesize=A4,leftMargin=M,rightMargin=M,topMargin=48,bottomMargin=43,title='VortexBird - Arquitectura y validación - AndesRetail',author='VortexBird / AndesRetail',pageCompression=1)
doc.addPageTemplates([PageTemplate(id='portrait',pagesize=A4,frames=Frame(M,43,CW,PH-91,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0),onPage=chrome),PageTemplate(id='landscape',pagesize=landscape(A4),frames=Frame(M,43,LW-2*M,LH-91,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0),onPage=chrome)])
doc.multiBuild(story)
reader=PdfReader(dest);text='\n'.join(page.extract_text() or '' for page in reader.pages)
assert all(x in text for x in ['Índice','Cultura y liderazgo','Atlas de arquitectura','Despliegue AWS'])
assert len(list((ROOT/'diagrams'/'vector').glob('*.svg')))==14
result={'file':str(dest),'pages':len(reader.pages),'landscape_pages':sum(float(page.mediabox.width)>float(page.mediabox.height) for page in reader.pages),'vector_figures':14,'text_chars':len(text)}
(OUT/'architecture-build-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
