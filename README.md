# Proyecto BI AndesMarket

Proyecto de Inteligencia de Negocios para una empresa ficticia de retail omnicanal en Peru: AndesMarket S.A.C.

## Entorno

- Python 3.10+
- Power BI Desktop
- Git

Instalacion:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Orden de ejecucion

1. `notebooks/00_generacion_datos.ipynb`: genera datos sinteticos reproducibles en `data/raw/`.
2. `notebooks/01_datamart_etl.ipynb`: limpia datos, valida calidad y exporta tablas a `data/processed/`.
3. `notebooks/02_visualizacion.ipynb`: visualizaciones exploratorias e insights.
4. `notebooks/03_clasificacion.ipynb`: prediccion de abandono.
5. `notebooks/04_segmentacion.ipynb`: segmentacion RFM con K-Means.
6. `notebooks/05_asociacion.ipynb`: reglas de asociacion y canasta de mercado.
7. `notebooks/06_regresion.ipynb`: pronostico de ventas/demanda.

## Estructura

```text
proyecto-bi-andesmarket/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   ├── 00_generacion_datos.ipynb
│   ├── 01_datamart_etl.ipynb
│   ├── 02_visualizacion.ipynb
│   ├── 03_clasificacion.ipynb
│   ├── 04_segmentacion.ipynb
│   ├── 05_asociacion.ipynb
│   └── 06_regresion.ipynb
├── powerbi/
│   └── AndesMarket.pbix
├── prompts/
│   └── registro_prompts.md
└── informe/
    └── Informe_PG_AndesMarket.pdf
```

## Reproducibilidad

La generacion de datos usa semilla fija `42`. Los datos crudos no se sobrescriben durante el ETL; las salidas limpias se guardan en `data/processed/`.

## Criterios del trabajo

- Caso adoptado: AndesMarket S.A.C., recomendado por la guia del curso.
- Desarrollo: individual.
- Power BI se construye en una maquina virtual con Power BI Desktop.
