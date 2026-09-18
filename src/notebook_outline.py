"""Inspect a Jupyter notebook without loading its whole content.

Two modes:

    python src/notebook_outline.py notebooks/03_bronze_data_quality.ipynb
        Outline: index, cell type, source size and first line of every cell.

    python src/notebook_outline.py notebooks/03_bronze_data_quality.ipynb 13 14 21
        Full source of the given cell indexes, in the order they were passed.

The outline is the cheap way to locate a cell before editing it; the second
mode prints only what is needed, keeping large notebooks manageable.
"""

import json
import sys


def carregar(caminho):
    """Return the notebook as a dict."""
    with open(caminho, encoding="utf-8") as fh:
        return json.load(fh)


def imprimir_estrutura(nb):
    """Print one line per cell: index, type, size in characters, first line."""
    for i, cell in enumerate(nb["cells"]):
        src = "".join(cell["source"])
        linhas = src.strip().splitlines()
        cabeca = linhas[0][:110] if linhas else ""
        print(f"{i:3d} {cell['cell_type'][:2]:3s} {len(src):6d}  {cabeca}")


def imprimir_celulas(nb, indices):
    """Print the full source of the requested cells."""
    total = len(nb["cells"])
    for i in indices:
        if not 0 <= i < total:
            print(f"===== cell {i}: fora do intervalo (0 a {total - 1}) =====")
            continue
        cell = nb["cells"][i]
        print(f"===== cell {i} ({cell['cell_type']}) =====")
        print("".join(cell["source"]))
        print()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    caminho = sys.argv[1]
    indices = [int(a) for a in sys.argv[2:]]
    nb = carregar(caminho)

    if indices:
        imprimir_celulas(nb, indices)
    else:
        imprimir_estrutura(nb)


if __name__ == "__main__":
    main()
