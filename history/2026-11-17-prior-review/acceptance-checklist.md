# Matriz de aceptación del texto pegado

## Criterios de cierre del 17 de noviembre de 2026

| Criterio | Estado | Evidencia |
| --- | --- | --- |
| ECS Fargate como arquitectura inicial | Cumplido en diseño e IaC | ADR 0009, diagramas 01–02, raíz `terraform-ecs/` y validación con proveedor AWS. |
| EKS como alternativa | Cumplido | Terraform, Kubernetes, IAM y workflows conservados como alternativa. |
| Task Roles y Execution Roles | Definidos y verificados en plan simulado | IAM por servicio, permisos SQS solo para el worker, secretos por servicio. Permisos efectivos en AWS pendientes. |
| Pod Identity en el alcance correcto | Cumplido | Referencias en los archivos de EKS y la documentación de la alternativa. |
| SDK oficial AWSSDK.SQS | Cumplido | Paquete 4.0.100.26, cliente AmazonSQSClient y build .NET 10. |
| Publicación y consumo de SQS | Cumplido en entorno disponible | HTTP controlado y proceso ElasticMQ. SQS AWS pendiente. |
| Idempotencia outbox/inbox | Validada localmente | PostgreSQL 17.12, cuatro solicitudes de API con una única creación, historia de la saga e inbox completado en transporte local y ElasticMQ. |
| Reentrega, visibilidad y DLQ | Aprobado en ElasticMQ | Cambio de visibilidad, reentrega, acuse, quinto intento y replay. Redrive administrado de AWS pendiente. |
| Inventario de once manuales | Cumplido | `manual-inventory.md`. |
| Diez grupos obligatorios | Cumplido | Diez grupos más Reportes. |
| Lectura general sin autenticación | Aprobado | Playwright recorrió todos los procedimientos, FAQ e impresión sin `/auth/me`. |
| Ayuda desde login | Aprobado | Login, registro y recuperación. |
| Ayuda contextual | Aprobado | 18 rutas y retorno con ruta, query y hash. |
| Contenido corresponde al portal | Revisado | Controles, pasos y permisos cotejados. Capturas regeneradas con datos sintéticos. |
| Documentación viva con CI | Configurado y probado localmente | Changelog, versiones, anclas, capturas y requisitos por módulo. |
| Estado remoto de GitHub Actions | Registrado | Workflows configurados y equivalentes locales ejecutados. Corridas remotas pendientes. |
| PostgreSQL, Keycloak y Mercado Pago | PostgreSQL local aprobado. Keycloak y Mercado Pago por verificar externamente. | El informe enumera la API con PostgreSQL 17.12, validación JWT con TestServer, arranque Keycloak bloqueado y 61 pruebas de pagos con transporte controlado. |
| Pendientes externos | Documentados | AWS, ACM/DNS, credenciales sandbox y validación operativa. |
| Diagramas | Cumplido | 14 Mermaid y PNG. Vista EKS histórica adicional. |
| Assessment PDF | Cumplido | Nueve secciones con decisión, IAM, SQS, ayuda, CI y estado de pruebas. |
| Matriz de evidencia | Cumplido | `implementation-status.md` y `closure-report.md`. |

## Evidencia histórica de la revisión inicial del 17 de noviembre de 2026

