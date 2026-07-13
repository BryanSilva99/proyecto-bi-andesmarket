# Resumen de asociacion - canasta de mercado

- Boletas analizadas: 32,712.
- Boletas con al menos dos categorias: 26,690.
- Metodo: Apriori sobre categorias compradas por boleta.
- Criterio de relevancia: reglas con lift > 1.

## Reglas principales

- **Congelados -> Carnes**: soporte 0.163, confianza 0.942, lift 5.17. Promocionar Carnes a clientes que compran Congelados; usar exhibicion conjunta, cupon cruzado o recomendacion online.
- **Carnes -> Congelados**: soporte 0.163, confianza 0.896, lift 5.17. Promocionar Congelados a clientes que compran Carnes; usar exhibicion conjunta, cupon cruzado o recomendacion online.
- **Panaderia -> Lacteos**: soporte 0.224, confianza 0.968, lift 4.05. Promocionar Lacteos a clientes que compran Panaderia; usar exhibicion conjunta, cupon cruzado o recomendacion online.
- **Lacteos -> Panaderia**: soporte 0.224, confianza 0.937, lift 4.05. Promocionar Panaderia a clientes que compran Lacteos; usar exhibicion conjunta, cupon cruzado o recomendacion online.
- **Abarrotes -> Limpieza**: soporte 0.206, confianza 0.936, lift 4.02. Promocionar Limpieza a clientes que compran Abarrotes; usar exhibicion conjunta, cupon cruzado o recomendacion online.
- **Limpieza -> Abarrotes**: soporte 0.206, confianza 0.887, lift 4.02. Promocionar Abarrotes a clientes que compran Limpieza; usar exhibicion conjunta, cupon cruzado o recomendacion online.
