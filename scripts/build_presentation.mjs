import fs from 'node:fs/promises';
import path from 'node:path';
import { constants as fsConstants } from 'node:fs';
import { createHash } from 'node:crypto';
import { fileURLToPath, pathToFileURL } from 'node:url';

// Reproducible executive deck. Runtime-owned dependencies are never vendored.
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const WORKSPACE = path.resolve(ROOT, '..');
const RUNTIME = process.env.CODEX_PRIMARY_RUNTIME_ROOT || 'C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1116-1210-0_26.1116.1210.0_x64__3k8sg7r9htsxt/dependencies';
const MODULES = process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES || path.join(RUNTIME, 'node/node_modules');
const PYTHON = process.env.CODEX_PRIMARY_RUNTIME_PYTHON || path.join(RUNTIME, 'python/python.exe');
process.env.RUNTIME_NODE_MODULES = MODULES;
process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES = MODULES;
const SKILL = 'C:/Users/Arukado/.codex/plugins/cache/openai-primary-runtime/presentations/26.1116.12010/skills/presentations';
const { Presentation, PresentationFile } = await import(pathToFileURL(path.join(MODULES, '@oai/artifact-tool/dist/artifact_tool.mjs')).href);
const TMP = path.join(WORKSPACE, '.work/executive-presentation');
const OUTPUT = path.join(ROOT, 'output/presentation');
await fs.mkdir(TMP, { recursive: true });
await fs.mkdir(OUTPUT, { recursive: true });
const evidenceFile = path.join(ROOT, 'output/presentation-evidence.json');
let evidence = {};
try { evidence = JSON.parse(await fs.readFile(evidenceFile, 'utf8')); } catch {}

const C = { navy:'#102B42', teal:'#007E82', ink:'#17394D', muted:'#59707C', pale:'#EAF3F4', line:'#C6D7DF', white:'#FFFFFF', amber:'#A96810' };
const p = Presentation.create({ slideSize:{width:1280,height:720} });
const FONT = 'Arial';
function txt(s, text, x,y,w,h, size=25, color=C.ink, bold=false, align='left') {
  const q=s.shapes.add({geometry:'textbox',name:text.slice(0,70),position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
  q.text=text; q.text.style={fontFamily:FONT,fontSize:size,color,bold,alignment:align}; q.text.insets=0; return q;
}
function line(s,x,y,w,color=C.line){return s.shapes.add({geometry:'line',position:{left:x,top:y,width:w,height:0},fill:'none',line:{fill:color,width:1}});}
function rect(s,x,y,w,h,fill,stroke='none'){return s.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:h},fill,line:{fill:stroke,width:stroke==='none'?0:1.4}});}
function node(s,label,x,y,w=240,h=85,fill=C.pale,color=C.ink){const q=rect(s,x,y,w,h,fill,C.line);q.text=label;q.text.style={fontFamily:FONT,fontSize:24,color,bold:true,alignment:'center',verticalAlignment:'middle'};q.text.insets=12;return q;}
function connect(s,a,b,from='right',to='left',color=C.teal){return s.shapes.connect(a,b,{kind:'elbow',fromSide:from,toSide:to,line:{fill:color,width:2},tail:{type:'triangle',width:'sm',length:'sm'}});}
function add(title,notes,dark=false){const s=p.slides.add();s.background.fill=dark?C.navy:C.white;
 txt(s,title,64,60,1152,110,44,dark?C.white:C.navy,true);
 txt(s,'VortexBird / AndesRetail',64,671,750,22,14,dark?'#A4C8D0':C.muted);
 txt(s,String(p.slides.items.length).padStart(2,'0'),1145,671,70,22,14,dark?'#A4C8D0':C.muted,false,'right');
 s.speakerNotes.text=notes+'\n\nFuente: repositorios locales VortexBird, assessment arquitectónico y evidencia de revisión del 17 de noviembre de 2026. La arquitectura objetivo no acredita un despliegue.';
 return s;}
