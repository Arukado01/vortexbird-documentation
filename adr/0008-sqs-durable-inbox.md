# ADR 0008 - SQS opcional y consumidor con inbox durable

Estado: implementado; 20 controles de orquestación y nueve del pipeline aprobados; ejecución externa pendiente. Fecha: 2026-11-13.

Contexto: el outbox local demuestra persistencia y reintento, pero AWS necesita transporte y acuse reales. Los duplicados y timeouts ambiguos exigen idempotencia del consumidor y protección contra workers con lease vencido.

Decisión: conservar local como predeterminado y seleccionar SQS por configuración. El cliente usa marshalling JSON propio y el pipeline oficial AWSSDK.Core para credenciales, firma SigV4, HTTP y retry; no afirmar que está instalado AWSSDK.SQS generado. Publicar solo eventos del propio outbox y validar origen, partner y fingerprint antes de reclamar inbox. Handler idempotente, finalización condicionada al lease y DeleteMessage solo después de finalización durable.

Alternativas: paquete generado SQS (preferible si está disponible y validado), HTTP firmado manualmente (rechazado), transporte local únicamente (insuficiente para la ruta AWS). La dependencia Core disponible permite reutilizar el mecanismo de firma/credenciales oficial, con marshalling limitado y pruebas de protocolo.

Consecuencias: el consumidor depende del outbox canónico en la misma persistencia; no es un bus abierto a productores arbitrarios. Un crash después del efecto y antes de completar inbox puede repetir el handler. Se procesa un mensaje por reclamación/recepción para acotar leases; capacidad de alto volumen no demostrada. Visibility120s y deadline menor, sin renovación periódica declarada. Mensajes venenosos quedan para redrive/DLQ.

Identidad: el despliegue backend usa EKS Pod Identity y cadena de credenciales del SDK; Keycloak y CNI conservan IRSA. El emulador HTTP solo se permite en Development con destino local autorizado y credenciales dummy. Ninguno de estos archivos acredita un despliegue o prueba AWS.

Validación requerida: firmas y marshalling del pipeline, acuse después de finalización, duplicados, lease perdido, fallo de envío ambiguo, reinicios y redrive. Las pruebas controladas deben distinguirse de las sesiones PostgreSQL, ElasticMQ y AWS reales.
