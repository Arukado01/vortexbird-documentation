# Guía de presentación ejecutiva

Usar `output/presentation/VortexBird_AndesRetail_Executive.pptx`. La presentación contiene notas del expositor y distingue código, interfaz aislada y despliegue pendiente.

## Recorrido de 20 minutos

| Tiempo | Tema | Evidencia |
| --- | --- | --- |
| 0-3 min | Problema de integración y objetivo de negocio | Contexto y arquitectura modular |
| 3-8 min | Pedidos, reservas, pagos y compensación | Diagramas de flujos y límites del simulador |
| 8-12 min | Seguridad y operación | Permisos por partner, outbox/inbox e IAM objetivo |
| 12-15 min | Interfaz y documentación viva | Capturas de UI actual con datos sintéticos y 11 manuales |
| 15-18 min | Resultados y estado | 302 controles acotados, bloqueo de loopback y AWS pendiente |
| 18-20 min | Decisiones necesarias | Entorno conectado, sandbox, plan y presupuesto |

## Mensaje de apertura

VortexBird concentra los contratos que conectan los canales de AndesRetail con inventario, precios, pedidos y pagos. La revisión corrigió defectos y verificó código e interfaz en pruebas acotadas. El entorno no permitió validar todos los servicios comunicados; por ello el despliegue AWS sigue pendiente.

## Demostración

Usar el entorno conectado solo después de confirmar readiness y login. Las direcciones y UUID antiguos no se toman como disponibles. Crear una orden sintética, repetir su clave idempotente, consultar historial y probar un rechazo compensado. Si el entorno continúa bloqueado, presentar las capturas con su alcance visible y no llamarlas demostración end-to-end.

## Preguntas que deben responderse con precisión

- AWS: arquitectura e IaC preparadas; no despliegue ni URL remota acreditados.
- Pagos: simulador por defecto y adaptador sandbox con 61 pruebas controladas; cuenta externa pendiente.
- SLO: 99,9 % y p95 <300 ms son objetivos sin medición suficiente.
- Costos: reserva orientativa USD 220-290/mes para piloto con identidad; no aprobación ni cotización exacta Ohio.
- Integración empresarial: ERP, WMS, OMS y CRM de demostración son simulados.
