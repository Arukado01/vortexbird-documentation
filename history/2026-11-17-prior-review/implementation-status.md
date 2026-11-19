# Estado de implementación y evidencia

## Cierre del 17 de noviembre de 2026

| Capacidad | Estado | Evidencia y límite |
| --- | --- | --- |
| ECS Fargate | Arquitectura adoptada e IaC validada | Terraform 1.13.3 con AWS 6.73.0 y dos escenarios de plan con proveedor simulado. Cuenta, plan real y despliegue pendientes. |
| EKS | Alternativa conservada | Raíz propia, manifiestos, Pod Identity y flujo de EKS. |
| IAM y secretos ECS | Definidos y comprobados localmente | Task Roles por servicio, solo worker con permiso SQS. Execution Roles por imagen, logs y secreto. Validar políticas y rotación en staging. |
| SDK SQS | Implementado y validado localmente | AmazonSQSClient, 9 controles HTTP y 2 escenarios TCP con ElasticMQ. Prueba AWS y redrive administrado pendientes. |
| Outbox e inbox | Implementados y probados por alcance | 20 controles de orquestación, índice de idempotencia SQL y pruebas del protocolo de entrega. |
| PostgreSQL 17.12 por TCP | Validado localmente | API con cuatro solicitudes simultáneas y persistencia de saga/inbox tanto en transporte local como ElasticMQ. PGlite aportó 45 comprobaciones complementarias. |
| Centro de ayuda | 11 guías generales públicas | Playwright verificó secciones, FAQ, búsqueda, enlaces profundos, recarga, retorno e impresión. [Inventario](manual-inventory.md). |
| Documentación viva | Integrada en CI | Validaciones de metadatos, rutas, anclas, capturas y cambios por PR. Ejecución local equivalente verificada. |
| GitHub Actions | Configurado | CI frontend, backend e infraestructura y plan ECS mediante OIDC. Evidencia remota pendiente. |
| Keycloak y Mercado Pago | Validación controlada | JWT y alcance aplicados en TestServer, 61 pruebas de pagos. El arranque Keycloak autónomo quedó en preparación Quarkus. Faltan sesión OIDC completa y cuenta sandbox disponible. |
| Infraestructura, pagos y SLO | Pendientes de validación externa | Requieren cuenta, DNS, ACM, secretos, credenciales sandbox, plan revisado y pruebas operativas. |

El [informe de cierre](closure-report.md) contiene los comandos ejecutados, entornos y límites. El [checklist](acceptance-checklist.md) registra el estado actual por criterio. Las secciones siguientes conservan evidencia histórica.

## Revisión inicial del 17 de noviembre de 2026

| Capacidad | Estado | Evidencia y alcance |
| --- | --- | --- |
| Centro de ayuda y manuales | Implementado y validado | [Arquitectura](../vortexbird-frontend/docs/architecture/help-center.md), [11 manuales](../vortexbird-frontend/docs/user-manuals/), `e2e/help.spec.ts`. Chromium verificó el login público, enlaces contextuales, permisos, búsqueda, filtros, tema, tres tamaños y PDF A4. |
| Documentación viva | Implementada y validada localmente | [Guía](../vortexbird-frontend/DOCUMENTATION_GUIDELINES.md), [historial](../vortexbird-frontend/DOCUMENTATION_CHANGELOG.md) y `scripts/check-docs.mjs`. GitHub Actions contiene controles en frontend y backend. Ejecución remota pendiente. |
| Contrato de órdenes y simulador | Implementado y validado en HTTP | `CreateOrderRequest`, `OrderSimulationEndpoints.cs` y `ApiBoundaryChecks` 26/26. El contrato público rechaza `paymentOutcome` y las rutas de prueba existen solo en Development con el simulador. |
| Pagos, idempotencia y conciliación | Implementado con pruebas parciales | `PaymentChecks` 61/61 con HTTP controlado. `RequestFingerprint` conserva hashes de las solicitudes anteriores. Pendiente probar concurrencia, checkout, webhooks y compensación con PostgreSQL y cuenta externa de prueba. |
| ERP, WMS, OMS, CRM y pagos de demo | Simulados para demostración | `Infrastructure/Adapters.cs`. Persistencia de demo y capturas con datos ficticios. |
| Mensajería y DLQ | Implementada con pruebas parciales | `MessagingChecks` 20/20 y `SqsTransportChecks` 9/9 con transporte controlado. Outbox, inbox, reintentos, deduplicación y definición de DLQ. Pendientes `AWSSDK.SQS`, ElasticMQ/SQS real y redrive con PostgreSQL. |
| Integraciones externas | Pendientes de validación | Mercado Pago sandbox y OIDC tienen flujos implementados. Credenciales de prueba, Keycloak/SMTP y conectores empresariales requieren un entorno disponible. |
| ECS con Fargate | Diseñado arquitectónicamente | Comparación y recomendación en sección 3 del assessment. IaC, costo regional y ensayo de rollback pendientes. |
| Infraestructura productiva | Pendiente de despliegue | Existe IaC para EKS. Plan validado, conectividad, aprobación, recuperación y medición de SLO pendientes. |