function rows(s,items,start=190){items.forEach(([a,b],i)=>{const y=start+i*101;txt(s,a,64,y,340,64,28,C.teal,true);txt(s,b,430,y,750,72,25);if(i<items.length-1)line(s,64,y+84,1152);});}
function table(s,values,widths,top=190,height=360,font=23){const t=s.tables.add({rows:values.length,columns:values[0].length,left:64,top,width:1152,height,values,columnWidths:widths});
 t.borders.assign({fill:C.white,width:2});
 for(let r=0;r<values.length;r++)for(let c=0;c<values[r].length;c++){const cell=t.getCell(r,c);cell.fill=r===0?C.navy:r%2?C.pale:C.white;cell.text.style={fontFamily:FONT,fontSize:font,color:r===0?C.white:C.ink,bold:r===0};}
 return t;}
function note(s,text,y=604){txt(s,text,64,y,1152,54,19,C.muted);}
async function screenshot(s,imagePath,x,y,w,h,alt){const bytes=await fs.readFile(imagePath);s.images.add({blob:bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),contentType:'image/png',alt,fit:'contain',position:{left:x,top:y,width:w,height:h}});}

// 01
let s=add('VortexBird', 'Presentar la plataforma de interoperabilidad para AndesRetail. La reunión separa lo implementado, la evidencia disponible y el siguiente paso operativo. Explicar que las integraciones empresariales de la demostración usan simuladores y que AWS todavía no está desplegado. El objetivo de la sesión es que negocio y tecnología comprendan los flujos y acuerden las condiciones de un piloto verificable.',true);
txt(s,'Plataforma de interoperabilidad\npara AndesRetail',64,235,1090,160,48,C.white,true);
txt(s,'Arquitectura, funcionamiento y estado verificable',64,445,1100,60,28,'#B7DDE0');
txt(s,'Revisión ejecutiva · 17 de noviembre de 2026',64,570,1100,40,20,'#B7DDE0');

// 02
s=add('El problema de las integraciones punto a punto','Explicar el contexto del assessment. Los canales de venta necesitan datos de varios sistemas y las dependencias crecen con cada integración. Los impactos son riesgos del caso de negocio y no métricas observadas en una operación real de AndesRetail. Relacionar cada problema con una consecuencia concreta: duplicados, conciliación, retrasos y falta de visibilidad.');
rows(s,[['Reglas duplicadas','Cada canal interpreta stock, precios y pedidos por separado.'],['Dependencias frágiles','Una caída del ERP puede afectar la experiencia de compra.'],['Estados inconsistentes','Los reintentos y eventos tardíos requieren conciliación.'],['Diagnóstico disperso','El equipo debe reconstruir una venta entre varios sistemas.']]);

// 03
s=add('Objetivos de la plataforma','Presentar objetivos evaluables y evitar prometer porcentajes de ahorro sin línea base. Una orden debe conservar su identidad ante reintentos. Una reserva debe confirmarse o liberarse de forma trazable. Cada operación debe mantener el contexto del partner y canal. La integración de otro sistema debe modificar su adaptador y no propagar su modelo al resto del negocio.');
rows(s,[['Pedidos trazables','Identidad estable, historial y correlación de extremo a extremo.'],['Inventario protegido','Reserva autoritativa y compensación ante fallos del pago.'],['Acceso controlado','Permisos de negocio y aislamiento por partner y canal.'],['Integraciones sustituibles','Contratos comunes y adaptadores para cada sistema externo.']]);

// 04
s=add('Visión general de VortexBird','Recorrer el diagrama desde los canales y el portal hasta la API, la persistencia y los workers. PostgreSQL mantiene el estado durable. El worker ejecuta trabajo recuperable y las integraciones quedan detrás de puertos. En el entorno de demostración los sistemas empresariales se simulan. La distribución de servicios en AWS es objetivo separado de esta arquitectura lógica.');
const ch=node(s,'Canales comerciales',64,200,300), portal=node(s,'Portal de operación',64,350,300),api=node(s,'API de negocio',490,275,300),db=node(s,'PostgreSQL',906,200,310),wk=node(s,'Workers',906,350,310),ad=node(s,'ERP · WMS · OMS · CRM',490,505,420);
connect(s,ch,api);connect(s,portal,api);connect(s,api,db);connect(s,api,wk);connect(s,wk,ad,'bottom','right');note(s,'Modelo lógico. Adaptadores empresariales simulados en la demostración.');

