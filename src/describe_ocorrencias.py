"""
ANEEL emergency occurrences - side-by-side schema and content description.

Purpose
-------
Compares the 2025 and 2026 Parquet files of the "Ocorrencias Emergenciais nas
Redes de Distribuicao" dataset to explain the layout change (15 columns in
2022-2025 versus 23 columns in 2026) and to support the data reconciliation
section of the MVP report.

What it produces
----------------
1. Positional schema comparison: column order side by side, which reveals
   renames and reordering, not only additions.
2. Set comparison: columns exclusive to each year, common columns, and type
   changes among the common ones.
3. Footer statistics per column: null count, min and max, read from Parquet
   row-group metadata without loading the table.
4. A transposed sample of the first rows of each file, so the actual content
   of every column can be read at a glance.
5. Optional value counts for low-cardinality text columns, computed in a
   single streaming pass with bounded memory.

Output goes to the console and to data/describe_ocorrencias.md.

Usage
-----
    python describe_ocorrencias.py
    python describe_ocorrencias.py --sample 25
    python describe_ocorrencias.py --counts
    python describe_ocorrencias.py --counts --max-cardinality 100
    python describe_ocorrencias.py --years 2024 2025 2026

Requirements: pandas, pyarrow
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

PROJECT_DIR = Path(r"C:\python_projects\puc-mvp-01-performance-dx")
RAW_DIR = PROJECT_DIR / "data" / "raw"
REPORT_MD = PROJECT_DIR / "data" / "describe_ocorrencias.md"

FILE_TEMPLATE = "ocorrencias-emergenciais-rede-distribuicao-{year}.parquet"
DEFAULT_YEARS = [2024, 2025, 2026]

SAMPLE_ROWS = 15                # rows shown in the transposed sample
MAX_CARDINALITY = 60            # above this, a column is reported as high-cardinality
COUNT_BATCH_ROWS = 250_000      # streaming batch size for value counts
SAMPLE_TRUNCATE_CHARS = 60      # cell truncation in the sample table


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def human_size(num_bytes: float) -> str:
    """Format a byte count as a human readable string."""
    value = float(num_bytes)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(value) < 1024.0:
            return f"{value:,.1f} {unit}"
        value /= 1024.0
    return f"{value:,.1f} PB"


def truncate(value: object, limit: int = SAMPLE_TRUNCATE_CHARS) -> str:
    """Render a cell value as a single short line."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return "(nulo)"
    text = str(value).replace("\n", " ").replace("|", "/").strip()
    return text if len(text) <= limit else text[: limit - 3] + "..."


# --------------------------------------------------------------------------
# Metadata extraction
# --------------------------------------------------------------------------

def read_file_info(path: Path) -> dict:
    """Read schema, row count and per-column footer statistics from a Parquet file."""
    parquet_file = pq.ParquetFile(path)
    metadata = parquet_file.metadata
    schema = parquet_file.schema_arrow

    # Aggregate statistics across row groups. Reading the footer only.
    stats: dict[str, dict] = {
        name: {"nulls": 0, "min": None, "max": None, "has_stats": False}
        for name in schema.names
    }

    for group_index in range(metadata.num_row_groups):
        group = metadata.row_group(group_index)
        for column_index in range(group.num_columns):
            column = group.column(column_index)
            name = column.path_in_schema.split(".")[0]
            entry = stats.setdefault(
                name, {"nulls": 0, "min": None, "max": None, "has_stats": False}
            )
            statistics = column.statistics
            if statistics is None:
                continue
            entry["has_stats"] = True
            entry["nulls"] += statistics.null_count
            if statistics.has_min_max:
                low, high = statistics.min, statistics.max
                entry["min"] = low if entry["min"] is None else min(entry["min"], low)
                entry["max"] = high if entry["max"] is None else max(entry["max"], high)

    return {
        "path": path,
        "rows": metadata.num_rows,
        "row_groups": metadata.num_row_groups,
        "disk_bytes": path.stat().st_size,
        "created_by": metadata.created_by,
        "names": list(schema.names),
        "types": {name: str(dtype) for name, dtype in zip(schema.names, schema.types)},
        "stats": stats,
        "parquet_file": parquet_file,
    }


def read_sample(info: dict, rows: int) -> pd.DataFrame:
    """Read the first N rows of the file without loading the whole table."""
    batch = next(info["parquet_file"].iter_batches(batch_size=rows))
    return batch.to_pandas().head(rows)


def count_values(info: dict, max_cardinality: int) -> dict[str, object]:
    """Count distinct values of text columns in one streaming pass.

    A column whose distinct count exceeds max_cardinality is abandoned and
    reported as high-cardinality, which keeps memory bounded.
    """
    text_columns = [
        name for name in info["names"] if "string" in info["types"][name].lower()
    ]
    if not text_columns:
        return {}

    counters: dict[str, Counter] = {name: Counter() for name in text_columns}
    abandoned: set[str] = set()

    for batch in info["parquet_file"].iter_batches(
        batch_size=COUNT_BATCH_ROWS, columns=text_columns
    ):
        frame = batch.to_pandas()
        for name in text_columns:
            if name in abandoned:
                continue
            counters[name].update(frame[name].dropna().tolist())
            if len(counters[name]) > max_cardinality:
                abandoned.add(name)
                counters[name] = Counter()
        if len(abandoned) == len(text_columns):
            break

    return {
        name: ("alta cardinalidade" if name in abandoned else counters[name])
        for name in text_columns
    }


