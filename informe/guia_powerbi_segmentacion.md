# Guia Power BI - Segmentacion de clientes

## Archivos a importar

En el mismo archivo `powerbi/AndesMarket.pbix`, importar:

```text
data/processed/segmentos_clientes.csv
data/processed/perfil_segmentos.csv
```

Separador:

```text
;
```

## Relacion principal

Crear relacion:

```text
dim_cliente[id_cliente] 1 -> * segmentos_clientes[id_cliente]
```

Direccion de filtro:

```text
Simple
```

`perfil_segmentos.csv` puede quedar como tabla independiente para mostrar resumen agregado por segmento.

## Pagina sugerida

Nombre de pagina:

```text
Segmentacion de clientes
```

Visuales:

1. Tarjeta: total de clientes segmentados.
2. Barras: clientes por `segmento_rfm`.
3. Barras: monto total por `segmento_rfm`.
4. Matriz: `segmento_rfm`, recencia promedio, frecuencia promedio, monto promedio.
5. Dispersión:
   - X: `segmentos_clientes[recencia]`
   - Y: `segmentos_clientes[monto]`
   - Tamaño: `segmentos_clientes[frecuencia]`
   - Leyenda: `segmentos_clientes[segmento_rfm]`
6. Tabla: `segmento_rfm`, `id_cliente`, `monto`, `frecuencia`, `recencia`, `segmento_programa`.
7. Segmentador: `segmento_rfm`.
8. Segmentador: `segmento_programa`.

## Medidas DAX sugeridas

```DAX
Clientes Segmentados =
DISTINCTCOUNT(segmentos_clientes[id_cliente])
```

```DAX
Monto Segmentado =
SUM(segmentos_clientes[monto])
```

```DAX
Recencia Promedio =
AVERAGE(segmentos_clientes[recencia])
```

```DAX
Frecuencia Promedio =
AVERAGE(segmentos_clientes[frecuencia])
```

```DAX
Monto Promedio Cliente =
AVERAGE(segmentos_clientes[monto])
```