### Resultado de la auditoría

- Se retiraron los campos del simulador del contrato público de órdenes y del puerto que consume el proveedor externo. El consumidor mantiene compatibilidad con eventos de outbox ya persistidos. Los controles del portal consultan la capacidad de simulación de la API.
- El centro de ayuda centraliza guías versionadas y ayuda contextual para 18 rutas autenticadas. Los manuales incluyen acceso, dashboard, usuarios y permisos, partners y canales, catálogo e inventario y precios, órdenes, pagos, eventos y webhooks, auditoría, integraciones y configuración, y reportes.
- El workflow de frontend valida el catálogo, rutas, capturas y versión de guías por cambio. El de backend solicita evidencia documental para cambios de API, contratos o pagos. La documentación de permisos públicos y operativos se conserva en el repositorio frontend.
- La suite de navegador registró 20 aprobadas y dos omisiones previstas en móvil. Chromium cargó los archivos de la compilación mediante respuestas locales de Playwright porque el entorno bloqueó el acceso a localhost. Las respuestas de API fueron sintéticas.
- Compilaron backend y frontend. Pasaron las suites de dominio, invariantes, seguridad, API, pagos, cuotas, caché, mensajería y SQS controlado, más 16 pruebas de Vitest. `verify.ps1` ejecuta las suites base y los logs de la revisión registran su alcance.
- Docker Desktop denegó acceso a su motor. NuGet no resolvió los hosts de distribución de `AWSSDK.SQS`. Se conserva el transporte funcional con `AWSSDK.Core` y marshalling existente. Sin acceso a servicios quedan abiertas las pruebas de base de datos, identidad, redrive y pagos de proveedor.
- El assessment mantiene nueve secciones y cinco escenarios de liderazgo. Incluye la matriz, los cambios en pagos y mensajería, el análisis ECS/EKS, aceptación, roadmap y once diagramas.

## Línea base del 13 de noviembre de 2026

Revisión de evidencia: 13 de noviembre de 2026. Los resultados distinguen código, pruebas aisladas, integración y despliegue. No se declara preparación productiva ni cumplimiento de SLO. Las pruebas controladas y SQL embebidas están diferenciadas de las sesiones de servicios externos aún pendientes.

