# Matriz de auditoría integral

17-Nov-2026. Evidencia actual contrastada con código y ejecuciones disponibles.

| Componente | Estado actual | Evidencia | Problema identificado | Acción realizada o necesaria | Prueba de corrección |
| --- | --- | --- | --- | --- | --- |
| Repositorios | Cuatro repositorios locales | Git y carpetas independientes | Cambios previos sin publicar | Conservar cambios y límites de repositorio | Builds y revisión de diff; publicación remota sin acreditar |
| Paginación | Corregida a 10 | Endpoints administrativos/operativos y frontend | Default anterior de 20 | Aplicar 10 y actualizar guías | Builds y pruebas frontend; recorrido DB pendiente |
| Proveedor de pago | Configuración corregida | AdministrationEndpoints | Settings anunciaba simulator fijo | Leer proveedor activo de IPaymentGateway | Build y límites HTTP; DB pendiente |
| Readiness | Corregido | Program.cs | Conexión DB no garantizaba migraciones | Exigir ausencia de migraciones pendientes | Build aprobado; DB vacía/migrada pendiente |
| Resolución de pagos simulados | Corrección implementada | OrderHandlers y Integration.ps1 | Tracking podía conservar estado previo al lock | Limpiar y releer bajo lock | Pruebas controladas pasan; ocho solicitudes concurrentes pendientes |
| OIDC en recarga | Recuperación implementada | Auth provider y pruebas unitarias | Recarga perdía sesión en memoria | Reautorización PKCE silenciosa y retorno al origen | Unitarias pasan; Keycloak real pendiente |
| Roles | Guía y controles alineados | usuarios-permisos.json y UI | Permisos conjuntos y autoasignación mal descritos | Documentar users.update + roles.assign_permissions y bloqueo propio | docs:check y pruebas controladas |
| Accesibilidad | Corregida parcialmente | CSS y DashboardPage | Contraste y gráfica oculta en móvil | Botón 5,12:1, hover 6,35:1; gráfica visible | Contraste calculado, lint y navegador aislado |
| Manuales | Once guías actuales | JSON, docs:check y help.spec | Versiones y pasos afectados | Actualizar versiones e historial | 20 casos UI aislada; capturas actuales |
| PostgreSQL / Redis | Integración sin acreditar | Probes y logs de arranque | Socket 10013 | Procedimiento reproducible preparado; ejecutar sesión habilitada | Health, SQL, persistencia y concurrencia conectados |
| Keycloak / ElasticMQ | Integración bloqueada | Logs y errores LoopbackConnector | Red local denegada | Conservar configuración; no modificar permisos del sistema | OIDC y protocolo reales en loopback |
| Pagos externos | Pendientes | 61 controles de pago | Sin sesión sandbox acreditada | Obtener credenciales de prueba y webhook HTTPS | Checkout, firma, conciliación y compensación reales sandbox |
| AWS ECS | IaC presente | Terraform y workflows | Sin puerta local, plan real ni presupuesto | Completar requisitos antes de apply | Plan de cuenta, IAM efectivo y smoke remoto |
| Evidencia documental | Actualizada | JSON, cierre e historial | Manifest y tablas antiguas mezclaban épocas | Separar historia y registrar ejecución vigente | Coherencia de fechas, cifras y límites |
| PDF y presentación | Rediseñados | Fuentes y salidas reproducibles | PNG antiguos y ausencia de PPTX | Atlas SVG, PDF completo y deck independiente | Render, texto, notas y revisión visual |

Ninguna columna declara un flujo integrado completado si la prueba conectada está pendiente.
