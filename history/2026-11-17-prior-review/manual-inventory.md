# Inventario de manuales públicos

Revisión del 17 de noviembre de 2026. Las audiencias orientan la búsqueda. Los permisos de esta tabla habilitan las operaciones del workspace.

| Identificador | Manual y módulo | Ruta pública | Audiencia | Permisos de operación | Versión | Fecha | Validación |
| --- | --- | --- | --- | --- | --- | --- | --- |
| acceso | Acceso a la plataforma | /help/acceso | Visitante, Usuario estándar, Administrador, Administrador de partners, Operador | Acceso según IdP | 1.1.0 | 2026-11-17 | Playwright, lectura y recarga sin sesión |
| dashboard | Dashboard | /help/dashboard | Usuario estándar, Administrador, Administrador de partners, Operador | dashboard.read | 1.1.0 | 2026-11-17 | Playwright, lectura y recarga sin sesión |
| usuarios-permisos | Usuarios, roles y permisos | /help/usuarios-permisos | Administrador, Administrador de partners | roles.read, users.read, users.update | 1.1.0 | 2026-11-17 | Playwright, lectura y recarga sin sesión |
| partners-canales | Partners y canales | /help/partners-canales | Administrador, Administrador de partners | channels.read, partners.read | 1.1.0 | 2026-11-17 | Playwright, lectura y recarga sin sesión |
| catalogo-inventario-precios | Catálogo, inventario y precios | /help/catalogo-inventario-precios | Usuario estándar, Administrador, Administrador de partners, Operador | inventory.read, pricing.read, products.read | 1.1.0 | 2026-11-17 | Playwright, lectura y recarga sin sesión |
| ordenes | Gestión de órdenes | /help/ordenes | Usuario estándar, Administrador, Administrador de partners, Operador | orders.create, orders.read | 1.1.0 | 2026-11-17 | Playwright, lectura y recarga sin sesión |
| pagos | Pagos y conciliación | /help/pagos | Administrador, Administrador de partners, Operador | payments.manage, payments.read | 1.1.0 | 2026-11-17 | Playwright, lectura y recarga sin sesión |
| eventos-webhooks | Eventos y webhooks | /help/eventos-webhooks | Administrador, Administrador de partners, Operador | events.read, webhooks.read | 1.1.0 | 2026-11-17 | Playwright, lectura y recarga sin sesión |
| auditoria | Auditoría y Activity Log | /help/auditoria | Administrador, Administrador de partners, Operador | activity_logs.read | 1.1.0 | 2026-11-17 | Playwright, lectura y recarga sin sesión |
| integraciones-configuracion | Integraciones y configuración | /help/integraciones-configuracion | Administrador, Operador | integrations.read, settings.read | 1.1.0 | 2026-11-17 | Playwright, lectura y recarga sin sesión |
| reportes | Reportes de órdenes | /help/reportes | Usuario estándar, Administrador, Administrador de partners, Operador | reports.read | 1.1.0 | 2026-11-17 | Playwright, lectura y recarga sin sesión |

Los primeros diez registros corresponden a los diez grupos del alcance. Reportes reúne las consultas y la exportación por período.

Fuente de versión y pasos en los JSON del frontend. Pruebas en e2e/help.spec.ts. Los permisos de los endpoints se aplican en la API.