| Criterio | Resultado | Evidencia de aceptación |
| --- | --- | --- |
| 1. Ayuda pública | Aprobado | Chromium abre `/help` y enlaces profundos sin sesión. |
| 2. Ayuda desde el acceso | Aprobado en el portal | Login, registro y recuperación muestran ayuda antes del redireccionamiento. Redirección y correo reales requieren Keycloak configurado. |
| 3. Acceso contextual | Aprobado | Playwright recorre las 18 rutas de workspace y verifica el retorno al detalle de una orden. |
| 4. Búsqueda y filtros | Aprobado | Consultas sin tildes, filtros por módulo y perfil, persistencia en URL y estado vacío. |
| 5. Permisos de manual y sección | Aprobado con API controlada | Acceso general público, procedimientos según permisos efectivos y acceso denegado a módulos restringidos. |
| 6. Versiones y fechas | Aprobado localmente | Historial visible en las guías. `docs:check` valida fechas, versiones crecientes y conservación de entradas previas. |
| 7. Cambios con impacto documental | Aprobado localmente | `docs:check` comparó la revisión con la base. Hay reglas por ruta y módulo y registro de motivos verificables sin impacto. |
| 8. Pasos coherentes con la interfaz | Revisado | Guías referencian controles y rutas existentes. Las operaciones dependientes de permisos, simulación o Keycloak se identifican en contexto. |
| 9. Capturas actuales | Aprobado | Chromium regeneró login y dashboard con datos ficticios. Las pruebas verificaron que el lector carga la imagen del manual de acceso. |
| 10. Impresión y PDF | Aprobado | Se probó el botón y el modo de impresión. Chromium generó un PDF A4 y validó su firma de archivo. |
| 11. Escritorio, tablet y móvil | Aprobado en Chromium | Desktop y móvil en Playwright, más 1280, 820 y 390 px en el lector. Se verificó el tema oscuro. |
| 12. Integración CI | Configurado y validado localmente | Frontend verifica manuales y cambios por PR. Backend verifica evidencia documental y corre regresiones HTTP. Corrida remota pendiente. |
| Contrato público de pagos | Aprobado en TestServer | HTTP 400 ante campos de simulación, rutas fuera de Development ausentes y OpenAPI sin los campos de prueba. |
| Idempotencia y conciliación | Validación parcial | Control de recurrencia en navegador y pruebas aisladas en backend. Integración PostgreSQL y cuenta Mercado Pago externa pendientes. |
| AWS y SQS | Validación parcial | Transporte AWS Core y deduplicación comprobados con mocks. Migración a AWSSDK.SQS, redrive y métricas reales pendientes. ECS comparado con EKS en el assessment. |

## Línea base del 13 de noviembre de 2026

Fecha: 2026-11-13. **Implementado** significa código presente; **validado** identifica una comprobación ejecutada; **bloqueado** requiere una dependencia externa; **objetivo** aún requiere desarrollo o verificación adicional. Ningún estado implica certificación de seguridad ni preparación productiva. Rutas relativas a la carpeta principal VortexBird.

