from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data/raw"
PROCESSED_DIR = PROJECT_ROOT / "data/processed"
DOCS_DIR = PROJECT_ROOT / "informe"


SPANISH_MONTHS = {
    "enero": "January",
    "febrero": "February",
    "marzo": "March",
    "abril": "April",
    "mayo": "May",
    "junio": "June",
    "julio": "July",
    "agosto": "August",
    "septiembre": "September",
    "setiembre": "September",
    "octubre": "October",
    "noviembre": "November",
    "diciembre": "December",
}


def _read_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(RAW_DIR / f"{name}.csv", sep=";", encoding="utf-8")


def _write_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, sep=";", index=False, encoding="utf-8")


def _strip_accents(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(char for char in normalized if not unicodedata.combining(char))


def normalizar_categoria(value: object) -> object:
    if pd.isna(value):
        return value
    text = _strip_accents(str(value)).strip().upper()
    text = re.sub(r"\s+", " ", text)
    mapping = {
        "LACTEOS": "Lacteos",
        "BEBIDAS": "Bebidas",
        "BEBDIA": "Bebidas",
        "SNACKS": "Snacks",
        "SNACK": "Snacks",
        "ABARROTES": "Abarrotes",
        "ABAROTE": "Abarrotes",
        "LIMPIEZA": "Limpieza",
        "CUIDADO PERSONAL": "Cuidado personal",
        "PANADERIA": "Panaderia",
        "CARNES": "Carnes",
        "FRUTAS Y VERDURAS": "Frutas y verduras",
        "CONGELADOS": "Congelados",
    }
    return mapping.get(text, text.title())


def parse_fecha(series: pd.Series) -> pd.Series:
    values = series.astype("string").str.strip()
    for es, en in SPANISH_MONTHS.items():
        values = values.str.replace(es, en, case=False, regex=False)
    values = values.str.replace(r"\s+de\s+", " ", regex=True)
    parsed = pd.to_datetime(values, errors="coerce", dayfirst=True, format="mixed")
    return parsed.dt.date


def cargar_raw() -> dict[str, pd.DataFrame]:
    return {
        "dim_cliente": _read_csv("dim_cliente"),
        "dim_producto": _read_csv("dim_producto"),
        "dim_tienda": _read_csv("dim_tienda"),
        "dim_tiempo": _read_csv("dim_tiempo"),
        "dim_promocion": _read_csv("dim_promocion"),
        "fact_ventas": _read_csv("fact_ventas"),
    }


def metricas_calidad(tablas: dict[str, pd.DataFrame]) -> pd.DataFrame:
    productos = tablas["dim_producto"]
    ventas = tablas["fact_ventas"]
    rows = []
    for nombre, df in tablas.items():
        row = {
            "tabla": nombre,
            "filas": len(df),
            "columnas": df.shape[1],
            "duplicados": int(df.duplicated().sum()),
            "nulos_total": int(df.isna().sum().sum()),
        }
        if nombre == "fact_ventas":
            row["claves_huerfanas_producto"] = int((~ventas["id_producto"].isin(productos["id_producto"])).sum())
        rows.append(row)
    return pd.DataFrame(rows)


def limpiar_dim_cliente(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["fecha_nacimiento"] = parse_fecha(out["fecha_nacimiento"])
    out["fecha_alta"] = parse_fecha(out["fecha_alta"])
    out["distrito"] = out["distrito"].fillna("No especificado").astype(str).str.strip().str.title()
    out["nombre"] = out["nombre"].astype(str).str.strip()
    out["sexo"] = out["sexo"].astype(str).str.strip().str.upper()
    out["segmento_programa"] = out["segmento_programa"].astype(str).str.strip().str.title()
    return out.drop_duplicates(subset=["id_cliente"])


def limpiar_dim_producto(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["categoria"] = out["categoria"].apply(normalizar_categoria)
    categoria_por_subcategoria = (
        out.dropna(subset=["categoria"])
        .groupby("subcategoria")["categoria"]
        .agg(lambda x: x.mode().iloc[0] if not x.mode().empty else "Sin categoria")
    )
    out["categoria"] = out.apply(
        lambda row: categoria_por_subcategoria.get(row["subcategoria"], "Sin categoria")
        if pd.isna(row["categoria"])
        else row["categoria"],
        axis=1,
    )
    out["nombre"] = out["nombre"].astype(str).str.strip()
    out["subcategoria"] = out["subcategoria"].astype(str).str.strip().str.title()
    out["marca"] = out["marca"].astype(str).str.strip().str.title()
    out["precio_lista"] = pd.to_numeric(out["precio_lista"], errors="coerce")
    out["costo"] = pd.to_numeric(out["costo"], errors="coerce")
    out["precio_lista"] = out["precio_lista"].clip(lower=0.5, upper=250)
    out["costo"] = np.minimum(out["costo"], out["precio_lista"] * 0.95)
    return out.drop_duplicates(subset=["id_producto"])


def limpiar_dim_tiempo(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["fecha"] = parse_fecha(out["fecha"])
    return out.drop_duplicates(subset=["fecha"])


def limpiar_dim_promocion(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["fecha_inicio"] = parse_fecha(out["fecha_inicio"])
    out["fecha_fin"] = parse_fecha(out["fecha_fin"])
    out["descuento_pct"] = pd.to_numeric(out["descuento_pct"], errors="coerce").fillna(0)
    sin_promo = out["id_promocion"].eq("PR000")
    out.loc[sin_promo, "fecha_inicio"] = pd.Timestamp("2024-01-01").date()
    out.loc[sin_promo, "fecha_fin"] = pd.Timestamp("2025-12-30").date()
    return out.drop_duplicates(subset=["id_promocion"])


def limpiar_fact_ventas(
    ventas: pd.DataFrame,
    productos: pd.DataFrame,
    clientes: pd.DataFrame,
    tiendas: pd.DataFrame,
    promociones: pd.DataFrame,
) -> pd.DataFrame:
    out = ventas.copy()
    out["fecha"] = parse_fecha(out["fecha"])
    out["cantidad"] = pd.to_numeric(out["cantidad"], errors="coerce")
    out["precio_unitario"] = pd.to_numeric(out["precio_unitario"], errors="coerce")
    out["descuento"] = pd.to_numeric(out["descuento"], errors="coerce").fillna(0)

    out = out.drop_duplicates(subset=["id_venta", "id_producto"])
    out = out[out["id_producto"].isin(productos["id_producto"])]
    out = out[out["id_cliente"].isin(clientes["id_cliente"])]
    out = out[out["id_tienda"].isin(tiendas["id_tienda"])]
    out = out[out["id_promocion"].isin(promociones["id_promocion"])]
    out = out.dropna(subset=["fecha", "cantidad", "precio_unitario"])

    cantidad_q99 = out["cantidad"].quantile(0.99)
    precio_q99 = out["precio_unitario"].quantile(0.99)
    out["cantidad"] = out["cantidad"].clip(lower=1, upper=max(10, cantidad_q99))
    out["precio_unitario"] = out["precio_unitario"].clip(lower=0.5, upper=precio_q99)
    out["descuento"] = out["descuento"].clip(lower=0, upper=0.8)

    costos = productos[["id_producto", "costo"]]
    out = out.merge(costos, on="id_producto", how="left")
    out["importe"] = out["cantidad"] * out["precio_unitario"] * (1 - out["descuento"])
    out["costo_total"] = out["cantidad"] * out["costo"]
    out["margen"] = out["importe"] - out["costo_total"]
    out = out.drop(columns=["costo"])

    ordered_cols = [
        "id_venta",
        "fecha",
        "id_cliente",
        "id_producto",
        "id_tienda",
        "id_promocion",
        "cantidad",
        "precio_unitario",
        "descuento",
        "importe",
        "costo_total",
        "margen",
    ]
    return out[ordered_cols].reset_index(drop=True)


def diccionario_datos() -> pd.DataFrame:
    rows = [
        ("dim_cliente", "id_cliente", "string", "PK", "Identificador unico del cliente"),
        ("dim_cliente", "nombre", "string", "", "Nombre sintetico del cliente"),
        ("dim_cliente", "sexo", "string", "", "Sexo declarado F/M"),
        ("dim_cliente", "fecha_nacimiento", "date", "", "Fecha de nacimiento sintetica"),
        ("dim_cliente", "distrito", "string", "", "Distrito o ciudad de residencia"),
        ("dim_cliente", "fecha_alta", "date", "", "Fecha de afiliacion al programa"),
        ("dim_cliente", "segmento_programa", "string", "", "Nivel AndesPlus"),
        ("dim_producto", "id_producto", "string", "PK", "Identificador unico del producto"),
        ("dim_producto", "nombre", "string", "", "Nombre sintetico del producto"),
        ("dim_producto", "categoria", "string", "", "Categoria homologada"),
        ("dim_producto", "subcategoria", "string", "", "Subcategoria del producto"),
        ("dim_producto", "marca", "string", "", "Marca sintetica"),
        ("dim_producto", "precio_lista", "float", "", "Precio regular"),
        ("dim_producto", "costo", "float", "", "Costo unitario estimado"),
        ("dim_tienda", "id_tienda", "string", "PK", "Identificador unico de tienda"),
        ("dim_tienda", "canal", "string", "", "Canal fisico u online"),
        ("dim_tiempo", "fecha", "date", "PK", "Fecha calendario"),
        ("dim_promocion", "id_promocion", "string", "PK", "Identificador de promocion"),
        ("fact_ventas", "id_venta", "string", "Degenerate", "Identificador de boleta/transaccion"),
        ("fact_ventas", "fecha", "date", "FK", "Fecha de venta"),
        ("fact_ventas", "id_cliente", "string", "FK", "Cliente que compra"),
        ("fact_ventas", "id_producto", "string", "FK", "Producto vendido"),
        ("fact_ventas", "id_tienda", "string", "FK", "Tienda o canal de venta"),
        ("fact_ventas", "id_promocion", "string", "FK", "Promocion aplicada"),
        ("fact_ventas", "cantidad", "float", "Medida", "Unidades vendidas"),
        ("fact_ventas", "precio_unitario", "float", "Medida", "Precio unitario aplicado"),
        ("fact_ventas", "descuento", "float", "Medida", "Porcentaje de descuento"),
        ("fact_ventas", "importe", "float", "Medida", "Venta neta"),
        ("fact_ventas", "costo_total", "float", "Medida", "Costo total de la linea"),
        ("fact_ventas", "margen", "float", "Medida", "Margen bruto de la linea"),
    ]
    return pd.DataFrame(rows, columns=["tabla", "campo", "tipo", "rol", "descripcion"])


def ejecutar_etl() -> dict[str, pd.DataFrame]:
    raw = cargar_raw()
    calidad_antes = metricas_calidad(raw)

    dim_cliente = limpiar_dim_cliente(raw["dim_cliente"])
    dim_producto = limpiar_dim_producto(raw["dim_producto"])
    dim_tienda = raw["dim_tienda"].drop_duplicates(subset=["id_tienda"]).copy()
    dim_tiempo = limpiar_dim_tiempo(raw["dim_tiempo"])
    dim_promocion = limpiar_dim_promocion(raw["dim_promocion"])
    fact_ventas = limpiar_fact_ventas(raw["fact_ventas"], dim_producto, dim_cliente, dim_tienda, dim_promocion)

    processed = {
        "dim_cliente": dim_cliente,
        "dim_producto": dim_producto,
        "dim_tienda": dim_tienda,
        "dim_tiempo": dim_tiempo,
        "dim_promocion": dim_promocion,
        "fact_ventas": fact_ventas,
    }
    calidad_despues = metricas_calidad(processed)
    diccionario = diccionario_datos()

    for name, df in processed.items():
        _write_csv(df, PROCESSED_DIR / f"{name}.csv")
    _write_csv(calidad_antes, PROCESSED_DIR / "calidad_antes.csv")
    _write_csv(calidad_despues, PROCESSED_DIR / "calidad_despues.csv")
    _write_csv(diccionario, PROCESSED_DIR / "diccionario_datos.csv")

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / "modelo_estrella.md").write_text(
        "# Modelo estrella AndesMarket\n\n"
        "Grano: una linea de venta, es decir, un producto dentro de una boleta.\n\n"
        "```text\n"
        "Dim_Cliente   Dim_Producto   Dim_Tienda   Dim_Tiempo   Dim_Promocion\n"
        "     \\             |             |            |              /\n"
        "      \\            |             |            |             /\n"
        "                    Fact_Ventas\n"
        "```\n\n"
        "Relaciones esperadas en Power BI: todas las dimensiones filtran a Fact_Ventas en cardinalidad uno-a-muchos.\n",
        encoding="utf-8",
    )

    return processed | {
        "calidad_antes": calidad_antes,
        "calidad_despues": calidad_despues,
        "diccionario_datos": diccionario,
    }


def main() -> None:
    resultados = ejecutar_etl()
    print("Calidad antes del ETL")
    print(resultados["calidad_antes"].to_string(index=False))
    print("\nCalidad despues del ETL")
    print(resultados["calidad_despues"].to_string(index=False))


if __name__ == "__main__":
    main()
