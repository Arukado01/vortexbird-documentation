# ADR 0008 - SQS opcional y consumidor con inbox durable

Estado al 17 de noviembre de 2026. SDK oficial integrado. Se aprobaron 20 controles de orquestación, nueve de transporte controlado y dos escenarios contra ElasticMQ 1.6.12. SQS real queda pendiente.

Contexto: el outbox local demuestra persistencia y reintento, pero AWS necesita transporte y acuse reales. Los duplicados y timeouts ambiguos exigen idempotencia del consumidor y protección contra workers con lease vencido.

Compose conserva el transporte local como predeterminado. El piloto ECS usa AmazonSQSClient mediante AWSSDK.SQS 4.0.100.26. IQueueTransport limita la dependencia del proveedor. El consumidor valida origen, partner y fingerprint antes de reclamar el inbox. El acuse ocurre una vez persistida la finalización con el lease vigente.

La implementación anterior delegaba la firma a AWSSDK.Core y mantenía serialización de protocolo propia. El SDK oficial de servicio sustituye esa serialización y valida la integridad del mensaje al recibir.

Consecuencias: el consumidor depende del outbox canónico en la misma persistencia; no es un bus abierto a productores arbitrarios. Un crash después del efecto y antes de completar inbox puede repetir el handler. Se procesa un mensaje por reclamación/recepción para acotar leases; capacidad de alto volumen no demostrada. Visibility120s y deadline menor, sin renovación periódica declarada. Mensajes venenosos quedan para redrive/DLQ.

El Task Role del worker ECS habilita solo las operaciones sobre la cola de eventos. Pod Identity e IRSA permanecen en la alternativa EKS. El endpoint HTTP emulado se admite en Development y usa una identidad local de prueba.

ElasticMQ valida la visibilidad, reentrega, acuse, DLQ y republicación explícita. AWS StartMessageMoveTask e IAM de cuenta requieren una prueba autorizada.
