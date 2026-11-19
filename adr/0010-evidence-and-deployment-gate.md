# ADR 0010 - Evidencia por entorno y puerta de despliegue

Adoptado el 17-Nov-2026 durante la ejecución de `Texto pegado(9).txt`.

## Contexto

Los controles locales de código y UI pueden ejecutarse con TestServer o respuestas interceptadas, mientras la sesión rechaza sockets de loopback con 10013. Las revisiones anteriores contienen evidencia útil, pero no prueban que la misma conexión funcione ahora. La aceptación exige plataforma conectada antes de aprovisionar AWS y presupuesto aprobado antes de crear recursos facturables.

## Decisión

Cada resultado identifica fecha, comando, entorno y límite. Se separan pruebas en proceso, interfaz aislada, integración local, servicios de proveedor y despliegue AWS. El histórico se conserva en una carpeta con fecha. El estado vigente usa los resultados de esta ejecución.

La puerta AWS permanece cerrada mientras no se supere la aceptación local. Se preparan código, documentación, diagramas y presentación que no dependan de ese acceso, sin convertirlos en aceptación operativa. El plan y costo concretos se someten a una única aprobación cuando la cuenta y dependencias permitan revisarlos.

## Consecuencias

No se altera la seguridad del sistema para eludir el bloqueo, ni se despliega sobre la base de compilaciones o planes simulados. La entrega identifica trabajo terminado y dependencias externas pendientes. Los objetivos de disponibilidad y latencia requieren medición separada.

## Verificación

`execution-evidence.json`, `closure-report.md`, `acceptance-checklist.md` y los informes QA comparten cifras y alcance. Los artefactos visuales etiquetan las capturas sintéticas y el estado AWS pendiente.
