# ADR 0001 - Núcleo modular con Clean Architecture

Estado: aceptado para el incremento. Fecha: 2026-11-13.

Contexto: hay varios dominios, un equipo pequeño y un plazo breve. El assessment exige interoperabilidad, no una cantidad de procesos.

Alternativas: monolito sin límites, microservicios por cada menú, núcleo modular con puertos y workers separables.

Decisión: Domain y Application no dependen de API/Infrastructure. Comandos y consultas se separan; persistencia e integración implementan puertos. La base inicial es compartida con propiedad lógica por contexto.

Consecuencias: menor complejidad operativa y transacciones locales simples, a cambio de despliegue parcialmente acoplado. No llamar microservicio a cada carpeta. Extraer un contexto cuando escala, aislamiento o equipo autónomo lo justifiquen.

Validación: prueba arquitectónica de referencias y recorrido de una orden sin modelos de proveedor en Domain.
