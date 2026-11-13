# ADR 0007 - Checkout durable y conciliación autoritativa

Estado: implementado y probado por reglas/transporte controlado; sesión externa y saga sobre PostgreSQL pendientes. Fecha: 2026-11-13.

Contexto: perder la respuesta de creación de checkout no significa que el proveedor no lo creó. Un webhook firmado o retorno del navegador tampoco acredita por sí solo que el pago corresponda a la orden.

Decisión: mantener Simulator por defecto. El gateway sandbox requiere activación explícita y verifica vendedor test_user. Persistir intención/lease y referencia antes del POST. Ante incertidumbre, buscar/verificar por referencia sin repetir creación automáticamente. Guardar inbox después de validar manifest HMAC canónico; el worker consulta el pago autoritativo y verifica live_mode=false, vendedor, referencia, importe y COP antes de aplicar transición.

Compensación: registrar cada pago por separado. Aprobación tardía o duplicada agenda reembolso con clave estable y lectura posterior. Solo refunded confirma compensación. Antes del despacho se restituye inventario una vez; después requiere revisión, sin reposición automática. Estados antiguos no degradan una aprobación ni revierten un reembolso.

Alternativas: confiar en frontend/webhook (rechazada), recobrar/recrear ante timeout (rechazada), conciliación durable con referencias estables (elegida). Se usa Checkout Pro Preferences para el checkout alojado; revisar Orders API y disponibilidad regional antes de producción.

Consecuencias: existen estados unknown/refund_pending/manual_review y operación de excepciones. Las credenciales/HTTPS y pruebas externas no se inventan. Los 61 controles aislados acreditan reglas y transporte controlado, no integración productiva.