// 05
s=add('Arquitectura tecnológica','Los cuatro repositorios tienen responsabilidades distintas. React y TypeScript implementan el portal. .NET 10 y EF Core soportan dominio, casos de uso y persistencia. Infraestructura concentra Compose, Keycloak y Terraform. Documentación conserva decisiones y evidencia. El núcleo modular evita introducir distribución innecesaria y permite extraer servicios cuando la escala o la autonomía lo justifiquen.');
table(s,[['Repositorio','Tecnología','Responsabilidad'],['Frontend','React + TypeScript','Portal, formularios y ayuda'],['Backend','.NET 10 + EF Core','API, dominio, saga y workers'],['Infraestructura','Compose + Terraform','Entorno local y objetivo AWS'],['Documentación','Markdown + PDF + diagramas','Decisiones y evidencia']], [275,350,527],190,365,23);
note(s,'PostgreSQL mantiene el estado durable. Redis es una optimización opcional.');

// 06
s=add('Integración de sistemas y canales','Distinguir con claridad los roles y el estado de implementación. ERP, WMS, OMS y CRM tienen adaptadores de demostración persistentes, no conexiones empresariales productivas. E-commerce y marketplaces usan los contratos públicos, pero no se acredita una integración con una tienda real. La pasarela externa es una ruta sandbox opcional que requiere credenciales válidas y verificación completa.');
table(s,[['Sistema','Contrato de negocio','Estado del alcance'],['ERP','Catálogo y precios','Simulador'],['WMS','Stock y reservas','Simulador'],['OMS / CRM','Fulfillment y clientes','Simuladores'],['Canales comerciales','APIs de stock, precio y órdenes','Contratos implementados']], [270,500,382],180,400,23);
note(s,'La conexión productiva requiere credenciales, contratos y pruebas con cada proveedor.');

// 07
s=add('Flujo de pedidos y reservas','Explicar que la consulta de stock es orientativa y la reserva decide la disponibilidad. La solicitud incluye una clave de idempotencia y contexto autorizado. El commit guarda orden y outbox. Un rechazo de pago libera la reserva y registra la compensación. Una aceptación permite confirmar el pedido. Los efectos externos requieren su propia idempotencia.');
const n1=node(s,'Validar solicitud',64,220,240),n2=node(s,'Reservar stock',410,220,240),n3=node(s,'Orden + outbox',756,220,300),n4=node(s,'Procesar pago',756,395,300),n5=node(s,'Confirmar pedido',410,520,260),n6=node(s,'Liberar reserva',64,395,260);
connect(s,n1,n2);connect(s,n2,n3);connect(s,n3,n4,'bottom','top');connect(s,n4,n5,'bottom','right');connect(s,n4,n6,'left','right',C.amber);txt(s,'Rechazado',440,400,220,30,20,C.amber);txt(s,'Aprobado',960,505,230,30,20,C.teal);note(s,'Misma clave y mismo contenido: misma orden. Contenido distinto: conflicto.',620);

// 08
s=add('Pagos, conciliación y compensaciones','El navegador nunca confirma un pago. La intención se persiste antes de llamar al proveedor y el callback se almacena antes del acuse. El conciliador consulta la fuente autoritativa y valida referencia, importe, moneda y vendedor. Un estado desconocido exige consulta, no volver a cobrar. Los reembolsos usan referencias estables. Solo se permiten pruebas sandbox y simuladas.');
rows(s,[['Checkout durable','La intención y su referencia existen antes de contactar al proveedor.'],['Webhook firmado','La API valida la firma y conserva el aviso en un inbox.'],['Consulta autoritativa','Se contrastan estado, referencia, importe, moneda y vendedor.'],['Compensación','Un rechazo libera stock. Un cobro incompatible requiere reembolso.']]);

// 09
s=add('Seguridad, usuarios y permisos','La identidad OIDC y los permisos de negocio se validan en capas diferentes. Keycloak es el proveedor definido, pero el arranque y la sesión completa siguen pendientes en este entorno. La API comprueba firma, emisor, audiencia y vigencia del token, luego aplica permisos y alcance. Los simuladores están limitados a Development. La interfaz oculta acciones sin sustituir las guardas del backend.');
const i1=node(s,'Identidad OIDC',64,220,280),i2=node(s,'Validación JWT',482,220,280),i3=node(s,'Permisos de negocio',900,220,316),i4=node(s,'Partner + canal',482,430,280),i5=node(s,'Operación autorizada',900,430,316);
connect(s,i1,i2);connect(s,i2,i3);connect(s,i3,i4,'bottom','top');connect(s,i4,i5);txt(s,'La API autoriza cada operación',64,445,325,90,30,C.teal,true);note(s,'Keycloak completo pendiente de verificación. Rutas de simulación restringidas a Development.');

