# ADR 0009 - ECS Fargate para el piloto

Adoptado el 17 de noviembre de 2026. Terraform y dos escenarios de plan simulado validados. El despliegue requiere plan regional, costo, dependencias y aprobación.

El piloto usa tres servicios ECS Fargate. El ALB enruta hacia el frontend y la API. El worker procesa outbox e inbox y utiliza el mismo digest de backend con workers habilitados. Las tareas privadas escalan independientemente. RDS es la fuente transaccional y Redis TLS es opcional. Keycloak se opera como dependencia externa.

Cada tarea tiene un Task Role y un Execution Role distinto. El worker opera sobre la cola de eventos. El Execution Role inyecta su propio secreto y permite lectura de imagen y escritura de logs. El redrive AWS queda bajo un rol operativo. GitHub Actions usa OIDC y una raíz de estado independiente para ECS.

EKS conserva infraestructura, manifests y workflows con su modelo Pod Identity e IRSA. Reevaluar esa alternativa si AndesRetail requiere controladores Kubernetes propios, una plataforma compartida o portabilidad entre clústeres.

[Roles IAM de ECS](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-iam-role-overview.html)
