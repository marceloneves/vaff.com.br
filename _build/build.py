# -*- coding: utf-8 -*-
"""Gera as páginas estáticas do site VAFF Engenharia.

Uso:  python3 _build/build.py
As páginas são escritas em pastas (/construcao/index.html etc.) para ter URLs
limpas. Os links usam caminhos absolutos, então o site precisa ser servido
a partir da raiz de um servidor (ex.: python3 -m http.server na pasta do site).
"""
import json
import os
from html import escape

import sys

from dados import (EMPRESA as E, HUBS, HUB, MARCAS, PERFIS, OBRAS, OBRAS_CATEGORIAS,
                   REGIOES, FORM_TIPOS, MENU, PERFIL_URL, REGIAO_SLUG, OBRAS_CATEGORIAS_PAGINAS)
import indice as I

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANO = 2026
ANOS = ANO - E["desde"]


# ===========================================================================
# Utilidades
# ===========================================================================
def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


def org_ld():
    return {
        "@context": "https://schema.org", "@type": "GeneralContractor",
        "name": E["nome"], "legalName": E["razao"], "url": E["site"],
        "logo": E["site"] + "/assets/img/logo-vaff.png",
        "telephone": E["tel_link"], "email": E["email"], "foundingDate": str(E["desde"]),
        "slogan": E["frase"],
        "address": {"@type": "PostalAddress", "streetAddress": "Av. Nossa Senhora Aparecida, 746, sala 02",
                    "addressLocality": "São José", "addressRegion": "SC", "addressCountry": "BR"},
        "areaServed": [c for c, _ in REGIOES],
        "sameAs": [E["instagram"]],
    }


def breadcrumb_ld(itens):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": E["site"] + u}
                                for i, (n, u) in enumerate(itens)]}


def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def redes():
    return f'''<div class="redes">
          <a href="{E["instagram"]}" target="_blank" rel="noopener" aria-label="Instagram"><i class="fa-brands fa-instagram"></i></a>
          <a href="https://wa.me/{E["wpp_link"]}" target="_blank" rel="noopener" aria-label="WhatsApp"><i class="fa-brands fa-whatsapp"></i></a>
        </div>'''


def logo(branco=False):
    arq = "logo-vaff-branco.png" if branco else "logo-vaff.png"
    return f'<a href="/" class="logo" aria-label="VAFF Engenharia — página inicial"><img src="/assets/img/{arq}" alt="VAFF Engenharia" width="520" height="205"></a>'


# ===========================================================================
# Mega menus
# ===========================================================================
def mega_servicos():
    cols = []
    for h in HUBS:
        itens = "".join(f'<li><a href="{I.url_por_palavra(d, "/" + h["slug"] + "/")}">{escape(d)}</a></li>' for d in h["destaques"][:4])
        cols.append(f'''<div class="mega__col">
            <h4><a href="/{h["slug"]}/"><i class="{h["icone"]}"></i>{h["nome"]}</a></h4>
            <ul>{itens}<li><a class="ver-todos" href="/{h["slug"]}/">Ver todos &rarr;</a></li></ul>
          </div>''')
    return f'''<div class="mega">
        <div class="mega__grid">{"".join(cols)}</div>
        <div class="mega__rodape">Não sabe qual serviço precisa? <a href="/para-voce/">Veja soluções pelo seu perfil</a> ou <a href="/solicitar-proposta/">fale com um engenheiro</a>.</div>
      </div>'''


def mega_marcas():
    cols = []
    for grupo, cats in MARCAS:
        itens = "".join(f'<li><a href="/marcas-e-sistemas/#{s}">{n}</a></li>' for s, n, *_ in cats)
        cols.append(f'<div class="mega__col"><h4><a href="/marcas-e-sistemas/">{grupo}</a></h4><ul>{itens}</ul></div>')
    return f'<div class="mega"><div class="mega__grid mega__grid--5">{"".join(cols)}</div></div>'


def menu_desktop(atual):
    lis = []
    for url, nome, mega in MENU:
        ativo = ' class="ativo" aria-current="page"' if atual == url else ""
        if mega:
            painel = mega_servicos() if mega == "servicos" else mega_marcas()
            lis.append(f'<li class="tem-mega"><a href="{url}"{ativo} aria-haspopup="true" aria-expanded="false">{nome}<i class="fa-solid fa-chevron-down seta-menu"></i></a>{painel}</li>')
        else:
            lis.append(f'<li><a href="{url}"{ativo}>{nome}</a></li>')
    return "\n          ".join(lis)


def menu_mobile():
    serv = "".join(f'<a href="/{h["slug"]}/">{h["nome"]}</a>' for h in HUBS)
    marc = "".join(f'<a href="/marcas-e-sistemas/#{s}">{n}</a>' for _, cats in MARCAS for s, n, *_ in cats)
    simples = "".join(f'<a href="{u}">{n}</a>' for u, n, m in MENU if not m)
    return f'''<div class="acordeao"><button type="button" class="acordeao__botao" aria-expanded="false">Serviços <i class="fa-solid fa-chevron-down"></i></button><div class="acordeao__painel"><a href="/servicos/"><strong>Todos os serviços</strong></a>{serv}</div></div>
        <div class="acordeao"><button type="button" class="acordeao__botao" aria-expanded="false">Marcas e Sistemas <i class="fa-solid fa-chevron-down"></i></button><div class="acordeao__painel">{marc}</div></div>
        {simples}
        <a href="/solicitar-proposta/">Solicitar proposta</a>'''


# ===========================================================================
# Cabeçalho e rodapé
# ===========================================================================
def head(titulo, desc, atual="", ld=None, url=None, noindex=False):
    ld_html = "\n  ".join(jsonld(x) for x in (ld or []))
    if url and noindex:
        NOINDEX.add(url)
    robots = '\n  <meta name="robots" content="noindex, follow">' if noindex else ""
    canonical = f'\n  <link rel="canonical" href="{E["site"]}{url}">' if url else ""
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(titulo)}</title>
  <meta name="description" content="{escape(desc)}">{robots}{canonical}
  <meta property="og:title" content="{escape(titulo)}">
  <meta property="og:description" content="{escape(desc)}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:image" content="/assets/img/logo-vaff.png">
  <meta name="theme-color" content="#0f3760">
  <link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300..900;1,9..40,400..600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
  <link rel="stylesheet" href="/assets/css/style.css">
  {ld_html}
</head>
<body>

  <div class="topo">
    <div class="container">
      <ul class="topo__info">
        <li><i class="fa-solid fa-phone"></i> <a href="tel:{E["tel_link"]}">{E["tel"]}</a></li>
        <li><i class="fa-solid fa-envelope"></i> <a href="mailto:{E["email"]}">{E["email"]}</a></li>
        <li><i class="fa-regular fa-clock"></i> {E["horario"]}</li>
      </ul>
      {redes()}
    </div>
  </div>

  <header class="cabecalho">
    <div class="container">
      {logo()}
      <nav aria-label="Menu principal">
        <ul class="menu">
          {menu_desktop(atual)}
        </ul>
      </nav>
      <div class="cabecalho__acoes">
        <a href="/solicitar-proposta/" class="btn btn--base">Solicitar proposta</a>
        <button class="menu-toggle" type="button" aria-label="Abrir menu" aria-expanded="false" aria-controls="menu-mobile"><i class="fa-solid fa-bars"></i></button>
      </div>
    </div>
  </header>

  <div class="menu-mobile" id="menu-mobile" aria-hidden="true">
    <div class="menu-mobile__fundo"></div>
    <div class="menu-mobile__painel">
      <div class="menu-mobile__topo">
        {logo(True)}
        <button class="menu-mobile__fechar" type="button" aria-label="Fechar menu"><i class="fa-solid fa-xmark"></i></button>
      </div>
      <nav aria-label="Menu mobile">
        {menu_mobile()}
      </nav>
      <ul class="menu-mobile__contato">
        <li><i class="fa-solid fa-phone"></i> <a href="tel:{E["tel_link"]}">{E["tel"]}</a></li>
        <li><i class="fa-brands fa-whatsapp"></i> <a href="https://wa.me/{E["wpp_link"]}">{E["wpp"]}</a></li>
        <li><i class="fa-solid fa-envelope"></i> <a href="mailto:{E["email"]}">{E["email"]}</a></li>
      </ul>
      {redes()}
    </div>
  </div>
