# Estado de implementación y evidencia

Revisión del 17 de noviembre de 2026. Línea base de `Texto pegado(9).txt` y continuación progresiva de `Texto pegado(10).txt`.

**Estado global: validación parcial.** Se corrigió código y se ejecutaron 302 comprobaciones de aplicación e interfaz: 260 backend, 22 unitarias frontend y 20 de Chromium aislado. Dos casos móviles duplicados quedaron omitidos. No se validó el conjunto de servicios conectados ni se desplegó AWS.

| Componente | Estado actual | Evidencia y límite |
| --- | --- | --- |
| Backend .NET 10 | Build y publish aprobados | Cero advertencias y errores. 260 comprobaciones en proceso y transportes controlados; `../qa/backend-validation-2026-11-17.json`. |
| Contratos, pagos y cuotas | Validación acotada aprobada | JWT en TestServer, reglas de pagos y transportes controlados. No sustituye PostgreSQL conectado, proveedor sandbox o carga multirréplica. |
| Frontend React | Build, lint y 22 pruebas aprobados | Recuperación de sesión OIDC, paginación de 10, contraste y controles de permisos actualizados. |
| Interfaz y once manuales | 20 pruebas aprobadas en Chromium aislado | Bundle actual con API interceptada y datos sintéticos. Dos casos omitidos por duplicación en móvil; no es E2E integral. |
| Entorno local conectado | PostgreSQL comprobado en Windows. Aceptación integral pendiente | La consulta SQL autenticada devolvió 1 en la consola de Windows. En la sesión del agente se confirmó 10013. Keycloak compiló y cargó su configuración con Java 25. El login y las suites conectadas requieren la siguiente ejecución normal. |
| Keycloak y sesión OIDC | Pendientes de integración | El cliente tiene pruebas controladas; login, refresh, logout y SMTP reales requieren un IdP accesible. |
| Concurrencia de pagos simulados | Corrección implementada, regresión conectada pendiente | Limpieza de tracking antes del lock. Escenario de ocho solicitudes añadido; no ejecutado por falta de PostgreSQL accesible. |
| Infraestructura | 36 controles de configuración y 6 de gate aprobados | Parser de seis scripts y ValidateOnly aprobados. Terraform validate/test con proveedor bloqueados en esta ejecución; resultados históricos no repetidos. `../qa/infra-validation-2026-11-17.json`. |
| AWS | No desplegado | No se superó la puerta local y no existe presupuesto aprobado. Sin plan real, apply, endpoints ni smoke remoto acreditados. |
| PDF, SVG y presentación | Entregables documentales de esta revisión | Assessment completo con atlas de 14 SVG y PowerPoint ejecutivo con notas. Estados y límites visibles. |
| SLO y disponibilidad | Sin acreditar | No se ejecutó carga integrada ni observación de producción. No se declara p95 <300 ms o disponibilidad del 99,9 %. |

## Continuación incremental del encargo

La tabla anterior describe la línea base ya ejecutada; no suma otra vez sus 302 comprobaciones. La referencia de ejecución vigente es [FINAL_EXECUTION_CHECKLIST.md](../FINAL_EXECUTION_CHECKLIST.md) y el [informe progresivo](../VORTEXBIRD_FINAL_DELIVERY_REPORT.md).

| Cambio o comprobación nueva | Estado y límite |
| --- | --- |
| Continuación local nativa | `Continuar-VortexBird.cmd` preparado; parser y ValidateOnly aprobados. No hubo un nuevo inicio de servicios ni se resolvió el socket 10013. Redis nativo queda deshabilitado; no es aceptación integral. |
| AWS Ohio, lectura real | Inventario regional y tarifas consultados. No se observó despliegue VortexBird; los recursos de otros proyectos no están autorizados para reutilización. No hubo mutaciones, plan ni apply. |
| Identidad opcional ECS | `identity*.tf` prepara Keycloak privado, RDS propia, digest, bootstrap separado, DNS/ACM opt-in y administración restringida. 12 controles estructurales y formato aprobados; proveedor, imagen en ejecución, realm y login pendientes. |
| Migrador, bootstrap inicial y release ECS | Implementación incremental coordinada con backend e infraestructura; resultados exactos en el informe progresivo y QA por componente. Pruebas conectadas y pipeline remoto pendientes. |
| Costos Ohio | Piloto con identidad y Redis estimado en USD 211,07-247,97/mes; escenario HA USD 537,24-625,04/mes. Reservas orientativas, sin presupuesto aprobado ni plan concreto. |
| PDF y PowerPoint | Artefactos de la revisión anterior conservados. Regeneración suspendida hasta validación local y AWS; no documentan todavía estos cambios incrementales. |

La matriz de auditoría está en [audit-matrix.md](audit-matrix.md). El [informe de cierre previo](closure-report.md) registra los límites de aquella revisión; no cierra la continuación. `../qa/current-validation.json` consolida la ejecución actual. [history/](history/README.md) conserva evidencia anterior sin presentarla como repetida.
