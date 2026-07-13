# Modelo estrella AndesMarket

Grano: una linea de venta, es decir, un producto dentro de una boleta.

```text
Dim_Cliente   Dim_Producto   Dim_Tienda   Dim_Tiempo   Dim_Promocion
     \             |             |            |              /
      \            |             |            |             /
                    Fact_Ventas
```

Relaciones esperadas en Power BI: todas las dimensiones filtran a Fact_Ventas en cardinalidad uno-a-muchos.