'''


CTA = '''
  <section class="cta">
    <div class="container">
      <div class="cta__texto">
        <span class="cta__icone"><i class="fa-solid fa-helmet-safety"></i></span>
        <div>
          <h2>Vamos construir o seu sonho?</h2>
          <p>Engenharia de alto padrão, do projeto à entrega, sem dor de cabeça.</p>
        </div>
      </div>
      <a href="/solicitar-proposta/" class="btn btn--branco">Solicitar proposta <i class="fa-solid fa-arrow-right"></i></a>
    </div>
  </section>
'''


def foot():
    hubs = "".join(f'<li><a href="/{h["slug"]}/">{h["nome"]}</a></li>' for h in HUBS)
    regs = "".join(f'<li><a href="/regioes/{REGIAO_SLUG[c]}/">{c}</a></li>' for c, _ in REGIOES[:8])
    return f'''
  <footer class="rodape">
    <div class="container rodape__principal">
      <div class="rodape__sobre">
        {logo(True)}
        <p>{E["frase"]} Desde {E["desde"]} entregando projetos, laudos e obras em Santa Catarina.</p>
        <ul class="rodape__contato">
          <li><i class="fa-solid fa-location-dot"></i><span>{E["end_sj"]}</span></li>
          <li><i class="fa-solid fa-location-dot"></i><span>{E["end_pl"]}</span></li>
          <li><i class="fa-solid fa-phone"></i><a href="tel:{E["tel_link"]}">{E["tel"]}</a></li>
          <li><i class="fa-brands fa-whatsapp"></i><a href="https://wa.me/{E["wpp_link"]}" target="_blank" rel="noopener">{E["wpp"]}</a></li>
          <li><i class="fa-solid fa-envelope"></i><a href="mailto:{E["email"]}">{E["email"]}</a></li>
        </ul>
      </div>
      <div>
        <h4>Serviços</h4>
        <ul class="rodape__links">{hubs}</ul>
      </div>
      <div>
        <h4>Regiões atendidas</h4>
        <ul class="rodape__links">{regs}<li><a href="/regioes/">Ver todas</a></li></ul>
      </div>
      <div>
        <h4>Siga a VAFF</h4>
        <p style="margin-bottom:20px">Acompanhe nossas obras e bastidores.</p>
        {redes()}
        <h4 style="margin-top:35px">Institucional</h4>
        <ul class="rodape__links">
          <li><a href="/sobre/">Sobre a VAFF</a></li>
          <li><a href="/obras/">Obras</a></li>
          <li><a href="/perguntas-frequentes/">Perguntas frequentes</a></li>
          <li><a href="/contato/">Contato</a></li>
        </ul>
      </div>
    </div>
    <div class="rodape__base">
      <div class="container">
        <p>© <span data-ano>{ANO}</span> {E["razao"]} · CNPJ {E["cnpj"]} · {E["crea"]}</p>
        <p><a href="/politica-de-privacidade/">Política de privacidade</a> · <a href="mailto:{E["email"]}?subject=Trabalhe%20conosco">Trabalhe conosco</a></p>
      </div>
    </div>
  </footer>

  <div class="barra-mobile">
    <a class="wpp" href="https://wa.me/{E["wpp_link"]}" target="_blank" rel="noopener"><i class="fa-brands fa-whatsapp"></i> WhatsApp</a>
    <a class="prop" href="/solicitar-proposta/"><i class="fa-solid fa-file-pen"></i> Solicitar proposta</a>
  </div>

  <button class="voltar-topo" type="button" aria-label="Voltar ao topo"><i class="fa-solid fa-arrow-up"></i></button>

  <script src="/assets/js/main.js"></script>
</body>
</html>
'''


def page_header(titulo, trilha, img="fundo-1.svg"):
    """trilha: lista de (nome, url) sem incluir a página atual."""
    migalhas = '<li><a href="/">Início</a></li>' + "".join(f'<li><a href="{u}">{n}</a></li>' for n, u in trilha) + f"<li>{titulo}</li>"
    return f'''
  <section class="page-header" style="background-image:url('/assets/img/{img}')">
    <div class="container">
      <h1>{titulo}</h1>
      <nav aria-label="Você está em"><ul class="breadcrumb">{migalhas}</ul></nav>
    </div>
  </section>
'''


def titulo_secao(sub, h2, p="", centro=True, claro=False, h="h2"):
    cls = "titulo-secao" + (" titulo-secao--centro" if centro else "") + (" titulo-secao--claro" if claro else "")
    return f'<div class="{cls} anima"><span class="subtitulo">{sub}</span><{h}>{h2}</{h}>' + (f"<p>{p}</p>" if p else "") + "</div>"


def cards_hubs(lista=HUBS):
    out = []
    for i, h in enumerate(lista):
        out.append(f'''<a href="/{h["slug"]}/" class="card-hub anima" data-atraso="{i % 4}">
          <span class="card-hub__icone"><i class="{h["icone"]}"></i></span>
          <h3>{h["nome"]}</h3>
          <p>{h["resumo"]}</p>
          <span class="link-mais">Ver serviços <i class="fa-solid fa-arrow-right"></i></span>
        </a>''')
    return "\n        ".join(out)


def faq_html(faqs):
    return "\n".join(f'''        <div class="faq__item{' aberto' if i == 0 else ''}">
          <button type="button" class="faq__pergunta" aria-expanded="{'true' if i == 0 else 'false'}">{escape(q)} <i class="fa-solid fa-plus"></i></button>
          <div class="faq__resposta"><p>{escape(a)}</p></div>
        </div>''' for i, (q, a) in enumerate(faqs))


def processo():
    passos = [("fa-solid fa-comments", "Contato inicial", "Entendemos sua necessidade e enviamos uma proposta clara."),
              ("fa-solid fa-magnifying-glass-location", "Visita e diagnóstico", "Visita técnica ao local, levantamento e análise."),
              ("fa-solid fa-pen-ruler", "Planejamento", "Projeto, laudo ou plano de obra com escopo, prazo e custo."),
              ("fa-solid fa-handshake", "Execução e entrega", "Execução acompanhada, entrega com ART e suporte pós-obra.")]
    itens = "".join(f'<div class="passo anima" data-atraso="{i}"><div class="passo__icone"><i class="{ic}"></i><span class="passo__num">0{i + 1}</span></div><h3>{t}</h3><p>{d}</p></div>'
                    for i, (ic, t, d) in enumerate(passos))
    return f'''
  <section class="secao">
    <div class="container">
      {titulo_secao("Como trabalhamos", "Nosso processo de <span>trabalho</span>")}
      <div class="processo__grid">{itens}</div>
    </div>
  </section>
