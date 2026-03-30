from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
DOWNTIME_PATH = REPO_ROOT / "input" / "SRV_DOWNTIME.parquet"
POZOS_PATH = REPO_ROOT / "input" / "SRV_POZOS.parquet"
OUTPUT_PATH = REPO_ROOT / "input" / "SRV_DOWNTIME_MERGED_POZOS.parquet"


def normalize_well_name(series: pd.Series) -> pd.Series:
    return (
        series.astype("string")
        .str.strip()
        .str.upper()
        .str.replace(r"\s+", " ", regex=True)
    )


def main() -> None:
    downtime = pd.read_parquet(DOWNTIME_PATH).copy()
    pozos = pd.read_parquet(POZOS_PATH).copy()

    downtime["_merge_key"] = normalize_well_name(downtime["POZO"])
    pozos["_merge_key"] = normalize_well_name(pozos["NOMBRE"])

    pozos_unique = pozos.drop_duplicates(subset="_merge_key", keep="first")

    merged = downtime.merge(
        pozos_unique,
        on="_merge_key",
        how="inner",
        suffixes=("_DOWNTIME", "_POZOS"),
    )

    merged = merged.drop(columns=["_merge_key"])
    merged.to_parquet(OUTPUT_PATH, index=False)

    print(f"Archivo generado: {OUTPUT_PATH}")
    print(f"Filas SRV_DOWNTIME originales: {len(downtime):,}")
    print(f"Filas luego del merge: {len(merged):,}")
    print(f"Filas descartadas: {len(downtime) - len(merged):,}")
    print(f"Pozos unicos en SRV_DOWNTIME: {downtime['POZO'].nunique(dropna=True):,}")
    print(f"Pozos unicos matcheados: {merged['POZO'].nunique(dropna=True):,}")


if __name__ == "__main__":
    main()
