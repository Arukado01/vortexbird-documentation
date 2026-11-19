# Informe de cierre de VortexBird para AndesRetail

17 de noviembre de 2026. Revisión a partir de `Texto pegado(5).txt` y del assessment anterior.

## Auditoría y cambios

| Repositorio | Hallazgo | Cambio |
| --- | --- | --- |
| Backend | El transporte delegaba firma al SDK Core y mantenía el protocolo SQS en código propio. | `Messaging/SqsTransport.cs` y `Registration.cs` usan AmazonSQSClient. Se mantuvo IQueueTransport y se añadió una comprobación del worker para ECS. |
| Frontend | Solo el manual de acceso mostraba procedimientos antes del login. | `HelpCenter`, `HelpLink` y los JSON abren lectura, búsqueda e impresión de las once guías. El regreso recupera ruta, query y hash. |
| Infraestructura | El diseño de primer piloto y los archivos de AWS apuntaban a orquestadores distintos. | `terraform-ecs/` define el piloto. La raíz `terraform/`, los manifiestos Kubernetes y sus workflows documentan EKS como alternativa. |
| Documentación | Los diagramas y matrices reflejaban el diseño y los bloqueos anteriores. | Assessment en nueve apartados, ADR, 14 Mermaid con exportación, evidencia, aceptación e inventario de manuales. |

## Despliegue e IAM

ECS Fargate es la arquitectura inicial. El ALB recibe HTTPS una vez configurado ACM y separa tráfico de frontend y API. Los servicios privados de frontend, API y worker escalan independientemente. API y worker comparten imagen y usan distintos roles, configuraciones y secretos. RDS PostgreSQL es privado. Redis TLS se habilita con un grupo ACL validado.

El Execution Role obtiene la imagen, escribe logs e inyecta el secreto del servicio cuando corresponde. El Task Role del worker publica, recibe, cambia visibilidad y confirma sobre una sola cola. API y frontend carecen de políticas SQS. El permiso de redrive de AWS se reserva para un rol operativo. No se requiere acceso S3 desde la aplicación para los reportes CSV. EKS conserva Pod Identity e IRSA en su propia raíz.

El plan que usa Terraform con proveedor simulado no acredita permisos efectivos de AWS, disponibilidad de tipos, preparación de ACM, presupuesto, DNS ni recuperación. Como dependencias quedan el rol de OIDC/plan, bucket de estado, regiones y cuotas, ECR por digest, migraciones, CA de RDS, secretos, certificados y Keycloak HTTPS.

## Mensajería e idempotencia

`AWSSDK.SQS` 4.0.100.26 está restaurado con Core 4.0.103. El adaptador usa las cuatro operaciones oficiales de SQS con long polling, visibilidad, cancelación y retroceso. El código de negocio conserva el outbox transaccional, el inbox por consumidor, la verificación del origen y la finalización durable previa al acuse. El envío ambiguo puede duplicar mensajes y las operaciones de negocio deben seguir siendo idempotentes.

ElasticMQ se ejecutó como proceso Java en loopback. Se verificaron reentrega por expiración de visibilidad, acuse, traslado a DLQ tras cinco recepciones y republicación controlada. El ensayo de redrive administrado de AWS y la prueba de IAM efectivo permanecen pendientes.

## Ayuda pública y documentación viva

[Inventario de manuales](manual-inventory.md) lista los diez grupos obligatorios y Reportes. Chromium abrió desde el login y recorrió directamente y con recarga las once guías sin solicitar `/auth/me`. Verificó lectura de secciones, preguntas frecuentes, búsqueda, impresión y retorno a la pantalla de origen. Las acciones del workspace siguen autorizadas.

El control de documentación compara cambios de PR, valida metadatos, anclas, rutas, capturas y conservación del historial. El criterio de terminado distingue actualización de manual y registro justificado de un cambio sin impacto. Se ajustaron pasos que usaban etiquetas o controles distintos de los que muestra el portal.

## Evidencia de pruebas

Los comandos se ejecutan desde la raíz del repositorio correspondiente, salvo los que mencionan `verify.ps1`, que se ejecuta desde el directorio que reúne los repositorios.