'''


def form_proposta(claro=True, tipo_padrao=None, compacto=False):
    c = "formulario" + (" formulario--claro" if claro else "")
    ops = "".join(f'<option data-slug="{s}"{" selected" if s == tipo_padrao else ""}>{n}</option>' for s, n in FORM_TIPOS)
    extra = "" if compacto else '''
          <div class="linha">
            <label class="visually-hidden" for="f-cidade">Cidade e bairro</label>
            <input id="f-cidade" name="Cidade/bairro" type="text" placeholder="Cidade e bairro do imóvel">
            <label class="visually-hidden" for="f-prazo">Prazo desejado</label>
            <select id="f-prazo" name="Prazo desejado">
              <option value="">Quando pretende começar?</option>
              <option>Imediatamente</option><option>Em até 3 meses</option><option>De 3 a 6 meses</option><option>Mais de 6 meses</option><option>Ainda estou pesquisando</option>
            </select>
          </div>
          <label class="visually-hidden" for="f-imovel">Tipo de imóvel</label>
          <select id="f-imovel" name="Tipo de imóvel">
            <option value="">Tipo de imóvel</option>
            <option>Casa</option><option>Apartamento</option><option>Condomínio / edifício</option><option>Comercial</option><option>Industrial / galpão</option><option>Terreno</option>
          </select>'''
    return f'''<form class="{c}" data-mailto="{E["email"]}">
          <label class="visually-hidden" for="f-tipo">Tipo de demanda</label>
          <select id="f-tipo" name="Tipo de demanda" data-tipo required>
            <option value="">Qual é a sua demanda?</option>{ops}
          </select>
          <div class="linha">
            <label class="visually-hidden" for="f-nome">Nome</label>
            <input id="f-nome" name="Nome" type="text" placeholder="Seu nome" required autocomplete="name">
            <label class="visually-hidden" for="f-tel">Telefone</label>
            <input id="f-tel" name="Telefone" type="tel" placeholder="Telefone / WhatsApp" required autocomplete="tel">
          </div>
          <label class="visually-hidden" for="f-email">E-mail</label>
          <input id="f-email" name="E-mail" type="email" placeholder="Seu e-mail" required autocomplete="email">{extra}
          <label class="visually-hidden" for="f-msg">Mensagem</label>
          <textarea id="f-msg" name="Mensagem" placeholder="Conte um pouco sobre o seu imóvel ou projeto"></textarea>
          <button type="submit" class="btn btn--base">Enviar solicitação <i class="fa-solid fa-paper-plane"></i></button>
          <p class="form-msg" role="status">Obrigado! Seu aplicativo de e-mail foi aberto para concluir o envio.</p>
        </form>'''


def escrever(url, html):
    pasta = os.path.join(RAIZ, url.strip("/"))
    os.makedirs(pasta, exist_ok=True)
    with open(os.path.join(pasta, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    PAGINAS.append(url)


PAGINAS = []
NOINDEX = set()


# ===========================================================================
# Home
# ===========================================================================
def pagina_home():
    slides = [
        ("hero-1", "Engenharia de alto padrão", "Engenharia de alto padrão, <span>livre de dor de cabeça</span>", "Construção, reformas, projetos e laudos técnicos na Grande Florianópolis, com conformidade legal, segurança estrutural e tranquilidade do início ao fim.", "h1"),
        ("hero-3", "Construção e reformas", "Obras de alto padrão, <span>das pranchas à entrega</span>", "Gestão, cronograma e acompanhamento técnico em cada etapa para você não precisar se preocupar com a obra.", "h2"),
        ("hero-2", "Laudos e vistorias", "Laudos que trazem <span>segurança</span> e respaldo", "Laudos estruturais, vistorias de entrega, inspeção predial e perícias com responsabilidade técnica e ART.", "h2"),
    ]
    hero = "\n".join(f'''    <div class="hero__slide{' ativo' if i == 0 else ''}">
      <div class="hero__bg" style="background-image:url('/assets/img/{img}.svg')"></div>
      <div class="container">
        <div class="hero__conteudo">
          <span class="hero__etiqueta"><i class="fa-solid fa-helmet-safety"></i> {tag}</span>
          <{h} class="hero__titulo">{t}</{h}>
          <p>{txt}</p>
          <div class="hero__botoes">
            <a href="/solicitar-proposta/" class="btn btn--destaque">Solicitar proposta <i class="fa-solid fa-arrow-right"></i></a>
            <a href="/servicos/" class="btn btn--contorno">Ver serviços</a>
          </div>
        </div>
      </div>
    </div>''' for i, (img, tag, t, txt, h) in enumerate(slides))

    perfis = "\n".join(f'''        <a href="/para-voce/#{s}" class="card-perfil anima" data-atraso="{i % 4}"><i class="{ic}"></i><h3>{n}</h3><p>{d}</p></a>''' for i, (s, n, ic, d, _) in enumerate(PERFIS))

    obras = "\n".join(f'''        <article class="card-projeto anima" data-atraso="{i % 3}">
          <img src="/assets/img/{img}.svg" alt="{t}" loading="lazy">
          <div class="card-projeto__info"><div><span>{dict(OBRAS_CATEGORIAS)[c]}</span><h3>{t}</h3></div><a href="/obras/" class="seta" aria-label="Ver obras"><i class="fa-solid fa-arrow-right"></i></a></div>
        </article>''' for i, (img, c, t) in enumerate(OBRAS))

    depo = [("MR", "Mariana R.", "Síndica — Condomínio residencial", "O laudo de inspeção predial foi claro e objetivo. Conseguimos priorizar a manutenção e apresentar tudo na assembleia com segurança."),
            ("CA", "Carlos A.", "Proprietário — Reforma comercial", "Precisávamos reformar e regularizar a loja com prazo apertado. A VAFF cuidou de tudo e nos manteve informados em cada etapa."),
            ("PS", "Paulo S.", "Proprietário — Construção residencial", "Construí morando fora de SC e acompanhei tudo pelos relatórios. A obra foi entregue sem surpresas.")]
    depo_html = "\n".join(f'''            <div class="depoimento"><div class="depoimento__caixa"><i class="fa-solid fa-quote-right aspas"></i>
              <div class="estrelas" aria-label="5 estrelas">{'<i class="fa-solid fa-star"></i>' * 5}</div>
              <p>“{t}”</p>
              <div class="depoimento__autor"><span class="avatar">{ini}</span><div><strong>{n}</strong><span>{c}</span></div></div>
            </div></div>''' for ini, n, c, t in depo)

    html = head("VAFF Engenharia — Construção, reformas, projetos e laudos em Florianópolis",
                "Engenharia de alto padrão livre de dor de cabeça: construção, reformas, projetos, laudos, vistorias e regularização na Grande Florianópolis e em SC.",
                "/", [org_ld()]) + f'''
  <main>
  <section class="hero" aria-label="Destaques">
{hero}
    <div class="hero__nav">
      <button type="button" data-hero="anterior" aria-label="Slide anterior"><i class="fa-solid fa-arrow-left"></i></button>
      <button type="button" data-hero="proximo" aria-label="Próximo slide"><i class="fa-solid fa-arrow-right"></i></button>
    </div>
    <div class="hero__pontos"></div>
  </section>

  <section class="secao secao--clara">
    <div class="container">
      {titulo_secao("O que fazemos", "Soluções completas em <span>engenharia</span>", "Doze frentes de atuação para cuidar do seu imóvel em todas as fases: do terreno ao pós-obra.")}
      <div class="hubs__grid">
        {cards_hubs()}
      </div>
    </div>
  </section>

  <section class="secao">
    <div class="container sobre__grid">
      <div class="sobre__imagens anima">
        <img class="img-principal" src="/assets/img/sobre-1.svg" alt="Equipe VAFF em obra" loading="lazy">
        <img class="img-secundaria" src="/assets/img/sobre-2.svg" alt="Vistoria técnica" loading="lazy">
        <div class="selo-experiencia"><strong>{ANOS}</strong><span>anos de<br>experiência</span></div>
      </div>
      <div class="sobre__texto anima" data-atraso="1">
        {titulo_secao("Sobre a VAFF", f"Sinônimo de <span>engenharia</span> desde {E['desde']}", centro=False)}
        <p class="sobre__destaque">Entregamos projetos e construções com uma experiência de alta qualidade e livre de dor de cabeça.</p>
        <p>Com uma equipe multidisciplinar de engenheiros, arquitetos e técnicos, unimos tecnologia e gestão para garantir resultados padronizados e foco total no sucesso do cliente. Nosso maior compromisso é o bem-estar e a segurança em cada m² contratado.</p>
        <ul class="lista-check">
          <li><i class="fa-solid fa-check"></i> Empresa registrada no CREA-SC</li>
          <li><i class="fa-solid fa-check"></i> ART em todos os serviços</li>
          <li><i class="fa-solid fa-check"></i> Engenheiro responsável dedicado</li>
          <li><i class="fa-solid fa-check"></i> Relatórios e transparência</li>
        </ul>
        <div class="sobre__rodape">
          <a href="/sobre/" class="btn btn--base">Conheça a VAFF <i class="fa-solid fa-arrow-right"></i></a>
          <div class="assinatura"><span class="avatar">VN</span><div><strong>Vladimir Nunes</strong><span>Diretor e Engenheiro Civil</span></div></div>
        </div>
      </div>
    </div>
  </section>

  <section class="secao secao--escura">
    <div class="container">
      {titulo_secao("Para você", "Encontre a solução pelo seu <span>perfil</span>", "Não sabe o nome do serviço? Comece por quem você é.", claro=True)}
      <div class="perfis__grid">
{perfis}
      </div>
    </div>
  </section>

  <section class="secao">
    <div class="container triangulo">
      <div class="anima">
        <svg class="triangulo__svg" viewBox="0 0 400 360" role="img" aria-label="Triângulo preço, prazo e qualidade">
          <polygon points="200,20 380,330 20,330" fill="rgba(7,7,173,0.06)" stroke="#0707ad" stroke-width="3"/>
          <polygon points="200,120 290,280 110,280" fill="#0f3760"/>
          <text x="200" y="235" text-anchor="middle" fill="#ffde00" font-size="26">VAFF</text>
          <circle cx="200" cy="20" r="14" fill="#ffde00"/><circle cx="380" cy="330" r="14" fill="#ffde00"/><circle cx="20" cy="330" r="14" fill="#ffde00"/>
          <text x="200" y="68" text-anchor="middle" fill="#0f3760" font-size="20">Qualidade</text>
          <text x="330" y="315" text-anchor="end" fill="#0f3760" font-size="20">Prazo</text>
          <text x="70" y="315" text-anchor="start" fill="#0f3760" font-size="20">Preço</text>
        </svg>
      </div>
      <div class="anima" data-atraso="1">
        {titulo_secao("Preço, prazo e qualidade", "O equilíbrio que define uma <span>boa obra</span>", "Toda obra equilibra três forças. Deixamos claro, desde a proposta, como cada escolha afeta as outras duas.", centro=False)}
        <ul class="triangulo__lista">
          <li><span class="num">1</span><div><h3>Qualidade não se negocia</h3><p>Especificações, normas técnicas e segurança estrutural são o ponto de partida de toda proposta.</p></div></li>
          <li><span class="num">2</span><div><h3>Prazo é compromisso</h3><p>Cronograma físico-financeiro realista, acompanhado e comunicado em cada etapa.</p></div></li>
          <li><span class="num">3</span><div><h3>Preço transparente</h3><p>Orçamento detalhado por etapa, sem letras miúdas, para você decidir com segurança.</p></div></li>
        </ul>
      </div>
    </div>
  </section>

  <section class="secao secao--clara">
    <div class="container">
      {titulo_secao("Antes de começar", "O que você precisa para <span>iniciar</span>", "Com essas informações conseguimos entender a sua demanda e enviar uma proposta assertiva.")}
      <div class="prereq__grid">
        <div class="card-prereq anima"><h3>O imóvel ou terreno</h3><p>Endereço, metragem aproximada e, se houver, matrícula e fotos do local.</p></div>
        <div class="card-prereq anima" data-atraso="1"><h3>O que já existe</h3><p>Projetos, laudos anteriores, orçamentos recebidos ou contratos em andamento.</p></div>
        <div class="card-prereq anima" data-atraso="2"><h3>Seu objetivo</h3><p>O que você quer resolver, construir ou reformar, e o padrão de acabamento desejado.</p></div>
        <div class="card-prereq anima" data-atraso="3"><h3>Prazo e investimento</h3><p>Quando precisa começar ou terminar e a faixa de investimento prevista.</p></div>
      </div>
    </div>
  </section>

  <section class="secao">
    <div class="container">
      <div class="projetos__topo">
        {titulo_secao("Obras", "Obras que falam por <span>nós</span>", centro=False)}
        <a href="/obras/" class="btn btn--escuro">Ver portfólio <i class="fa-solid fa-arrow-right"></i></a>
      </div>
      <div class="projetos__grid">
{obras}
      </div>
    </div>
  </section>

  <section class="secao secao--clara">
    <div class="container depoimentos__grid">
      <div class="anima">
        {titulo_secao("Depoimentos", "O que nossos <span>clientes</span> dizem", centro=False)}
        <div class="carrossel" aria-roledescription="carrossel"><div class="carrossel__trilho">
{depo_html}
        </div></div>
        <div class="carrossel__controles">
          <button type="button" data-carrossel="anterior" aria-label="Depoimento anterior"><i class="fa-solid fa-arrow-left"></i></button>
          <button type="button" data-carrossel="proximo" aria-label="Próximo depoimento"><i class="fa-solid fa-arrow-right"></i></button>
        </div>
      </div>
      <div class="form-box anima" data-atraso="1">
        <h3>Solicite uma proposta</h3>
        <p>Um engenheiro retorna o seu contato.</p>
        {form_proposta(claro=False, compacto=True)}
      </div>
    </div>
  </section>
  </main>
