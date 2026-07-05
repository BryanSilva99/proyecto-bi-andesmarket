# Registro de prompts

| N | Parte | Objetivo del prompt | Herramienta / Modelo | Resultado / Uso | Ajustes del equipo |
|---|---|---|---|---|---|
| 1 | Datos | Disenar el caso de negocio y el modelo dimensional de AndesMarket S.A.C. | Asistente IA | Caso retail omnicanal, dimensiones Cliente, Producto, Tienda, Tiempo, Promocion y Fact_Ventas | Se adopto el caso recomendado por las instrucciones del curso |
| 2 | Datos | Generar datos sinteticos reproducibles con problemas de calidad controlados | Asistente IA + Python | Datos reproducibles con semilla 42 y archivos CSV en `data/raw/` | Se implemento y valido en `notebooks/00_generacion_datos.ipynb` |

## Prompt maestro de generacion de datos

Actua como ingeniero de datos. Genera un script de Python usando pandas, numpy y faker, con datos sinteticos reproducibles para una empresa ficticia llamada AndesMarket S.A.C. Fija semilla 42. Genera dimensiones de cliente, producto, tienda, tiempo y promocion, mas una tabla de hechos de ventas con dos anos de datos. Incluye estacionalidad en julio y diciembre, concentracion Pareto de productos y clientes, coherencia de precios, afinidad de canasta y comportamiento de abandono. Introduce en `data/raw/` problemas de calidad: fechas mixtas, nulos, duplicados, categorias inconsistentes, errores de tipeo, outliers y claves huerfanas. Exporta CSV con separador `;` y codificacion UTF-8. Imprime resumen de filas, nulos, duplicados y claves huerfanas.
