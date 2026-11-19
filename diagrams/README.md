# Diagramas editables

## Atlas vectorial vigente

La entrega del 17-Nov-2026 incorpora catorce SVG en `vector/`, generados por `../scripts/vector_atlas.py`. `vector/manifest.json` registra número, título, estado y explicación. El PDF incluye una página horizontal por figura, con texto y conectores vectoriales.

Los temas actuales son: arquitectura general, AWS, autenticación, integraciones empresariales, pedidos, pagos, saga, outbox/inbox, SQS/DLQ, seguridad IAM, observabilidad, CI/CD, documentación viva y proceso de despliegue. Las figuras indican implementación, simulación o diseño objetivo; AWS sigue sin desplegar.

## Fuentes de la revisión anterior

Las 14 fuentes Mermaid se editan en esta carpeta y `rendered/` contiene sus imágenes para el assessment. El diagrama 02 representa la IaC de ECS Fargate. La vista EKS histórica se conserva en `alternatives/`. Los diagramas representan diseño y código. [Estado de implementación](../implementation-status.md) acompaña cada validación.

1. Arquitectura general.
2. Despliegue objetivo ECS Fargate.
3. Dependencias Clean Architecture.
4. Adaptadores ERP/WMS/OMS/CRM.
5. Secuencia de orden.
6. Checkout sandbox opcional, inbox, conciliación y compensación.
7. OIDC y autorización contextual.
8. Saga y compensaciones.
9. AWS SDK para SQS, outbox, inbox y DLQ.
10. Modelo relacional lógico.
11. Centro de ayuda público y contextual.
12. Identidad ECS y separación de permisos.
13. Documentación viva y criterios de revisión.
14. Integración y entrega con plan ECS revisable.

No se usan diagramas para afirmar que un componente ya está desplegado. La coherencia se revisa contra código y evidencia de ejecución.