// 10
s=add('Infraestructura objetivo en AWS','ECS Fargate es la arquitectura elegida para el primer piloto. El ALB recibe HTTPS y enruta a frontend y API. Los workers escalan por separado. RDS permanece privado y SQS incorpora DLQ. Redis es opcional y debe justificarse por carga. Los permisos de tareas y ejecución están separados. Este diagrama representa IaC y diseño, no recursos activos. No se ha ejecutado el despliegue por la puerta local y presupuestaria pendiente.');
const alb=node(s,'ALB / HTTPS',64,205,270),front=node(s,'Frontend Fargate',64,405,270),aapi=node(s,'API Fargate',483,205,290),worker=node(s,'Worker Fargate',483,405,290),rds=node(s,'RDS privado',946,205,270),sqs=node(s,'SQS + DLQ',946,405,270);
connect(s,alb,aapi);connect(s,alb,front,'bottom','top');connect(s,aapi,rds);connect(s,worker,sqs);connect(s,worker,rds,'top','bottom');note(s,'Arquitectura objetivo. AWS no desplegado. Secretos, IAM y logs por servicio.');

// 11
s=add('Resiliencia del proceso de venta','Relacionar cada fallo con una respuesta recuperable. Outbox e inbox reducen pérdidas y duplicados, pero no ofrecen exactamente una vez entre sistemas. La reserva y el estado de pago determinan las compensaciones. La DLQ requiere diagnóstico y replay controlado. La disponibilidad y la latencia son objetivos que requieren carga y observación, no resultados de pruebas unitarias.');
rows(s,[['Reintento del cliente','Idempotencia conserva una única orden por referencia.'],['Evento duplicado','Inbox y transición válida protegen los efectos del negocio.'],['Proveedor incierto','Conciliación y estado pendiente evitan un segundo cobro.'],['Fallo persistente','Backoff, DLQ y replay controlado permiten recuperación.']]);

// 12
s=add('Monitoreo y observabilidad','El código incluye logging estructurado y correlación, además de instrumentación nativa Activity y Meter. Las exportaciones a observabilidad externa y las alertas operativas deben verificarse en un entorno desplegado. Explicar qué señales conectan tecnología con negocio: pedidos pendientes, edad del outbox, rechazos, compensaciones y latencia. No presentar dashboards objetivo como capturas de un sistema de monitoreo activo.');
table(s,[['Señal','Pregunta operativa','Estado'],['Logs y correlación','¿Qué pasó con esta orden?','Instrumentación local'],['Métricas de proceso','¿Dónde se acumulan pendientes?','Validación operativa pendiente'],['Trazas distribuidas','¿Qué dependencia consume el tiempo?','Exportación por verificar'],['Alertas y SLO','¿Cuándo intervenir?','Objetivos por medir']], [330,510,312],185,380,22);
note(s,'No hay evidencia suficiente para afirmar 99,9 % de disponibilidad o p95 inferior a 300 ms.');

// 13
s=add('Centro de ayuda y documentación viva','Las once guías cubren acceso, administración y operación. Se pueden consultar sin iniciar sesión y tienen ayuda contextual desde los módulos. Las acciones siguen exigiendo permisos. Los controles de documentación verifican versiones, rutas, anclas y capturas. El contenido técnico privado y los secretos no forman parte de la ayuda pública. La siguiente validación integrada debe confirmar que cada procedimiento coincide con el entorno operativo.');
txt(s,'11',64,200,250,150,112,C.teal,true);txt(s,'guías públicas',64,360,350,60,32,C.navy,true);
txt(s,'Búsqueda por módulo y perfil\nNavegación contextual\nPreguntas frecuentes\nImpresión A4\nHistorial y versión',480,205,690,330,32);
note(s,'Los permisos documentados habilitan operaciones del workspace, no la lectura general.');

