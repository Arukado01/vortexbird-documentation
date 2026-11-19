# VortexBird - documentación de entrega

Revisión integral del 17-Nov-2026. **Validación parcial: servicios conectados y AWS pendientes.**

| Archivo | Uso |
| --- | --- |
| `implementation-status.md` | Estado vigente, evidencia y límites |
| `audit-matrix.md` | Componente, defecto, acción y prueba |
| `acceptance-checklist.md` | Criterios por fase del nuevo encargo |
| `closure-report.md` | Comandos, resultados y pendientes concretos |
| `operation-runbook.md` | Arranque, detención, diagnóstico y reanudación |
| `manual-inventory.md` | Once guías vivas y versiones actuales |
| `vortexbird-architecture-assessment.md` | Assessment técnico completo de nueve secciones |
| `output/pdf/vortexbird-architecture-assessment.pdf` | PDF rediseñado con índice y atlas vectorial |
| `output/presentation/VortexBird_AndesRetail_Executive.pptx` | Presentación ejecutiva con notas |
| `diagrams/vector/` | Catorce SVG y manifiesto |
| `execution-evidence.json` | Datos de resultados y capturas para los artefactos |
| `history/` | Evidencia anterior, conservada con fecha |

## Generación reproducible

Python 3.12 con ReportLab, pypdf y Pillow:

```powershell
python scripts/vector_atlas.py
python scripts/build_professional_pdf.py
python scripts/validate_docs.py
```

Usar `scripts/build_presentation.mjs` y el runtime de `@oai/artifact-tool` para el PowerPoint. Las rutas específicas del runtime pueden variar por instalación. Renderizar salidas y revisar texto, tamaños, tablas y diagramas antes de entregar.

Los diagramas vectoriales son la edición actual. Mermaid y PNG anteriores se conservan como fuentes históricas auxiliares; su cantidad no acredita el nuevo alcance. ECS Fargate es el destino inicial y EKS una alternativa. Ningún artefacto presenta una simulación como integración real ni un diseño AWS como despliegue.
