# -*- coding: utf-8 -*-
"""Save the chart outputs of an exported notebook as PNG files for the README.

Databricks exports a notebook as .ipynb with its outputs; each matplotlib chart is
an image/png output. This writes every chart to a folder, named after the closest
heading above it, so the README can reference stable file names.

    python src/extrair_figuras.py <notebook.ipynb> <pasta_saida>
"""

import base64
import json
import os
import re
import sys
import unicodedata


def slug(texto, limite=45):
    """Lowercase ASCII slug for file names that GitHub links handle safely."""
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    texto = re.sub(r"[^a-zA-Z0-9]+", "-", texto.lower()).strip("-")
    return texto[:limite].rstrip("-") or "figura"


def titulo(celula):
    """Last markdown heading of a cell, or None when it has none."""
    titulos = re.findall(r"^#{1,6}\s+(.+)$", "".join(celula["source"]), flags=re.M)
    return titulos[-1] if titulos else None


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    entrada, saida = sys.argv[1], sys.argv[2]
    with open(entrada, encoding="utf-8") as fh:
        nb = json.load(fh)
    os.makedirs(saida, exist_ok=True)

    secao, contador = "inicio", 0
    for celula in nb["cells"]:
        if celula["cell_type"] == "markdown":
            secao = titulo(celula) or secao
            continue
        for resultado in celula.get("outputs", []):
            png = resultado.get("data", {}).get("image/png")
            if not png:
                continue
            contador += 1
            nome = f"fig{contador:02d}_{slug(secao)}.png"
            with open(os.path.join(saida, nome), "wb") as fh:
                fh.write(base64.b64decode("".join(png)))
            print(nome)
    print(f"{contador} figuras gravadas em {saida}")


if __name__ == "__main__":
    main()
