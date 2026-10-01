# -*- coding: utf-8 -*-
"""Índice de páginas montado a partir da planilha (abas Mapa de Serviços,
Mapa de Marcas, Marcas e Camadas Programáticas).

PAG[url]    -> {"tipo", "titulo", "pai", "hub", "row", "origem"}
FILHOS[url] -> urls das páginas filhas (na ordem da planilha)
SECOES[url] -> linhas que viram seções (#ancora) dentro da página
"""
import re
from collections import defaultdict

from dados import HUBS, NOINDEX_TIPOS, NOINDEX_URLS
from planilha import carregar

P = carregar()
HUB_POR_NOME = {h["nome"]: h for h in HUBS}
HUB_URLS = {f'/{h["slug"]}/': h for h in HUBS}

TIPOS_SERV = {"Página de subhub", "Página de serviço", "Guia para download", "Calculadora", "Página pilar de conteúdo"}
TIPOS_MARCA = {"Página de categoria de marca", "Página de marca", "Página de marca por serviço",
               "Página de sistema construtivo", "Página de sistema por serviço", "Página local"}
TIPOS_COMBO = {"Página local", "Página local de bairro"}
SECAO_SERV = {"Seção dentro de outra página", "Seção em página de serviço"}
SECAO_MARCA = {"Seção na página da marca", "Seção na página do sistema", "Seção em página de serviço"}

PAG = {}
FILHOS = defaultdict(list)
SECOES = defaultdict(list)
KW_URL = {}            # palavra-chave (minúsculas) -> url
FLORIPA_PRINCIPAL = set()  # serviços otimizados para Florianópolis (camada "Página de serviço principal")
MARCA_INFO = {}        # aba Marcas, por nome da marca


def _add(url, tipo, titulo, pai, hub, row, origem):
    PAG[url] = {"tipo": tipo, "titulo": titulo, "pai": pai or "/", "hub": hub, "row": row, "origem": origem}
    FILHOS[pai or "/"].append(url)
    KW_URL.setdefault(titulo.lower(), url)


for r in P["servicos"]:
    t = r["Tipo de página"]
    if t in TIPOS_SERV:
        _add(r["URL sugerida"], t, r["Palavra-chave"], r["Página pai"], r["Hub"], r, "S")
    elif t in SECAO_SERV:
        SECOES[r["Página pai"]].append(r)

for r in P["marcas_mapa"]:
    t = r["Tipo de página"]
    if t in TIPOS_MARCA:
        _add(r["URL sugerida"], t, r["Palavra-chave"], r["Página pai"], r["Hub"], r, "M")
    elif t in SECAO_MARCA:
        SECOES[r["Página pai"]].append(r)

for r in P["combos"]:
    t = r["Tipo de página"]
    if t in TIPOS_COMBO:
        _add(r["URL sugerida"], t, r["Palavra-chave"], r["Página pai"], r["Hub"], r, "C")
    elif t == "Página de serviço principal":
        FLORIPA_PRINCIPAL.add(r["URL sugerida"])

for r in P["marcas"]:
    MARCA_INFO.setdefault(r["Marca / Operadora"], r)

# ---------------------------------------------------------------------------
# Consultas
# ---------------------------------------------------------------------------
NOMES_FIXOS = {"/": "Início", "/servicos/": "Serviços", "/marcas-e-sistemas/": "Marcas e Sistemas",
               "/guias/": "Guias", "/ferramentas/": "Ferramentas", "/blog/": "Conteúdo"}
NOMES_FIXOS.update({u: h["nome"] for u, h in HUB_URLS.items()})


def nome(url):
    return PAG[url]["titulo"] if url in PAG else NOMES_FIXOS.get(url, url)


def trilha(url):
    """Lista (nome, url) dos ancestrais, sem a própria página e sem o Início."""
    tipo = PAG[url]["tipo"]
    if tipo in ("Guia para download", "Página pilar de conteúdo"):
        return [("Conteúdo", "/blog/"), ("Guias", "/guias/")]
    if tipo == "Calculadora":
        return [("Conteúdo", "/blog/"), ("Ferramentas", "/ferramentas/")]
    out, p, guarda = [], PAG[url]["pai"], 0
    while p and p != "/" and guarda < 8:
        out.insert(0, (nome(p), p))
        p = PAG[p]["pai"] if p in PAG else "/"
        guarda += 1
    return out


def filhos(url, *tipos):
    return [u for u in FILHOS.get(url, []) if not tipos or PAG[u]["tipo"] in tipos]


def subhubs_do_hub(hub_nome):
    return [u for u, p in PAG.items() if p["tipo"] == "Página de subhub" and p["hub"] == hub_nome]


def guias_do_hub(hub_slug):
    return [u for u, p in PAG.items() if p["tipo"] in ("Guia para download", "Calculadora", "Página pilar de conteúdo")
            and (p["pai"] == f"/{hub_slug}/" or p["pai"].startswith(f"/{hub_slug}/"))]


def url_por_palavra(kw, padrao=None):
    return KW_URL.get(kw.lower(), padrao)


def noindex(url):
    if url in NOINDEX_URLS:
        return True
    return url in PAG and PAG[url]["tipo"] in NOINDEX_TIPOS


VERBOS = {"Quer", "Precisa", "Tem", "Está", "Recebeu", "Já", "Viu", "Vai", "Desconfia", "Sofreu", "Terminou",
          "Convive", "Enfrenta", "Não", "Recebe", "Descobriu", "Busca", "Comprou", "Mora", "Pretende", "Planeja",
          "Herdou", "Pensa", "Acabou", "Começou", "Teve", "Notou", "Percebeu", "Mudou", "Vende", "Aluga",
          "Constrói", "Reforma", "Administra", "Investe", "Faz", "Deseja", "Procura", "Possui", "Ganhou", "Perdeu"}


def para_quem(txt):
    """Converte a 1ª frase da coluna 'Intenção por trás da busca' em texto para o visitante."""
    t = (txt or "").strip()
    if t.startswith("Visitante que já sabe"):
        t = t.split(". ", 1)[1] if ". " in t else ""
    if not t:
        return ""
    frase = t.split(". ")[0].rstrip(".").strip()
    primeira = frase.split()[0].rstrip(",")
    if primeira in ("A", "O", "Existe", "É", "Florianópolis"):
        return ""
    corpo = (frase[0].lower() + frase[1:]).replace("com um engenheiro", "com nosso engenheiro")
    return ("Para quem " if primeira in VERBOS else "Indicado para ") + corpo + "."


def minus(t):
    """Primeira letra minúscula, preservando siglas e nomes próprios no início."""
    if not t:
        return t
    w = t.split()[0]
    if len(w) > 1 and (w.isupper() or any(c.isdigit() for c in w)):
        return t
    return t[0].lower() + t[1:]


def link_da_nota(nota):
    m = re.search(r"em (/[a-z0-9\-/]+/)", nota or "")
    return m.group(1) if m and m.group(1) in PAG else None


def ancora(url):
    return url.split("#", 1)[1] if "#" in url else ""
