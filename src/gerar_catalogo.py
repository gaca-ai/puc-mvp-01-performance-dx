# -*- coding: utf-8 -*-
"""Write docs/catalogo_dados.md from the exported run of 05_catalogo_dados.

The notebook prints the catalog as markdown between two markers. This script
reads the notebook exported from Databricks with its outputs, takes the text
between the markers and saves it, so the catalog is never retyped by hand.

    python src/gerar_catalogo.py [notebook.ipynb] [saida.md]
"""

import json
import os
import sys

INICIO_MD = "<!-- CATALOGO_INICIO -->"
FIM_MD = "<!-- CATALOGO_FIM -->"

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRADA_PADRAO = os.path.join(RAIZ, "docs", "img", "05_catalogo_dados", "05_catalogo_dados.ipynb")
SAIDA_PADRAO = os.path.join(RAIZ, "docs", "catalogo_dados.md")


def texto_das_saidas(caminho):
    """Concatenate every stream and text/plain output of the notebook."""
    with open(caminho, encoding="utf-8") as fh:
        nb = json.load(fh)
    partes = []
    for celula in nb["cells"]:
        for saida in celula.get("outputs", []):
            if saida.get("output_type") == "stream":
                partes.append("".join(saida.get("text", "")))
            elif "text/plain" in saida.get("data", {}):
                partes.append("".join(saida["data"]["text/plain"]))
    return "\n".join(partes)


def main():
    entrada = sys.argv[1] if len(sys.argv) > 1 else ENTRADA_PADRAO
    saida = sys.argv[2] if len(sys.argv) > 2 else SAIDA_PADRAO

    texto = texto_das_saidas(entrada)
    if INICIO_MD not in texto or FIM_MD not in texto:
        raise SystemExit("marcadores do catalogo nao encontrados; o notebook foi exportado com as saidas?")

    catalogo = texto.split(INICIO_MD, 1)[1].split(FIM_MD, 1)[0].strip() + "\n"
    with open(saida, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(catalogo)

    tabelas = catalogo.count("\n### ")
    print(f"catalogo gravado em {saida}: {tabelas} tabelas com colunas detalhadas")


if __name__ == "__main__":
    main()
