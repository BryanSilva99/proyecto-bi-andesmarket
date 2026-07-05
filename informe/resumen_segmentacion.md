# Resumen de segmentacion RFM

- Fecha de referencia: 2025-12-30.
- Variables de clustering: log(recencia + 1), log(frecuencia + 1) y log(monto + 1), escaladas con StandardScaler.
- Numero de clusters elegido: 4.

## Perfil y estrategias

- **Campeones**: 612 clientes, monto total S/ 1,363,762, recencia promedio 23.3 dias. Estrategia: Mantener beneficios exclusivos, acceso anticipado a promociones y seguimiento de satisfaccion.
- **Leales de valor**: 1784 clientes, monto total S/ 663,736, recencia promedio 143.2 dias. Estrategia: Impulsar venta cruzada y paquetes premium para aumentar frecuencia sin sacrificar margen.
- **Ocasionales**: 1159 clientes, monto total S/ 404,453, recencia promedio 14.9 dias. Estrategia: Activar campañas de recurrencia con cupones moderados y recomendaciones por categoria.
- **En riesgo**: 1400 clientes, monto total S/ 149,369, recencia promedio 237.7 dias. Estrategia: Ejecutar acciones de recuperacion con ofertas personalizadas y comunicacion directa.
