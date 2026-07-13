from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker


SEED = 42
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data/raw"
PROCESSED_DIR = PROJECT_ROOT / "data/processed"


@dataclass(frozen=True)
class DataConfig:
    n_clientes: int = 5000
    n_productos: int = 500
    n_tiendas_fisicas: int = 14
    n_promociones: int = 40
    n_ventas: int = 60000
    fecha_inicio: str = "2024-01-01"
    fecha_fin: str = "2025-12-30"


def _rng() -> np.random.Generator:
    return np.random.default_rng(SEED)


def _fake() -> Faker:
    fake = Faker("es_ES")
    Faker.seed(SEED)
    return fake


def _write_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, sep=";", index=False, encoding="utf-8")


def _weighted_choice(rng: np.random.Generator, values: list[str], weights: list[float], size: int) -> np.ndarray:
    weights_array = np.array(weights, dtype=float)
    weights_array = weights_array / weights_array.sum()
    return rng.choice(values, size=size, p=weights_array)


def generar_dim_cliente(config: DataConfig, rng: np.random.Generator, fake: Faker) -> pd.DataFrame:
    distritos = [
        "Miraflores",
        "San Isidro",
        "Surco",
        "La Molina",
        "San Miguel",
        "Los Olivos",
        "Comas",
        "Ate",
        "Callao",
        "Trujillo",
        "Arequipa",
        "Cusco",
        "Piura",
        "Chiclayo",
        "Huancayo",
    ]
    segmentos = ["Bronce", "Plata", "Oro", "Black"]
    segmento_p = [0.52, 0.30, 0.14, 0.04]

    rows = []
    for i in range(1, config.n_clientes + 1):
        sexo = rng.choice(["F", "M"], p=[0.53, 0.47])
        nombre = fake.name_female() if sexo == "F" else fake.name_male()
        rows.append(
            {
                "id_cliente": f"C{i:05d}",
                "nombre": nombre,
                "sexo": sexo,
                "fecha_nacimiento": fake.date_between(start_date="-70y", end_date="-18y"),
                "distrito": rng.choice(distritos),
                "fecha_alta": fake.date_between(start_date="-5y", end_date="-30d"),
                "segmento_programa": rng.choice(segmentos, p=segmento_p),
            }
        )
    return pd.DataFrame(rows)


def generar_dim_producto(config: DataConfig, rng: np.random.Generator) -> pd.DataFrame:
    catalogo = {
        "Lacteos": ["Leche", "Yogurt", "Queso", "Mantequilla"],
        "Bebidas": ["Gaseosa", "Agua", "Jugo", "Energizante"],
        "Snacks": ["Papas", "Galletas", "Chocolates", "Frutos secos"],
        "Abarrotes": ["Arroz", "Fideos", "Aceite", "Conservas"],
        "Limpieza": ["Detergente", "Lavavajilla", "Desinfectante", "Suavizante"],
        "Cuidado personal": ["Shampoo", "Jabon", "Pasta dental", "Desodorante"],
        "Panaderia": ["Pan molde", "Bizcocho", "Tostadas", "Keke"],
        "Carnes": ["Pollo", "Res", "Cerdo", "Embutidos"],
        "Frutas y verduras": ["Manzana", "Platano", "Papa", "Tomate"],
        "Congelados": ["Helado", "Hamburguesa", "Verduras congeladas", "Pizza"],
    }
    marcas = ["Andes", "Sol", "Inti", "Norte", "Valle", "Premium", "Ayni", "Kantu"]
    rows = []
    categorias = list(catalogo)
    categoria_weights = [0.10, 0.12, 0.11, 0.17, 0.10, 0.09, 0.08, 0.10, 0.08, 0.05]

    for i in range(1, config.n_productos + 1):
        categoria = rng.choice(categorias, p=categoria_weights)
        subcategoria = rng.choice(catalogo[categoria])
        precio_lista = round(float(rng.lognormal(mean=3.0, sigma=0.55)), 2)
        precio_lista = min(max(precio_lista, 2.5), 180.0)
        costo = round(precio_lista * float(rng.uniform(0.55, 0.82)), 2)
        rows.append(
            {
                "id_producto": f"P{i:04d}",
                "nombre": f"{subcategoria} {rng.choice(marcas)} {i:03d}",
                "categoria": categoria,
                "subcategoria": subcategoria,
                "marca": rng.choice(marcas),
                "precio_lista": precio_lista,
                "costo": costo,
            }
        )
    return pd.DataFrame(rows)