''' + CTA + foot()
    escrever("/", html)


# ===========================================================================
# Serviços (todos os hubs)
# ===========================================================================
def pagina_servicos():
    blocos = []
    for h in HUBS:
        subs = "".join(f'<a class="chip" href="{u}"><i class="fa-solid fa-angle-right"></i>{escape(I.nome(u))}</a>' for u in I.subhubs_do_hub(h["nome"]))
        blocos.append(f'''<div class="perfil-bloco anima" id="{h["slug"]}">
          <span class="perfil-bloco__icone"><i class="{h["icone"]}"></i></span>
          <div>
            <h2><a href="/{h["slug"]}/">{h["nome"]}</a></h2>
            <p>{h["resumo"]}</p>
            <div class="chips">{subs}</div>
            <a href="/{h["slug"]}/" class="link-mais">Ver {h["nome"].lower()} <i class="fa-solid fa-arrow-right"></i></a>
          </div>
        </div>''')
    html = head("Serviços — VAFF Engenharia", "Todos os serviços da VAFF Engenharia: construção, reformas, projetos, laudos, vistorias, perícias, gestão de obras, condomínios, consultoria, regularização, manutenção e instalações.",
                "/servicos/", [org_ld(), breadcrumb_ld([("Início", "/"), ("Serviços", "/servicos/")])]) + page_header("Serviços", []) + f'''
  <main>
  <section class="secao secao--clara">
    <div class="container">
      {titulo_secao("12 frentes de atuação", "Todos os nossos <span>serviços</span>", "Escolha a área e veja as categorias de serviço.")}
      <div class="hubs__grid">{cards_hubs()}</div>
    </div>
  </section>
  <section class="secao">
    <div class="container">
      {"".join(blocos)}
    </div>
  </section>
  </main>
