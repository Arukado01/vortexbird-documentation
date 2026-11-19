"""Deterministic raster diagrams matching editable Mermaid relationships.

No external service is required. Mermaid remains the editable source; these
publication figures make layout predictable in the PDF build.
"""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "diagrams" / "rendered"
OUT.mkdir(parents=True, exist_ok=True)
NAVY = "#09263E"
TEAL = "#087F8C"
BG = "#F5F8FA"

def font(size, bold=False):
    paths = [Path("C:/Windows/Fonts") / ("arialbd.ttf" if bold else "arial.ttf"),
             Path("/usr/share/fonts/truetype/dejavu") / ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")]
    return ImageFont.truetype(str(next(p for p in paths if p.exists())), size)

def wrap(draw, text, f, width):
    lines=[]
    for para in text.split("\n"):
        row=""
        for word in para.split():
            candidate=(row+" "+word).strip()
            if draw.textlength(candidate,font=f)>width and row:
                lines.append(row); row=word
            else: row=candidate
        lines.append(row)
    return lines

def arrow(draw, a, b, label=None, dashed=False):
    color="#678092"
    if dashed:
        steps=max(1,int(math.dist(a,b)//18))
        for i in range(steps):
            if i%2==0:
                p=tuple(a[k]+(b[k]-a[k])*i/steps for k in (0,1))
                q=tuple(a[k]+(b[k]-a[k])*(i+1)/steps for k in (0,1))
                draw.line((p,q),fill=color,width=3)
    else: draw.line((a,b),fill=color,width=3)
    ang=math.atan2(b[1]-a[1],b[0]-a[0])
    pts=[b,(b[0]-16*math.cos(ang-.4),b[1]-16*math.sin(ang-.4)),(b[0]-16*math.cos(ang+.4),b[1]-16*math.sin(ang+.4))]
    draw.polygon(pts,fill=color)
    if label:
        mid=((a[0]+b[0])/2,(a[1]+b[1])/2)
        f=font(20); width=draw.textlength(label,font=f)
        draw.rectangle((mid[0]-width/2-6,mid[1]-15,mid[0]+width/2+6,mid[1]+15),fill=BG)
        draw.text(mid,label,font=f,fill=NAVY,anchor="mm")

def diagram(filename,title,subtitle,nodes,edges,height=1000):
    im=Image.new("RGB",(1500,height),BG); d=ImageDraw.Draw(im)
    d.rectangle((0,0,1500,130),fill=NAVY)
    d.text((55,30),title,font=font(34,True),fill="white")
    d.text((55,82),subtitle,font=font(21),fill="#A8DDE1")
    boxes={}
    for key,text,x,y in nodes:
        boxes[key]=(x,y,x+340,y+110)
    for edge in edges:
        source,target,*rest=edge; a=boxes[source]; b=boxes[target]
        ac=((a[0]+a[2])/2,(a[1]+a[3])/2); bc=((b[0]+b[2])/2,(b[1]+b[3])/2)
        if abs(ac[0]-bc[0])>abs(ac[1]-bc[1])*1.5:
            p=(a[2] if bc[0]>ac[0] else a[0],ac[1]); q=(b[0] if bc[0]>ac[0] else b[2],bc[1])
        else:
            p=(ac[0],a[3] if bc[1]>ac[1] else a[1]); q=(bc[0],b[1] if bc[1]>ac[1] else b[3])
        arrow(d,p,q,rest[0] if rest else None)
    for key,text,x,y in nodes:
        d.rounded_rectangle(boxes[key],radius=16,fill="white",outline="#B7CCD5",width=2)
        d.rectangle((x+1,y+18,x+6,y+92),fill=TEAL)
        lines=wrap(d,text,font(24,True),305)
        start=y+55-len(lines)*15
        for i,line in enumerate(lines): d.text((x+170,start+i*30),line,font=font(24,True),fill=NAVY,anchor="mt")
    d.text((55,height-40),"VortexBird Integration Platform  |  Diseño técnico de AndesRetail",font=font(18),fill="#687E8D")
    im.save(OUT/filename)

def sequence(filename,title,participants,steps,note):
    height=220+len(steps)*100+130
    im=Image.new("RGB",(1500,height),BG); d=ImageDraw.Draw(im)
    d.rectangle((0,0,1500,115),fill=NAVY); d.text((45,30),title,font=font(32,True),fill="white")
    xs=[140+i*(1220/max(len(participants)-1,1)) for i in range(len(participants))]
    for x,name in zip(xs,participants):
        d.rounded_rectangle((x-126,145,x+126,215),radius=12,fill="white",outline="#B7CCD5",width=2)
        lines=wrap(d,name,font(21,True),232)
        for j,line in enumerate(lines):d.text((x,159+j*25),line,font=font(21,True),fill=NAVY,anchor="mt")
        d.line((x,215,x,height-130),fill="#CCD9DF",width=2)
    for i,(src,tgt,text) in enumerate(steps):
        y=275+i*100
        if src==tgt:
            x=xs[src]; d.line((x,y,x+70,y,x+70,y+30),fill=TEAL,width=3); arrow(d,(x+70,y+30),(x,y+30))
            d.text((x+85,y),text,font=font(20),fill=NAVY)
        else:
            arrow(d,(xs[src],y+30),(xs[tgt],y+30))
            left=min(xs[src],xs[tgt]); width=abs(xs[src]-xs[tgt])-20
            lines=wrap(d,text,font(21),max(width,200))
            for j,line in enumerate(lines):d.text((left+10,y-25+j*25),line,font=font(21),fill=NAVY)
    for j,line in enumerate(wrap(d,note,font(19),1400)):
        d.text((45,height-95+j*25),line,font=font(19),fill="#687E8D")
    im.save(OUT/filename)

diagram("01-architecture.png","01 / Arquitectura general","ECS Fargate es el destino inicial. Adaptadores de negocio de demostración.",[
 ("browser","Portal y canales",580,180),("edge","ALB HTTPS",580,350),("identity","Keycloak externo OIDC",1060,350),
 ("web","Frontend ECS",100,530),("api","API .NET en ECS",580,530),("cache","Redis TLS opcional",1060,530),
 ("db","PostgreSQL y outbox",580,710),("worker","Worker ECS",580,880),("sqs","SQS Standard y DLQ",100,880),
 ("adapters","Adaptadores simulados y sandbox",1060,880)],
 [("browser","edge"),("edge","web"),("edge","api"),("identity","api"),("identity","web"),("api","cache"),
  ("api","db"),("db","worker"),("worker","sqs"),("worker","adapters")],1060)

diagram("02-aws-deployment.png","02 / Despliegue ECS Fargate","Terraform definido. Las tareas se ubican en subredes privadas.",[
 ("dns","DNS y ACM externos",580,175),("alb","ALB en subredes públicas",580,340),
 ("web","Frontend Fargate",100,515),("api","API Fargate",580,515),("worker","Worker Fargate",1060,515),
 ("cache","Redis TLS opcional",100,700),("rds","RDS PostgreSQL privado",580,700),("sqs","SQS Standard y DLQ",1060,700),
 ("ops","ECR, CloudWatch y Secrets Manager",1060,175)],
 [("dns","alb"),("alb","web"),("alb","api"),("api","rds"),("worker","rds"),("api","cache"),
  ("worker","sqs"),("ops","api"),("ops","worker")],880)

diagram("03-components.png","03 / Dependencias de componentes","Las flechas representan dependencias de código",[
 ("api","API: endpoints / auth",100,200),("infra","Infrastructure: EF / adapters",1060,200),
 ("app","Application: casos de uso",580,410),("ports","Puertos definidos al interior",1060,610),("domain","Domain: invariantes",580,800)],
 [("api","app"),("api","infra"),("infra","app"),("app","domain"),("infra","domain"),("app","ports"),("infra","ports")],1020)

diagram("04-adapters.png","04 / Integración y capa anticorrupción","Sistemas empresariales explícitamente simulados en la demo",[
 ("app","Modelo canónico",580,190),("acl","Puertos / ACL",580,390),("erp","ERP: catálogo / precio",100,600),
 ("wms","WMS: stock / reserva",580,600),("oms","OMS: orden / despacho",1060,600),("crm","CRM: cliente / compra",580,810)],
 [("app","acl"),("acl","erp"),("acl","wms"),("acl","oms"),("acl","crm")],1020)

sequence("05-create-order.png","05 / Crear una orden",["Canal","API / handler","DB / adapters locales","Worker"],[
 (0,1,"Token, clave y contenido"),(1,2,"Lock de idempotencia"),(1,2,"CRM / precio ERP / reserva WMS"),(1,2,"Commit orden y outbox"),
 (1,0,"202 reserved y recibo"),(3,2,"Reclamar evento con lease"),(3,2,"Iniciar proveedor configurado"),(3,2,"Confirmar o compensar"),(0,1,"Consultar orden"),(1,2,"Leer estado e historial"),(1,0,"Estado actualizado")],
 "Contrato público sin datos de simulación. Las rutas de prueba solo se registran en Development con Simulator.")

sequence("06-payments.png","06 / Checkout sandbox y conciliación",["Workers","Mercado Pago sandbox","API","PostgreSQL","Portal"],[
 (0,3,"Intención durable antes del POST"),(0,1,"Verificar test_user y crear preferencia"),(1,0,"URL o respuesta incierta"),(0,3,"Persistir pending / unknown"),
 (4,2,"Consultar checkout autorizado"),(2,3,"Leer intención vigente"),(2,4,"URL válida, sin confirmar pago"),(1,2,"Webhook firmado"),(2,3,"Inbox canónica y durable"),(2,1,"200 después del commit"),
 (0,1,"GET del pago autoritativo"),(1,0,"Estado y correlación verificables"),(0,3,"Lock, transición y outbox"),(0,1,"Si corresponde: reembolso estable"),(0,1,"GET de confirmación refunded"),(0,3,"Compensación o revisión pendiente")],
 "Flujo implementado, no ejecutado contra cuenta externa. URL/retorno del navegador no confirman pagos; Simulator sigue por defecto.")

sequence("07-oidc.png","07 / OIDC y autorización contextual",["Navegador","Keycloak","API","Permisos DB"],[
 (0,1,"Authorization Code + PKCE"),(1,0,"Código de autorización"),(0,1,"Código + verifier"),(1,0,"Access token breve"),
 (0,2,"Bearer token"),(2,3,"Permisos / partner / canal"),(3,2,"Resultado de autorización"),(2,0,"Respuesta o 401 / 403")],
 "API verifica firma, issuer, audience y tiempo. El portal no decide autorización; demo auth es una ruta aparte y limitada.")

diagram("08-saga.png","08 / Saga y compensaciones","Estados del incremento local con pagos y fulfillment simulados",[
 ("pending","pending",100,190),("reserved","reserved",580,190),("awaiting","awaiting_payment",1060,190),
 ("failed","failed",100,420),("comp","compensating",580,420),("confirmed","confirmed",1060,420),
 ("cancelled","cancelled",580,680),("shipped","shipped",1060,680),("delivered","delivered",1060,870)],
 [("pending","reserved"),("pending","failed"),("reserved","awaiting"),("reserved","comp"),("awaiting","comp"),("awaiting","confirmed"),
 ("comp","cancelled"),("comp","failed"),("confirmed","comp"),("confirmed","shipped"),("shipped","delivered")],1100)

diagram("09-events.png","09 / Outbox, consumo y excepciones","AmazonSQSClient con HTTP controlado y ElasticMQ. AWS real pendiente.",[
 ("tx","Commit: orden + outbox",100,190),("pub","Publicador con lease",580,190),("queue","AmazonSQSClient / SQS Standard",1060,190),
 ("complete","Finalización durable",100,420),("handler","Handler idempotente",580,420),("inbox","Inbox: origen, hash, lease",1060,420),
 ("ack","Acuse / DeleteMessage",100,680),("retry","Backoff / visibilidad",580,680),("dlq","DLQ / estado de excepción",1060,680),
 ("fix","Corrección y redrive",1060,900)],
 [("tx","pub"),("pub","queue"),("queue","inbox"),("inbox","handler"),("handler","complete"),("complete","ack"),("handler","retry"),("retry","queue"),("retry","dlq"),("dlq","fix"),("fix","queue")],1140)

diagram("10-data-model.png","10 / Modelo relacional lógico","Relaciones principales; DDL y migraciones son la autoridad física",[
 ("partner","Partner / Channel / QuotaCounter",100,190),("order","Order / OrderItem",580,190),("product","Product / Inventory",1060,190),
 ("idem","IdempotencyRecord",100,420),("payment","Payment / Checkout / Receipt / Reservation",580,420),("outbox","Outbox / MessagingInbox / PaymentInbox",1060,420),
 ("user","User / UserRole",100,680),("role","Role / RolePermission",580,680),("perm","Permission",1060,680)],
 [("partner","order"),("partner","idem"),("order","product"),("order","payment"),("order","outbox"),("user","role"),("role","perm")],920)
diagram("11-help-center.png","11 / Centro de ayuda público","Las once guías, preguntas frecuentes e impresión son públicas.",[
 ("access","Login, registro y recuperación",100,180),("workspace","Ayuda contextual",580,180),
 ("sources","Guías JSON y capturas",1060,180),("help","Catálogo público y búsqueda",580,360),
 ("reader","Procedimientos y preguntas frecuentes",580,540),("pdf","Impresión A4",100,720),
 ("actions","Operación autenticada del workspace",1060,720)],
 [("access","help"),("workspace","help"),("sources","help"),("help","reader"),("reader","pdf"),("reader","actions")],890)

diagram("12-ecs-iam.png","12 / Identidad e IAM de ECS","Credenciales temporales por tarea. Sin claves AWS en imágenes.",[
 ("ecs","Principal ECS Tasks",580,170),("exec","Execution Role por servicio",100,360),
 ("app","Task Role por servicio",1060,360),("boot","ECR, logs y secreto propio",100,560),
 ("worker","Worker: cola de eventos",1060,560),("other","API y frontend sin acceso SQS",580,560),
 ("operator","Operador independiente",100,750),("dlq","Revisión y redrive de DLQ",580,750)],
 [("ecs","exec"),("ecs","app"),("exec","boot"),("app","worker"),("app","other"),("operator","dlq")],940)

diagram("13-living-documentation.png","13 / Documentación viva","Reglas de revisión documental en el pull request.",[
 ("change","Cambio funcional",580,175),("impact","Revisar impacto documental",580,350),
 ("update","Guía, versión, historial y capturas",100,535),("reason","Registrar motivo sin impacto",1060,535),
 ("verify","Validar enlaces y flujo",580,710),("ci","Controles del pull request",580,880)],
 [("change","impact"),("impact","update"),("impact","reason"),("update","verify"),("reason","verify"),("verify","ci")],1050)

diagram("14-cicd.png","14 / Integración y entrega","CI configurada. Plan AWS y despliegue requieren su entorno.",[
 ("pr","Pull request",580,170),("build","Build, pruebas y documentación",100,350),
 ("iac","HCL y planes simulados",1060,350),("images","Imágenes ECR por digest",100,530),
 ("plan","Plan ECS mediante OIDC",580,530),("review","Revisar plan y costo",580,700),
 ("deploy","Despliegue autorizado",580,870),("checks","Health y rollback",1060,870)],
 [("pr","build"),("pr","iac"),("build","images"),("iac","plan"),("images","plan"),
  ("plan","review"),("review","deploy"),("deploy","checks")],1040)

print(f"Rendered {len(list(OUT.glob('*.png')))} diagrams")
