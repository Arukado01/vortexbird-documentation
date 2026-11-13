# Diagramas editables

Los diez archivos `.mmd` son fuentes Mermaid editables. Las imágenes en `rendered/` son representaciones de esas relaciones para el PDF. El diagrama 02 describe el objetivo AWS no desplegado. El 06 muestra el checkout sandbox implementado, pero no una sesión externa verificada. Los diagramas 05 y 08 muestran creación de orden y estados; el simulador sigue habilitado por defecto. El modelo 10 es lógico, no un DDL exhaustivo: las referencias de inbox a pago no implican una FK antes de recibir evidencia del proveedor. El diagrama 03 muestra dependencias de código. Consultar `implementation-status.md` para pruebas ejecutadas.

1. Arquitectura general.
2. Despliegue AWS objetivo.
3. Dependencias Clean Architecture.
4. Adaptadores ERP/WMS/OMS/CRM.
5. Secuencia de orden.
6. Checkout sandbox opcional, inbox, conciliación y compensación.
7. OIDC y autorización contextual.
8. Saga y compensaciones.
9. Outbox, consumo y DLQ.
10. Modelo relacional lógico.

No se usan diagramas para afirmar que un componente ya está desplegado. La coherencia se revisa contra código y evidencia de ejecución.
