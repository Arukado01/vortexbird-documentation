# Operación y continuidad

En este equipo se comprobó SQL desde Windows antes de que fallara Keycloak. El lanzador prepara ahora una copia optimizada desde el ZIP local verificado y conserva el realm. La siguiente ejecución archiva el resumen anterior en `.work/native-runtime/history/`. Para comprobar el resultado actual, revisa la fecha, `checks`, `liveTests` y `businessTests` en `.work/native-runtime/continuation-result.json`. [Procedimiento de ejecución local](../vortexbird-infrastructure/native-continuation.md).

Estado del 17-Nov-2026: procedimientos preparados; plataforma conectada no acreditada por bloqueo de loopback. La continuación vigente se registra en [FINAL_EXECUTION_CHECKLIST.md](../FINAL_EXECUTION_CHECKLIST.md).

## Inicio y detención principal

Desde la carpeta que reúne los cuatro repositorios, usar `Iniciar-VortexBird.cmd`. Requiere Docker Desktop accesible, conserva `.env` y volúmenes y comprueba las dependencias. `Detener-VortexBird.cmd` detiene sin borrar datos.

Desde `vortexbird-infrastructure`:

```powershell
docker compose config --quiet
docker compose up --build -d
docker compose ps
docker compose logs --tail 150 backend frontend keycloak postgres redis
docker compose down
```

Confirmar nombres reales de servicios con `docker compose config --services` si se utilizan overlays. No emplear `down -v` para una detención ordinaria.

## Alternativa nativa

Los scripts `scripts/Start-Native.ps1` y `scripts/Stop-Native.ps1` coordinan la alternativa local. Identidad y mensajería tienen scripts propios `Start-KeycloakNative.ps1` y `Start-Native-Messaging.ps1`. Leer parámetros y prerequisitos en el README de infraestructura. No ejecutar varios launchers simultáneos sobre los mismos puertos.

El arranque de un proceso no basta: comprobar readiness, API por HTTP, frontend, descubrimiento OIDC, persistencia y consumo de mensajes. Si aparece `Permission denied` o socket `10013`, conservar logs y ejecutar el procedimiento desde una sesión autorizada que permita loopback. No cambiar permisos o firewall automáticamente.

## Verificación

Para retomar una sola vez desde una sesión normal, ejecutar `.\Continuar-VortexBird.cmd -RunLiveTests -RunBusinessTests` en la raíz con PowerShell 7.4 o posterior. El procedimiento usa OIDC, conserva `.env`, no eleva privilegios y escribe diagnóstico/resultados en `.work/native-runtime/`. Consultar [native-continuation.md](../vortexbird-infrastructure/native-continuation.md). Tras readiness intenta ambas suites independientemente: autenticación/lectura y negocio con API temporal sobre una base nueva `vortexbird_acceptance_*`, conservada al terminar, sin usar la base de plataforma. Proveedores y pagos de negocio son simulados. Reservar 6-8 minutos para autenticación por el TTL, más arranque y negocio. Conserva servicios y registra conteos nuevos, errores y omisiones explícitos. ValidateOnly solo acredita preparación; Redis nativo queda deshabilitado si falta su ejecutable. Estas suites no completan toda la aceptación operativa.

Ejecutar `verify.ps1` para controles locales y su opción `-IncludeApi` solo después de confirmar servicios accesibles. Repetir `vortexbird-backend/tests/Integration.ps1` contra una base de prueba aislada. Usar exclusivamente datos sintéticos y pagos simulados o Sandbox.

## Operación diaria

- Revisar readiness, errores, retraso de outbox y DLQ antes de aceptar tráfico.
- Consultar historial de orden y correlation-id antes de reintentar o compensar.
- Ante pago incierto, conciliar por referencia; no crear otro cobro para resolver incertidumbre.
- Aplicar redrive tras corregir la causa y verificar idempotencia del consumidor.
- Conservar backups y ensayar restauración antes de producción.
- Revisar costos y retención de logs en el piloto autorizado. Detener tareas no elimina todos los costos de red o base de datos.

## Reanudar AWS

Primero cerrar aceptación local. Después verificar identidad AWS, región, estado remoto, dependencias TLS/IdP, secretos y plan Terraform. Presentar inventario y costo para una aprobación concreta. Aplicar solo recursos autorizados. Verificar imágenes por digest, migraciones, salud, smoke y rollback. Registrar endpoints reales únicamente tras comprobarlos.

El inventario del 17-Nov ya consultó Ohio sin modificar recursos; no se observó despliegue VortexBird. Consultar `../qa/aws-readonly-inventory-2026-11-17.json` y [costs-and-approval.md](../vortexbird-infrastructure/costs-and-approval.md). Los recursos ajenos no están autorizados para reutilizar y los presupuestos de la cuenta no equivalen a aprobación de este despliegue.

La identidad propia se prepara con [identity-aws.md](../vortexbird-infrastructure/terraform-ecs/identity-aws.md). Por defecto no crea recursos. Habilitar infraestructura, cargar secretos y habilitar servicio son etapas separadas sujetas al plan aprobado. Usar hostname/zona explícitos, esquema de identidad independiente, imagen por digest y administrador temporal separado; retirar el bootstrap tras crear la administración permanente. Nunca inyectar el secreto maestro RDS en Keycloak.

## Cambios de esta continuación

Se añadieron el launcher único de reanudación, inventario/costos regionales y configuración opt-in de identidad; migración aislada y release ECS se documentan progresivamente en el informe raíz. PDF/PPT permanecen en la revisión previa hasta cumplir las puertas local y AWS. Ninguno de estos procedimientos constituye evidencia de ejecución remota.
