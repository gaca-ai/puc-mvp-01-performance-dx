# -*- coding: utf-8 -*-
"""Extract command outputs from a Databricks notebook exported as HTML.

The export embeds the whole notebook model as base64 of a URL-encoded JSON in
__DATABRICKS_NOTEBOOK_MODEL. This decodes it and reads the results of each
command without opening the page.

Two modes:

    python src/notebook_html_outputs.py <arquivo.html> [inicio] [fim]
        Prints the raw payload of each command, for inspection.

    python src/notebook_html_outputs.py <arquivo.html> --markdown [saida.md]
        Writes a markdown file with the outputs already formatted as tables and
        code blocks, grouped under the headings of the notebook itself, ready to
        be quoted as evidence in the README.

`inicio` and `fim` are command indexes, zero based; Databricks labels them Cmd 1
upward, so Cmd N is index N-1.
"""

import base64
import html
import json
import os
import re
import sys
import urllib.parse

MAX_LINHAS_TABELA = 25


def carregar_modelo(caminho):
    """Decode the notebook model embedded in the exported HTML."""
    with open(caminho, encoding="utf-8", errors="replace") as fh:
        bruto = fh.read()
    m = re.search(r"__DATABRICKS_NOTEBOOK_MODEL = '([^']+)'", bruto)
    if not m:
        raise SystemExit("modelo do notebook nao encontrado no HTML")
    cru = base64.b64decode(m.group(1)).decode("utf-8")
    return json.loads(urllib.parse.unquote(cru))


def limpar(texto, preservar_espacos=False):
    """Strip HTML tags from a result payload and collapse blank runs.

    Printed output relies on column alignment, so runs of spaces are kept when
    `preservar_espacos` is true; they are collapsed only in prose payloads.
    """
    texto = re.sub(r"<[^>]+>", " ", texto)
    texto = html.unescape(texto)
    if not preservar_espacos:
        texto = re.sub(r"[ \t]{2,}", " ", texto)
    return re.sub(r"\n{3,}", "\n\n", texto).strip()


def celula(valor):
    """Render one table value, protecting the markdown pipe."""
    if valor is None:
        return ""
    return str(valor).replace("|", "\\|").replace("\n", " ")


def tabela_markdown(dados, esquema):
    """Turn a Databricks table result into a markdown table."""
    nomes = [c.get("name", f"c{i}") for i, c in enumerate(esquema)]
    linhas = ["| " + " | ".join(nomes) + " |",
              "|" + "|".join(["---"] * len(nomes)) + "|"]
    for registro in dados[:MAX_LINHAS_TABELA]:
        linhas.append("| " + " | ".join(celula(v) for v in registro) + " |")
    if len(dados) > MAX_LINHAS_TABELA:
        linhas.append(f"\n_{len(dados)} linhas no total; "
                      f"{MAX_LINHAS_TABELA} exibidas._")
    return "\n".join(linhas)


def titulo_markdown(fonte):
    """Return the first heading of a %md cell, if it has one."""
    for linha in fonte.splitlines():
        if linha.strip().startswith("#"):
            return linha.strip()
    return None


def blocos_do_resultado(res):
    """Yield the formatted blocks of one command result."""
    dados = res.get("data")
    if isinstance(dados, list):
        for item in dados:
            tipo = item.get("type")
            if tipo == "table":
                yield tabela_markdown(item.get("data", []), item.get("schema", []))
            elif tipo == "ansi":
                texto = limpar(str(item.get("data", "")), preservar_espacos=True)
                if texto:
                    yield "```\n" + texto + "\n```"
    elif dados:
        texto = limpar(str(dados), preservar_espacos=True)
        if texto:
            yield "```\n" + texto + "\n```"


def gerar_markdown(modelo, destino, origem):
    """Write one markdown file with every command output of the notebook."""
    partes = [f"# Saidas de `{modelo.get('name', 'notebook')}`", "",
              f"Extraido de `{os.path.basename(origem)}`. "
              "Gerado por `src/notebook_html_outputs.py`; nao editar a mao.", ""]

    titulo_pendente = None
    for i, cmd in enumerate(modelo.get("commands", [])):
        fonte = (cmd.get("command") or "").strip()

        if fonte.startswith("%md"):
            titulo_pendente = titulo_markdown(fonte[3:]) or titulo_pendente
            continue

        blocos = list(blocos_do_resultado(cmd.get("results") or {}))
        if not blocos:
            continue

        if titulo_pendente:
            partes += [titulo_pendente, ""]
            titulo_pendente = None

        primeira = fonte.splitlines()[0] if fonte else ""
        partes += [f"**Cmd {i + 1}** — `{primeira[:90]}`", ""]
        for bloco in blocos:
            partes += [bloco, ""]

    with open(destino, "w", encoding="utf-8") as fh:
        fh.write("\n".join(partes).rstrip() + "\n")

    print(f"markdown gerado: {destino}")


def imprimir_bruto(modelo, inicio, fim):
    """Print the raw payload of each command, for inspection."""
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
            corpo = json.dumps(dados[:MAX_LINHAS_TABELA], ensure_ascii=False)
        else:
            corpo = limpar(str(dados))

        if not corpo and not cabeca:
            continue

        print(f"\n===== Cmd {i + 1} [{res.get('type', '')}] {cabeca}")
        if corpo:
            print(corpo[:4000])


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    caminho = sys.argv[1]
    modelo = carregar_modelo(caminho)

    if "--markdown" in sys.argv:
        pos = sys.argv.index("--markdown")
        if len(sys.argv) > pos + 1:
            destino = sys.argv[pos + 1]
        else:
            destino = os.path.splitext(caminho)[0] + "_saidas.md"
        gerar_markdown(modelo, destino, caminho)
        return

    inicio = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    fim = int(sys.argv[3]) if len(sys.argv) > 3 else 10**6
    imprimir_bruto(modelo, inicio, fim)


if __name__ == "__main__":
    main()
