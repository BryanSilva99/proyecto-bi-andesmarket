# Guia Power BI - Pronostico de demanda

## Archivos a importar

En el mismo archivo `powerbi/AndesMarket.pbix`, importar:

```text
data/processed/pronostico_ventas.csv
data/processed/metricas_regresion.csv
```

Separador:

```text
;
```

Estas tablas pueden quedar aisladas. `pronostico_ventas.csv` ya contiene fecha, venta real, pronostico, error y tipo de periodo.

## Pagina sugerida

Nombre de pagina:

```text
Pronostico de demanda
```

Visuales simples:

1. Tarjeta: MAPE del mejor modelo.
2. Tarjeta: RMSE del mejor modelo.
3. Linea: `fecha` con `ventas` y `pronostico`.
4. Columnas: `fecha` con `abs_error`.
5. Tabla: metricas por modelo desde `metricas_regresion`.
6. Segmentador: `tipo` (`validacion` / `futuro`).

## Medidas DAX sugeridas

En `metricas_regresion`:

```DAX
MAPE Mejor Modelo =
MIN(metricas_regresion[MAPE])
```

```DAX
RMSE Mejor Modelo =
MIN(metricas_regresion[RMSE])
```

En `pronostico_ventas`:

```DAX
Venta Real =
SUM(pronostico_ventas[ventas])
```

```DAX
Venta Pronosticada =
SUM(pronostico_ventas[pronostico])
```

```DAX
Error Absoluto =
SUM(pronostico_ventas[abs_error])
```

## Interpretacion rapida

- `validacion`: periodo donde existen ventas reales y pronostico para evaluar error.
- `futuro`: siguientes 30 dias pronosticados; ventas reales aparecen vacias.
- MAPE bajo indica menor error porcentual promedio.

