# Informe PG - AndesMarket S.A.C.

## 1. Caratula

**Universidad:** Universidad Nacional Mayor de San Marcos  
**Facultad:** Facultad de Ingenieria de Sistemas e Informatica  
**Escuela:** Ingenieria de Software  
**Asignatura:** Inteligencia de Negocios  
**Proyecto:** Solucion integral de BI para AndesMarket S.A.C.  
**Modalidad:** Individual  
**Estudiante:** [Completar nombres y codigo]  
**Docente:** Mg. Juan Gamarra Moreno

## 2. Resumen ejecutivo

El proyecto desarrolla una solucion integral de Inteligencia de Negocios para AndesMarket S.A.C., empresa ficticia de retail omnicanal en Peru. La solucion cubre generacion de datos sinteticos, limpieza y ETL, construccion de datamart, visualizacion en Power BI y modelos de mineria de datos: clasificacion, segmentacion, asociacion y regresion.

La base analitica se construyo con datos sinteticos reproducibles, generados con semilla fija 42. Los datos crudos incorporan problemas de calidad controlados como fechas mixtas, nulos, duplicados, errores de categoria, outliers y claves huerfanas. El ETL corrige estos problemas y exporta tablas limpias en `data/processed/`.

Los principales resultados son:

- Datamart con esquema estrella a nivel de linea de venta.
- Tablero Power BI con paginas de ventas, categorias, region, tiempo, abandono, segmentacion, canasta de mercado y pronostico.
- Modelo de abandono con Random Forest como uno de los mejores modelos, con recall alto para detectar clientes en riesgo.
- Segmentacion RFM con cuatro segmentos: Campeones, Leales de valor, Ocasionales y En riesgo.
- Reglas de canasta de mercado con lift positivo, destacando combinaciones como Congelados -> Carnes, Panaderia -> Lacteos y Snacks -> Bebidas.
- Pronostico de ventas diarias con Regresion Lineal como mejor modelo, MAPE aproximado de 7.48% y R2 de 0.931.

## 3. Empresa ficticia, problematica y preguntas de negocio

AndesMarket S.A.C. es una cadena ficticia de supermercados con tiendas fisicas y canal online. Cuenta con un programa de fidelizacion llamado AndesPlus. La gerencia busca transformar datos transaccionales dispersos en informacion confiable para tomar decisiones sobre ventas, clientes, promociones e inventario.

Problematica:

- Datos operativos dispersos.
- Fechas y categorias inconsistentes.
- Registros duplicados y valores faltantes.
- Ausencia de un datamart unico.
- Falta de tableros y modelos predictivos para apoyar decisiones.

Preguntas de negocio:

- Como evolucionan ventas y margen por categoria, tienda, canal y periodo?
- Que clientes tienen mayor probabilidad de abandono?
- Que segmentos de clientes existen y que estrategia aplicar a cada uno?
- Que categorias se compran juntas?
- Cual sera la venta esperada para planificar inventario y campanas?

## 4. Generacion de datos sinteticos

La generacion se realizo en `notebooks/00_generacion_datos.ipynb`. Se usaron `pandas`, `numpy` y `faker` con semilla fija 42.

Tablas generadas:

- `dim_cliente`: clientes sinteticos, sexo, fecha de nacimiento, distrito, fecha de alta y segmento AndesPlus.
- `dim_producto`: productos, categoria, subcategoria, marca, precio y costo.
- `dim_tienda`: tiendas fisicas y canal online.
- `dim_tiempo`: calendario de dos anos.
- `dim_promocion`: promociones con fechas y descuentos.
- `fact_ventas`: ventas a nivel de linea de boleta.

Reglas de realismo:

- Estacionalidad en julio y diciembre.
- Concentracion tipo Pareto en productos y clientes.
- Precios derivados de precio lista con variacion controlada.
- Promociones aplicadas segun vigencia.
- Afinidades de canasta entre categorias.
- Clientes con comportamiento de abandono.