// 14
s=add('Demostración del portal','Mostrar la pantalla de dashboard como evidencia de la interfaz real compilada. Aclarar que los datos de esta captura son sintéticos y que la API fue interceptada para la validación visual aislada. No equivale a un flujo integral contra PostgreSQL y servicios reales. Señalar la distribución de estados y la navegación hacia órdenes. Si se dispone de un entorno completo, sustituir esta explicación por una demostración viva y conservar su evidencia.');
const dashboard=evidence.dashboardScreenshot || path.join(WORKSPACE,'vortexbird-frontend/public/help-media/dashboard.png');
await screenshot(s,dashboard,64,175,1152,410,'Dashboard real de VortexBird con datos sintéticos');
note(s,'Interfaz actual · datos sintéticos · prueba aislada. No acredita integración completa.');

// 15
s=add('Acceso y orientación del usuario','Mostrar la pantalla de acceso de la aplicación. La ayuda pública permite conocer procedimientos antes de autenticarse. La imagen representa la interfaz real y no prueba una sesión OIDC completa. Señalar la diferencia entre un acceso de demostración limitado a Development y el proveedor de identidad que deberá verificarse en el piloto. Los errores y la persistencia deben probarse con los servicios operativos.');
const login=evidence.loginScreenshot || path.join(WORKSPACE,'vortexbird-frontend/public/help-media/acceso.png');
await screenshot(s,login,64,175,1152,410,'Pantalla real de acceso de VortexBird');
note(s,'Interfaz actual · datos sintéticos · prueba aislada. Sesión completa con Keycloak pendiente.');

// 16
s=add('Resultados de validación','Presentar únicamente la evidencia etiquetada de esta corrida. Las pruebas locales controladas demuestran comportamientos concretos, pero no prueban la operación de todos los servicios conectados. Un error de socket del entorno bloquea las conexiones loopback. La prueba integral, las sesiones OIDC y los ensayos externos no se declaran aprobados. Consultar el informe final para comandos, fecha, entorno y limitaciones.');
const checks=evidence.results || [['Código y contratos','Controles locales','Ver informe de ejecución'],['Interfaz y manuales','Pruebas aisladas','API sintética / inspección'],['Plataforma completa','No acreditada','Conexiones locales bloqueadas'],['AWS y sandbox externo','No ejecutados','Requisitos pendientes']];
table(s,[['Alcance','Resultado','Límite'],...checks],[360,300,492],180,410,22);note(s,'Cada resultado debe leerse junto con su entorno. Pruebas aisladas no equivalen a E2E integral.');

// 17
s=add('Estado del despliegue','Ser directo: no se declara completada la plataforma integral ni el despliegue AWS. El proceso PostgreSQL y Vite pueden iniciar, pero las conexiones del entorno reciben socket 10013. Eso impide superar la puerta local. No existe presupuesto AWS aprobado y no se crearon recursos. El siguiente paso es ejecutar el mismo procedimiento en una sesión autorizada, validar flujos completos y luego revisar identidad, plan y costo en AWS.');
txt(s,'Entorno local',64,205,500,70,34,C.teal,true);txt(s,'Servicios iniciables\nConectividad bloqueada\nValidación integral pendiente',64,300,520,230,30);
txt(s,'AWS',710,205,500,70,34,C.teal,true);txt(s,'Infraestructura declarada\nSin recursos desplegados\nSin presupuesto aprobado',710,300,500,230,30);
note(s,'Reserva preliminar del piloto: USD 220–290/mes. Estimación sin aprobación y sujeta a cotización regional.');

// 18
s=add('Beneficios esperados para AndesRetail','Presentar beneficios como hipótesis que se validarán durante el piloto. No hay ahorro cuantificado ni SLA operativo demostrado. Proponer mediciones simples para vincular la arquitectura con resultados: duplicados, tiempo de conciliación, tiempo para incorporar un canal y recuperación de incidentes. La línea base del cliente es necesaria para evaluar el impacto.');
table(s,[['Capacidad','Beneficio esperado','Medición del piloto'],['Idempotencia','Menos pedidos duplicados','Duplicados por reintento'],['Saga e historial','Conciliación más rápida','Tiempo de resolución'],['Adaptadores','Cambios más contenidos','Tiempo de incorporar canal'],['Observabilidad','Diagnóstico más directo','Tiempo de recuperación']], [330,430,392],190,380,22);
note(s,'Beneficios propuestos. El piloto debe establecer línea base y resultados.');

