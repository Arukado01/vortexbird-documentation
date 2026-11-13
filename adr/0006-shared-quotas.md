# ADR 0006 - Cuotas de partner y canal compartidas en PostgreSQL

Estado: implementado; concurrencia multirréplica y costo bajo carga pendientes de medición. Fecha: 2026-11-13.

Contexto: un contador en memoria permite multiplicar el presupuesto al escalar réplicas. Además, elegir un canal mediante una cabecera ignorada por el endpoint puede reducir indebidamente el presupuesto que consume una consulta agregada.

Decisión: resolver partner/canal desde identidad y recurso autorizado; consumir presupuesto de partner y canales realmente alcanzados. En agregados se consumen todos los canales autorizados. El store PostgreSQL toma advisory lock por partner, usa clock_timestamp de DB y verifica todos los límites antes de UPSERT en una transacción. Ventanas fijas de un minuto; 429 incluye segundos hasta el cierre. Error DB no habilita un fallback ilimitado.

Alternativas: limitador por proceso (insuficiente entre réplicas), Redis/Lua (menor costo potencial pero otra autoridad operativa), gateway con estado compartido (válido si demuestra políticas por objeto/canal). PostgreSQL reutiliza persistencia durable y permite demostrar atomicidad.

Consecuencias: una transacción adicional por petición y serialización dentro del partner; una ráfaga puede cruzar el borde de ventana. No afirmar p95 ni capacidad 10x sin medir contención. Token bucket o Redis pueden reemplazar el store detrás del puerto si la carga lo justifica.

Evidencia: 17 controles de planner/parser y siete comprobaciones SQL del UPSERT, aislamiento y rollback en una sesión PostgreSQL WASM. No equivalen a carreras Npgsql ni failover.