| Prueba | Comando | Resultado y entorno | Límite |
| --- | --- | --- | --- |
| Build backend | `dotnet build VortexBird.sln --no-restore` | Aprobado, .NET 10 en Windows, 0 errores y 0 advertencias. | Compilación local. |
| Backend y frontend base | `./verify.ps1` | 13 etapas aprobadas. Incluye backend, API, pagos, seguridad, cuotas, Redis, outbox/inbox, SQS y frontend. | Excluye el smoke opcional de servidor. |
| API y validación JWT | `dotnet run --project tests/ApiBoundaryChecks --no-build` | 26/26. TestServer y comprobación de tokens con claves RSA de prueba. | Validación de la aplicación. El flujo Keycloak se reporta aparte. |
| Keycloak 26.4.0 autónomo | `kc.bat start-dev --import-realm` y `node e2e/keycloak-smoke.mjs` | El IdP local quedó en la preparación de Quarkus y su puerto no respondió. Se conserva el smoke configurado y se valida la aplicación con TestServer. | Login, refresh, logout y SMTP con un Keycloak disponible quedan pendientes. |
| Mercado Pago en transporte controlado | `dotnet run --project tests/PaymentChecks --no-build` | 61/61. Checkout, idempotencia, webhook firmado, validación de referencia, importe, moneda y vendedor, conciliación y reembolso. | Sesión real de sandbox pendiente de credenciales válidas. |
| API con PostgreSQL 17.12 | `./tests/Integration.ps1 -Port 15089`, una vez con transporte local y otra con ElasticMQ | Dos corridas aprobadas. Migraciones EF, Npgsql por TCP, cuatro solicitudes concurrentes con una creación, tres replays, conflicto de payload, reserva y compensación, historial y dashboard. `psql` confirmó finalización durable del inbox en las dos bases. | Servidor Windows de prueba en loopback, bases descartables y sin failover de RDS. |
| Orquestación inbox/outbox | `dotnet run --project tests/MessagingChecks --no-build` | 20/20. Duplicados, leases, fallos y orden persistir/confirmar. | Colaboradores controlados y metadatos EF. |
| Cliente oficial + ElasticMQ | `dotnet run --project tests/SqsTransportChecks --no-build -- --elasticmq=http://127.0.0.1:19324` | 11/11. Nueve respuestas HTTP controladas y dos escenarios TCP contra ElasticMQ 1.6.12. | Sin IAM AWS ni operación StartMessageMoveTask. |
| Esquema, informes, cuotas y pagos SQL | `npm run test:sql` y `node tests/Postgres*Checks.cjs` con rutas de esquema, fuente de cuotas y salida | 45 comprobaciones acumuladas en PGlite 18.6. | Motor embebido WASM, sin sockets ni concurrencia real. |
| Documentación viva | `npm run docs:check -- <sha-base>` | Aprobado, 11 manuales y 18 rutas. | La revisión humana contrasta los pasos. |
| Frontend y navegación | `npm run build`, `npm test` y `npm run test:e2e -- --reporter=list --workers=2` | 16/16 Vitest y 20 Playwright aprobadas. Dos casos se ejecutan solo en escritorio. Chromium con Vite y respuestas de API sintéticas para workspace. | Móvil emulado y ancho de tablet. |
| Terraform ECS | `terraform -chdir=terraform-ecs fmt -check -recursive`, `validate` y `test` | Terraform 1.13.3 y proveedor AWS 6.73.0. Configuración válida y dos planes simulados aprobados. | Sin plan contra cuenta AWS. |
| Terraform EKS alternativo | `terraform init -backend=false -input=false` y `terraform validate` | Válido con AWS 6.73.0 y TLS 4.1.0 en copia temporal. | La alternativa conserva su raíz. Sin plan de cuenta. |
| Configuración y llegada a Docker | `npm run test:config`, `npm run test:gates`, `docker compose config --quiet` y `docker info` | 34 controles de configuración y seis del gate. Compose base y overlay SQS válidos. El daemon rechazó acceso al pipe de Windows. | Compose y seguridad de configuración son comprobaciones estáticas. |

## CI/CD y estado operativo

Los workflows de frontend, backend e infraestructura están configurados. Se ejecutaron equivalentes locales de build, pruebas, lint, validación de documentación, Terraform ECS y gate de despliegue. El nuevo workflow ECS obtiene un plan mediante OIDC en un ambiente configurado. El workflow EKS permanece en su raíz alternativa. Las ejecuciones remotas están pendientes de un repositorio y una corrida accesibles. Checkov está configurado en GitHub Actions y queda pendiente acreditar su resultado remoto.

## Riesgos restantes

Quedan en el piloto autorizado las políticas IAM efectivas, TLS y DNS, conectividad y CA de RDS, procedimientos de bootstrap, rotación, restauración, pruebas de carga y rollback. Mercado Pago requiere credenciales sandbox y webhook HTTPS válido. La observabilidad y las cuotas de AWS deben verificarse con tráfico representativo. El [checklist](acceptance-checklist.md) registra el estado de cada criterio.