Problemas de calidad introducidos:

- Fechas en formatos mixtos.
- Valores faltantes en descuento, distrito y categoria.
- Duplicados en ventas.
- Texto inconsistente en categorias.
- Errores de tipeo.
- Outliers en cantidad y precio.
- Claves huerfanas de producto.

## 5. Parte 1 - Datamart y ETL

El ETL se implemento en `notebooks/01_datamart_etl.ipynb`.

Grano:

- Una linea de venta, es decir, un producto dentro de una boleta.

Modelo dimensional:

- `fact_ventas`
- `dim_cliente`
- `dim_producto`
- `dim_tienda`
- `dim_tiempo`
- `dim_promocion`

Tratamientos aplicados:

- Parseo robusto de fechas.
- Homologacion de categorias.
- Imputacion de nulos.
- Eliminacion de duplicados.
- Validacion de claves huerfanas.
- Tratamiento de outliers.
- Calculo de `importe`, `costo_total` y `margen`.

Resultado de calidad posterior:

- `fact_ventas`: sin nulos, sin duplicados y sin claves huerfanas.
- Dimensiones limpias y listas para Power BI.

## 6. Parte 2 - Visualizacion

La visualizacion en Python se desarrollo en `notebooks/02_visualizacion.ipynb`. Se exportaron graficos a `informe/img/` e insights a `informe/insights_visualizacion.md`.

Hallazgos:

- La categoria con mayor venta es Bebidas.
- El mes de mayor venta es 2025-07.
- El 20% superior de productos concentra una parte importante de ventas.
- Lima es la region con mayor aporte.
- El canal online tiene participacion menor frente al canal fisico.
- El margen bruto global muestra que no todas las decisiones deben basarse solo en volumen.

En Power BI se construyo un tablero con paginas de resumen ejecutivo, categorias/productos, canal/region y tendencia temporal.

## 7. Parte 3 - Clasificacion

La clasificacion se desarrollo en `notebooks/03_clasificacion.ipynb`.

Objetivo:

- Predecir abandono de clientes.

Definicion:

- Se uso una ventana temporal para evitar fuga de informacion. Las variables se calcularon con informacion historica y la etiqueta de abandono se definio segun ausencia de compra en el periodo futuro.

Modelos comparados:

- Regresion Logistica.
- Arbol de Decision.
- Random Forest.

Metricas principales:

- Accuracy.
- Precision.
- Recall.
- F1.
- ROC-AUC.

Salida para Power BI:

- `data/processed/predicciones_abandono.csv`
- `data/processed/metricas_clasificacion.csv`
- `data/processed/importancia_variables_clasificacion.csv`

Acciones recomendadas:

- Priorizar clientes de riesgo alto y alto monto historico.
- Aplicar descuentos selectivos.
- Contactar clientes con alta recencia y baja frecuencia.
- Adaptar acciones por segmento AndesPlus.

## 8. Parte 4 - Segmentacion

La segmentacion se desarrollo en `notebooks/04_segmentacion.ipynb`.

Variables RFM:

- Recencia.
- Frecuencia.
- Monto.

Metodologia:

- Transformacion logaritmica para reducir efecto de outliers.
- Escalamiento con `StandardScaler`.
- Evaluacion de `k` con codo y silueta.
- K-Means con `k = 4`.

Segmentos:

- Campeones.
- Leales de valor.
- Ocasionales.
- En riesgo.

Salida para Power BI:

- `data/processed/segmentos_clientes.csv`
- `data/processed/perfil_segmentos.csv`
- `data/processed/evaluacion_k_segmentacion.csv`

Estrategias:

- Campeones: beneficios exclusivos.
- Leales de valor: venta cruzada y paquetes premium.
- Ocasionales: campanas de recurrencia.
- En riesgo: recuperacion con ofertas personalizadas.