''' + CTA + foot()
    escrever("/servicos/", html)


# ===========================================================================
# Páginas pilar dos hubs
# ===========================================================================
def pagina_hub(h):
    subs = "\n".join(f'<a href="{u}" class="card-subhub anima" data-atraso="{i % 3}"><h3><span>{i + 1:02d}</span>{escape(I.nome(u))}</h3><p>{len(I.filhos(u, "Página de serviço"))} serviços</p></a>'
                     for i, u in enumerate(I.subhubs_do_hub(h["nome"])))
    dest = "".join(f'<li><i class="fa-solid fa-check"></i> <a href="{I.url_por_palavra(d, "#subhubs")}">{d}</a></li>' for d in h["destaques"])
    guias = I.guias_do_hub(h["slug"])
    relacionados = [x for x in HUBS if x["slug"] != h["slug"]]
    idx = HUBS.index(h)
    rel = [relacionados[(idx + k) % len(relacionados)] for k in range(4)]
    marcas_rel = [(s, n) for _, cats in MARCAS for s, n, _, _, hubs in cats if h["slug"] in hubs]
    marcas_html = ""
    if marcas_rel:
        chips = "".join(f'<a class="chip" href="/marcas-e-sistemas/#{s}"><i class="fa-solid fa-tag"></i>{n}</a>' for s, n in marcas_rel)
        marcas_html = f'''<h3 style="margin:40px 0 16px;font-size:20px">Materiais e sistemas relacionados</h3><div class="chips">{chips}</div>'''

    ld = [org_ld(),
          {"@context": "https://schema.org", "@type": "Service", "name": h["pilar"], "serviceType": h["nome"],
           "description": h["resumo"], "provider": {"@type": "GeneralContractor", "name": E["nome"], "url": E["site"]},
           "areaServed": [c for c, _ in REGIOES], "url": f'{E["site"]}/{h["slug"]}/'},
          breadcrumb_ld([("Início", "/"), (h["nome"], f'/{h["slug"]}/')]),
          faq_ld(h["faq"])]
    html = head(f'{h["pilar"]} — VAFF Engenharia', f'{h["pilar"]}: {h["resumo"]} Atendimento na Grande Florianópolis e em SC.', "/servicos/", ld, url=f'/{h["slug"]}/') \
        + page_header(h["nome"], []) + f'''
  <main>
  <section class="secao">
    <div class="container pilar__intro">
      <div class="anima">
        {titulo_secao(h["nome"], h["pilar"], centro=False)}
        <p class="sobre__destaque">{h["resumo"]}</p>
        <p>Na VAFF, cada serviço de {h["nome"].lower()} é conduzido por um engenheiro responsável, com escopo claro, cronograma e ART. Você sabe o que está sendo feito, por quê e quanto custa, do primeiro contato à entrega.</p>
        {marcas_html}
      </div>
      <aside class="caixa-destaque anima" data-atraso="1" id="servicos">
        <h3>Serviços em destaque</h3>
        <ul class="lista-check">{dest}</ul>
        <a href="/solicitar-proposta/{h["form"]}/" class="btn btn--destaque">Solicitar proposta <i class="fa-solid fa-arrow-right"></i></a>
      </aside>
    </div>
  </section>

  <section class="secao secao--clara" id="subhubs">
    <div class="container">
      {titulo_secao("Categorias", f'Tudo em {h["nome"].lower()} em um só <span>lugar</span>')}
      <div class="subhubs__grid">
{subs}
      </div>
    </div>
  </section>
''' + processo() + (f'''
  <section class="secao">
    <div class="container">
      {titulo_secao("Materiais gratuitos", "Guias e <span>ferramentas</span>")}
      <div class="links__grid">{"".join(f'<a href="{u}" class="card-link anima"><h3>{escape(I.nome(u))}</h3><span class="link-mais">Acessar <i class="fa-solid fa-arrow-right"></i></span></a>' for u in guias)}</div>
    </div>
  </section>
''' if guias else "") + f'''
  <section class="secao secao--clara">
    <div class="container">
      {titulo_secao("Dúvidas frequentes", f'Perguntas sobre {h["nome"].lower()}')}
      <div class="faq">
{faq_html(h["faq"])}
      </div>
    </div>
  </section>

  <section class="secao">
    <div class="container">
      {titulo_secao("Veja também", "Serviços <span>relacionados</span>")}
      <div class="hubs__grid">{cards_hubs(rel)}</div>
    </div>
  </section>
  </main>
''' + CTA + foot()
    escrever(f'/{h["slug"]}/', html)


# ===========================================================================
# Marcas e sistemas
# ===========================================================================
def pagina_marcas():
    grupos = []
    for grupo, cats in MARCAS:
        cards = "".join(f'''<div class="card-marca anima" id="{s}">
            <h3><i class="{ic}"></i><a href="/marcas-e-sistemas/{s}/">{n}</a></h3>
            <p>{", ".join(f'<a href="{u}">{escape(I.PAG[u]["row"]["Marca / Operadora"] if I.PAG[u]["tipo"] == "Página de marca" else I.nome(u))}</a>' for u in I.filhos(f"/marcas-e-sistemas/{s}/", "Página de marca", "Página de sistema construtivo")) or marcas}</p>
            <p class="relacionados">Serviços relacionados: {", ".join(f'<a href="/{x}/">{HUB[x]["nome"]}</a>' for x in hubs)}</p>
          </div>''' for s, n, ic, marcas, hubs in cats)
        grupos.append(f'<div class="marcas__grupo"><h2>{grupo}</h2><div class="marcas__grid">{cards}</div></div>')
    html = head("Marcas e sistemas construtivos — VAFF Engenharia", "Materiais, acabamentos, equipamentos e sistemas construtivos com que a VAFF projeta, executa, instala e avalia obras em SC.",
                "/marcas-e-sistemas/", [org_ld(), breadcrumb_ld([("Início", "/"), ("Marcas e Sistemas", "/marcas-e-sistemas/")])]) \
        + page_header("Marcas e Sistemas", []) + f'''
  <main>
  <section class="secao">
    <div class="container">
      {titulo_secao("Materiais e sistemas", "Marcas e sistemas <span>construtivos</span>", "Projetamos, executamos, instalamos e avaliamos obras com os principais materiais, equipamentos e sistemas do mercado. Escolha a categoria e veja os serviços relacionados.")}
      {"".join(grupos)}
      <p class="aviso"><strong>Importante:</strong> as marcas citadas pertencem aos seus respectivos fabricantes e são mencionadas apenas como referência de materiais e equipamentos com que trabalhamos. A menção não indica parceria, credenciamento ou vínculo comercial com a VAFF Engenharia.</p>
    </div>
  </section>
  </main>
