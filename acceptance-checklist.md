# Matriz de aceptación del texto pegado

Fecha: 2026-11-13. **Implementado** significa código presente; **validado** identifica una comprobación ejecutada; **bloqueado** requiere una dependencia externa; **objetivo** aún requiere desarrollo o verificación adicional. Ningún estado implica certificación de seguridad ni preparación productiva. Rutas relativas a la carpeta principal VortexBird.

| Criterio solicitado | Estado | Evidencia / límite |
| --- | --- | --- |
| Tres repositorios independientes | Validado con aclaración | Cuatro repositorios Git locales `vortexbird-{backend,frontend,infrastructure,documentation}` conforme al desglose inicial del texto. GitHub remoto bloqueado por conectividad. |
| Backend .NET con Clean Architecture | Validado por compilación | Solución completa .NET 10, cero advertencias/errores; pruebas de límites de dependencias aprobadas. |
| CQRS funcional | Implementado | `Application/Abstractions/Contracts.cs`, `Infrastructure/OrderHandlers.cs`: command/query handlers separados. Cobertura del resto de módulos por completar. |
| Entity Framework Core | Validado parcialmente | EF/Npgsql y migraciones compiladas; SQL ejecutado en motor embebido. EF runtime con PostgreSQL externo pendiente. |
| PostgreSQL | Validado parcialmente | 17 comprobaciones SQL aprobadas en PostgreSQL 18.6 WASM; 26 tablas/58 índices. Destino PG17 y concurrencia pendientes. |
| Migraciones y seeders | Implementado / SQL validado | InitialIntegrationPlatform, OperationalReplicas y ReportingViews; script idempotente scripts/schema.sql. Seed completo con clientes CRM y réplicas OMS. |
| Índices y vistas documentados | Validado parcialmente | 58 índices y seis vistas consultables; evidencia en infrastructure/reports/postgresql-schema-validation.json. EXPLAIN con carga representativa pendiente. |
| Paginación desde backend | Implementado | `API/OperationalEndpoints.cs` aplica Skip/Take/Count en IQueryable, pageSize máximo 100. |
| Login y registro | Implementado / integración pendiente | Ruta demo Development y frontend OIDC; registro real depende de Keycloak operativo. |
| OAuth2/OIDC y JWT | Implementado / integración pendiente | `API/Program.cs`, `Security.cs`; Keycloak realm preparado, flujo real no validado end-to-end. |
| Roles y permisos dinámicos | Implementado | Tablas/DTO/endpoints de administración y política HttpActor. |
| Administración de permisos | Implementado | API y vista con creación de permisos, eliminación confirmada de roles y roles protegidos de solo lectura. Pruebas de interacción aisladas aprobadas. |
| Activity Log | Implementado | `API/Observability.cs`, `/activity-logs` con filtros/paginación y entidades de auditoría. |
| Gestión de partners y canales | Implementado | Endpoints/entidades con contexto de acceso y validación de asociación. |
| APIs de inventario y precios | Implementado | `/inventory/stock`, `/inventory`, `/pricing` consultan DB. Frescura externa y rendimiento no acreditados. |
| Creación y consulta de órdenes | Implementado | Handler transaccional y `/orders`, `/orders/{id}`. Ejecución sobre PostgreSQL pendiente. |
| Idempotencia | Implementado / validación parcial | Advisory lock DB, índice partner+key, fingerprint SHA-256 y recibo persistido 24 h; pruebas de concurrencia real DB pendientes. |
| Adaptadores ERP/WMS/OMS/CRM | Implementado / simulación | `Infrastructure/Adapters.cs`: puertos ERP/WMS/OMS/CRM y SimulatedPaymentGateway funcionales sobre DB local. Sin conexiones empresariales reales. |
| Saga Pattern | Implementado local / objetivo externo | `OrderSaga`: reserva, pago simulado, confirmar/liberar/cancelar; reconciliación de pasarela externa pendiente. |
| Eventos y DLQ | Implementado local / objetivo SQS | `OutboxWorker` leases, backoff, cinco intentos, dead_letter y replay; SQS definido en Terraform sin conexión runtime. |
| Webhooks | Implementado / validación parcial | Suscripciones, HMAC, control SSRF, reintentos y deduplicación. Suite de seguridad 50/50; receptor externo no probado. |
| Pasarela de pagos en sandbox | Piloto implementado / integración pendiente | Infrastructure/Payments + README-payments.md: cliente HTTP y firmas, 24/24 pruebas aisladas. Falta integrarlo con saga, checkout persistido, inbox y conciliación; sin contacto externo. |
| Dashboard con gráficas agregadas desde PostgreSQL | Implementado | `API/DashboardEndpoints.cs` y frontend; datos agregados en backend. Ejecutar contra PostgreSQL para validar. |
| Redis | Implementado / runtime pendiente | `Infrastructure/Cache.cs` y Compose Redis7; TTL stock 10 s. Fallback y cuotas distribuidas por verificar. |
| Logging estructurado | Implementado alternativa nativa | JSON logging .NET; Serilog no disponible en caché/red. No presentarlo como instalado. |
| Distributed tracing | Implementado parcialmente / objetivo | Instrumentación nativa Activity/Meter y correlación; exportación OpenTelemetry/ADOT requiere paquetes/configuración y verificación. |
| Rate limiting | Implementado local / producción pendiente | RequestsPerMinute efectivo por partner, canales heredan presupuesto. Login10/min, anónimo300/min; techo autenticado100000 compatible con configuración. Distribución y presupuesto por canal independientes pendientes. |
| Circuit Breaker y retries | Implementado parcialmente | Circuito simulador y backoff outbox; endurecimiento de adaptadores reales pendiente. |
| Frontend React responsive | Build/lint/pruebas aprobados | TypeScript/Vite/React, 12 pruebas; E2E de navegador y revisión visual bloqueados por transporte local. CSS de tokens propio, no Tailwind/shadcn. |
| Modo Light y Dark | Implementado / validación pendiente | Preferencia de tema frontend; confirmar contraste y persistencia. |
| Skeleton loaders | Implementado / validación pendiente | Componentes de carga del frontend; confirmar pantallas. |
| Accesibilidad | Implementado parcialmente | Controles/estados diseñados accesibles; auditoría de teclado/contraste/screen-reader pendiente. |
| CI/CD con GitHub Actions | Implementado / no ejecutado remoto | Workflows por repositorio; sin publicación GitHub ni ejecución cloud. |
| Infraestructura Terraform | Implementado / bloqueado validación | `vortexbird-infrastructure/terraform`; binario no disponible y descarga DNS bloqueada. |
| Despliegue AWS aprobado y verificado | Bloqueado / no autorizado aún | No apply ni recursos creados. `costs-and-approval.md` prepara plan y presupuesto; falta aprobación explícita y acceso. |
| Pruebas automatizadas | Validadas parcialmente | 24 dominio + 19 invariantes + 50 seguridad + 11 API + 24 pagos aislados + 12 frontend + 17 SQL. Ver qa/verification-summary.json; E2E y carga pendientes. |
| Pruebas de rendimiento | Preparadas / no medidas | Escenarios k6 en QA; ningún SLO 99,9% o p95 < 300 ms declarado cumplido. |
| Documento completo de nueve entregables | Validado | `vortexbird-documentation/vortexbird-architecture-assessment.md`; `scripts/validate_docs.py`. |
| Diez diagramas | Validado | Diez `.mmd` y diez PNG en `diagrams/`; objetivo versus incremento etiquetado. |
| Guía de sustentación | Validado | `presentation-guide.md` con recorrido, fallos, preguntas y límites. |

## Dependencias adicionales relevantes

FluentValidation, Serilog y OpenTelemetry no se sustituyen silenciosamente por nombres de clases. El incremento dispone de validación y telemetría nativas, y documenta la diferencia. Registro, recuperación de contraseña y rotación de sesiones se delegan a Keycloak, no se duplican contraseñas/refresh tokens en una identidad paralela. La política de secretos productivos, HA, observabilidad exportada, restauración y costos deben validarse antes de promover este incremento.

## Evidencia mínima para cerrar lo pendiente

1. Levantar PostgreSQL/Redis/Keycloak y ejecutar migraciones, seed y smoke con identidad real.
2. Ejecutar pruebas de orden concurrente, aislamiento partner/canal, outbox tras reinicio y compensaciones contra DB.
3. Verificar frontend con backend real, teclado, tamaños móviles y estados de error.
4. Con credenciales de prueba, integrar/validar pasarela, firma de webhook y conciliación; nunca usar pagos reales.
5. Validar Terraform/plan, inventario y costo regional, obtener aprobación y solo entonces desplegar y medir.