| Componente | Resultado observado | Límite |
| --- | --- | --- |
| Repositorios | Cuatro proyectos Git independientes | GitHub tiene sesión de navegador disponible; la API desde terminal falla por conectividad. No se declaran remotos publicados. |
| Verificación integral | Backend compilado sin advertencias ni errores; 268 controles de aplicación y frontend aprobados | `../qa/verification-summary.json` registra cada ejecución. Los 45 controles SQL y 34+6 de infraestructura se contabilizan aparte; sin ejecución de servicios externos. |
| Dominio y arquitectura | 24 + 19 comprobaciones aprobadas | No sustituyen concurrencia de PostgreSQL externo. |
| Seguridad | 50 comprobaciones aprobadas | Contexto, webhooks y validación; no es auditoría exhaustiva. |
| API/JWT y callbacks | 21 comprobaciones aprobadas con ASP.NET TestServer | Discovery RSA controlado y rechazos de callbacks antes de DB; sin Keycloak real ni webhook aceptado y persistido. |
| Mercado Pago sandbox | Gateway opcional, checkout durable, inbox, conciliación, compensaciones y 61 pruebas aprobadas | HTTP controlado y reglas de producción. Sin llamada externa ni saga ejecutada contra PostgreSQL desplegado. Simulator sigue siendo el valor por defecto. |
| Cuotas partner/canal | Contadores compartidos PostgreSQL con lock, reloj DB y transacción; 17 controles .NET y siete SQL aprobados | La implementación es compartida; no se midió concurrencia Npgsql entre réplicas. |
| Redis | Cliente RESP2 con TLS/AUTH, configuración segura y fallback; 32 comprobaciones aprobadas | Transporte controlado, sin conexión real ElastiCache ni medición de failover. |
| Migraciones y esquema SQL | 17 comprobaciones aprobadas: cinco migraciones, 31 tablas, 72 índices y seis vistas | SHA final f91b0ed9...; PostgreSQL 18.6 WASM, una sesión. Destino Compose PostgreSQL 17 y Npgsql pendientes. |
| Proyecciones PostgreSQL | Nueve pruebas aprobadas con dos partners y tres canales | Seis vistas, UTC y commit/rollback; no equivale a ejecutar handlers API. |
| Persistencia de pagos | Doce pruebas SQL aprobadas de checkout/inbox/receipts, constraints, leases y rollback | No ejecutan la saga C#; comparten SHA final con esquema/proyecciones/cuotas. |
| Frontend | Build, TypeScript, lint y 15 pruebas aprobados; todos los chunks bajo 500 kB | E2E y revisión visual integrada pendientes. Vite arrancó en 5175, pero la navegación local agotó el tiempo de conexión. |
| Interfaz | Checkout opcional con URL validada, cuotas por canal, foco/teclado y menú móvil | Requiere revisar navegación real y sesión sandbox con credenciales de prueba. |
| Adaptadores y saga | ERP/WMS/CRM/OMS simulados persistidos; pasarela simulada y proveedor sandbox opcional | No hay conexiones a ERP/WMS/CRM/OMS empresariales reales. |
| Eventos | Outbox e inbox durables, local/SQS opcional; 20 controles de orquestación y nueve del pipeline AWS Core aprobados | HTTP controlado y metadatos EF. No SQS/ElasticMQ externo ni ejecución Npgsql del consumidor. |
| Infraestructura | 34 checks estáticos y seis pruebas del gate CI aprobados; Compose con overlay SQS validado | Backend con EKS Pod Identity; Keycloak/CNI con IRSA. ElasticMQ no ejecutado; Terraform validate/plan pendientes. |
| AWS y Docker | Sin recursos creados ni modificados; Docker CLI disponible | Pipe Docker denegado; endpoint de identidad AWS inaccesible. No hay inventario válido de la cuenta. |
| Dependencias solicitadas | Validación, JSON logging, Activity/Meter nativos | FluentValidation, Serilog y exportadores OpenTelemetry siguen pendientes. Galería NuGet accesible, descarga CDN bloqueada; no se crearon sustitutos con esos nombres. |
| Rendimiento | Escenarios k6 preparados | Sin medición de tráfico 10x, 99,9 % mensual ni p95 menor de 300 ms. |
| Documentación | Nueve secciones, PDF de 20 páginas, diez diagramas, ocho ADR, guía y matriz actualizados | PDF regenerado y revisado visualmente; los diagramas distinguen implementación, simulación y diseño objetivo. |

## Evidencia

- `../qa/verification-summary.json`: última corrida integral registrada; revisar fecha y revisión antes de compararla con cambios posteriores.
- `../qa/security-results.json`, `../qa/api-boundary-results.json`, `../qa/quota-results.json`.
- `../qa/postgres-schema-results.json`, `../qa/postgres-projection-results.json`, `../qa/postgres-quota-results.json` y `../qa/postgres-payment-results.json`: motor, SHA del esquema, alcance y límites.
- `../qa/sqs-transport-results.json`: nueve controles del pipeline oficial con HTTP sintético, sin sockets AWS.
- `../vortexbird-backend/tests/PaymentChecks/results.json` y resultados del cliente Redis.
- `../vortexbird-infrastructure/reports/infrastructure-validation.json` y evidencia de gate CI.
- `../verify.ps1`: ejecución reproducible; no omitir ni reinterpretar fallos como éxitos.

## Verificaciones todavía pendientes

1. Ejecutar SQS/ElasticMQ con PostgreSQL conectado, identidad de runtime, reinicios, redelivery y redrive. Código y pruebas controladas ya están disponibles.
2. Ejecutar API, PostgreSQL, Redis, Keycloak y frontend juntos; verificar registro, SMTP, recuperación, refresh/revocación y permisos.
3. Ejecutar checkout, webhook, consulta autoritativa y compensación contra una cuenta de Mercado Pago de prueba. El código existe; faltan credenciales, endpoints HTTPS y ejecución externa.
4. Probar carreras reales de órdenes, cuotas, callbacks, cancelación y despacho con varias sesiones Npgsql; no inferirlo de una sesión WASM.
5. Instalar y verificar FluentValidation, Serilog y exportador OpenTelemetry cuando el acceso autorizado a dependencias funcione.
6. Validar Terraform/proveedores/plan, inventario, dominio/TLS, secretos y costos; solicitar aprobación explícita antes de provisionar.
7. Ejecutar E2E visual, accesibilidad, carga 10x, fallos/reinicio, restauración y conciliación operativa.

Las cuotas ya tienen presupuestos independientes por partner y canal compartidos en PostgreSQL. Que el algoritmo esté implementado y probado por partes no acredita escalabilidad ni contención de varias réplicas bajo carga.
