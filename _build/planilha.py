# -*- coding: utf-8 -*-
"""Leitura da planilha de arquitetura (planilha.xlsx) sem dependências externas."""
import os
import zipfile
import xml.etree.ElementTree as ET

ARQ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "planilha.xlsx")
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
_M = "{%s}" % NS["m"]


def _col(ref):
    n = 0
    for ch in ref:
        if ch.isalpha():
            n = n * 26 + ord(ch.upper()) - 64
        else:
            break
    return n - 1


def ler_abas():
    z = zipfile.ZipFile(ARQ)
    ss = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            ss.append("".join(t.text or "" for t in si.iter(_M + "t")))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
    abas = {}
    for sh in wb.find("m:sheets", NS):
        alvo = rels[sh.get("{%s}id" % NS["r"])].lstrip("/")
        alvo = alvo if alvo.startswith("xl/") else "xl/" + alvo
        linhas = []
        for row in ET.fromstring(z.read(alvo)).iter(_M + "row"):
            vals = {}
            for c in row.findall("m:c", NS):
                v, t = c.find("m:v", NS), c.get("t")
                if t == "s" and v is not None:
                    val = ss[int(v.text)]
                elif t == "inlineStr":
                    val = "".join(x.text or "" for x in c.iter(_M + "t"))
                elif v is not None:
                    val = v.text
                else:
                    continue
                vals[_col(c.get("r"))] = val.strip()
            if vals:
                linhas.append([vals.get(i, "") for i in range(max(vals) + 1)])
        abas[sh.get("name")] = linhas
    return abas


def tabela(linhas, primeira_coluna):
    """Converte linhas em dicts a partir da linha de cabeçalho cuja 1ª coluna é `primeira_coluna`."""
    out, cab = [], None
    for ln in linhas:
        if cab is None:
            if ln and ln[0] == primeira_coluna:
                cab = ln
            continue
        if not ln or not ln[0] or ln[0] == primeira_coluna:
            continue
        if len([x for x in ln if x]) <= 1:  # títulos de bloco
            break
        out.append({cab[i]: (ln[i] if i < len(ln) else "") for i in range(len(cab)) if cab[i]})
    return out


def carregar():
    abas = ler_abas()
    camadas = abas["Camadas Programáticas"]
    inicio_combos = next(i for i, l in enumerate(camadas) if l and l[0].startswith("COMBINAÇÕES"))
    return {
        "servicos": tabela(abas["Mapa de Serviços"], "ID"),
        "marcas_mapa": tabela(abas["Mapa de Marcas"], "ID"),
        "marcas": tabela(abas["Marcas"], "Marca / Operadora"),
        "combos": tabela(camadas[inicio_combos:], "Camada"),
    }
