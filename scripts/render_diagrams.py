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

diagram("01-architecture.png","01 / Arquitectura general","Simuladores locales; sandbox opcional sin sesión externa verificada",[
 ("portal","Portal React",100,190),("channels","E-commerce / marketplaces",580,190),("identity","Keycloak / OIDC",1060,380),
 ("api","API: contratos, permisos, cuotas",580,380),("cache","Redis: consultas",100,380),
 ("core","Application / Domain / saga",580,570),("db","PostgreSQL: estado, outbox, cuotas",100,760),
 ("adapters","Adaptadores simulados",1060,570),("worker","Workers: eventos y reintentos",580,760),("payments","Checkout sandbox opcional",1060,760)],
 [("portal","api"),("channels","api"),("identity","api"),("identity","portal"),("api","cache"),("api","core"),("core","db"),("core","adapters"),("db","worker"),("worker","adapters"),("worker","payments")],1000)

diagram("02-aws-deployment.png","02 / Despliegue AWS objetivo","Backend: Pod Identity; Keycloak/CNI: IRSA. Infraestructura no desplegada",[
 ("edge","DNS y TLS propios",580,180),("waf","WAF / ALB",580,360),("kong","Kong en EKS",580,540),
 ("pods","API / frontend / workers",580,720),("db","RDS privado",100,910),("redis","ElastiCache privado",580,910),("sqs","SQS / DLQ",1060,910),
 ("secret","Secrets / Pod Identity backend",100,720),("obs","CloudWatch / trazas",1060,720)],
 [("edge","waf"),("waf","kong"),("kong","pods"),("pods","db"),("pods","redis"),("pods","sqs"),("pods","secret"),("pods","obs")],1150)

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
 (1,0,"202 reserved y recibo"),(3,2,"Reclamar evento con lease"),(3,2,"Saga de pago simulado"),(3,2,"Confirmar o compensar"),(0,1,"Consultar orden"),(1,2,"Leer estado e historial"),(1,0,"Estado actualizado")],
 "IPaymentGateway fuera de transacción: simulador por defecto, sandbox opcional. No hay ERP/WMS/OMS/CRM reales conectados.")

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

diagram("09-events.png","09 / Outbox, consumo y excepciones","Local o SQS opcional implementados; sin ejecución AWS/ElasticMQ verificada",[
 ("tx","Commit: orden + outbox",100,190),("pub","Publicador con lease",580,190),("queue","Local o SQS opcional",1060,190),
 ("complete","Finalización durable",100,420),("handler","Handler idempotente",580,420),("inbox","Inbox: origen, hash, lease",1060,420),
 ("ack","Acuse / DeleteMessage",100,680),("retry","Backoff / visibilidad",580,680),("dlq","DLQ / estado de excepción",1060,680),
 ("fix","Corrección y redrive",1060,900)],
 [("tx","pub"),("pub","queue"),("queue","inbox"),("inbox","handler"),("handler","complete"),("complete","ack"),("handler","retry"),("retry","queue"),("retry","dlq"),("dlq","fix"),("fix","queue")],1140)

diagram("10-data-model.png","10 / Modelo relacional lógico","Relaciones principales; DDL y migraciones son la autoridad física",[
 ("partner","Partner / Channel / QuotaCounter",100,190),("order","Order / OrderItem",580,190),("product","Product / Inventory",1060,190),
 ("idem","IdempotencyRecord",100,420),("payment","Payment / Checkout / Receipt / Reservation",580,420),("outbox","Outbox / MessagingInbox / PaymentInbox",1060,420),
 ("user","User / UserRole",100,680),("role","Role / RolePermission",580,680),("perm","Permission",1060,680)],
 [("partner","order"),("partner","idem"),("order","product"),("order","payment"),("order","outbox"),("user","role"),("role","perm")],920)
print(f"Rendered {len(list(OUT.glob('*.png')))} diagrams")