| Criterio solicitado | Estado | Evidencia / límite |
| --- | --- | --- |
| Tres repositorios independientes | Validado con aclaración | Cuatro repositorios Git locales conforme al desglose inicial. Sesión GitHub en navegador disponible; conexión API desde terminal fallida. Sin remotos publicados acreditados. |
| Backend .NET con Clean Architecture | Validado por compilación | Solución completa .NET 10, cero advertencias/errores; pruebas de límites de dependencias aprobadas. |
| CQRS funcional | Implementado | `Application/Abstractions/Contracts.cs`, `Infrastructure/OrderHandlers.cs`: command/query handlers separados. Cobertura del resto de módulos por completar. |
| Entity Framework Core | Validado parcialmente | EF/Npgsql y migraciones compiladas; SQL ejecutado en motor embebido. EF runtime con PostgreSQL externo pendiente. |
| PostgreSQL | Validado parcialmente | 45 comprobaciones SQL: 17 esquema, nueve proyecciones, siete cuotas y doce pagos. Cinco migraciones, 31 tablas, 72 índices y seis vistas, SHA final f91b0ed9...; PostgreSQL18.6 WASM, una sesión. PG17/Npgsql y concurrencia pendientes. |
| Migraciones y seeders | Implementado / SQL validado | Cinco migraciones versionadas y script idempotente ejecutados dos veces; seed AndesRetail CRM/OMS. Reportes SQL comparten SHA final; ejecución EF/Npgsql externa pendiente. |
| Índices y vistas documentados | Validado parcialmente | 72 índices y seis vistas en esquema final. Proyecciones probadas con dos partners/tres canales, UTC y commit/rollback; EXPLAIN y carga representativa pendientes. |
| Paginación desde backend | Implementado | `API/OperationalEndpoints.cs` aplica Skip/Take/Count en IQueryable, pageSize máximo 100. |
| Login y registro | Implementado / integración pendiente | Ruta demo Development y frontend OIDC; registro real depende de Keycloak operativo. |
| OAuth2/OIDC y JWT | Implementado / límite HTTP validado | 21 comprobaciones API incluyen JWT y rechazo de callbacks. Keycloak real, registro/SMTP, refresh y revocación end-to-end pendientes. |
| Roles y permisos dinámicos | Implementado | Tablas/DTO/endpoints de administración y política HttpActor. |
| Administración de permisos | Implementado | API y vista con creación de permisos, eliminación confirmada de roles y roles protegidos de solo lectura. Pruebas de interacción aisladas aprobadas. |
| Activity Log | Implementado | `API/Observability.cs`, `/activity-logs` con filtros/paginación y entidades de auditoría. |
| Gestión de partners y canales | Implementado | Endpoints/entidades con contexto de acceso y validación de asociación. |
| APIs de inventario y precios | Implementado | `/inventory/stock`, `/inventory`, `/pricing` consultan DB. Frescura externa y rendimiento no acreditados. |
| Creación y consulta de órdenes | Implementado | Handler, reservas, outbox y consulta por contexto. Flujos completos y carreras sobre PostgreSQL externo no ejecutados. |
| Idempotencia | Implementado / validación parcial | Advisory lock DB, índice partner+key, fingerprint SHA-256 y recibo persistido 24 h; pruebas de concurrencia real DB pendientes. |
| Adaptadores ERP/WMS/OMS/CRM | Implementado / simulación | `Infrastructure/Adapters.cs`: puertos ERP/WMS/OMS/CRM y SimulatedPaymentGateway funcionales sobre DB local. Sin conexiones empresariales reales. |
| Saga Pattern | Implementado / reglas aisladas verificadas | Simulador y gateway sandbox opcional; confirmación, liberación, conciliación, reembolso tardío/duplicado y revisión tras despacho. Sin ejecución integral de saga en PostgreSQL. |
| Eventos y DLQ | Implementado / pruebas controladas aprobadas | Local/SQS opcional, pipeline AWS Core, inbox durable y leases, retry/DLQ; 20 controles de orquestación y nueve de protocolo/firma. Sin SQS/ElasticMQ externo ni consumidor Npgsql ejecutado. |
| Webhooks | Implementado / validación parcial | Suscripciones, HMAC, control SSRF, reintentos y deduplicación. Suite de seguridad 50/50; receptor externo no probado. |
| Pasarela de pagos en sandbox | Implementado / ejecución externa bloqueada | Gateway conectado, checkout durable, inbox HMAC, conciliación y compensaciones; 61 pruebas de HTTP controlado y reglas. Sin cuenta/credenciales ni sesión Mercado Pago externa verificada. |
| Dashboard con gráficas agregadas desde PostgreSQL | Implementado | `API/DashboardEndpoints.cs` y frontend; datos agregados en backend. Ejecutar contra PostgreSQL para validar. |
| Redis | Implementado / 32 controles aprobados | RESP2 acotado, TLS/AUTH obligatorios fuera de Development y fallback PostgreSQL; TTL stock 10 s / cotización 60 s. Transporte controlado, sin ElastiCache/failover real. |
| Logging estructurado | Implementado alternativa nativa | JSON logging .NET; Serilog no disponible en caché/red. No presentarlo como instalado. |
| Distributed tracing | Implementado parcialmente / objetivo | Instrumentación nativa Activity/Meter y correlación; exportación OpenTelemetry/ADOT requiere paquetes/configuración y verificación. |
| Rate limiting | Implementado compartido / validación por partes | Cuotas independientes partner/canal en PostgreSQL, lock+reloj DB+transacción, 429 Retry-After y fallo cerrado. 17 controles .NET y siete SQL; concurrencia multirréplica no medida. |
| Circuit Breaker y retries | Implementado parcialmente | Circuito simulador y backoff outbox; endurecimiento de adaptadores reales pendiente. |
| Frontend React responsive | Build/lint/typecheck/15 pruebas aprobados | Todos los chunks bajo 500 kB, principal 382,40 kB. CSS propio, no Tailwind/shadcn. Vite arrancó; navegación local y E2E integrada no verificadas. |
| Modo Light y Dark | Implementado / validación pendiente | Preferencia de tema frontend; confirmar contraste y persistencia. |
| Skeleton loaders | Implementado / validación pendiente | Componentes de carga del frontend; confirmar pantallas. |
| Accesibilidad | Mejoras implementadas / revisión integrada pendiente | Foco, teclado, menú móvil, formularios, diálogos, contraste y movimiento reducido. No se declara auditoría completa ni prueba con lector de pantalla. |
| CI/CD con GitHub Actions | Implementado / gate probado | 34 checks estáticos de infraestructura y seis del gate de apply; main+dispatch manual+reviewers+branch rules. Sin ejecución remota GitHub ni despliegue. |
| Infraestructura Terraform | Implementado / validación CLI bloqueada | YAML/wiring y Compose con overlay ElasticMQ validados. Terraform ausente y descarga DNS bloqueada: validate/plan no ejecutados. |
| Despliegue AWS aprobado y verificado | Bloqueado / no autorizado aún | No apply ni recursos creados. `costs-and-approval.md` prepara plan y presupuesto; falta aprobación explícita y acceso. |
| Pruebas automatizadas | Verificación integral aprobada por alcance | 268 controles: 24 dominio, 19 invariantes, 50 seguridad, 21 API, 61 pagos, 17 cuotas, 32 caché, 20 mensajería, nueve SQS, 15 frontend. Aparte: SQL45 e infraestructura34+6. `../qa/verification-summary.json`; no equivale a cobertura end-to-end. |
| Pruebas de rendimiento | Preparadas / no medidas | Escenarios k6 en QA; ningún SLO 99,9% o p95 < 300 ms declarado cumplido. |
| Documento completo de nueve entregables | Validado | Markdown de nueve secciones y PDF de 20 páginas, regenerado y revisado; cuotas, checkout, caché, SQS y esquema final reflejados. Ocho ADR complementan decisiones. |
| Diez diagramas | Validado | Diez fuentes Mermaid y PNG actualizados: checkout, inbox/SQS y Pod Identity del backend. El esquema gráfico no demuestra un despliegue. |
| Guía de sustentación | Validado | `presentation-guide.md` con recorrido, fallos, preguntas y límites. |

