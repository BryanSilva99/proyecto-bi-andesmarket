# Guion breve de sustentacion

## 1. Apertura

El proyecto presenta una solucion integral de Inteligencia de Negocios para AndesMarket S.A.C., empresa ficticia de retail omnicanal. El objetivo fue pasar de datos sinteticos con problemas de calidad a un datamart, tableros Power BI y modelos analiticos para apoyar decisiones.

## 2. Datos y ETL

- Datos sinteticos generados con semilla 42.
- Tablas: clientes, productos, tiendas, tiempo, promociones y ventas.
- Problemas de calidad introducidos: nulos, duplicados, fechas mixtas, categorias inconsistentes, outliers y claves huerfanas.
- El ETL limpia datos y deja `fact_ventas` sin nulos, duplicados ni claves huerfanas.

## 3. Datamart y Power BI

- Modelo estrella.
- Grano: linea de venta.
- Dimensiones: Cliente, Producto, Tienda, Tiempo y Promocion.
- Power BI tiene paginas de ventas, categorias, region, tiempo y modelos analiticos.

## 4. Visualizacion

- Categoria lider: Bebidas.
- Mes fuerte: julio de 2025.
- Lima concentra mayor aporte.
- El canal online tiene menor participacion, pero se analiza como canal diferenciado.

## 5. Clasificacion

- Objetivo: predecir abandono.
- Se uso ventana temporal para evitar fuga de informacion.
- Modelos comparados: Regresion Logistica, Arbol de Decision y Random Forest.
- Resultado exportado a Power BI como riesgo bajo, medio y alto.

## 6. Segmentacion

- Variables RFM: recencia, frecuencia y monto.
- K-Means con cuatro segmentos.
- Segmentos: Campeones, Leales de valor, Ocasionales y En riesgo.
- Cada segmento tiene estrategia comercial diferenciada.

## 7. Asociacion

- Metodo Apriori.
- Transacciones por boleta.
- Reglas con soporte, confianza y lift.
- Reglas destacadas: Congelados -> Carnes, Panaderia -> Lacteos, Abarrotes -> Limpieza, Snacks -> Bebidas.

## 8. Regresion

- Objetivo: pronosticar ventas diarias.
- Validacion temporal.
- Mejor modelo: Regresion Lineal.
- MAPE aproximado: 7.48%.
- Se exporto real vs pronostico y 30 dias futuros.

## 9. Cierre

La solucion demuestra el flujo completo de BI: generacion de datos, ETL, datamart, visualizacion, mineria de datos, Power BI y comunicacion de recomendaciones. Todo es reproducible mediante notebooks y archivos CSV.