def generar_dim_tienda(config: DataConfig) -> pd.DataFrame:
    tiendas = [
        ("T001", "AndesMarket Miraflores", "fisico", "Lima", "Lima"),
        ("T002", "AndesMarket San Isidro", "fisico", "Lima", "Lima"),
        ("T003", "AndesMarket Surco", "fisico", "Lima", "Lima"),
        ("T004", "AndesMarket San Miguel", "fisico", "Lima", "Lima"),
        ("T005", "AndesMarket Los Olivos", "fisico", "Lima", "Lima"),
        ("T006", "AndesMarket Callao", "fisico", "Callao", "Callao"),
        ("T007", "AndesMarket Arequipa", "fisico", "Sur", "Arequipa"),
        ("T008", "AndesMarket Cusco", "fisico", "Sur", "Cusco"),
        ("T009", "AndesMarket Trujillo", "fisico", "Norte", "Trujillo"),
        ("T010", "AndesMarket Piura", "fisico", "Norte", "Piura"),
        ("T011", "AndesMarket Chiclayo", "fisico", "Norte", "Chiclayo"),
        ("T012", "AndesMarket Huancayo", "fisico", "Centro", "Huancayo"),
        ("T013", "AndesMarket Ica", "fisico", "Sur", "Ica"),
        ("T014", "AndesMarket Cajamarca", "fisico", "Norte", "Cajamarca"),
        ("T015", "AndesMarket Online", "online", "Nacional", "Online"),
    ]
    return pd.DataFrame(tiendas, columns=["id_tienda", "nombre", "canal", "region", "ciudad"])


def generar_dim_tiempo(config: DataConfig) -> pd.DataFrame:
    fechas = pd.date_range(config.fecha_inicio, config.fecha_fin, freq="D")
    feriados = {
        "01-01",
        "05-01",
        "07-28",
        "07-29",
        "08-30",
        "10-08",
        "11-01",
        "12-08",
        "12-25",
    }
    df = pd.DataFrame({"fecha": fechas})
    df["dia"] = df["fecha"].dt.day
    df["mes"] = df["fecha"].dt.month
    df["trimestre"] = df["fecha"].dt.quarter
    df["anio"] = df["fecha"].dt.year
    df["dia_semana"] = df["fecha"].dt.day_name(locale="C")
    df["es_feriado"] = df["fecha"].dt.strftime("%m-%d").isin(feriados)
    return df


def generar_dim_promocion(config: DataConfig, rng: np.random.Generator) -> pd.DataFrame:
    tipos = ["2x1", "Descuento", "Cupon", "Cyber", "Temporada"]
    fechas = pd.date_range(config.fecha_inicio, config.fecha_fin, freq="D")
    rows = [{"id_promocion": "PR000", "nombre": "Sin promocion", "tipo": "Sin promocion", "descuento_pct": 0.0, "fecha_inicio": pd.NaT, "fecha_fin": pd.NaT}]
    for i in range(1, config.n_promociones + 1):
        inicio = pd.Timestamp(rng.choice(fechas[:-30]))
        duracion = int(rng.integers(5, 31))
        descuento = float(rng.choice([0.05, 0.10, 0.15, 0.20, 0.25, 0.30], p=[0.2, 0.25, 0.2, 0.2, 0.1, 0.05]))
        tipo = rng.choice(tipos, p=[0.15, 0.45, 0.15, 0.10, 0.15])
        rows.append(
            {
                "id_promocion": f"PR{i:03d}",
                "nombre": f"{tipo} {i:02d}",
                "tipo": tipo,
                "descuento_pct": descuento,
                "fecha_inicio": inicio.date(),
                "fecha_fin": (inicio + pd.Timedelta(days=duracion)).date(),
            }
        )
    return pd.DataFrame(rows)