''' + CTA + foot()
    escrever("/marcas-e-sistemas/", html)


# ===========================================================================
# Para você (perfis)
# ===========================================================================
def pagina_para_voce():
    blocos = []
    for s, n, ic, d, hubs in PERFIS:
        chips = "".join(f'<a class="chip" href="/{x}/"><i class="{HUB[x]["icone"]}"></i>{HUB[x]["nome"]}</a>' for x in hubs)
        blocos.append(f'''<div class="perfil-bloco anima" id="{s}">
          <span class="perfil-bloco__icone"><i class="{ic}"></i></span>
          <div>
            <h2>Para {n.lower()}</h2>
            <p>{d}</p>
            <div class="chips">{chips}</div>
            <a href="{PERFIL_URL[s]}" class="link-mais">Ver soluções para {n.lower()} <i class="fa-solid fa-arrow-right"></i></a>
          </div>
        </div>''')
    html = head("Soluções por perfil — VAFF Engenharia", "Proprietários, síndicos, empresas, incorporadores, arquitetos, advogados, corretores e quem mora fora: encontre a solução de engenharia certa para você.",
                "/para-voce/", [org_ld(), breadcrumb_ld([("Início", "/"), ("Para você", "/para-voce/")])]) + page_header("Para você", []) + f'''
  <main>
  <section class="secao">
    <div class="container">
      {titulo_secao("Soluções por perfil", "Qual é o <span>seu caso</span>?", "Cada perfil tem dores diferentes. Veja os serviços mais indicados para você.")}
      {"".join(blocos)}
    </div>
  </section>
  </main>
''' + CTA + foot()
    escrever("/para-voce/", html)


# ===========================================================================
# Obras (portfólio)
# ===========================================================================
def pagina_obras():
    filtros = '<button type="button" class="ativo" data-filtro="*" aria-pressed="true">Todas</button>' + "".join(
        f'<button type="button" data-filtro="{s}" aria-pressed="false">{n}</button>' for s, n in OBRAS_CATEGORIAS)
    cards = "\n".join(f'''        <article class="card-projeto anima" data-atraso="{i % 3}" data-categoria="{c}">
          <img src="/assets/img/{img}.svg" alt="{t}" loading="lazy">
          <div class="card-projeto__info"><div><span>{dict(OBRAS_CATEGORIAS)[c]}</span><h3>{t}</h3></div><a href="/solicitar-proposta/" class="seta" aria-label="Quero uma obra assim"><i class="fa-solid fa-arrow-right"></i></a></div>
        </article>''' for i, (img, c, t) in enumerate(OBRAS))
    html = head("Obras e portfólio — VAFF Engenharia", "Portfólio de obras da VAFF Engenharia: residenciais, comerciais, saúde, educação, condomínios, edifícios e galpões em SC.",
                "/obras/", [org_ld(), breadcrumb_ld([("Início", "/"), ("Obras", "/obras/")])]) + page_header("Obras", [], "fundo-2.svg") + f'''
  <main>
  <section class="secao">
    <div class="container">
      <div class="projetos__topo">
        {titulo_secao("Portfólio", "Nossas <span>obras</span>", centro=False)}
        <div class="filtros" role="group" aria-label="Filtrar obras">{filtros}</div>
      </div>
      <div class="projetos__grid">
{cards}
      </div>
      <div class="chips" style="justify-content:center;margin-top:40px">{"".join(f'<a class="chip" href="/obras/{s}/"><i class="fa-solid fa-folder-open"></i>{n}</a>' for s, n in OBRAS_CATEGORIAS_PAGINAS)}</div>
      <p class="obras__aviso">Em breve: cada obra com desafio, solução, prazo, fotos e depoimento do cliente.</p>
    </div>
  </section>
  </main>
''' + CTA + foot()
    escrever("/obras/", html)


# ===========================================================================
# Sobre
# ===========================================================================
def pagina_sobre():
    equipe = [("equipe-1", "Vladimir Nunes", "Diretor e Engenheiro Civil"), ("equipe-2", "Juliane Carnelutti", "Gestora administrativa"),
              ("equipe-3", "Nome do colaborador", "Arquiteto(a)"), ("equipe-4", "Nome do colaborador", "Técnico(a) em edificações")]
    eq = "\n".join(f'<div class="membro anima" data-atraso="{i}"><div class="membro__foto"><img src="/assets/img/{img}.svg" alt="{n}" loading="lazy"></div><h3>{n}</h3><span>{c}</span></div>'
                   for i, (img, n, c) in enumerate(equipe))
    html = head("Sobre a VAFF Engenharia", f"Desde {E['desde']}, a VAFF Engenharia entrega excelência em projetos e obras em Santa Catarina. Conheça equipe, método, valores e garantia.",
                "/sobre/", [org_ld(), breadcrumb_ld([("Início", "/"), ("Sobre", "/sobre/")])]) + page_header("Sobre a VAFF", []) + f'''
  <main>
  <section class="secao">
    <div class="container sobre__grid">
      <div class="sobre__imagens anima">
        <img class="img-principal" src="/assets/img/sobre-1.svg" alt="Equipe VAFF em obra" loading="lazy">
        <img class="img-secundaria" src="/assets/img/sobre-2.svg" alt="Vistoria técnica" loading="lazy">
        <div class="selo-experiencia"><strong>{ANOS}</strong><span>anos de<br>experiência</span></div>
      </div>
      <div class="sobre__texto anima" data-atraso="1">
        {titulo_secao("Quem somos", "Engenharia que constrói <span>sonhos</span>", centro=False)}
        <p class="sobre__destaque">Desde {E['desde']}, a VAFF Engenharia entrega excelência em projetos e obras em todo o estado de Santa Catarina.</p>
        <p>Com uma equipe multidisciplinar de engenheiros, arquitetos e técnicos, unimos tecnologia e gestão para garantir resultados padronizados e foco total no sucesso do cliente. Nosso maior compromisso é o bem-estar e a segurança em cada m² contratado.</p>
        <ul class="lista-check">
          <li><i class="fa-solid fa-check"></i> {E["crea"]}</li>
          <li><i class="fa-solid fa-check"></i> Unidades em São José e Paulo Lopes</li>
          <li><i class="fa-solid fa-check"></i> Equipe multidisciplinar</li>
          <li><i class="fa-solid fa-check"></i> Suporte pós-obra</li>
        </ul>
        <div class="chips" style="margin-bottom:30px">
          <a class="chip" href="/sobre/equipe/"><i class="fa-solid fa-users"></i>Equipe</a>
          <a class="chip" href="/sobre/metodo/"><i class="fa-solid fa-diagram-project"></i>Como trabalhamos</a>
          <a class="chip" href="/sobre/reconhecimentos/"><i class="fa-solid fa-award"></i>Reconhecimentos</a>
          <a class="chip" href="/sobre/depoimentos/"><i class="fa-solid fa-comment-dots"></i>Depoimentos</a>
          <a class="chip" href="/sobre/garantia/"><i class="fa-solid fa-shield-halved"></i>Garantia</a>
        </div>
        <a href="/solicitar-proposta/" class="btn btn--base">Solicitar proposta <i class="fa-solid fa-arrow-right"></i></a>
      </div>
    </div>
  </section>

  <section class="secao secao--clara">
    <div class="container">
      {titulo_secao("Nosso nome, nossos valores", "Cada letra carrega um <span>valor</span>")}
      <div class="vaff__grid">
        <div class="card-letra anima"><div class="card-letra__letra">V</div><h3>Sonhar</h3><small>do grego</small><p>Nossa capacidade de inspirar e realizar os sonhos dos nossos clientes.</p></div>
        <div class="card-letra anima" data-atraso="1"><div class="card-letra__letra">A</div><h3>Planejar</h3><small>do grego</small><p>O cuidado e a precisão em cada etapa do planejamento.</p></div>
        <div class="card-letra anima" data-atraso="2"><div class="card-letra__letra">F</div><h3>Fomentar</h3><small>do italiano fomentare</small><p>O incentivo à inovação e ao desenvolvimento constante.</p></div>
        <div class="card-letra anima" data-atraso="3"><div class="card-letra__letra">F</div><h3>Fazer</h3><small>do italiano fare</small><p>Ação e compromisso com a excelência na execução dos projetos.</p></div>
      </div>
      <p class="citacao anima">Engenharia civil não é sobre construir coisas, mas sim construir sonhos.</p>
    </div>
  </section>

  <section class="secao">
    <div class="container">
      {titulo_secao("Missão e visão", "Quem somos e onde queremos <span>chegar</span>")}
      <div class="valores__grid">
        <div class="card-valor anima"><i class="fa-solid fa-bullseye"></i><h3>Missão</h3><p>Entregar projetos e construções com uma experiência de alta qualidade e livre de dor de cabeça.</p></div>
        <div class="card-valor anima" data-atraso="1"><i class="fa-solid fa-eye"></i><h3>Visão</h3><p>Expandir nossas operações para atuar em obras de grande porte e importância em todo o estado de Santa Catarina.</p></div>
        <div class="card-valor anima" data-atraso="2"><i class="fa-solid fa-gem"></i><h3>Valores</h3><p>Excelência, satisfação do cliente, pontualidade, responsabilidade e aprendizado contínuo.</p></div>
      </div>
    </div>
  </section>