// 19
s=add('Roadmap y condiciones de avance','El roadmap tiene puertas verificables. Primero se desbloquea y valida la plataforma local. Después se realiza el plan AWS con credenciales, dominio y presupuesto concretos. El piloto incorpora pruebas postdespliegue, alertas, rollback y restauración. La conexión de sistemas reales y expansión requieren contratos y credenciales empresariales. No asignar fechas de cumplimiento que no tengan equipo y dependencias confirmadas.');
rows(s,[['1. Validación integral','Sesión autorizada, servicios conectados y recorridos por perfil.'],['2. Piloto AWS','Identidad, plan regional, secretos, HTTPS y costo aprobado.'],['3. Operación verificable','Smoke remoto, alertas, rollback y recuperación ensayada.'],['4. Integraciones reales','Contratos, credenciales y pruebas con ERP, WMS, OMS y CRM.']]);

// 20
s=add('Decisiones para el siguiente paso','Cerrar recordando el valor del diseño y el estado real. Las capacidades y controles aislados están documentados, pero la aceptación integral sigue abierta. Solicitar que se acuerde el entorno de ejecución y, cuando haya un plan revisable, el presupuesto del piloto. Abrir preguntas sobre propiedad de datos, prioridades de integración y operación. No pedir autorización para una infraestructura aún sin plan concreto.',true);
txt(s,'Un flujo de venta trazable\ny recuperable',64,215,1100,160,48,C.white,true);
txt(s,'Pendiente: entorno integral verificable y piloto AWS autorizado',64,430,1100,80,28,'#B7DDE0');
txt(s,'Preguntas',64,565,1100,60,36,C.white,true);

const candidate=path.join(TMP,'candidate.pptx');
await (await PresentationFile.exportPptx(p)).save(candidate);
await fs.writeFile(path.join(TMP,'deck.json'),JSON.stringify(p.toProto()));
for(let i=0;i<p.slides.items.length;i++){
 const slide=p.slides.items[i]; const stem=`slide-${String(i+1).padStart(2,'0')}`;
 const png=await p.export({slide,format:'png',scale:1}); await fs.writeFile(path.join(TMP,`${stem}.png`),new Uint8Array(await png.arrayBuffer()));
 const lay=await slide.export({format:'layout'});await fs.writeFile(path.join(TMP,`${stem}.layout.json`),await lay.text());
}
const finalPath=path.join(OUTPUT,process.env.PRESENTATION_OUTPUT_NAME || 'VortexBird_AndesRetail_Executive.pptx');
const {finalizePresentation}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
let validation;
try { validation=await finalizePresentation({workspaceDir:WORKSPACE,candidatePath:candidate,finalPath,pythonExecutable:PYTHON,
 integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),
 layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit',...[5,6,12,16,18].flatMap(n=>['--require-native-table-slide',String(n)])],
 explicitTotalSlideCount:20,requiredNativeTableOwnerSlides:[5,6,12,16,18],requiredNativeChartOwnerSlides:[],
 fontPolicy:{basis:'design',families:[FONT]},verifyArtifactToolImport:true,receiptPath:path.join(TMP,'validation.json')}); }
catch(error) {
 if(error.code!=='EPERM'||error.syscall!=='link'||error.dest!==finalPath) throw error;
 // Windows sandbox permits ordinary file creation but not the finalizer's hard link.
 // The helper reaches this point only after integrity, layout, fonts, tables and
 // first-party import have passed. Preserve those exact bytes by exclusive copy.
 const before=await fs.readFile(candidate); const hash=createHash('sha256').update(before).digest('hex');
 await fs.copyFile(candidate,finalPath,fsConstants.COPYFILE_EXCL);
 if(createHash('sha256').update(await fs.readFile(finalPath)).digest('hex')!==hash) throw new Error('Final copy hash mismatch');
 validation={status:'validated-copy',finalSha256:hash,byteCount:before.length,slides:20,nativeTableSlides:[5,6,12,16,18],
   validation:'Package integrity, layout, font policy, native tables and Artifact Tool reimport completed before hard-link publication.',
   publicationFallback:'Hard-link unavailable (EPERM). Copied the unchanged candidate using COPYFILE_EXCL and verified SHA-256.'};
 await fs.writeFile(path.join(TMP,'validation.json'),JSON.stringify(validation,null,2));
}
console.log(JSON.stringify({finalPath,slides:p.slides.items.length,validation}));
