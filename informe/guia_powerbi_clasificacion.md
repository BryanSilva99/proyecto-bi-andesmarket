# Guia Power BI - Riesgo de abandono

## Archivo a importar

Desde Power BI Desktop, en el mismo archivo `powerbi/AndesMarket.pbix`, importar:

```text
data/processed/predicciones_abandono.csv
```

Separador:

```text
;
```

## Relacion

Crear relacion:

```text
dim_cliente[id_cliente] 1 -> * predicciones_abandono[id_cliente]
```

Direccion de filtro:

```text
Simple
```

## Pagina sugerida

Nombre de pagina:

```text
Riesgo de abandono
```

Visuales:

1. Tarjeta: clientes en riesgo alto.
2. Tarjeta: probabilidad promedio de abandono.
3. Barras: cantidad de clientes por `nivel_riesgo`.
4. Tabla: `id_cliente`, `segmento_programa`, `probabilidad_abandono`, `nivel_riesgo`, `monto_total`, `recencia_dias`.
5. Barras o dispersión: `monto_total` vs `probabilidad_abandono`.
6. Segmentador: `nivel_riesgo`.
7. Segmentador: `segmento_programa`.

## Medidas DAX sugeridas

```DAX
Clientes Riesgo Alto =
CALCULATE(
    DISTINCTCOUNT(predicciones_abandono[id_cliente]),
    predicciones_abandono[nivel_riesgo] = "Alto"
)
```

```DAX
Probabilidad Abandono Promedio =
AVERAGE(predicciones_abandono[probabilidad_abandono])
```

```DAX
Clientes Evaluados =
DISTINCTCOUNT(predicciones_abandono[id_cliente])
```

```DAX
Venta Historica Clientes Riesgo =
SUM(predicciones_abandono[monto_total])
```

