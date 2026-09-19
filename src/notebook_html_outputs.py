# -*- coding: utf-8 -*-
"""Extract command outputs from a Databricks notebook exported as HTML.

The export embeds the whole notebook model as base64 of a URL-encoded JSON in
__DATABRICKS_NOTEBOOK_MODEL. This decodes it and prints, per command, the first
line of the source and the text of its results, so the outputs of a run can be
read without opening the page.

    python src/notebook_html_outputs.py <arquivo.html> [inicio] [fim]

`inicio` and `fim` are command indexes, zero based; Databricks labels them Cmd 1
upward, so Cmd N is index N-1.
"""

import base64
import html
import json
import re
import sys
import urllib.parse


def carregar_modelo(caminho):
    """Decode the notebook model embedded in the exported HTML."""
    with open(caminho, encoding="utf-8", errors="replace") as fh:
        bruto = fh.read()
    m = re.search(r"__DATABRICKS_NOTEBOOK_MODEL = '([^']+)'", bruto)
    if not m:
        raise SystemExit("modelo do notebook nao encontrado no HTML")
    cru = base64.b64decode(m.group(1)).decode("utf-8")
    return json.loads(urllib.parse.unquote(cru))


def limpar(texto):
    """Strip HTML tags from a result payload and collapse blank runs."""
    texto = re.sub(r"<[^>]+>", " ", texto)
    texto = html.unescape(texto)
    texto = re.sub(r"[ \t]{2,}", " ", texto)
    return re.sub(r"\n{3,}", "\n\n", texto).strip()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    caminho = sys.argv[1]
    inicio = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    fim = int(sys.argv[3]) if len(sys.argv) > 3 else 10**6

    modelo = carregar_modelo(caminho)
    comandos = modelo.get("commands", [])
    print(f"comandos no notebook: {len(comandos)}")

    for i, cmd in enumerate(comandos):
        if not inicio <= i < fim:
            continue
        fonte = (cmd.get("command") or "").strip().splitlines()
        cabeca = fonte[0][:100] if fonte else ""
        res = cmd.get("results") or {}
        dados = res.get("data", "")

        if isinstance(dados, list):
            corpo = json.dumps(dados[:25], ensure_ascii=False)
        else:
            corpo = limpar(str(dados))

        if not corpo and not cabeca:
            continue

        print(f"\n===== Cmd {i + 1} [{res.get('type', '')}] {cabeca}")
        if corpo:
            print(corpo[:4000])


if __name__ == "__main__":
    main()
