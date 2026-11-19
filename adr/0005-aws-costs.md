# ADR 0005 - AWS declarativo y separación de perfiles

La decisión inicial de despliegue se actualizó en [ADR 0009](0009-ecs-fargate-pilot.md). Este registro conserva el contexto de la alternativa EKS.

Estado: propuesta preparada, sin autorización de provisión. Fecha: 2026-11-13.

Contexto: el usuario propone AWS/EKS, región inicial us-east-2, y exige aprobación antes de crear recursos facturables.

Decisión: Terraform describe nuevos recursos aislados; demo y producción difieren en HA/capacidad. Compose permite desarrollar localmente. Revisar inventario, plan y costo antes de apply; no destruir recursos existentes.

Alternativas: EKS completo, cómputo administrado más simple, solo demo local. EKS ofrece estándares Kubernetes pero agrega costo y operación.

Consecuencias: RDS Multi-AZ, NAT, Redis y control plane tienen costo fijo aun sin tráfico. Dominio, certificados, secretos y rol OIDC no se inventan. Conectividad bloqueada no se resuelve simulando un despliegue.

Validación: fmt/validate/plan y escaneo, revisión de permisos, presupuesto aprobado, despliegue y smoke test posteriores. Ver estimación actual en infraestructura.
