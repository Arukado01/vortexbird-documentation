# Guía de sustentación

## Cómo estudiar y practicar con la plataforma local

1. Lee las secciones 1 y 3 del assessment para entender el problema y el recorrido entre portal, API, PostgreSQL y adaptadores. Abre el diagrama [01 - Arquitectura](diagrams/01-architecture.mmd).
2. Entra al [portal local](http://localhost:5173). Usa el correo y la contraseña de demostración definidos como `DEMO_EMAIL` y `DEMO_PASSWORD` en `vortexbird-infrastructure/.env`. En **Dashboard**, compara los estados y el volumen de E-commerce y Marketplace. Luego abre **Órdenes** y sigue un caso de principio a fin.
3. Abre el historial del pedido y revisa qué estado cambió y por qué. Pasa por **Pagos** e **Inventario** para entender cuándo se consume una reserva y cuándo se libera. En **Eventos** y **Activity Log**, usa el ID de correlación para relacionar la orden con el trabajo asíncrono y con la auditoría.
4. Lee la sección 4 del assessment y los diagramas de [creación de orden](diagrams/05-create-order.mmd), [saga](diagrams/08-saga.mmd) y [eventos](diagrams/09-events.mmd). Explica en voz alta qué queda guardado al recibir el `202` y qué completa el worker.
5. Abre [Swagger](http://localhost:15080/swagger/index.html). Ejecuta `POST /api/v1/auth/demo-login` con los datos de demo, copia `accessToken` en **Authorize** y consulta `GET /api/v1/orders/{id}`. Prueba luego `POST /api/v1/orders` con una clave nueva en `Idempotency-Key`. Repite la misma solicitud para ver el mismo ID. Cambia la cantidad conservando la clave para observar el `409`. En PowerShell, el lanzador `Iniciar-VortexBird.cmd` reconstruye las imágenes locales cuando hay cambios.
6. En **Integraciones**, usa **Probar conexión** para ver una ejecución del adaptador simulado. Lee las secciones 5 a 7 del assessment para explicar autorización por partner y canal, Redis, reintentos y observabilidad. Consulta `implementation-status.md` junto con el manifiesto de evidencia `../qa/release-manifest.json` para distinguir las pruebas locales de lo pendiente en AWS.

### Pedidos para el ensayo local

El 14 de noviembre de 2026 se agregaron 30 pedidos por la API en la base de datos local. Al verificar, había 48 pedidos en total, incluidos 18 anteriores, y 30 pagos simulados.

| Caso | Qué observar |
| --- | --- |
| [CUST-001 · Entregado](http://localhost:5173/orders/72aef47a-77cf-4d45-ba27-43a68873d9de) | Reserva, pago aprobado, confirmación, despacho y entrega. |
| [CUST-007 · Despachado](http://localhost:5173/orders/da7a3336-2cb7-496e-b4cf-a01e801272f7) | Pago aprobado y entrega aún pendiente. |
| [CUST-011 · Confirmado](http://localhost:5173/orders/af11dd2d-b418-4f6a-b6c3-6a2869807a4d) | Inventario consumido y listo para despachar. |
| [CUST-019 · Pago rechazado](http://localhost:5173/orders/d1d67108-9acf-46ca-8966-df468164a7ce) | El historial pasa por compensación y cancelación. |
| [CUST-026 · Pago pendiente al verificar](http://localhost:5173/orders/f9ef2271-12f0-4e58-9f66-ae998b72b47e) | Reserva temporal en Marketplace. Si ya venció, crea otra orden con **Pendiente** en el simulador. |

### Explicación de apertura

«VortexBird conecta los canales de venta de AndesRetail con inventario, precios, clientes y pagos. Voy a mostrar una orden desde que se reserva inventario hasta que se confirma o se cancela. La operación queda persistida en PostgreSQL y los adaptadores de la demo simulan las respuestas de los sistemas externos».

## Recorrido sugerido: 20 minutos

| Tiempo | Contenido | Evidencia |
| --- | --- | --- |
| 0-2 min | Problema, propiedad de datos y alcance de la demo | Resumen ejecutivo y supuestos. |
| 2-5 min | Arquitectura, límites y sync/async | Diagramas 01, 03 y 04. |
| 5-10 min | Orden, idempotencia, reserva, pago y compensación | Mismo request repetido, caso de rechazo y timeline. |
| 10-13 min | Seguridad y aislamiento | Permisos dinámicos, token inválido, partner ajeno. |
| 13-16 min | Promociones y operación | Caché/frescura, errores de adaptador, outbox y auditoría. |
| 16-18 min | Validaciones reales y limitaciones | implementation-status.md y salidas de pruebas. |
| 18-20 min | Roadmap, costos y liderazgo | Opciones productivas y decisiones por validar. |

## Preparación de la demo

1. Verificar prerequisitos del README de infraestructura y levantar el entorno local. No intentar una primera instalación durante la entrevista.
2. Confirmar health/readiness, inicio de sesión y seed de AndesRetail. Mantener visible que ERP/WMS/OMS/CRM son simulados.
3. Elegir un SKU con inventario suficiente y un partner/canal autorizado. No usar PII ni credenciales reales.
4. Crear una orden con clave idempotente y guardar la respuesta. Repetir exactamente la petición; luego cambiar la cantidad conservando la clave para mostrar conflicto.
5. Inducir rechazo de pago mediante el simulador y mostrar cancelación, liberación e historial. Si existe una cuenta sandbox configurada y verificada, consultar checkout, abrir la URL permitida y explicar que el navegador no confirma el pago: inbox, consulta autoritativa y saga deciden. Un timeout deja `unknown` y no repite el POST de creación.
6. Abrir Activity Log por correlation-id y relacionar orden, pago y evento. Mostrar permisos efectivos con un usuario limitado.
7. Mostrar la cuota del canal y explicar cómo consume también el presupuesto del partner en PostgreSQL. Un listado agregado alcanza todos los canales autorizados; quitar channelId no evita el límite. No afirmar que se midió concurrencia entre réplicas si solo se ejecutó la prueba SQL embebida.
8. Presentar los resultados de pruebas realmente ejecutadas. Si Docker, navegador integrado o AWS no pudieron verificarse, decirlo y mostrar la configuración preparada sin convertirla en evidencia de ejecución.

## Preguntas probables y argumento central

**¿Por qué no diez microservicios desde el inicio?** Los contextos y puertos permiten separar responsabilidades ahora. Distribuir exige contratos, despliegue, observabilidad y conciliación adicionales; se extrae un servicio cuando su autonomía o carga lo justifica.

**¿Cómo evitas sobreventa si consultas desde Redis?** La consulta es orientativa y tiene frescura explícita; la reserva autoritativa es atómica y decide la venta. Invalidación y TTL reducen inconsistencias, pero no reemplazan esa reserva.

**¿Qué pasa si cobras y se cae la API?** La intención se persiste antes de llamar al proveedor. Una respuesta perdida deja estado unknown y se busca por referencia sin repetir el POST. El callback se guarda antes del acuse; la conciliación obtiene el pago autoritativo y verifica vendedor, importe, moneda y referencia. El outbox conserva la intención de notificar, pero no vuelve atómica a la pasarela.

**¿Qué sucede con una aprobación tardía o un segundo pago?** La política comprueba la reserva vigente y el pago aceptado. Si ya no corresponde cumplir, agenda un reembolso con clave estable y verifica el estado después. El segundo pago se compensa por separado sin cancelar el primero. Antes del despacho puede restituirse inventario una vez; después exige revisión. Estas reglas tienen pruebas aisladas, todavía no una sesión externa acreditada.

**¿El límite por partner funciona con varias réplicas?** El estado está compartido en PostgreSQL y la decisión usa lock, reloj DB y transacción. Las pruebas actuales cubren planificación, parser y SQL en una sesión; faltan carreras Npgsql y carga para medir contención y latencia. La ventana fija y el bloqueo por partner son trade-offs explícitos.

**¿Hay exactly-once?** No end-to-end. Hay entrega al menos una vez y efectos diseñados para ser idempotentes. Una transacción local puede unir inbox y efecto DB, pero un efecto externo necesita idempotencia propia.

**¿Dónde está el tenant?** En identidad verificada y políticas del backend. Cada consulta por objeto, caché, clave idempotente y entrega debe mantener ese contexto. Un UUID difícil de adivinar no es autorización.

**¿Cumples 99,9% y p95 < 300 ms?** Son objetivos. Solo se presentan mediciones con entorno, duración y carga identificados. La disponibilidad mensual exige observación de producción y diseño operativo, no una captura del dashboard.

**¿Qué mostrarías primero con solo cinco minutos?** La creación de una orden repetida sin duplicación, un fallo con compensación y su trazabilidad. Es el recorrido que conecta arquitectura con impacto de negocio.

## Límites que conviene decir con claridad

- Demo y producción tienen requisitos y costos distintos.
- Los adaptadores simulados no acreditan integraciones empresariales reales.
- La ruta demo de autenticación, si se usa, no es el flujo OIDC productivo.
- No se procesan pagos reales; un adaptador sin credenciales de prueba verificadas no se presenta como sandbox integrado.
- El despliegue AWS requiere un plan concreto, costo revisado y aprobación del propietario.

La sustentación debe explicar decisiones que el candidato comprende y puede defender. Ensayar los fallos ofrece más valor que memorizar nombres de patrones.