## Dependencias adicionales relevantes

FluentValidation, Serilog y OpenTelemetry no se sustituyen silenciosamente por nombres de clases. El incremento dispone de validación y telemetría nativas, y documenta la diferencia. Registro, recuperación de contraseña y rotación de sesiones se delegan a Keycloak, no se duplican contraseñas/refresh tokens en una identidad paralela. La galería oficial de NuGet pudo abrirse, pero la descarga del CDN quedó bloqueada; no se crearon stubs ni se afirmó instalar esos paquetes. La política de secretos productivos, HA, observabilidad exportada, restauración y costos deben validarse antes de promover este incremento.

## Evidencia mínima para cerrar lo pendiente

1. Levantar PostgreSQL/Redis/Keycloak y ejecutar migraciones, seed y smoke con identidad real.
2. Ejecutar pruebas de orden concurrente, aislamiento partner/canal, outbox tras reinicio y compensaciones contra DB.
3. Verificar frontend con backend real, teclado, tamaños móviles y estados de error.
4. Con credenciales de prueba, ejecutar el flujo de pasarela ya implementado: checkout, firma de webhook, consulta autoritativa y compensación; nunca usar pagos reales.
5. Validar Terraform/plan, inventario y costo regional, obtener aprobación y solo entonces desplegar y medir.
