"""Exact, editable vector architecture figures shared by the PDF and SVG exports."""
from pathlib import Path
from reportlab.graphics.shapes import Drawing, Rect, Line, Polygon, String
from reportlab.graphics import renderSVG
from reportlab.lib.colors import HexColor, Color, white
from reportlab.pdfbase.pdfmetrics import stringWidth

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'diagrams' / 'vector'
NAVY='#102A43'; TEAL='#087F8C'; BLUE='#2563A6'; AMBER='#AD6500'; MUTED='#526D82'
W,H=1120,650

def txt(d,x,y,t,size=15,color=NAVY,bold=False):
    d.add(String(x,y,t,fontName='Helvetica-Bold' if bold else 'Helvetica',fontSize=size,fillColor=HexColor(color)))

def wrapped(t,width,size=14,bold=False):
    f='Helvetica-Bold' if bold else 'Helvetica'; lines=[]
    for para in t.split('\n'):
        row=''
        for word in para.split():
            s=(row+' '+word).strip()
            if stringWidth(s,f,size)>width and row: lines.append(row); row=word
            else: row=s
        lines.append(row)
    return lines

def arrow(d,points,label='',color=MUTED,dashed=False):
    for a,b in zip(points,points[1:]):
        d.add(Line(*a,*b,strokeColor=HexColor(color),strokeWidth=1.8,strokeDashArray=[5,4] if dashed else None))
    a,b=points[-2:]; import math
    theta=math.atan2(b[1]-a[1],b[0]-a[0]); size=9
    p=[b[0],b[1],b[0]-size*math.cos(theta-.45),b[1]-size*math.sin(theta-.45),b[0]-size*math.cos(theta+.45),b[1]-size*math.sin(theta+.45)]
    d.add(Polygon(p,fillColor=HexColor(color),strokeColor=None))
    if label:
        a,b=points[(len(points)-2)//2:(len(points)-2)//2+2]; x=(a[0]+b[0])/2;y=(a[1]+b[1])/2+7
        tw=stringWidth(label,'Helvetica',10)
        d.add(Rect(x-tw/2-4,y-3,tw+8,14,fillColor=white,strokeColor=None))
        txt(d,x-tw/2,y,label,10,color)

def base(number,title,status):
    d=Drawing(W,H)
    d.add(Rect(0,0,W,H,fillColor=white,strokeColor=None))
    txt(d,32,608,f'{number:02d}',20,TEAL,True)
    txt(d,88,608,title,25,NAVY,True)
    txt(d,32,574,status,13,MUTED)
    d.add(Line(32,554,W-32,554,strokeColor=HexColor('#CCDDE7'),strokeWidth=1))
    txt(d,32,22,'VORTEXBIRD / ANDESRETAIL',10,MUTED,True)
    txt(d,420,22,'Verde: aplicación   Azul: datos   Ámbar: externo   Gris: objetivo cloud',10,MUTED)
    return d

def graph(number,title,status,nodes,edges,caption):
    d=base(number,title,status); positions={}
    for key,label,detail,col,row,kind in nodes:
        x=32+col*275; y=433-row*170; positions[key]=(x,y,230,90)
    for src,tgt,label in edges:
        x,y,w,h=positions[src]; xx,yy,ww,hh=positions[tgt]
        if abs(y-yy)<3:
            direction=1 if xx>x else -1
            a=(x+w if direction==1 else x,y+h/2);b=(xx if direction==1 else xx+ww,yy+hh/2)
            points=[a,b]
        elif abs(x-xx)<3:
            a=(x+w/2,y if yy<y else y+h);b=(xx+ww/2,yy+hh if yy<y else yy)
            points=[a,b]
        else:
            a=(x+w/2,y if yy<y else y+h);b=(xx+ww/2,yy+hh if yy<y else yy)
            mid=(a[1]+b[1])/2;points=[a,(a[0],mid),(b[0],mid),b]
        arrow(d,points,label)
    for key,label,detail,col,row,kind in nodes:
        x,y,w,h=positions[key]; color={'app':TEAL,'data':BLUE,'external':AMBER,'target':MUTED}.get(kind,TEAL)
        d.add(Rect(x,y,w,h,rx=6,ry=6,fillColor=HexColor('#F5F8FB'),strokeColor=HexColor('#C7D9E6'),strokeWidth=1))
        d.add(Rect(x,y+4,4,h-8,fillColor=HexColor(color),strokeColor=None))
        for i,line in enumerate(wrapped(label,w-28,16,True)):txt(d,x+14,y+h-26-i*19,line,16,NAVY,True)
        lines=wrapped(detail,w-28,13)
        for i,line in enumerate(lines[:2]):txt(d,x+14,y+27-i*15,line,13,MUTED)
    return {'number':number,'title':title,'status':status,'caption':caption,'drawing':d}

def sequence(number,title,status,actors,steps,caption):
    d=base(number,title,status); xs=[135+i*280 for i in range(len(actors))]
    for x,a in zip(xs,actors):
        d.add(Rect(x-100,489,200,43,rx=5,ry=5,fillColor=HexColor('#E9F2F6'),strokeColor=None))
        tw=stringWidth(a,'Helvetica-Bold',14); txt(d,x-tw/2,505,a,14,NAVY,True)
        d.add(Line(x,485,x,65,strokeColor=HexColor('#CBDBE5'),strokeWidth=1,strokeDashArray=[4,4]))
    gap=390/max(len(steps),1)
    for i,(a,b,label) in enumerate(steps):
        y=465-i*gap
        if a==b:
            arrow(d,[(xs[a],y-12),(xs[a]+65,y-12),(xs[a]+65,y-28),(xs[a],y-28)])
            txt(d,xs[a]+12,y,label,11,MUTED)
        else:
            arrow(d,[(xs[a],y-12),(xs[b],y-12)])
            txt(d,min(xs[a],xs[b])+9,y,f'{i+1}. {label}',12,NAVY)
    return {'number':number,'title':title,'status':status,'caption':caption,'drawing':d}

def atlas():
    g=[]; add=g.append
    add(graph(1,'Arquitectura general','Implementación modular. Sistemas empresariales de demostración.',[
      ('channels','Canales comerciales','E-commerce y marketplaces',0,0,'external'),('web','Portal React','Operación y ayuda pública',1,0,'app'),('api','API .NET 10','Contratos y permisos',2,0,'app'),('idp','Keycloak','OIDC / PKCE',3,0,'external'),
      ('adapters','Adaptadores','ERP, WMS, OMS y CRM simulados',0,1,'external'),('worker','Worker','Saga y tareas recuperables',1,1,'app'),('db','PostgreSQL','Órdenes, outbox e inbox',2,1,'data'),('redis','Redis opcional','Caché; no fuente de verdad',3,1,'data'),
      ('queue','Mensajería','Local / ElasticMQ / SQS',1,2,'target')],
      [('channels','api','API versionada'),('web','api','HTTPS'),('idp','api','JWT'),('api','db','Persistencia'),('api','redis','Lectura'),('worker','db','Estado durable'),('worker','adapters','Puertos'),('worker','queue','Entrega')],
      'Los límites del dominio no dependen de proveedores externos. La validación integral conectada permanece bloqueada en esta ejecución.'))
    add(graph(2,'Arquitectura AWS','Objetivo ECS Fargate. No existen recursos desplegados acreditados.',[
      ('dns','DNS y ACM','Dominio y certificado requeridos',0,0,'target'),('alb','Application Load Balancer','Subredes públicas / HTTPS',1,0,'target'),('ecr','ECR y secretos','Imagen por digest / inyección',2,0,'target'),('idp','Identidad HTTPS','Keycloak externo configurado',3,0,'external'),
      ('web','Frontend Fargate','Servicio privado',0,1,'target'),('api','API Fargate','Servicio privado',1,1,'target'),('worker','Worker Fargate','Servicio privado',2,1,'target'),('cw','CloudWatch','Logs y alarmas',3,1,'target'),
      ('redis','Redis opcional','TLS y red privada',0,2,'data'),('rds','RDS PostgreSQL','Base privada / backups',1,2,'data'),('sqs','SQS y DLQ','Colas con IAM limitado',2,2,'target')],
      [('dns','alb','TLS'),('alb','web','SPA'),('alb','api','/api'),('ecr','worker','Arranque'),('api','rds','SQL'),('api','redis','Caché'),('worker','rds','SQL'),('worker','sqs','Eventos'),('idp','cw','Operación')],
      'La cuenta, el plan real, TLS, identidad y presupuesto deben verificarse antes de provisionar. El diagrama expresa el destino de la IaC.'))
    add(sequence(3,'Autenticación y autorización','Código OIDC presente. Sesión real Keycloak pendiente de validación.',
      ['Navegador','Keycloak','API','Permisos DB'],[(0,1,'Authorization Code con PKCE'),(1,0,'Código y validación de estado'),(0,1,'Canje con verifier'),(1,0,'Tokens de sesión'),(0,2,'Petición con Bearer'),(2,3,'Cuenta, permisos y contexto'),(3,2,'Alcance autorizado'),(2,0,'Respuesta o 401 / 403')],
      'El backend valida firma, emisor, audiencia, vigencia y alcance. El login de demostración solo corresponde a Development.'))
    add(graph(4,'Integraciones empresariales','Puertos implementados. Los adaptadores empresariales son simuladores.',[
      ('orders','Órdenes y catálogo','Modelo canónico de negocio',1,0,'app'),('ports','Contratos internos','Capa anticorrupción',1,1,'app'),('erp','ERP','Catálogo y precios',0,2,'external'),('wms','WMS','Stock y reserva',1,2,'external'),('oms','OMS','Pedido y despacho',2,2,'external'),('crm','CRM','Cliente y compra',3,2,'external')],
      [('orders','ports','Puertos'),('ports','erp','Adaptador'),('ports','wms','Adaptador'),('ports','oms','Adaptador'),('ports','crm','Adaptador')],
      'Conectar un sistema real requiere credenciales, contrato, idempotencia y ensayo de sus fallos. Un simulador no acredita una integración productiva.'))
    add(sequence(5,'Pedidos y reservas','Secuencia del código. Persistencia conectada no revalidada en esta corrida.',
      ['Canal','API','PostgreSQL','Worker'],[(0,1,'Token, pedido y clave idempotente'),(1,2,'Bloqueo por partner y clave'),(1,2,'Validar precio y reservar'),(1,2,'Commit orden y outbox'),(1,0,'202 y recibo estable'),(3,2,'Reclamar evento con lease'),(3,2,'Pago, confirmación o compensación'),(0,1,'Consultar estado e historial')],
      'Repetir el mismo contenido conserva la orden. Reutilizar la clave con un contenido distinto produce conflicto.'))
    add(sequence(6,'Pagos y conciliación','Simulador predeterminado. Mercado Pago sandbox externo no verificado.',
      ['Portal','API / worker','Proveedor sandbox','PostgreSQL'],[(1,3,'Guardar intención de checkout'),(1,2,'Crear preferencia idempotente'),(2,1,'URL o resultado incierto'),(0,1,'Consultar checkout autorizado'),(2,1,'Webhook firmado'),(1,3,'Persistir inbox antes del acuse'),(1,2,'Consultar pago autoritativo'),(1,3,'Validar y transicionar'),(1,2,'Reembolso si corresponde')],
      'El importe, moneda, vendedor y referencia se comprueban contra el proveedor. El regreso del navegador no confirma pagos.'))
    add(graph(7,'Saga y compensaciones','Estados de la aplicación con efectos recuperables.',[
      ('pending','Solicitud','Validación del pedido',0,0,'app'),('reserve','Reservado','Stock comprometido',1,0,'app'),('pay','Esperando pago','Pendiente o incierto',2,0,'app'),('confirm','Confirmado','Pago y reserva válidos',3,0,'app'),
      ('fail','Fallo de validación','No iniciar cobro',0,1,'external'),('comp','Compensación','Liberar / conciliar reembolso',1,1,'external'),('cancel','Cancelado','Efectos compensados',2,1,'app'),('ship','Despachado','Revisión ante reversión',3,1,'app'),('delivered','Entregado','Estado de cumplimiento',3,2,'app')],
      [('pending','reserve',''),('reserve','pay',''),('pay','confirm','Aprobado'),('pending','fail','Inválido'),('reserve','comp','Fallo'),('pay','comp','Rechazo'),('comp','cancel',''),('confirm','ship',''),('ship','delivered','')],
      'Las transacciones SQL no abarcan proveedores. Cada compensación debe poder repetirse de forma segura y conservar su evidencia.'))
    add(graph(8,'Outbox e Inbox','Persistencia local y deduplicación. Entrega al menos una vez.',[
      ('tx','Transacción de negocio','Orden y outbox en el commit',0,0,'data'),('pub','Publicador','Lease y envío recuperable',1,0,'app'),('bus','Transporte','Local o SQS',2,0,'target'),('origin','Validar origen','Comparar outbox y fingerprint',3,0,'app'),
      ('ack','Acuse de cola','Solo tras finalización durable',0,1,'app'),('done','Completar inbox','Actualización protegida por lease',1,1,'data'),('handler','Consumidor idempotente','Efectos de negocio repetibles',2,1,'app'),('inbox','Reclamar inbox','Clave evento + consumidor',3,1,'data')],
      [('tx','pub',''),('pub','bus',''),('bus','origin',''),('origin','inbox',''),('inbox','handler',''),('handler','done',''),('done','ack','')],
      'Un fallo después del efecto y antes de marcar la inbox puede repetir el handler. La idempotencia protege ese intervalo.'))
    add(graph(9,'Mensajería SQS y DLQ','SDK oficial implementado. IAM y redrive AWS no probados.',[
      ('publisher','Worker publicador','SendMessage',0,0,'app'),('queue','SQS Standard','Cola de eventos',1,0,'target'),('consumer','Worker consumidor','Long polling y visibilidad',2,0,'app'),('effect','Procesar y persistir','Inbox y efecto idempotente',3,0,'data'),
      ('dlq','Dead Letter Queue','Mensajes agotados',0,1,'target'),('retry','Reentrega','Backoff de visibilidad',1,1,'app'),('delete','DeleteMessage','Tras commit durable',2,1,'app'),('ops','Operación','Diagnóstico y replay aprobado',0,2,'external')],
      [('publisher','queue',''),('queue','consumer',''),('consumer','effect',''),('effect','delete','Éxito'),('consumer','retry','Fallo'),('retry','queue',''),('retry','dlq','Agotado'),('dlq','ops','Revisión')],
      'ElasticMQ y respuestas HTTP controladas verifican partes del protocolo. El redrive administrado de AWS requiere cuenta y permisos reales.'))
    add(graph(10,'Seguridad e IAM','Separación de responsabilidades declarada para ECS.',[
      ('ecs','Principal ECS Tasks','Asume roles temporales',1,0,'target'),('exec','Execution Role','Imagen, logs y secreto propio',0,1,'target'),('api','Task Role API','Sin política SQS',1,1,'target'),('worker','Task Role worker','Cola específica de eventos',2,1,'target'),('front','Task Role frontend','Sin acceso a datos ni SQS',3,1,'target'),
      ('boot','ECR / Secrets / Logs','Permisos de arranque',0,2,'target'),('rds','Datos privados','SG, TLS y credenciales acotadas',1,2,'data'),('sqs','SQS','Publicar, leer, visibilidad, acuse',2,2,'target'),('ops','Rol operativo','Redrive y recuperación',3,2,'external')],
      [('ecs','exec',''),('ecs','api',''),('ecs','worker',''),('exec','boot',''),('api','rds',''),('worker','sqs',''),('ops','sqs','Controlado')],
      'No hay claves AWS dentro de las imágenes. La configuración declarada no reemplaza una prueba de permisos efectivos en staging.'))
    add(graph(11,'Observabilidad','Instrumentación nativa disponible. Exportación y alertas son objetivo.',[
      ('api','API y worker','Correlación y auditoría',0,0,'app'),('logs','Logs JSON','Eventos y contexto técnico',1,0,'app'),('metrics','Activity / Meter','Duración, errores, backlog',2,0,'app'),('business','Auditoría PostgreSQL','Actor, acción y resultado',3,0,'data'),
      ('cloud','CloudWatch / colector','Destino cloud por verificar',1,1,'target'),('dash','Paneles operativos','Trazas y señales de negocio',2,1,'target'),('alerts','Alertas accionables','Umbrales sujetos a carga',3,1,'target'),('runbook','Operación','Diagnóstico y recuperación',2,2,'external')],
      [('api','logs',''),('api','business','Auditoría'),('logs','cloud','Objetivo'),('metrics','dash','Objetivo'),('cloud','dash',''),('dash','alerts',''),('alerts','runbook','')],
      'No se acredita disponibilidad 99,9 % ni p95 inferior a 300 ms. Los SLO necesitan tráfico representativo y observación temporal.'))
    add(graph(12,'CI/CD','Workflows configurados. Ejecución remota y despliegue sin acreditar.',[
      ('pr','Pull request','Código y documentación',0,0,'app'),('ci','Build y pruebas','Backend, frontend y seguridad',1,0,'app'),('image','Imagen inmutable','ECR por digest',2,0,'target'),('plan','Plan Terraform real','Cuenta y estado remoto',3,0,'target'),
      ('smoke','Smoke y salud','Frontend, API y worker',0,1,'target'),('deploy','Actualizar ECS','Espera de estabilidad',1,1,'target'),('migrate','Migración controlada','Expand / contract',2,1,'target'),('approve','Puerta de aprobación','Costos, permisos y revisión',3,1,'external'),('rollback','Rollback','Digest anterior y diagnóstico',0,2,'target')],
      [('pr','ci',''),('ci','image',''),('image','plan',''),('plan','approve',''),('approve','migrate',''),('migrate','deploy',''),('deploy','smoke',''),('smoke','rollback','Si falla')],
      'Las comprobaciones locales ayudan a revisar los workflows. Solo una ejecución remota y sus endpoints demuestran el despliegue.'))
    add(graph(13,'Centro de documentación viva','Once guías públicas y ayuda contextual para 18 rutas.',[
      ('change','Cambio funcional','Evaluar impacto en la ayuda',0,0,'app'),('source','JSON versionado','Guía, pasos, FAQ e historial',1,0,'data'),('gate','Control documental','Rutas, permisos y capturas',2,0,'app'),('catalog','Catálogo público','Búsqueda y filtros',3,0,'app'),
      ('login','Login','Acceso sin sesión',0,1,'app'),('context','Ayuda contextual','Conservar ruta de origen',1,1,'app'),('reader','Lector de manual','Índice, FAQ e impresión A4',2,1,'app'),('roles','Operación autorizada','Permisos vigentes de la API',3,1,'app')],
      [('change','source',''),('source','gate',''),('gate','catalog',''),('login','reader',''),('context','reader',''),('catalog','reader',''),('reader','roles','Explica controles')],
      'Los permisos de operación no restringen la lectura general de los manuales. El control de acceso se ejecuta en la API.'))
    add(graph(14,'Proceso de despliegue','Puerta actual cerrada: validación integral local y presupuesto pendientes.',[
      ('audit','Auditar','Código, dependencias y evidencias',0,0,'app'),('local','Levantar y recorrer','Servicios conectados y usuarios',1,0,'external'),('fix','Corregir y repetir','Pruebas con evidencia',2,0,'app'),('aws','Preparar AWS','Identidad, costo, TLS y secretos',3,0,'target'),
      ('approve','Aprobar plan y gasto','Una revisión concreta',3,1,'external'),('apply','Aplicar y desplegar','Recursos autorizados',2,1,'target'),('validate','Verificar endpoints','Roles, saga, pagos sandbox',1,1,'target'),('operate','Operar y entregar','Manuales, costos y recuperación',0,1,'target')],
      [('audit','local',''),('local','fix',''),('fix','aws','Si cumple'),('aws','approve',''),('approve','apply',''),('apply','validate',''),('validate','operate','')],
      'El entorno actual rechaza conexiones de loopback con socket 10013. No se alteran permisos del sistema ni se omite esta puerta.'))
    return g

def export():
    OUT.mkdir(parents=True,exist_ok=True)
    import json
    figures=atlas(); manifest=[]
    for f in figures:
        name=f"{f['number']:02d}-vortexbird.svg"
        renderSVG.drawToFile(f['drawing'],str(OUT/name))
        manifest.append({k:f[k] for k in ('number','title','status','caption')}|{'file':name})
    (OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Exported {len(figures)} SVG figures to {OUT}')
    return figures

if __name__=='__main__': export()
