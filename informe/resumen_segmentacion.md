# Resumen de segmentacion RFM

- Fecha de referencia: 2025-12-30.
- Variables de clustering: log(recencia + 1), log(frecuencia + 1) y log(monto + 1), escaladas con StandardScaler.
- Numero de clusters elegido: 4.

## Perfil y estrategias

- **Campeones**: 620 clientes, monto total S/ 1,491,003, recencia promedio 23.2 dias. Estrategia: Mantener beneficios exclusivos, acceso anticipado a promociones y seguimiento de satisfaccion.
- **Leales de valor**: 1815 clientes, monto total S/ 727,873, recencia promedio 139.6 dias. Estrategia: Impulsar venta cruzada y paquetes premium para aumentar frecuencia sin sacrificar margen.
- **Ocasionales**: 1176 clientes, monto total S/ 446,710, recencia promedio 15.0 dias. Estrategia: Activar campañas de recurrencia con cupones moderados y recomendaciones por categoria.
- **En riesgo**: 1344 clientes, monto total S/ 154,460, recencia promedio 244.0 dias. Estrategia: Ejecutar acciones de recuperacion con ofertas personalizadas y comunicacion directa.