## 9. Parte 5 - Asociacion

La asociacion se desarrollo en `notebooks/05_asociacion.ipynb`.

Objetivo:

- Identificar categorias que se compran juntas y proponer promociones cruzadas.

Metodo:

- Transacciones por boleta.
- One-hot encoding.
- Algoritmo Apriori.
- Reglas con soporte, confianza y lift.
- Filtro de reglas con `lift > 1`.

Reglas destacadas:

- Congelados -> Carnes.
- Carnes -> Congelados.
- Panaderia -> Lacteos.
- Lacteos -> Panaderia.
- Abarrotes -> Limpieza.
- Snacks -> Bebidas.

Salida para Power BI:

- `data/processed/reglas_asociacion.csv`
- `data/processed/itemsets_frecuentes.csv`
- `data/processed/resumen_transacciones_asociacion.csv`

Acciones:

- Promociones cruzadas.
- Exhibicion conjunta.
- Cupones por compra complementaria.
- Recomendaciones online.

## 10. Parte 6 - Regresion

La regresion se desarrollo en `notebooks/06_regresion.ipynb`.

Objetivo:

- Pronosticar ventas diarias agregadas.

Features:

- Variables temporales.
- Indicador de meses altos.
- Promociones.
- Rezagos.
- Promedios moviles.

Validacion:

- Division temporal 80% entrenamiento y 20% prueba.

Modelos comparados:

- Regresion Lineal.
- Random Forest.
- Gradient Boosting.

Mejor resultado:

- Regresion Lineal.
- MAE: 246.01.
- RMSE: 316.41.
- MAPE: 7.48%.
- R2: 0.931.

Salida para Power BI:

- `data/processed/pronostico_ventas.csv`
- `data/processed/metricas_regresion.csv`

Uso de negocio:

- Planificacion de inventario.
- Programacion de campanas.
- Seguimiento de desviaciones entre real y pronostico.

## 11. Power BI

Archivo:

- `powerbi/AndesMarket.pbix`

Paginas implementadas:

1. Resumen Ejecutivo.
2. Categorias y Productos.
3. Canal y Region.
4. Tendencia Temporal.
5. Riesgo de abandono.
6. Segmentacion de clientes.
7. Canasta de mercado.
8. Pronostico de demanda.

## 12. Uso de IA, etica e integridad

Se uso IA como apoyo para estructurar el proyecto, validar enfoques, generar codigo base y documentar decisiones. Los prompts relevantes se registraron en `prompts/registro_prompts.md`.

El estudiante reviso, ejecuto y ajusto los resultados. Los datos son sinteticos y no corresponden a personas ni empresas reales. La solucion evita uso de datos personales reales y permite reflexionar sobre privacidad, sesgo y uso responsable de modelos predictivos.

Consideraciones eticas:

- No usar datos reales de clientes.
- Evitar decisiones automaticas sin revision humana.
- Usar modelos como apoyo y no como unica fuente de decision.
- Revisar sesgos por segmento, canal o ubicacion.
- Informar limitaciones de datos sinteticos y modelos.

## 13. Conclusiones

- Se construyo una solucion BI integral y reproducible para AndesMarket.
- El datamart permite analizar ventas, margen, categorias, tiendas, canal y tiempo.
- Los modelos de mineria aportan valor adicional para retencion, segmentacion, promociones cruzadas y pronostico.
- Power BI consolida la informacion en paginas orientadas a decision gerencial.
- La solucion es extensible: podria incorporar datos reales anonimizados, mas historico y automatizacion de refresh.

## 14. Recomendaciones

- Revisar semanalmente clientes en riesgo alto.
- Usar segmentos RFM para disenar campanas diferenciadas.
- Aplicar reglas de asociacion en promociones cruzadas y ubicacion de productos.
- Monitorear error del pronostico y recalibrar modelos con nuevos datos.
- Mantener un proceso ETL reproducible y documentado.

