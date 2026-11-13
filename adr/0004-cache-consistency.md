# ADR 0004 - Proyecciones y caché con frescura explícita

Estado: aceptado como estrategia; TTL por validar con negocio. Fecha: 2026-11-13.

Contexto: picos 10x no deben transferirse al ERP/WMS.

Decisión: consultas desde proyecciones y Redis; claves con partner/canal/tienda/SKU y cliente cuando aplique. Stock 15 s, precio60 s como iniciales. Reserva autoritativa decide la venta.

Alternativas: consultar siempre legados (latencia/acoplamiento), caché ilimitada (sobreventa), CQRS con proyecciones y límites de frescura.

Consecuencias: resultados pueden quedar desactualizados dentro de tolerancia acordada. Redis no es autoridad. Al fallar, fallback limitado a proyección; fuera de frescura se devuelve503.

Validación: invalidez tras reserva, colisión entre tenants, stampede y caída Redis bajo carga.
