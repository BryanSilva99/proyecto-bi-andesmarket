# Guia Power BI - Canasta de mercado

## Archivos a importar

En el mismo archivo `powerbi/AndesMarket.pbix`, importar:

```text
data/processed/reglas_asociacion.csv
data/processed/itemsets_frecuentes.csv
data/processed/resumen_transacciones_asociacion.csv
```

Separador:

```text
;
```

Estas tablas pueden quedar aisladas. No necesitan relacionarse con el modelo estrella porque son resultados agregados del algoritmo Apriori.

## Pagina sugerida

Nombre de pagina:

```text
Canasta de mercado
```

Visuales:

1. Tarjeta: cantidad de reglas.
2. Tarjeta: lift maximo.
3. Tarjeta: confianza promedio.
4. Barras: `regla` por `lift`.
5. Barras: `regla` por `confidence`.
6. Tabla: `antecedente`, `consecuente`, `support`, `confidence`, `lift`, `prioridad`, `propuesta_negocio`.
7. Segmentador: `prioridad`.
8. Segmentador: `antecedente`.

## Medidas DAX sugeridas

```DAX
Cantidad Reglas =
COUNTROWS(reglas_asociacion)
```

```DAX
Lift Maximo =
MAX(reglas_asociacion[lift])
```

```DAX
Confianza Promedio =
AVERAGE(reglas_asociacion[confidence])
```

```DAX
Soporte Promedio =
AVERAGE(reglas_asociacion[support])
```

## Interpretacion rapida

- `support`: proporcion de boletas donde aparece la combinacion.
- `confidence`: probabilidad de comprar el consecuente dado el antecedente.
- `lift`: fuerza de asociacion frente a una compra independiente. Si `lift > 1`, la regla es positiva.