''' + processo().replace('<section class="secao">', '<section class="secao secao--clara" id="metodo">', 1) + f'''
  <section class="secao" id="equipe">
    <div class="container">
      {titulo_secao("Equipe técnica", "Profissionais <span>qualificados</span>")}
      <div class="equipe__grid">
{eq}
      </div>
    </div>
  </section>

  <section class="secao secao--clara" id="garantia">
    <div class="container sobre__grid">
      <div class="anima">
        {titulo_secao("Garantia e pós-obra", "A obra acaba, o <span>compromisso</span> continua", centro=False)}
        <p>Ao final de cada obra entregamos a documentação técnica, as ARTs e as orientações de uso e manutenção do imóvel. Seguimos disponíveis para atendimento pós-obra e respondemos pela solidez e segurança da construção nos termos da legislação.</p>
      </div>
      <ul class="lista-check anima" data-atraso="1" style="grid-template-columns:1fr">
        <li><i class="fa-solid fa-check"></i> Entrega com documentação técnica e ART</li>
        <li><i class="fa-solid fa-check"></i> Manual de uso, operação e manutenção</li>
        <li><i class="fa-solid fa-check"></i> Canal direto para atendimento pós-obra</li>
        <li><i class="fa-solid fa-check"></i> Vistoria de acompanhamento após a entrega</li>
      </ul>
    </div>
  </section>
  </main>
''' + CTA + foot()
    escrever("/sobre/", html)


# ===========================================================================
# Conteúdo: blog e perguntas frequentes
# ===========================================================================
def pagina_blog():
    html = head("Conteúdo — VAFF Engenharia", "Artigos, guias e ferramentas sobre construção, reformas, laudos, condomínios e regularização de imóveis.",
                "/blog/", [org_ld(), breadcrumb_ld([("Início", "/"), ("Conteúdo", "/blog/")])]) + page_header("Conteúdo", []) + f'''
  <main>
  <section class="secao">
    <div class="container texto-corrido" style="text-align:center">
      {titulo_secao("Blog, guias e ferramentas", "Conteúdo para decidir <span>melhor</span>", "Guias práticos, ferramentas e respostas para as dúvidas mais comuns. Os artigos do blog serão publicados em breve.")}
      <div class="hero__botoes" style="justify-content:center">
        <a href="/guias/" class="btn btn--base">Guias gratuitos <i class="fa-solid fa-arrow-right"></i></a>
        <a href="/ferramentas/" class="btn btn--escuro">Ferramentas</a>
        <a href="/perguntas-frequentes/" class="btn btn--escuro">Perguntas frequentes</a>
      </div>
    </div>
  </section>
  </main>
''' + CTA + foot()
    escrever("/blog/", html)


def pagina_faq():
    todas = [(q, a) for h in HUBS for q, a in h["faq"]]
    secoes = "\n".join(f'''  <div class="marcas__grupo anima" id="{h["slug"]}"><h2>{h["nome"]}</h2><div class="faq" style="max-width:none">
{faq_html(h["faq"]).replace(' aberto', '')}
  </div></div>''' for h in HUBS)
    html = head("Perguntas frequentes — VAFF Engenharia", "Respostas para as dúvidas mais comuns sobre construção, reformas, projetos, laudos, vistorias, perícias, condomínios e regularização.",
                "/blog/", [org_ld(), breadcrumb_ld([("Início", "/"), ("Perguntas frequentes", "/perguntas-frequentes/")]), faq_ld(todas)]) \
        + page_header("Perguntas frequentes", [("Conteúdo", "/blog/")]) + f'''
  <main>
  <section class="secao">
    <div class="container">
{secoes}
    </div>
  </section>
  </main>
''' + CTA + foot()
    escrever("/perguntas-frequentes/", html)


# ===========================================================================
# Regiões
# ===========================================================================
def pagina_regioes():
    cards = "".join(f'<a href="/regioes/{REGIAO_SLUG[c]}/" class="card-regiao anima"><i class="fa-solid fa-location-dot"></i><div>{c}<small>{r}</small></div></a>' for c, r in REGIOES)
    html = head("Regiões atendidas — VAFF Engenharia", "A VAFF Engenharia atende Florianópolis, São José, Palhoça, Biguaçu, Balneário Camboriú, Itajaí, Joinville, Blumenau e todo o estado de Santa Catarina.",
                "", [org_ld(), breadcrumb_ld([("Início", "/"), ("Regiões atendidas", "/regioes/")])]) + page_header("Regiões atendidas", []) + f'''
  <main>
  <section class="secao secao--clara">
    <div class="container">
      {titulo_secao("Onde atuamos", "Grande Florianópolis e <span>todo o estado</span>", "Com unidades em São José e Paulo Lopes, atendemos as principais cidades de Santa Catarina. Não encontrou a sua? Fale com a gente.")}
      <div class="regioes__grid">{cards}</div>
      <div style="text-align:center;margin-top:50px"><a href="/solicitar-proposta/" class="btn btn--base">Solicitar proposta <i class="fa-solid fa-arrow-right"></i></a></div>
    </div>
  </section>
  </main>
