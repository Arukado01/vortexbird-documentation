# ADR 0003 - Keycloak y permisos de negocio

Estado: aceptado como diseño; validar integración OIDC desplegada. Fecha: 2026-11-13.

Contexto: sesión/credenciales y autorización de negocio cambian a ritmos distintos.

Alternativas: identidad propia, permisos estáticos en frontend, IdP OIDC más RBAC dinámico backend.

Decisión: Keycloak con Code+PKCE para portal y client credentials para partners. API valida JWT y consulta permisos/contexto. Roles dinámicos se guardan en aplicación. Ruta demo solo con Development explícito.

Consecuencias: no duplicar contraseñas ni refresh tokens si el IdP es propietario. Requiere mapeo de subject, invalidación de permisos y configuración de issuer/audience correcta. Rotación y recuperación de cuenta deben probarse contra el IdP.

Validación: token expirado/issuer/audience incorrecto, permiso revocado, tenant cruzado, registro/recuperación con SMTP de prueba.