# --------------------------------------------------------------------------
# Report sections
# --------------------------------------------------------------------------

def section_overview(infos: dict[int, dict]) -> list[str]:
    """Build the file-level overview table."""
    lines = [
        "## 1. Visao geral dos arquivos",
        "",
        "| Ano | Linhas | Colunas | Row groups | Disco | Gerado por |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for year, info in infos.items():
        lines.append(
            f"| {year} | {info['rows']:,} | {len(info['names'])} | "
            f"{info['row_groups']} | {human_size(info['disk_bytes'])} | "
            f"{info['created_by'] or 'n/d'} |"
        )
    lines.append("")
    return lines


def section_positional(infos: dict[int, dict]) -> list[str]:
    """Build the positional (column order) comparison table."""
    years = list(infos.keys())
    max_columns = max(len(info["names"]) for info in infos.values())

    header = "| Pos | " + " | ".join(str(year) for year in years) + " |"
    divider = "|---|" + "|".join(["---"] * len(years)) + "|"
    lines = [
        "## 2. Comparacao posicional (ordem das colunas)",
        "",
        "Colunas na ordem fisica de cada arquivo. Divergencia de posicao para o",
        "mesmo nome indica reordenacao; nome diferente na mesma posicao sugere",
        "renomeacao.",
        "",
        header,
        divider,
    ]

    for position in range(max_columns):
        cells = []
        for year in years:
            names = infos[year]["names"]
            if position < len(names):
                name = names[position]
                cells.append(f"`{name}` <br><sub>{infos[year]['types'][name]}</sub>")
            else:
                cells.append("—")
        lines.append(f"| {position + 1} | " + " | ".join(cells) + " |")

    lines.append("")
    return lines


def section_set_diff(infos: dict[int, dict]) -> list[str]:
    """Build the set-difference section: exclusive columns and type changes."""
    years = list(infos.keys())
    lines = ["## 3. Diferencas de esquema", ""]

    all_names: dict[str, set[int]] = {}
    for year, info in infos.items():
        for name in info["names"]:
            all_names.setdefault(name, set()).add(year)

    common = [n for n, y in all_names.items() if len(y) == len(years)]
    lines.append(f"Colunas comuns a todos os anos: {len(common)}")
    lines.append("")

    for year in years:
        exclusive = [n for n, y in all_names.items() if y == {year}]
        lines.append(f"### Exclusivas de {year} ({len(exclusive)})")
        lines.append("")
        if exclusive:
            lines.append("| Coluna | Tipo |")
            lines.append("|---|---|")
            for name in exclusive:
                lines.append(f"| `{name}` | {infos[year]['types'][name]} |")
        else:
            lines.append("Nenhuma.")
        lines.append("")

    type_changes = [
        name
        for name in common
        if len({infos[year]["types"][name] for year in years}) > 1
    ]
    lines.append(f"### Mudanca de tipo entre anos ({len(type_changes)})")
    lines.append("")
    if type_changes:
        lines.append("| Coluna | " + " | ".join(str(y) for y in years) + " |")
        lines.append("|---|" + "|".join(["---"] * len(years)) + "|")
        for name in type_changes:
            cells = " | ".join(infos[year]["types"][name] for year in years)
            lines.append(f"| `{name}` | {cells} |")
    else:
        lines.append("Nenhuma.")
    lines.append("")
    return lines


def section_stats(infos: dict[int, dict]) -> list[str]:
    """Build the per-column footer statistics section."""
    lines = ["## 4. Estatisticas por coluna (metadados do Parquet)", ""]
    for year, info in infos.items():
        lines += [
            f"### {year}",
            "",
            "| Coluna | Tipo | Nulos | % nulos | Min | Max |",
            "|---|---|---:|---:|---|---|",
        ]
        for name in info["names"]:
            entry = info["stats"].get(name, {})
            nulls = entry.get("nulls")
            if entry.get("has_stats") and nulls is not None:
                pct = f"{nulls / info['rows'] * 100:.2f}%" if info["rows"] else "n/d"
                nulls_text = f"{nulls:,}"
            else:
                pct, nulls_text = "n/d", "n/d"
            lines.append(
                f"| `{name}` | {info['types'][name]} | {nulls_text} | {pct} | "
                f"{truncate(entry.get('min'), 30)} | {truncate(entry.get('max'), 30)} |"
            )
        lines.append("")
    return lines


def section_sample(infos: dict[int, dict], rows: int) -> list[str]:
    """Build the transposed sample section, one table per year."""
    lines = [
        "## 5. Amostra transposta",
        "",
        f"Primeiras {rows} linhas de cada arquivo, com as colunas nas linhas "
        "para facilitar a leitura do conteudo.",
        "",
    ]
    for year, info in infos.items():
        sample = read_sample(info, rows)
        lines += [f"### {year}", ""]
        lines.append("| Coluna | " + " | ".join(f"L{i + 1}" for i in range(len(sample))) + " |")
        lines.append("|---|" + "|".join(["---"] * len(sample)) + "|")
        for name in info["names"]:
            cells = " | ".join(truncate(value) for value in sample[name].tolist())
            lines.append(f"| `{name}` | {cells} |")
        lines.append("")
    return lines


def section_counts(counts_by_year: dict[int, dict], max_cardinality: int) -> list[str]:
    """Build the value-counts section for low-cardinality text columns."""
    lines = [
        "## 6. Dominios das colunas de texto",
        "",
        f"Colunas com ate {max_cardinality} valores distintos. As demais sao "
        "marcadas como alta cardinalidade.",
        "",
    ]
    for year, counts in counts_by_year.items():
        lines += [f"### {year}", ""]
        for name, result in counts.items():
            if result == "alta cardinalidade":
                lines.append(f"- `{name}`: alta cardinalidade (acima do limite)")
                continue
            lines += ["", f"`{name}` — {len(result)} valores distintos", "",
                      "| Valor | Frequencia |", "|---|---:|"]
            for value, frequency in result.most_common():
                lines.append(f"| {truncate(value)} | {frequency:,} |")
        lines.append("")
    return lines


# --------------------------------------------------------------------------
# Console output
# --------------------------------------------------------------------------

def print_console_summary(infos: dict[int, dict]) -> None:
    """Print the essential comparison to the console."""
    years = list(infos.keys())

    print("\n=== VISAO GERAL ===\n")
    for year, info in infos.items():
        print(
            f"{year}: {info['rows']:>14,} linhas  {len(info['names']):>3} colunas  "
            f"{human_size(info['disk_bytes']):>10}"
        )

    print("\n=== ORDEM DAS COLUNAS ===\n")
    width = 42
    print("Pos  " + "".join(f"{year:<{width}}" for year in years))
    print("-" * (5 + width * len(years)))
    max_columns = max(len(info["names"]) for info in infos.values())
    for position in range(max_columns):
        cells = []
        for year in years:
            names = infos[year]["names"]
            cells.append(names[position] if position < len(names) else "-")
        print(f"{position + 1:<5}" + "".join(f"{cell:<{width}}" for cell in cells))

    all_names: dict[str, set[int]] = {}
    for year, info in infos.items():
        for name in info["names"]:
            all_names.setdefault(name, set()).add(year)

    print("\n=== EXCLUSIVAS POR ANO ===\n")
    for year in years:
        exclusive = [n for n, y in all_names.items() if y == {year}]
        print(f"{year}: {len(exclusive)} coluna(s)")
        for name in exclusive:
            print(f"    {name}  ({infos[year]['types'][name]})")


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Describe e compara os arquivos de ocorrencias emergenciais."
    )
    parser.add_argument(
        "--years", nargs="+", type=int, default=DEFAULT_YEARS,
        help=f"anos a comparar (padrao: {DEFAULT_YEARS})",
    )
    parser.add_argument(
        "--sample", type=int, default=SAMPLE_ROWS,
        help=f"linhas na amostra transposta (padrao: {SAMPLE_ROWS})",
    )
    parser.add_argument(
        "--counts", action="store_true",
        help="contar dominios das colunas de texto (passada extra sobre o arquivo)",
    )
    parser.add_argument(
        "--max-cardinality", type=int, default=MAX_CARDINALITY,
        help=f"limite de valores distintos por coluna (padrao: {MAX_CARDINALITY})",
    )
    args = parser.parse_args()

    infos: dict[int, dict] = {}
    for year in args.years:
        path = RAW_DIR / FILE_TEMPLATE.format(year=year)
        if not path.exists():
            print(f"ERRO: arquivo nao encontrado: {path}")
            continue
        print(f"Lendo metadados: {path.name}")
        infos[year] = read_file_info(path)

    if len(infos) < 2:
        print("ERRO: sao necessarios pelo menos dois arquivos para comparar.")
        return

    print_console_summary(infos)

    report = ["# Describe comparativo - Ocorrencias Emergenciais nas Redes de Distribuicao",
              "",
              f"Gerado em {pd.Timestamp.now():%d/%m/%Y %H:%M}",
              "",
              "Fonte: ANEEL Dados Abertos. Arquivos anuais em formato Parquet.",
              ""]
    report += section_overview(infos)
    report += section_positional(infos)
    report += section_set_diff(infos)
    report += section_stats(infos)
    report += section_sample(infos, args.sample)

    if args.counts:
        print("\n=== CONTANDO DOMINIOS (passada extra) ===\n")
        counts_by_year = {}
        for year, info in infos.items():
            print(f"  {year}...")
            counts_by_year[year] = count_values(info, args.max_cardinality)
        report += section_counts(counts_by_year, args.max_cardinality)

    REPORT_MD.parent.mkdir(parents=True, exist_ok=True)
    REPORT_MD.write_text("\n".join(report), encoding="utf-8")
    print(f"\nRelatorio: {REPORT_MD}")


if __name__ == "__main__":
    main()
