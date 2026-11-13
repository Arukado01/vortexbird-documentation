# Estado de implementación y evidencia

Revisión final: 13 de noviembre de 2026. Los resultados distinguen código, pruebas aisladas, integración y despliegue. El incremento es una demostración local; no se declara listo para producción ni se declaran cumplidos los SLO.

| Componente | Resultado observado | Límite |
| --- | --- | --- |
| Repositorios | Cuatro proyectos Git independientes | No publicados en GitHub: conexión no verificada. |
| Backend .NET 10 | Solución completa compila, cero advertencias y errores | Integración completa con servicios externos pendiente. |
| Dominio y arquitectura | 24 + 19 comprobaciones aprobadas | No sustituyen concurrencia de PostgreSQL externo. |
| Seguridad | 50 comprobaciones aprobadas | Aislamiento contextual, direcciones webhook y validaciones; no auditoría exhaustiva. |
| API/JWT | 11 comprobaciones aprobadas con ASP.NET TestServer | Discovery RSA de prueba; sin Keycloak real ni transporte TCP. |
| Piloto Mercado Pago | Cliente HTTP y firmas; 24 comprobaciones aprobadas con transporte de prueba | Aislado: falta conectar checkout, inbox y conciliación con saga. Sin sandbox externo verificado. |
| Migraciones PostgreSQL | Tres migraciones versionadas; script idempotente, seis vistas | Prueba SQL en PostgreSQL 18.6 WASM, destino Compose PostgreSQL 17. |
| Esquema SQL | 17 comprobaciones aprobadas, 26 tablas y 58 índices | Una sesión embebida, sin failover/concurrencia/rendimiento productivo. |
| Frontend | TypeScript/build, ESLint y 12 pruebas aprobadas | Build informa un chunk mayor de 500 kB; optimización adicional pendiente. |
| Interfaz | Módulos conectados a API, temas, skeletons y controles accesibles | E2E de navegador y revisión visual de la aplicación bloqueadas por conexión local. |
| Adaptadores y saga | ERP/WMS/CRM/OMS persistidos y pago simulado, idempotencia, outbox y compensación | Sistemas simulados. SQS runtime y pasarela externa no conectados. |
| Infraestructura | Compose, realm Keycloak, Terraform, Kubernetes, pipelines y costos preparados | Compose/configuración verificados; Docker inaccesible, Terraform validate/plan pendientes. |
| AWS | Sin recursos creados ni modificados | Requiere inventario válido, revisión del plan y aprobación explícita de costos. |
| Rendimiento | Escenarios k6 preparados | No se midió tráfico 10x, disponibilidad 99,9 % ni p95 menor de 300 ms. |
| Assessment | Nueve secciones, PDF de 19 páginas, diez diagramas, cinco ADR y guía | La arquitectura productiva está diferenciada del incremento implementado. |

Evidencia: `../qa/verification-summary.json`, `../qa/security-results.json`, `../qa/api-boundary-results.json`, `../qa/security-review.md`, `../vortexbird-infrastructure/reports/postgresql-schema-validation.json` y `../vortexbird-backend/tests/PaymentChecks/results.json`. El verificador reproducible está en `../verify.ps1`.

## Trabajo que aún requiere implementación o integración

1. Conectar SQS y su consumidor/inbox al outbox; la demostración actual usa una cola durable en PostgreSQL.
2. Integrar el piloto Mercado Pago con persistencia de checkout, callbacks verificados, conciliación y compensaciones externas; aportar credenciales de prueba.
3. Validar el flujo Keycloak completo (registro, SMTP, recuperación, refresh y revocación), PostgreSQL/Redis y el frontend real juntos.
4. Incorporar y validar los paquetes solicitados FluentValidation, Serilog y exportador OpenTelemetry cuando haya acceso a dependencias. Actualmente hay validación, logs JSON, Activity/Meter y correlación nativos.
5. Verificar Terraform con proveedores reales, TLS/dominio, secrets, restauración, límites distribuidos y costos antes de cualquier despliegue aprobado.
6. Completar carga 10x, resiliencia tras reinicios, accesibilidad/contraste y revisión visual. Incorporar el archivo oficial del logo; no se ha inventado uno.

Las cuotas de partner usan RequestsPerMinute de la base de datos, por proceso. Los canales firmados heredan conservadoramente ese presupuesto; aún no existe un presupuesto distribuido configurable independiente para cada canal.
