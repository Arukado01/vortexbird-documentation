# ADR 0002 - Saga persistente y outbox

Estado: aceptado; robustecimiento productivo requiere evidencia de recuperación. Fecha: 2026-11-13.

Contexto: una transacción de PostgreSQL no cubre WMS ni pasarela. Los timeouts dejan resultados inciertos.

Alternativas: transacción distribuida, coreografía de muchos eventos, saga orquestada.

Decisión: persistir paso/estado, usar referencias idempotentes y compensaciones; unir cambios locales y outbox en un commit. Consumidores deduplican y efectos externos soportan repetición.

Consecuencias: consistencia eventual y operación de excepciones explícita. No se promete exactly-once. Un timeout no se traduce en rechazo de pago. Un reembolso fallido queda pendiente.

Validación: claves concurrentes, payload distinto, reinicio después de enviar y antes de marcar, evento duplicado y conciliación de estado desconocido.
