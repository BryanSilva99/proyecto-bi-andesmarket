# Bitacora de trabajo

> Version base editable. El estudiante puede ajustar la redaccion final con sus propias palabras antes de la entrega.

| Etapa | Actividad realizada | Evidencia | Tiempo estimado | Observaciones |
|---|---|---|---:|---|
| Planificacion | Revision de instrucciones, rubrica, entregables y estructura esperada del proyecto. | `README.md`, estructura de carpetas | 1 h | Se adopto el caso AndesMarket S.A.C. recomendado por la guia. |
| Datos sinteticos | Definicion de dimensiones, tabla de hechos, volumenes, reglas de realismo y problemas de calidad. | `notebooks/00_generacion_datos.ipynb`, `data/raw/` | 2 h | Se uso semilla fija 42 para reproducibilidad. |
| Generacion de datos | Ejecucion del notebook de generacion y validacion de archivos crudos. | `data/raw/*.csv`, `data/raw/resumen_calidad_inicial.csv` | 1 h | Los datos crudos incluyen nulos, duplicados, fechas mixtas, outliers y claves huerfanas. |
| ETL y calidad | Limpieza de datos, normalizacion de categorias, parseo de fechas, eliminacion de duplicados y validacion referencial. | `notebooks/01_datamart_etl.ipynb`, `data/processed/` | 3 h | El resultado procesado queda sin nulos, duplicados ni claves huerfanas. |
| Datamart | Construccion de tablas limpias para modelo estrella y calculo de metricas derivadas. | `data/processed/fact_ventas.csv`, dimensiones procesadas | 2 h | El grano definido es linea de venta. |
| Documentacion tecnica | Elaboracion inicial de README, diccionario de datos y registro de prompts. | `README.md`, `data/processed/diccionario_datos.csv`, `prompts/registro_prompts.md` | 1 h | La documentacion se ira ampliando con cada parte. |
| Visualizacion | Desarrollo de graficos e insights en Python. | `notebooks/02_visualizacion.ipynb` | Pendiente | Se completara antes de construir el tablero en Power BI. |
| Power BI | Carga del datamart, relaciones, medidas DAX y paginas del tablero. | `powerbi/AndesMarket.pbix` | Pendiente | Se realizara en maquina virtual con Power BI Desktop. |
| Clasificacion | Construccion de tabla analitica de clientes, comparacion de modelos y exportacion de predicciones de abandono. | `notebooks/03_clasificacion.ipynb`, `data/processed/predicciones_abandono.csv` | 3 h | Se uso una ventana temporal para evitar fuga de informacion y se compararon Regresion Logistica, Arbol de Decision y Random Forest. |
| Segmentacion | Calculo de variables RFM, seleccion de k con codo/silueta, K-Means y exportacion de segmentos. | `notebooks/04_segmentacion.ipynb`, `data/processed/segmentos_clientes.csv` | 3 h | Se uso transformacion logaritmica para reducir efecto de outliers y obtener segmentos accionables. |
| Asociacion | Reglas de asociacion para canasta de mercado. | `notebooks/05_asociacion.ipynb` | Pendiente | Se filtraran reglas relevantes por confianza y lift. |
| Regresion | Pronostico de ventas/demanda y exportacion de real vs pronostico. | `notebooks/06_regresion.ipynb` | Pendiente | Se respetara el orden temporal en la validacion. |
| Informe final | Consolidacion de resultados, conclusiones, etica y anexos. | `informe/Informe_PG_AndesMarket.pdf` | Pendiente | Se completara al terminar notebooks y Power BI. |
