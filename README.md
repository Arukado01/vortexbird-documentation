# VortexBird - documentación

Repositorio independiente de documentación para la plataforma de interoperabilidad de AndesRetail.

- `vortexbird-architecture-assessment.md`: documento principal en los nueve apartados exigidos.
- `output/pdf/vortexbird-architecture-assessment.pdf`: versión maquetada del assessment.
- `diagrams/`: diez diagramas editables Mermaid y representaciones para el PDF.
- `adr/`: decisiones, alternativas y consecuencias.
- `presentation-guide.md`: recorrido de demo, preguntas y defensa de decisiones.
- `implementation-status.md`: estado observado y límites de verificación.
- `acceptance-checklist.md`: cada criterio del texto pegado, su estado y evidencia.
- El assessment distingue simulador predeterminado, checkout sandbox y SQS implementados con pruebas controladas, cuotas PostgreSQL compartidas y las ejecuciones externas todavía pendientes.
- `scripts/build_pdf.py`: construcción reproducible del PDF con ReportLab.
- `scripts/validate_docs.py`: comprobación estructural de entregables.

## Validación

Documento de nueve secciones, PDF de 20 páginas revisado visualmente, diez diagramas y ocho ADR. La corrida integral aprobó 268 controles de aplicación/frontend; SQL45 e infraestructura34+6 se registran por separado. Consultar `implementation-status.md` y `../qa/verification-summary.json` para alcances y limitaciones.

```powershell
python scripts/validate_docs.py
python scripts/build_pdf.py
```

Dependencias de generación: Python 3.12+, reportlab, Pillow y pypdf. Renderizar el PDF con Poppler (`pdftoppm -png`) y revisar las páginas antes de publicar. La compilación del PDF no valida por sí sola el contenido arquitectónico.

## Convenciones y mantenimiento

Ramas `main`, `develop`, `feature/*`, `fix/*` y `hotfix/*`. Conventional Commits: `docs:`, `fix:`, `chore:`. Una decisión importante añade o reemplaza un ADR conservando historia; el código y las pruebas mandan sobre la documentación de estado. Todo PR debe revisar contratos, diagramas, límites operativos y evidencia afectada.

La documentación pertenece a este repositorio; no contiene secretos ni credenciales. Los recursos AWS son objetivos o IaC preparada, no evidencia de despliegue. Ver los README hermanos de backend, frontend e infraestructura para ejecución.