def _sample_dates(config: DataConfig, rng: np.random.Generator, n: int) -> pd.DatetimeIndex:
    fechas = pd.date_range(config.fecha_inicio, config.fecha_fin, freq="D")
    weights = np.ones(len(fechas), dtype=float)
    months = fechas.month
    dow = fechas.dayofweek
    weights[np.isin(months, [7, 12])] *= 1.75
    weights[np.isin(months, [2, 3, 9])] *= 0.78
    weights[np.isin(dow, [5, 6])] *= 1.22
    weights = weights / weights.sum()
    return pd.DatetimeIndex(rng.choice(fechas, size=n, p=weights))


def _pareto_ids(rng: np.random.Generator, ids: pd.Series, n: int, alpha: float) -> np.ndarray:
    ranks = np.arange(1, len(ids) + 1)
    weights = 1 / np.power(ranks, alpha)
    weights = weights / weights.sum()
    shuffled_ids = ids.sample(frac=1, random_state=SEED).to_numpy()
    return rng.choice(shuffled_ids, size=n, p=weights)


def reforzar_afinidad_boletas(
    ventas: pd.DataFrame,
    productos: pd.DataFrame,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Introduce pares de categorias dentro de la misma boleta para reglas de asociacion."""
    out = ventas.copy()
    productos_por_categoria = {
        categoria: grupo[["id_producto", "precio_lista"]].to_dict("records")
        for categoria, grupo in productos.groupby("categoria")
    }
    pares = [
        ("Snacks", "Bebidas", 0.32),
        ("Panaderia", "Lacteos", 0.22),
        ("Abarrotes", "Limpieza", 0.20),
        ("Carnes", "Congelados", 0.16),
    ]

    boletas = out.groupby("id_venta").filter(lambda x: len(x) >= 2)["id_venta"].drop_duplicates().to_numpy()
    rng.shuffle(boletas)
    inicio = 0

    for cat_a, cat_b, pct in pares:
        cantidad = int(len(boletas) * pct)
        seleccion = boletas[inicio : inicio + cantidad]
        inicio += cantidad
        productos_a = productos_por_categoria[cat_a]
        productos_b = productos_por_categoria[cat_b]

        for id_venta in seleccion:
            idx = out.index[out["id_venta"].eq(id_venta)].tolist()[:2]
            if len(idx) < 2:
                continue
            prod_a = rng.choice(productos_a)
            prod_b = rng.choice(productos_b)
            for row_idx, prod in zip(idx, [prod_a, prod_b]):
                out.loc[row_idx, "id_producto"] = prod["id_producto"]
                out.loc[row_idx, "precio_unitario"] = round(float(prod["precio_lista"]) * float(rng.normal(1.0, 0.03)), 2)

    return out


def generar_fact_ventas(
    config: DataConfig,
    rng: np.random.Generator,
    clientes: pd.DataFrame,
    productos: pd.DataFrame,
    tiendas: pd.DataFrame,
    promociones: pd.DataFrame,
) -> pd.DataFrame:
    fechas = _sample_dates(config, rng, config.n_ventas)
    id_clientes = _pareto_ids(rng, clientes["id_cliente"], config.n_ventas, alpha=0.72)
    id_productos = _pareto_ids(rng, productos["id_producto"], config.n_ventas, alpha=0.88)
    id_tiendas = rng.choice(tiendas["id_tienda"].to_numpy(), size=config.n_ventas, p=[0.065] * 14 + [0.09])

    productos_idx = productos.set_index("id_producto")
    promociones_validas = promociones[promociones["id_promocion"] != "PR000"].copy()
    rows = []
    categorias_por_producto = productos_idx["categoria"].to_dict()
    precio_por_producto = productos_idx["precio_lista"].to_dict()

    venta_ids = np.repeat(np.arange(1, int(config.n_ventas / 2) + 1), 2)
    if len(venta_ids) < config.n_ventas:
        venta_ids = np.append(venta_ids, np.arange(len(venta_ids) + 1, config.n_ventas + 1))
    rng.shuffle(venta_ids)

    for i in range(config.n_ventas):
        producto = id_productos[i]
        categoria = categorias_por_producto[producto]

        if categoria == "Snacks" and rng.random() < 0.35:
            candidatos = productos.loc[productos["categoria"].eq("Bebidas"), "id_producto"].to_numpy()
            producto = rng.choice(candidatos)
        elif categoria == "Bebidas" and rng.random() < 0.28:
            candidatos = productos.loc[productos["categoria"].eq("Snacks"), "id_producto"].to_numpy()
            producto = rng.choice(candidatos)
        elif categoria == "Panaderia" and rng.random() < 0.22:
            candidatos = productos.loc[productos["categoria"].eq("Lacteos"), "id_producto"].to_numpy()
            producto = rng.choice(candidatos)

        fecha = fechas[i]
        promos_fecha = promociones_validas[
            (pd.to_datetime(promociones_validas["fecha_inicio"]) <= fecha)
            & (pd.to_datetime(promociones_validas["fecha_fin"]) >= fecha)
        ]
        if not promos_fecha.empty and rng.random() < 0.33:
            promo = promos_fecha.sample(1, random_state=int(rng.integers(0, 1_000_000))).iloc[0]
            id_promocion = promo["id_promocion"]
            descuento = float(promo["descuento_pct"])
        else:
            id_promocion = "PR000"
            descuento = 0.0

        precio_lista = precio_por_producto[producto]
        precio_unitario = round(precio_lista * float(rng.normal(1.0, 0.04)), 2)
        cantidad = int(rng.choice([1, 2, 3, 4, 5, 6], p=[0.48, 0.24, 0.13, 0.08, 0.05, 0.02]))
        rows.append(
            {
                "id_venta": f"V{venta_ids[i]:07d}",
                "fecha": fecha.date(),
                "id_cliente": id_clientes[i],
                "id_producto": producto,
                "id_tienda": id_tiendas[i],
                "id_promocion": id_promocion,
                "cantidad": cantidad,
                "precio_unitario": max(precio_unitario, 0.5),
                "descuento": descuento,
            }
        )

    ventas = pd.DataFrame(rows)
    ultima_fecha = pd.Timestamp(config.fecha_fin) - pd.DateOffset(months=4)
    clientes_churn = rng.choice(clientes["id_cliente"], size=int(len(clientes) * 0.23), replace=False)
    mask_churn_reciente = ventas["id_cliente"].isin(clientes_churn) & (pd.to_datetime(ventas["fecha"]) > ultima_fecha)
    ventas = ventas.loc[~mask_churn_reciente].copy()
    faltantes = config.n_ventas - len(ventas)
    if faltantes > 0:
        extras = ventas.sample(faltantes, replace=True, random_state=SEED).copy()
        extras["id_venta"] = [f"V9{i:06d}" for i in range(1, faltantes + 1)]
        ventas = pd.concat([ventas, extras], ignore_index=True)
    ventas = ventas.head(config.n_ventas).copy()
    ventas = reforzar_afinidad_boletas(ventas, productos, rng)
    return ventas


def introducir_problemas_calidad(
    rng: np.random.Generator,
    clientes: pd.DataFrame,
    productos: pd.DataFrame,
    ventas: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    clientes_raw = clientes.copy()
    productos_raw = productos.copy()
    ventas_raw = ventas.copy()

    for col in ["fecha_nacimiento", "fecha_alta"]:
        dates = pd.to_datetime(clientes_raw[col])
        formats = rng.choice(["dmy", "ymd", "texto"], size=len(clientes_raw), p=[0.45, 0.45, 0.10])
        clientes_raw[col] = [
            d.strftime("%d/%m/%Y") if f == "dmy" else d.strftime("%Y-%m-%d") if f == "ymd" else d.strftime("%d de %B de %Y")
            for d, f in zip(dates, formats)
        ]

    dates = pd.to_datetime(ventas_raw["fecha"])
    formats = rng.choice(["dmy", "ymd", "texto"], size=len(ventas_raw), p=[0.48, 0.47, 0.05])
    ventas_raw["fecha"] = [
        d.strftime("%d/%m/%Y") if f == "dmy" else d.strftime("%Y-%m-%d") if f == "ymd" else d.strftime("%d de %B de %Y")
        for d, f in zip(dates, formats)
    ]

    for df, col, pct in [(clientes_raw, "distrito", 0.05), (productos_raw, "categoria", 0.04), (ventas_raw, "descuento", 0.06)]:
        idx = rng.choice(df.index, size=int(len(df) * pct), replace=False)
        df.loc[idx, col] = np.nan

    dup_idx = rng.choice(ventas_raw.index, size=int(len(ventas_raw) * 0.015), replace=False)
    ventas_raw = pd.concat([ventas_raw, ventas_raw.loc[dup_idx]], ignore_index=True)

    typo_map = {
        "Lacteos": [" Lacteos", "lacteos ", "lácteos", "LACTEOS"],
        "Bebidas": [" bebidas", "BEBIDAS ", "Bebdia"],
        "Snacks": ["SNACKS", " snacks ", "Snack"],
        "Abarrotes": ["abarrotes ", "ABARROTES", "Abarote"],
        "Cuidado personal": [" cuidado personal", "CUIDADO PERSONAL ", "Cuidado Personal"],
    }
    candidates = productos_raw[productos_raw["categoria"].isin(typo_map)].index
    typo_idx = rng.choice(candidates, size=int(len(productos_raw) * 0.12), replace=False)
    for idx in typo_idx:
        original = productos_raw.loc[idx, "categoria"]
        productos_raw.loc[idx, "categoria"] = rng.choice(typo_map[original])

    outlier_idx = rng.choice(ventas_raw.index, size=int(len(ventas_raw) * 0.01), replace=False)
    half = len(outlier_idx) // 2
    ventas_raw.loc[outlier_idx[:half], "cantidad"] = rng.choice([25, 40, 60, 100], size=half)
    ventas_raw.loc[outlier_idx[half:], "precio_unitario"] = ventas_raw.loc[outlier_idx[half:], "precio_unitario"] * rng.choice([8, 12, 20], size=len(outlier_idx) - half)

    orphan_idx = rng.choice(ventas_raw.index, size=int(len(ventas_raw) * 0.005), replace=False)
    ventas_raw.loc[orphan_idx, "id_producto"] = [f"PX{i:04d}" for i in range(1, len(orphan_idx) + 1)]

    return clientes_raw, productos_raw, ventas_raw


def resumen_calidad(tablas: dict[str, pd.DataFrame], productos: pd.DataFrame | None = None) -> pd.DataFrame:
    rows = []
    for nombre, df in tablas.items():
        rows.append(
            {
                "tabla": nombre,
                "filas": len(df),
                "columnas": df.shape[1],
                "duplicados": int(df.duplicated().sum()),
                "nulos_total": int(df.isna().sum().sum()),
            }
        )
    resumen = pd.DataFrame(rows)
    if productos is not None and "Fact_Ventas" in tablas:
        ventas = tablas["Fact_Ventas"]
        huerfanas = (~ventas["id_producto"].isin(productos["id_producto"])).sum()
        resumen.loc[resumen["tabla"].eq("Fact_Ventas"), "claves_huerfanas_producto"] = int(huerfanas)
    return resumen


def generar_datos(config: DataConfig | None = None) -> dict[str, pd.DataFrame]:
    config = config or DataConfig()
    rng = _rng()
    fake = _fake()

    clientes = generar_dim_cliente(config, rng, fake)
    productos = generar_dim_producto(config, rng)
    tiendas = generar_dim_tienda(config)
    tiempo = generar_dim_tiempo(config)
    promociones = generar_dim_promocion(config, rng)
    ventas = generar_fact_ventas(config, rng, clientes, productos, tiendas, promociones)

    clientes_raw, productos_raw, ventas_raw = introducir_problemas_calidad(rng, clientes, productos, ventas)

    raw_tables = {
        "Dim_Cliente": clientes_raw,
        "Dim_Producto": productos_raw,
        "Dim_Tienda": tiendas,
        "Dim_Tiempo": tiempo,
        "Dim_Promocion": promociones,
        "Fact_Ventas": ventas_raw,
    }

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    for name, df in raw_tables.items():
        _write_csv(df, RAW_DIR / f"{name.lower()}.csv")

    for name, df in {
        "Dim_Tienda": tiendas,
        "Dim_Tiempo": tiempo,
        "Dim_Promocion": promociones,
    }.items():
        _write_csv(df, PROCESSED_DIR / f"{name.lower()}.csv")

    resumen = resumen_calidad(raw_tables, productos_raw)
    _write_csv(resumen, RAW_DIR / "resumen_calidad_inicial.csv")
    return raw_tables | {"Resumen_Calidad": resumen}


def main() -> None:
    tablas = generar_datos()
    resumen = tablas["Resumen_Calidad"]
    print("Datos sinteticos generados con semilla 42")
    print(resumen.to_string(index=False))


if __name__ == "__main__":
    main()