''' + foot()
    escrever("/regioes/", html)


# ===========================================================================
# Contato e Solicitar proposta
# ===========================================================================
def cards_contato():
    return f'''<div class="contato__cards">
        <div class="card-contato anima"><span class="icone"><i class="fa-solid fa-phone-volume"></i></span><h3>Telefones</h3><p><a href="tel:{E["tel_link"]}">{E["tel"]}</a></p><p><a href="https://wa.me/{E["wpp_link"]}" target="_blank" rel="noopener">WhatsApp {E["wpp"]}</a></p><p>{E["horario"]}</p></div>
        <div class="card-contato anima" data-atraso="1"><span class="icone"><i class="fa-solid fa-envelope-open-text"></i></span><h3>E-mail</h3><p><a href="mailto:{E["email"]}">{E["email"]}</a></p><p><a href="{E["instagram"]}" target="_blank" rel="noopener">@vaffengenharia</a></p></div>
        <div class="card-contato anima" data-atraso="2"><span class="icone"><i class="fa-solid fa-location-dot"></i></span><h3>Unidades</h3><p><strong>São José:</strong> {E["end_sj"]}</p><p><strong>Paulo Lopes:</strong> {E["end_pl"]}</p></div>
      </div>'''


def pagina_contato():
    html = head("Contato — VAFF Engenharia", "Fale com a VAFF Engenharia: telefone, WhatsApp, e-mail e endereços em São José e Paulo Lopes/SC.",
                "/contato/", [org_ld(), breadcrumb_ld([("Início", "/"), ("Contato", "/contato/")])]) + page_header("Contato", []) + f'''
  <main>
  <section class="secao">
    <div class="container">
      {cards_contato()}
      <div class="contato__grid">
        <div class="anima">
          {titulo_secao("Fale conosco", "Envie sua <span>mensagem</span>", centro=False)}
          {form_proposta(compacto=True)}
        </div>
        <div class="mapa anima" data-atraso="1">
          <iframe src="https://www.google.com/maps?q=Av.+Nossa+Senhora+Aparecida,+746,+Barreiros,+S%C3%A3o+Jos%C3%A9+-+SC&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Mapa da VAFF Engenharia em São José"></iframe>
        </div>
      </div>
    </div>
  </section>
  </main>
''' + foot()
    escrever("/contato/", html)


def pagina_proposta():
    tipos = "".join(f'<a class="chip" href="/solicitar-proposta/{s}/"><i class="fa-solid fa-file-pen"></i>{n}</a>' for s, n in FORM_TIPOS)
    html = head("Solicitar proposta — VAFF Engenharia", "Solicite uma proposta para obra, reforma, laudo, vistoria, projeto, condomínio ou consultoria. Um engenheiro da VAFF retorna o seu contato.",
                "", [org_ld(), breadcrumb_ld([("Início", "/"), ("Solicitar proposta", "/solicitar-proposta/")])]) + page_header("Solicitar proposta", []) + f'''
  <main>
  <section class="secao">
    <div class="container contato__grid">
      <div class="anima">
        {titulo_secao("Proposta sem compromisso", "Conte para a gente o que você <span>precisa</span>", "Quanto mais detalhes, mais assertiva será a proposta. Se tiver fotos, projetos ou documentos, envie depois pelo WhatsApp.", centro=False)}
        <div class="chips" style="margin-bottom:30px">{tipos}</div>
        {form_proposta()}
      </div>
      <aside class="caixa-destaque anima" data-atraso="1" style="align-self:start">
        <h3>Como funciona</h3>
        <ul class="lista-check">
          <li><i class="fa-solid fa-check"></i> Você envia a solicitação</li>
          <li><i class="fa-solid fa-check"></i> Um engenheiro entra em contato</li>
          <li><i class="fa-solid fa-check"></i> Agendamos visita ou reunião</li>
          <li><i class="fa-solid fa-check"></i> Você recebe a proposta detalhada</li>
        </ul>
        <a href="https://wa.me/{E["wpp_link"]}" target="_blank" rel="noopener" class="btn btn--destaque"><i class="fa-brands fa-whatsapp"></i> Prefiro WhatsApp</a>
      </aside>
    </div>
  </section>
  </main>
''' + foot()
    escrever("/solicitar-proposta/", html)


def pagina_privacidade():
    html = head("Política de privacidade — VAFF Engenharia", "Como a VAFF Engenharia coleta, usa e protege os seus dados pessoais, em conformidade com a LGPD.",
                "", [org_ld()]) + page_header("Política de privacidade", []) + f'''
  <main>
  <section class="secao">
    <div class="container texto-corrido">
      <p><em>Modelo a ser revisado pelo jurídico da VAFF antes da publicação.</em></p>
      <h2>1. Quem somos</h2>
      <p>{E["razao"]}, CNPJ {E["cnpj"]}, com sede em {E["end_sj"]}, é a controladora dos dados pessoais tratados por meio deste site.</p>
      <h2>2. Dados que coletamos</h2>
      <ul>
        <li>Dados informados nos formulários: nome, telefone, e-mail, cidade, tipo de imóvel e a descrição da sua demanda.</li>
        <li>Dados de navegação coletados automaticamente, como páginas visitadas e tipo de dispositivo, quando houver ferramentas de análise instaladas.</li>
      </ul>
      <h2>3. Para que usamos</h2>
      <ul>
        <li>Responder às suas solicitações e elaborar propostas.</li>
        <li>Executar contratos e cumprir obrigações legais e regulatórias.</li>
        <li>Melhorar o site e a comunicação com você.</li>
      </ul>
      <h2>4. Compartilhamento</h2>
      <p>Não vendemos dados pessoais. Podemos compartilhá-los com prestadores de serviço necessários à operação (como hospedagem e e-mail) e com autoridades, quando exigido por lei.</p>
      <h2>5. Seus direitos</h2>
      <p>Nos termos da Lei nº 13.709/2018 (LGPD), você pode solicitar confirmação, acesso, correção, anonimização, portabilidade ou exclusão dos seus dados pelo e-mail <a href="mailto:{E["email"]}">{E["email"]}</a>.</p>
      <h2>6. Contato</h2>
      <p>Dúvidas sobre esta política: <a href="mailto:{E["email"]}">{E["email"]}</a> ou {E["tel"]}.</p>
    </div>
  </section>
  </main>
''' + foot()
    escrever("/politica-de-privacidade/", html)


# ===========================================================================
# Sitemap, robots e 404
# ===========================================================================
def extras():
    urls = "".join(f"  <url><loc>{E['site']}{u}</loc></url>\n" for u in PAGINAS if u not in NOINDEX)
    with open(os.path.join(RAIZ, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    with open(os.path.join(RAIZ, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nDisallow: /_build/\nSitemap: {E['site']}/sitemap.xml\n")
    html = head("Página não encontrada — VAFF Engenharia", "Página não encontrada.") + page_header("Página não encontrada", []) + f'''
  <main>
  <section class="secao">
    <div class="container texto-corrido" style="text-align:center">
      <p>A página que você procura não existe ou mudou de endereço.</p>
      <div class="hero__botoes" style="justify-content:center;margin-top:30px"><a href="/" class="btn btn--base">Ir para o início</a><a href="/servicos/" class="btn btn--escuro">Ver serviços</a></div>
    </div>
  </section>
  </main>
''' + foot()
    with open(os.path.join(RAIZ, "404.html"), "w", encoding="utf-8") as f:
        f.write(html)


def limpar_antigos():
    """Remove as páginas da versão anterior (arquivos soltos na raiz)."""
    for nome in ("sobre.html", "servicos.html", "contato.html"):
        p = os.path.join(RAIZ, nome)
        if os.path.exists(p):
            os.remove(p)


if __name__ == "__main__":
    limpar_antigos()
    pagina_home()
    pagina_servicos()
    for h in HUBS:
        pagina_hub(h)
    pagina_marcas()
    pagina_para_voce()
    pagina_obras()
    pagina_sobre()
    pagina_blog()
    pagina_faq()
    pagina_regioes()
    pagina_contato()
    pagina_proposta()
    pagina_privacidade()
    import paginas
    paginas.gerar(sys.modules[__name__])
    extras()
    print(f"{len(PAGINAS)} páginas geradas ({len(PAGINAS) - len(NOINDEX)} indexáveis, {len(NOINDEX)} noindex).")
