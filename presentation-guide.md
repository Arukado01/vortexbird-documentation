# Guía de sustentación

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
5. Inducir rechazo de pago mediante el simulador si la versión implementada permite ese modo. Mostrar cancelación, liberación e historial. Un timeout se explica como incertidumbre, no como rechazo automático.
6. Abrir Activity Log por correlation-id y relacionar orden, pago y evento. Mostrar permisos efectivos con un usuario limitado.
7. Presentar los resultados de pruebas realmente ejecutadas. Si Docker o AWS no pudieron verificarse, decirlo y mostrar la configuración preparada sin convertirla en evidencia de ejecución.

## Preguntas probables y argumento central

**¿Por qué no diez microservicios desde el inicio?** Los contextos y puertos permiten separar responsabilidades ahora. Distribuir exige contratos, despliegue, observabilidad y conciliación adicionales; se extrae un servicio cuando su autonomía o carga lo justifica.

**¿Cómo evitas sobreventa si consultas desde Redis?** La consulta es orientativa y tiene frescura explícita; la reserva autoritativa es atómica y decide la venta. Invalidación y TTL reducen inconsistencias, pero no reemplazan esa reserva.

**¿Qué pasa si cobras y se cae la API?** Referencia estable, estado durable y conciliación por proveedor. La respuesta perdida no autoriza un segundo cobro. El outbox evita perder la intención de notificar, no vuelve atómica a la pasarela.

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
