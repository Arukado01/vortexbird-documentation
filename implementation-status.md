# Estado de implementación y evidencia

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
