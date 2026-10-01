# -*- coding: utf-8 -*-
"""Páginas geradas a partir da planilha: subhubs, serviços, páginas locais,
marcas, sistemas construtivos, guias, ferramentas, perfis, regiões, obras,
subpáginas do Sobre e formulários por tipo. Artigos de blog não são gerados.

Chamado por build.py: paginas.gerar(build_module)
"""
from html import escape

import indice as I
from dados import (EMPRESA as E, HUBS, PERFIS, PERFIL_URL, REGIOES, REGIAO_SLUG, GRANDE_FLORIPA,
                   FORM_TIPOS, OBRAS_CATEGORIAS_PAGINAS, SISTEMAS_DESC, MARCAS)

B = None  # módulo build (helpers de layout), definido em gerar()


# ===========================================================================
# Blocos comuns
# ===========================================================================
def hub_de(url):
    seg = "/" + url.strip("/").split("/")[0] + "/"
    return I.HUB_URLS.get(seg)


def form_do(url):
    h = hub_de(url)
    return h["form"] if h else "obra-ou-reforma"


def ld_pagina(url, servico=None, faqs=None):
    itens = [("Início", "/")] + I.trilha(url) + [(I.nome(url), url)]
    ld = [B.org_ld(), B.breadcrumb_ld(itens)]
    if servico:
        ld.append({"@context": "https://schema.org", "@type": "Service", "name": servico,
                   "provider": {"@type": "GeneralContractor", "name": E["nome"], "url": E["site"]},
                   "areaServed": [c for c, _ in REGIOES], "url": E["site"] + url})
    if faqs:
        ld.append(B.faq_ld(faqs))
    return ld


def caixa_proposta(form, titulo="Solicite uma proposta"):
    return f'''<aside class="caixa-destaque anima" data-atraso="1">
        <h3>{titulo}</h3>
        <ul class="lista-check">
          <li><i class="fa-solid fa-check"></i> Engenheiro responsável dedicado</li>
          <li><i class="fa-solid fa-check"></i> Escopo, prazo e preço na proposta</li>
          <li><i class="fa-solid fa-check"></i> ART e documentação técnica</li>
          <li><i class="fa-solid fa-check"></i> Relatórios de acompanhamento</li>
        </ul>
        <a href="/solicitar-proposta/{form}/" class="btn btn--destaque">Solicitar proposta <i class="fa-solid fa-arrow-right"></i></a>
      </aside>'''


def cards_links(urls, icone="fa-solid fa-arrow-right"):
    out = []
    for i, u in enumerate(urls):
        p = I.PAG[u]
        txt = I.para_quem(p["row"].get("Intenção por trás da busca", "")) if p["tipo"] not in ("Página local", "Página local de bairro") else ""
        out.append(f'''<a href="{u}" class="card-link anima" data-atraso="{i % 3}">
          <h3>{escape(p["titulo"])}</h3>{f"<p>{escape(txt)}</p>" if txt else ""}
          <span class="link-mais">Ver detalhes <i class="{icone}"></i></span>
        </a>''')
    return "\n".join(out)


def chips_links(urls, icone="fa-solid fa-location-dot", rotulo=None):
    return "".join(f'<a class="chip" href="{u}"><i class="{icone}"></i>{escape(rotulo(u) if rotulo else I.nome(u))}</a>' for u in urls)


def secoes_html(url, contexto):
    """Seções (#ancora) vindas da planilha: sinônimos, termos de seguradora, banco, órgão etc."""
    rows = I.SECOES.get(url, [])
    if not rows:
        return ""
    blocos = []
    for r in rows:
        anc = I.ancora(r["URL sugerida"])
        kw = r["Palavra-chave"]
        consolidar = r.get("Consolidar em")
        if consolidar:
            txt = f"{kw} é atendido pela VAFF como parte do serviço de {I.minus(consolidar)}: mesmo escopo técnico, mesmo engenheiro responsável e o mesmo processo de trabalho."
        else:
            txt = I.para_quem(r.get("Intenção por trás da busca", "")) or f"Também atendemos {I.minus(kw)}."
        destino = I.link_da_nota(r.get("Nota"))
        extra = f' <a class="link-mais" href="{destino}">Ver serviço <i class="fa-solid fa-arrow-right"></i></a>' if destino else ""
        blocos.append(f'<div class="card-termo anima" id="{anc}"><h3>{escape(kw)}</h3><p>{escape(txt)}{extra}</p></div>')
    return f'''
  <section class="secao secao--clara">
    <div class="container">
      {B.titulo_secao("Termos relacionados", contexto)}
      <div class="termos__grid">{"".join(blocos)}</div>
    </div>
  </section>
'''


def relacionados(url):
    p = I.PAG[url]
    irmaos = [u for u in I.filhos(p["pai"], p["tipo"]) if u != url][:3]
    extra = [p["pai"]] if p["pai"] in I.PAG else []
    alvo = irmaos + extra
    if not alvo:
        return ""
    return f'''
  <section class="secao">
    <div class="container">
      {B.titulo_secao("Veja também", "Serviços <span>relacionados</span>")}
      <div class="links__grid">{cards_links(alvo)}</div>
    </div>
  </section>
'''


def faq_generico(kw, url):
    h = hub_de(url)
    faqs = [(f"Quanto custa {I.minus(kw)}?",
             "O valor depende do porte, da complexidade e da localização do imóvel. Depois de entender a sua demanda, enviamos uma proposta com escopo, prazo e preço detalhados, sem compromisso."),
            (f"A VAFF atende {I.minus(kw)} fora de Florianópolis?",
             "Sim. Atendemos toda a Grande Florianópolis e outras cidades de Santa Catarina. Fora da Grande Florianópolis, avaliamos o porte da obra para viabilizar o deslocamento da equipe.")]
    if h:
        faqs.append(h["faq"][0])
    return faqs


def secao_faq(faqs, titulo="Perguntas <span>frequentes</span>"):
    return f'''
  <section class="secao secao--clara">
    <div class="container">
      {B.titulo_secao("Dúvidas", titulo)}
      <div class="faq">
{B.faq_html(faqs)}
      </div>
    </div>
  </section>
'''


def pagina(url, titulo_meta, desc, corpo, ld, cta=True):
    html = (B.head(titulo_meta, desc, "", ld, url=url, noindex=I.noindex(url))
            + B.page_header(escape(I.nome(url)) if url in I.PAG else titulo_meta, I.trilha(url) if url in I.PAG else [])
            + "\n  <main>" + corpo + "\n  </main>\n" + (B.CTA if cta else "") + B.foot())
    B.escrever(url, html)


def desc_curta(txt):
    txt = " ".join(txt.split())
    return txt if len(txt) <= 158 else txt[:155].rsplit(" ", 1)[0] + "..."


# ===========================================================================
# Subhub
# ===========================================================================
def gerar_subhub(url):
    p = I.PAG[url]
    kw, h = p["titulo"], I.HUB_POR_NOME[p["hub"]]
    servs = I.filhos(url, "Página de serviço")
    pq = I.para_quem(p["row"]["Intenção por trás da busca"])
    corpo = f'''
  <section class="secao">
    <div class="container pilar__intro">
      <div class="anima">
        {B.titulo_secao(h["nome"], f"{escape(kw)} com a <span>VAFF</span>", centro=False)}
        {f'<p class="sobre__destaque">{escape(pq)}</p>' if pq else ""}
        <p>Reunimos aqui os serviços de {escape(I.minus(kw))} que a VAFF Engenharia realiza na Grande Florianópolis e em Santa Catarina. Escolha o serviço mais próximo da sua necessidade ou fale com nosso engenheiro para receber orientação.</p>
      </div>
      {caixa_proposta(h["form"])}
    </div>
  </section>

  <section class="secao secao--clara" id="servicos">
    <div class="container">
      {B.titulo_secao("Serviços", f"{len(servs)} serviços em {escape(I.minus(kw))}")}
      <div class="links__grid">{cards_links(servs)}</div>
    </div>
  </section>
''' + secoes_html(url, f"Também conhecido como") + B.processo() + secao_faq(h["faq"])
    pagina(url, f"{kw} | VAFF Engenharia", desc_curta(f"{kw}: {pq or h['resumo']} Atendimento na Grande Florianópolis e em SC."),
           corpo, ld_pagina(url, kw, h["faq"]))


# ===========================================================================
# Serviço
# ===========================================================================
def gerar_servico(url):
    p = I.PAG[url]
    kw, h = p["titulo"], I.HUB_POR_NOME.get(p["hub"]) or hub_de(url)
    pq = I.para_quem(p["row"]["Intenção por trás da busca"])
    locais = I.filhos(url, "Página local", "Página local de bairro")
    marcas_filhas = I.filhos(url, "Página de marca")
    floripa = " Florianópolis é a nossa praça principal, com equipe e fornecedores na região." if url in I.FLORIPA_PRINCIPAL else ""
    faqs = faq_generico(kw, url)
    bloco_locais = ""
    if locais:
        bloco_locais = f'''
  <section class="secao">
    <div class="container">
      {B.titulo_secao("Onde atendemos", f"{escape(kw)} por <span>cidade e bairro</span>")}
      <div class="chips" style="justify-content:center">{chips_links(locais, rotulo=lambda u: I.PAG[u]["row"].get("Local", I.nome(u)))}</div>
    </div>
  </section>
'''
    bloco_marcas = ""
    if marcas_filhas:
        bloco_marcas = f'''
  <section class="secao">
    <div class="container">
      {B.titulo_secao("Por empresa ou instituição", f"{escape(kw)} <span>por caso</span>")}
      <div class="chips" style="justify-content:center">{chips_links(marcas_filhas, "fa-solid fa-building", rotulo=lambda u: I.PAG[u]["row"].get("Marca / Operadora", I.nome(u)))}</div>
    </div>
  </section>
'''
    corpo = f'''
  <section class="secao">
    <div class="container pilar__intro">
      <div class="anima">
        {B.titulo_secao(h["nome"] if h else "Serviço", f"{escape(kw)} com engenharia de <span>alto padrão</span>", centro=False)}
        {f'<p class="sobre__destaque">{escape(pq)}</p>' if pq else ""}
        <p>A VAFF Engenharia cuida de {escape(I.minus(kw))} do diagnóstico à entrega, com engenheiro responsável, escopo e prazo definidos na proposta e emissão de ART. Atendemos Florianópolis, São José, Palhoça e toda a Grande Florianópolis, além de outras cidades de Santa Catarina.{floripa}</p>
        <ul class="lista-check">
          <li><i class="fa-solid fa-check"></i> Visita técnica e diagnóstico</li>
          <li><i class="fa-solid fa-check"></i> Proposta com escopo claro</li>
          <li><i class="fa-solid fa-check"></i> Execução acompanhada</li>
          <li><i class="fa-solid fa-check"></i> Entrega com documentação</li>
        </ul>
      </div>
      {caixa_proposta(h["form"] if h else "obra-ou-reforma")}
    </div>
  </section>
''' + secoes_html(url, "Também atendemos") + B.processo() + bloco_marcas + bloco_locais + secao_faq(faqs) + relacionados(url)
    pagina(url, f"{kw} em Florianópolis | VAFF Engenharia", desc_curta(f"{kw} na Grande Florianópolis e em SC. {pq} Engenheiro responsável e ART."),
           corpo, ld_pagina(url, kw, faqs))


# ===========================================================================
# Páginas locais (cidade, bairro e órgão municipal)
# ===========================================================================
def gerar_local(url):
    p = I.PAG[url]
    kw, r = p["titulo"], p["row"]
    pai = p["pai"]
    servico = I.nome(pai)
    local = r.get("Local") or r.get("Marca / Operadora", "")
    cidade = local.replace("Prefeitura de ", "")
    perto = cidade in GRANDE_FLORIPA or r.get("Tipo de local") == "Bairro"
    if r.get("Marca / Operadora", "").startswith("Prefeitura"):
        intro = f"Cuidamos de todo o processo de {I.minus(kw)}: levantamento de documentos, projetos para aprovação, protocolo e acompanhamento até a emissão."
    else:
        intro = f"A VAFF Engenharia realiza {I.minus(servico)} em {local}, com engenheiro responsável, escopo e prazo definidos na proposta e emissão de ART."
    atendimento = ("Equipe baseada na Grande Florianópolis, com unidades em São José e Paulo Lopes." if perto
                   else "Atendimento sob consulta, conforme o porte da obra, para viabilizar o deslocamento da equipe.")
    h = hub_de(url)
    corpo = f'''
  <section class="secao">
    <div class="container pilar__intro">
      <div class="anima">
        {B.titulo_secao(escape(local), f"{escape(kw)}", centro=False)}
        <p class="sobre__destaque">{escape(intro)}</p>
        <ul class="lista-check" style="grid-template-columns:1fr">
          <li><i class="fa-solid fa-check"></i> {escape(atendimento)}</li>
          <li><i class="fa-solid fa-check"></i> Conhecimento das exigências da prefeitura e dos órgãos locais</li>
          <li><i class="fa-solid fa-check"></i> Engenheiro responsável e ART</li>
          <li><i class="fa-solid fa-check"></i> Relatórios e comunicação transparente</li>
        </ul>
        <a href="{pai}" class="link-mais">Saiba mais sobre {escape(I.minus(servico))} <i class="fa-solid fa-arrow-right"></i></a>
      </div>
      {caixa_proposta(h["form"] if h else "obra-ou-reforma")}
    </div>
  </section>
''' + B.processo()
    pagina(url, f"{kw} | VAFF Engenharia", desc_curta(f"{kw}: {intro}"), corpo, ld_pagina(url, kw))


# ===========================================================================
# Marcas e sistemas
# ===========================================================================
AVISO_MATERIAL = ("As marcas citadas pertencem aos seus respectivos fabricantes e são mencionadas apenas como referência de "
                  "materiais e equipamentos com que trabalhamos. A menção não indica parceria, credenciamento ou vínculo comercial com a VAFF Engenharia.")


def aviso_independente(marca):
    return (f"A VAFF Engenharia atua de forma independente e não possui parceria, credenciamento ou vínculo com {marca}. "
            "Os nomes citados pertencem aos seus respectivos titulares e são usados apenas para identificar o caso atendido.")


def intro_marca(r):
    marca, termo, kw = r["Marca / Operadora"], r["Tipo de termo"], r["Palavra-chave"]
    if termo in ("Marca de material", "Marca de equipamento"):
        return (f"A VAFF Engenharia projeta, executa, instala e avalia obras com produtos de diversos fabricantes, entre eles {marca}, "
                "sempre de acordo com o projeto, as normas técnicas e as orientações do fabricante."), AVISO_MATERIAL
    if termo == "Seguradora":
        return (f"Laudo técnico independente para sinistros envolvendo apólices da {marca}: vistoria, caracterização da causa do dano "
                "e orçamento de reparo, para embasar o seu pedido de indenização."), aviso_independente(marca)
    if termo == "Banco":
        return (f"Avaliação e medição de obra de acordo com as exigências de engenharia do {marca} para financiamento e garantia, "
                "com laudo técnico e ART."), aviso_independente(marca)
    if termo == "Construtora":
        return (f"Comprou um imóvel da {marca}? A vistoria independente, feita por engenheiro, registra o estado do imóvel e "
                "os itens a corrigir antes de você receber as chaves."), aviso_independente(marca)
    if termo in ("Concessionária", "Órgão público"):
        return (f"Cuidamos de {I.minus(kw)}: projetos, documentação, protocolo e acompanhamento do processo junto à {marca} até a aprovação."), aviso_independente(marca)
    return (f"A VAFF Engenharia realiza {I.minus(kw)} com engenheiro responsável, escopo e prazo definidos na proposta."), aviso_independente(marca)


def gerar_categoria_marca(url):
    p = I.PAG[url]
    kw = p["titulo"]
    marcas = I.filhos(url, "Página de marca", "Página de sistema construtivo")
    eh_sistema = url.endswith("/sistemas-construtivos/")
    hubs_rel = next((hubs for _, cats in MARCAS for s, n, _, _, hubs in cats if f"/marcas-e-sistemas/{s}/" == url), [])
    intro = ("Dominar diferentes sistemas construtivos permite indicar a solução certa para cada terreno, prazo e orçamento. Conheça os sistemas com que a VAFF trabalha."
             if eh_sistema else
             f"Trabalhamos com {I.minus(kw)} de diversos fabricantes, sempre seguindo a especificação do projeto e as recomendações técnicas de cada marca. Escolha a marca para ver os serviços relacionados.")
    corpo = f'''
  <section class="secao">
    <div class="container">
      {B.titulo_secao("Marcas e sistemas", escape(kw), intro)}
      <div class="links__grid">{cards_links(marcas)}</div>
      {f'<h3 style="margin:60px 0 18px;font-size:20px;text-align:center">Serviços relacionados</h3><div class="chips" style="justify-content:center">' + "".join(f'<a class="chip" href="/{x}/"><i class="{I.HUB_URLS[f"/{x}/"]["icone"]}"></i>{I.HUB_URLS[f"/{x}/"]["nome"]}</a>' for x in hubs_rel) + "</div>" if hubs_rel else ""}
      <p class="aviso">{AVISO_MATERIAL}</p>
    </div>
  </section>
'''
    pagina(url, f"{kw}: marcas e serviços | VAFF Engenharia", desc_curta(f"{kw}: {intro}"), corpo, ld_pagina(url))


def gerar_marca(url):
    p = I.PAG[url]
    r, kw = p["row"], p["titulo"]
    marca = r["Marca / Operadora"]
    intro, aviso = intro_marca(r)
    info = I.MARCA_INFO.get(marca, {})
    filhos_serv = I.filhos(url, "Página de marca por serviço")
    pq = I.para_quem(r.get("Intenção por trás da busca", ""))
    faqs = []
    comp = (info.get("Exemplo de busca avaliativa / comparativa") or "").strip()
    if comp and r["Tipo de termo"] in ("Marca de material", "Marca de equipamento"):
        faqs.append((comp[0].upper() + comp[1:].rstrip("?") + "?",
                     "A escolha depende da aplicação, da especificação do projeto e da disponibilidade na região. Na fase de projeto, a VAFF compara as opções tecnicamente e indica a mais adequada para a sua obra, sem vínculo com fabricantes."))
    faqs.append((f"A VAFF tem parceria com {marca}?",
                 "Não. A VAFF Engenharia atua de forma independente, sem parceria, credenciamento ou vínculo comercial. Isso garante uma orientação técnica neutra para o cliente."))
    pai_servico = p["pai"] if p["pai"] in I.PAG and I.PAG[p["pai"]]["tipo"] == "Página de serviço" else None
    corpo = f'''
  <section class="secao">
    <div class="container pilar__intro">
      <div class="anima">
        {B.titulo_secao(escape(marca), escape(kw), centro=False)}
        <p class="sobre__destaque">{escape(intro)}</p>
        {f"<p>{escape(pq)}</p>" if pq else ""}
        {f'<a href="{pai_servico}" class="link-mais">Saiba mais sobre {escape(I.minus(I.nome(pai_servico)))} <i class="fa-solid fa-arrow-right"></i></a>' if pai_servico else ""}
      </div>
      {caixa_proposta(form_do(pai_servico or url))}
    </div>
  </section>
''' + secoes_html(url, f"O que fazemos com {escape(marca)}") + (f'''
  <section class="secao">
    <div class="container">
      {B.titulo_secao("Serviços", f"Serviços com {escape(marca)}")}
      <div class="links__grid">{cards_links(filhos_serv)}</div>
    </div>
  </section>
''' if filhos_serv else "") + secao_faq(faqs) + f'''
  <section class="secao" style="padding-top:0"><div class="container"><p class="aviso">{escape(aviso)}</p></div></section>
'''
    pagina(url, f"{kw} | VAFF Engenharia", desc_curta(f"{kw}: {intro}"), corpo, ld_pagina(url, kw, faqs))


def gerar_marca_por_servico(url):
    p = I.PAG[url]
    r, kw = p["row"], p["titulo"]
    marca = r["Marca / Operadora"]
    pq = I.para_quem(r.get("Intenção por trás da busca", ""))
    destino = I.link_da_nota(r.get("Nota"))
    corpo = f'''
  <section class="secao">
    <div class="container pilar__intro">
      <div class="anima">
        {B.titulo_secao(escape(marca), escape(kw), centro=False)}
        {f'<p class="sobre__destaque">{escape(pq)}</p>' if pq else ""}
        <p>A VAFF Engenharia realiza {escape(I.minus(kw))} seguindo o projeto, as normas técnicas e as orientações do fabricante, com engenheiro responsável e ART.</p>
        <p><a href="{p["pai"]}" class="link-mais">Ver tudo sobre {escape(marca)} <i class="fa-solid fa-arrow-right"></i></a>
        {f'&nbsp;&nbsp;<a href="{destino}" class="link-mais">Ver o serviço <i class="fa-solid fa-arrow-right"></i></a>' if destino else ""}</p>
      </div>
      {caixa_proposta(form_do(destino or url))}
    </div>
  </section>
  <section class="secao" style="padding-top:0"><div class="container"><p class="aviso">{escape(AVISO_MATERIAL)}</p></div></section>
'''
    pagina(url, f"{kw} | VAFF Engenharia", desc_curta(f"{kw}: {pq}"), corpo, ld_pagina(url, kw))


def gerar_sistema(url):
    p = I.PAG[url]
    kw = p["titulo"]
    desc = SISTEMAS_DESC.get(kw, "")
    filhos_serv = I.filhos(url, "Página de sistema por serviço")
    faqs = [(f"Vale a pena construir em {I.minus(kw)}?",
             "Depende do terreno, do projeto, do prazo e do orçamento. Na consultoria inicial, comparamos o sistema com as alternativas e indicamos a solução mais adequada para a sua obra."),
            (f"A VAFF executa obras em {I.minus(kw)}?",
             "Sim. Projetamos, executamos e fiscalizamos obras em diferentes sistemas construtivos, sempre com engenheiro responsável e ART.")]
    corpo = f'''
  <section class="secao">
    <div class="container pilar__intro">
      <div class="anima">
        {B.titulo_secao("Sistema construtivo", escape(kw), centro=False)}
        <p class="sobre__destaque">{escape(desc)}</p>
        <p>Antes de escolher o sistema, avaliamos o clima litorâneo de Santa Catarina, o tipo de solo, o prazo desejado, o custo total e a manutenção ao longo da vida útil da edificação.</p>
      </div>
      {caixa_proposta("obra-ou-reforma")}
    </div>
  </section>
''' + secoes_html(url, f"Serviços em {escape(I.minus(kw))}") + (f'''
  <section class="secao">
    <div class="container">
      {B.titulo_secao("Serviços", f"{escape(kw)} na <span>prática</span>")}
      <div class="links__grid">{cards_links(filhos_serv)}</div>
    </div>
  </section>
''' if filhos_serv else "") + secao_faq(faqs)
    pagina(url, f"{kw}: o que é e quando usar | VAFF Engenharia", desc_curta(f"{kw}: {desc}"), corpo, ld_pagina(url, kw, faqs))


def gerar_sistema_por_servico(url):
    p = I.PAG[url]
    kw = p["titulo"]
    pq = I.para_quem(p["row"].get("Intenção por trás da busca", ""))
    corpo = f'''
  <section class="secao">
    <div class="container pilar__intro">
      <div class="anima">
        {B.titulo_secao("Sistemas construtivos", escape(kw), centro=False)}
        {f'<p class="sobre__destaque">{escape(pq)}</p>' if pq else ""}
        <p>A VAFF Engenharia conduz {escape(I.minus(kw))} do estudo de viabilidade à entrega: projeto compatibilizado, planejamento, execução acompanhada e ART.</p>
        <a href="{p["pai"]}" class="link-mais">Conheça o sistema <i class="fa-solid fa-arrow-right"></i></a>
      </div>
      {caixa_proposta("obra-ou-reforma")}
    </div>
  </section>
''' + B.processo()
    pagina(url, f"{kw} | VAFF Engenharia", desc_curta(f"{kw}: {pq}"), corpo, ld_pagina(url, kw))


# ===========================================================================
# Guias, ferramentas e página pilar de conteúdo
# ===========================================================================
def form_material(assunto, botao, campos_extra=""):
    return f'''<form class="formulario formulario--claro" data-mailto="{E["email"]}">
          <input type="hidden" name="Material" value="{escape(assunto)}">
          <div class="linha">
            <input name="Nome" type="text" placeholder="Seu nome" required autocomplete="name" aria-label="Nome">
            <input name="Telefone" type="tel" placeholder="Telefone / WhatsApp" autocomplete="tel" aria-label="Telefone">
          </div>
          <input name="E-mail" type="email" placeholder="Seu e-mail" required autocomplete="email" aria-label="E-mail">{campos_extra}
          <button type="submit" class="btn btn--base">{botao} <i class="fa-solid fa-paper-plane"></i></button>
          <p class="form-msg" role="status">Obrigado! Seu aplicativo de e-mail foi aberto para concluir o envio.</p>
        </form>'''


def gerar_guia(url):
    p = I.PAG[url]
    kw = p["titulo"]
    h = I.HUB_URLS.get(p["pai"])
    corpo = f'''
  <section class="secao">
    <div class="container contato__grid">
      <div class="anima">
        {B.titulo_secao("Guia gratuito", escape(kw), centro=False)}
        <p class="sobre__destaque">Material prático da VAFF Engenharia para você se organizar e tomar decisões com mais segurança{f" em {escape(I.minus(h['nome']))}" if h else ""}.</p>
        <p>Preencha o formulário para receber o guia por e-mail. Se quiser conversar com nosso engenheiro sobre o seu caso, é só responder a mensagem.</p>
        {f'<a href="{p["pai"]}" class="link-mais">Conheça os serviços de {escape(I.minus(h["nome"]))} <i class="fa-solid fa-arrow-right"></i></a>' if h else ""}
      </div>
      <div class="anima" data-atraso="1">
        {form_material(kw, "Quero receber o guia")}
      </div>
    </div>
  </section>
'''
    pagina(url, f"{kw}: guia gratuito | VAFF Engenharia", desc_curta(f"Baixe o guia gratuito {kw} da VAFF Engenharia."), corpo, ld_pagina(url))


def gerar_calculadora(url):
    p = I.PAG[url]
    kw = p["titulo"]
    campos = '''
          <div class="linha">
            <input name="Área (m²)" type="number" min="1" placeholder="Área aproximada (m²)" required aria-label="Área aproximada em metros quadrados">
            <select name="Padrão" required aria-label="Padrão de acabamento"><option value="">Padrão de acabamento</option><option>Médio</option><option>Alto</option><option>Luxo</option></select>
          </div>
          <input name="Cidade" type="text" placeholder="Cidade e bairro" aria-label="Cidade e bairro">'''
    corpo = f'''
  <section class="secao">
    <div class="container contato__grid">
      <div class="anima">
        {B.titulo_secao("Ferramenta", escape(kw), centro=False)}
        <p class="sobre__destaque">Informe a área, o padrão de acabamento e a localização para receber uma faixa de investimento de referência, calculada pela engenharia da VAFF.</p>
        <p>A estimativa é uma referência inicial. O valor final depende do projeto, das especificações e das condições do terreno ou do imóvel.</p>
      </div>
      <div class="anima" data-atraso="1">
        {form_material(kw, "Receber estimativa", campos)}
      </div>
    </div>
  </section>
'''
    pagina(url, f"{kw} | VAFF Engenharia", desc_curta(f"{kw}: receba uma faixa de investimento de referência da VAFF Engenharia."), corpo, ld_pagina(url))


def gerar_pilar_nbr16280(url):
    kw = I.PAG[url]["titulo"]
    faqs = [("A NBR 16280 vale para qualquer reforma?", "Vale para reformas que possam afetar a segurança da edificação, seus sistemas ou as áreas comuns, como intervenções em estrutura, vedações, instalações, impermeabilização e fachadas. Na dúvida, o síndico deve exigir o plano de reforma."),
            ("Quem elabora o plano de reforma?", "Um profissional habilitado, engenheiro ou arquiteto, que assume a responsabilidade técnica com a emissão de ART ou RRT."),
            ("O síndico pode impedir uma reforma?", "O síndico deve analisar o plano e pode condicionar ou não autorizar a obra quando houver risco à edificação ou descumprimento das regras do condomínio. Para isso, pode contar com uma análise técnica independente.")]
    corpo = f'''
  <section class="secao">
    <div class="container texto-corrido">
      <p class="sobre__destaque">A ABNT NBR 16280 estabelece como devem ser planejadas, autorizadas, executadas e registradas as reformas em edificações, especialmente em condomínios. O objetivo é proteger a segurança do prédio e de quem vive nele.</p>

      <h2>O que a norma exige</h2>
      <ul>
        <li><strong>Plano de reforma</strong> elaborado por profissional habilitado, com descrição da intervenção, impactos nos sistemas da edificação, projetos, cronograma, materiais e medidas de segurança.</li>
        <li><strong>Responsabilidade técnica</strong> registrada por ART (engenheiro) ou RRT (arquiteto).</li>
        <li><strong>Análise e autorização</strong> do responsável legal pela edificação, normalmente o síndico, antes do início da obra.</li>
        <li><strong>Execução conforme o plano</strong>, com identificação dos prestadores, respeito às regras e horários do condomínio e descarte correto de resíduos.</li>
        <li><strong>Encerramento e registro</strong>: ao final, a documentação deve ser arquivada e o manual e o histórico da edificação atualizados.</li>
      </ul>

      <h2>Antes da reforma</h2>
      <p>O condômino contrata o responsável técnico, que elabora o plano de reforma. O plano é entregue ao síndico, que analisa se a intervenção é segura e compatível com a edificação e com a convenção. Só depois da autorização a obra pode começar.</p>

      <h2>Durante a reforma</h2>
      <p>A obra deve seguir o que foi aprovado. Mudanças de escopo exigem atualização do plano. O síndico pode acompanhar e solicitar informações, e qualquer situação de risco deve ser comunicada.</p>

      <h2>Depois da reforma</h2>
      <p>Com a obra concluída, o responsável técnico declara o encerramento e a documentação passa a fazer parte do histórico da edificação, importante para futuras manutenções, vendas e eventuais disputas.</p>

      <h2>Responsabilidades de cada um</h2>
      <ul>
        <li><strong>Proprietário ou morador:</strong> contratar profissional habilitado, apresentar o plano e seguir as regras do condomínio.</li>
        <li><strong>Responsável técnico:</strong> elaborar o plano, emitir ART ou RRT e garantir que a execução siga as normas.</li>
        <li><strong>Síndico:</strong> analisar, autorizar ou não, acompanhar e arquivar a documentação.</li>
      </ul>

      <h2>Como a VAFF ajuda</h2>
      <p>Para condôminos, elaboramos o plano de reforma com ART e acompanhamos a obra. Para síndicos e administradoras, analisamos os planos recebidos, emitimos parecer técnico e orientamos a decisão, reduzindo a responsabilidade do condomínio.</p>
      <p><a href="/condominios/" class="link-mais">Engenharia para condomínios <i class="fa-solid fa-arrow-right"></i></a> &nbsp; <a href="/guias/nbr-16280-resumo-para-sindicos/" class="link-mais">Baixar o resumo para síndicos <i class="fa-solid fa-arrow-right"></i></a></p>
      <p class="aviso">Este conteúdo é um resumo orientativo e não substitui a leitura da norma ABNT NBR 16280 nem a análise de um profissional habilitado.</p>
    </div>
  </section>
''' + secao_faq(faqs)
    ld = ld_pagina(url, None, faqs)
    ld.append({"@context": "https://schema.org", "@type": "Article", "headline": kw, "author": {"@type": "Organization", "name": E["nome"]}})
    pagina(url, "NBR 16280: guia de reforma em condomínio | VAFF Engenharia",
           "Entenda o que a NBR 16280 exige antes, durante e depois de uma reforma em condomínio, e as responsabilidades do morador, do responsável técnico e do síndico.", corpo, ld)


def gerar_indices_conteudo():
    guias = [u for u, p in I.PAG.items() if p["tipo"] in ("Guia para download", "Página pilar de conteúdo")]
    ferramentas = [u for u, p in I.PAG.items() if p["tipo"] == "Calculadora"]
    for url, titulo, lista, sub in (("/guias/", "Guias", guias, "Materiais práticos e guias completos para você decidir com segurança."),
                                    ("/ferramentas/", "Ferramentas", ferramentas, "Ferramentas para estimar o investimento da sua obra.")):
        corpo = f'''
  <section class="secao">
    <div class="container">
      {B.titulo_secao("Conteúdo", titulo, sub)}
      <div class="links__grid">{cards_links(lista)}</div>
    </div>
  </section>
'''
        html = (B.head(f"{titulo} | VAFF Engenharia", sub, "/blog/", [B.org_ld(), B.breadcrumb_ld([("Início", "/"), ("Conteúdo", "/blog/"), (titulo, url)])], url=url)
                + B.page_header(titulo, [("Conteúdo", "/blog/")]) + "\n  <main>" + corpo + "\n  </main>\n" + B.CTA + B.foot())
        B.escrever(url, html)


# ===========================================================================
# Perfis, regiões, obras, sobre e formulários
# ===========================================================================
def gerar_perfis():
    guias_todos = [u for u, p in I.PAG.items() if p["tipo"] in ("Guia para download", "Página pilar de conteúdo")]
    for s, nome_p, ic, d, hubs in PERFIS:
        url = PERFIL_URL[s]
        guias = [u for u in guias_todos if any(I.PAG[u]["pai"].startswith(f"/{x}/") for x in hubs)][:6]
        corpo = f'''
  <section class="secao">
    <div class="container pilar__intro">
      <div class="anima">
        {B.titulo_secao("Para você", f"Engenharia para <span>{escape(nome_p.lower())}</span>", centro=False)}
        <p class="sobre__destaque">{escape(d)}</p>
        <p>Selecionamos os serviços que mais fazem diferença para o seu perfil. Se não encontrar exatamente o que procura, fale com nosso engenheiro e indicamos o caminho certo.</p>
      </div>
      {caixa_proposta("obra-ou-reforma", "Fale com nosso engenheiro")}
    </div>
  </section>
  <section class="secao secao--clara">
    <div class="container">
      {B.titulo_secao("Serviços indicados", "O que a VAFF faz por <span>você</span>")}
      <div class="hubs__grid">{B.cards_hubs([I.HUB_URLS[f"/{x}/"] for x in hubs])}</div>
    </div>
  </section>
''' + (f'''
  <section class="secao">
    <div class="container">
      {B.titulo_secao("Materiais gratuitos", "Guias para o seu <span>perfil</span>")}
      <div class="links__grid">{cards_links(guias)}</div>
    </div>
  </section>
''' if guias else "")
        titulo = f"Para {nome_p.lower()}"
        html = (B.head(f"{titulo} | VAFF Engenharia", desc_curta(d), "/para-voce/", [B.org_ld(), B.breadcrumb_ld([("Início", "/"), ("Para você", "/para-voce/"), (titulo, url)])], url=url)
                + B.page_header(titulo, [("Para você", "/para-voce/")]) + "\n  <main>" + corpo + "\n  </main>\n" + B.CTA + B.foot())
        B.escrever(url, html)


def gerar_regioes():
    for cidade, regiao in REGIOES:
        url = f"/regioes/{REGIAO_SLUG[cidade]}/"
        locais = [u for u, p in I.PAG.items() if p["tipo"] in ("Página local", "Página local de bairro")
                  and (p["row"].get("Local") == cidade or p["row"].get("Marca / Operadora") == f"Prefeitura de {cidade}")]
        perto = cidade in GRANDE_FLORIPA
        corpo = f'''
  <section class="secao">
    <div class="container pilar__intro">
      <div class="anima">
        {B.titulo_secao(escape(regiao), f"Engenharia em <span>{escape(cidade)}</span>", centro=False)}
        <p class="sobre__destaque">Construção, reformas, projetos, laudos, vistorias e regularização em {escape(cidade)}, com engenheiro responsável e ART.</p>
        <p>{"Nossa equipe está baseada na Grande Florianópolis, com unidades em São José e Paulo Lopes, o que garante agilidade nas visitas e no acompanhamento das obras." if perto else f"Atendemos {escape(cidade)} conforme o porte da obra, com o mesmo padrão de engenharia, relatórios e transparência."}</p>
      </div>
      {caixa_proposta("obra-ou-reforma")}
    </div>
  </section>
''' + (f'''
  <section class="secao secao--clara">
    <div class="container">
      {B.titulo_secao("Serviços locais", f"Serviços em <span>{escape(cidade)}</span>")}
      <div class="links__grid">{cards_links(locais)}</div>
    </div>
  </section>
''' if locais else "") + f'''
  <section class="secao">
    <div class="container">
      {B.titulo_secao("Áreas de atuação", "Todos os <span>serviços</span>")}
      <div class="hubs__grid">{B.cards_hubs()}</div>
    </div>
  </section>
'''
        titulo = f"Engenharia em {cidade}"
        ld = [B.org_ld(), B.breadcrumb_ld([("Início", "/"), ("Regiões atendidas", "/regioes/"), (cidade, url)])]
        html = (B.head(f"{titulo} | VAFF Engenharia", f"Construção, reformas, projetos, laudos e vistorias em {cidade}/SC com a VAFF Engenharia.", "", ld, url=url)
                + B.page_header(titulo, [("Regiões atendidas", "/regioes/")]) + "\n  <main>" + corpo + "\n  </main>\n" + B.CTA + B.foot())
        B.escrever(url, html)


def gerar_obras_categorias():
    for s, n in OBRAS_CATEGORIAS_PAGINAS:
        url = f"/obras/{s}/"
        I.NOINDEX_URLS.add(url)  # sem obras reais publicadas ainda
        corpo = f'''
  <section class="secao">
    <div class="container texto-corrido" style="text-align:center">
      {B.titulo_secao("Portfólio", f"Obras <span>{escape(n.lower())}</span>", "Em breve publicaremos aqui as obras desta categoria, com desafio, solução, prazo, fotos e depoimento do cliente.")}
      <div class="hero__botoes" style="justify-content:center"><a href="/obras/" class="btn btn--escuro">Ver todas as obras</a><a href="/solicitar-proposta/" class="btn btn--base">Quero uma obra assim</a></div>
    </div>
  </section>
'''
        html = (B.head(f"Obras {n.lower()} | VAFF Engenharia", f"Obras {n.lower()} realizadas pela VAFF Engenharia.", "/obras/",
                       [B.org_ld(), B.breadcrumb_ld([("Início", "/"), ("Obras", "/obras/"), (n, url)])], url=url, noindex=True)
                + B.page_header(f"Obras: {n}", [("Obras", "/obras/")], "fundo-2.svg") + "\n  <main>" + corpo + "\n  </main>\n" + B.CTA + B.foot())
        B.escrever(url, html)


def gerar_sobre_subpaginas():
    equipe = [("equipe-1", "Vladimir Nunes", "Diretor e Engenheiro Civil"), ("equipe-2", "Juliane Carnelutti", "Gestora administrativa"),
              ("equipe-3", "Nome do colaborador", "Arquiteto(a)"), ("equipe-4", "Nome do colaborador", "Técnico(a) em edificações")]
    eq = "\n".join(f'<div class="membro anima" data-atraso="{i}"><div class="membro__foto"><img src="/assets/img/{img}.svg" alt="{n}" loading="lazy"></div><h3>{n}</h3><span>{c}</span></div>'
                   for i, (img, n, c) in enumerate(equipe))
    paginas = {
        "/sobre/equipe/": ("Equipe técnica", "Conheça a equipe multidisciplinar de engenheiros, arquitetos e técnicos da VAFF Engenharia.", f'''
  <section class="secao">
    <div class="container">
      {B.titulo_secao("Equipe técnica", "Profissionais <span>qualificados</span>", "Engenheiros, arquitetos e técnicos que unem tecnologia e gestão para entregar resultados padronizados.")}
      <div class="equipe__grid">{eq}</div>
    </div>
  </section>
'''),
        "/sobre/metodo/": ("Como trabalhamos", "O método da VAFF Engenharia: contato, diagnóstico, planejamento, execução acompanhada e entrega com documentação.",
                           B.processo() + f'''
  <section class="secao secao--clara">
    <div class="container">
      {B.titulo_secao("Nossos compromissos", "Preço, prazo e <span>qualidade</span>")}
      <div class="valores__grid">
        <div class="card-valor anima"><i class="fa-solid fa-medal"></i><h3>Qualidade</h3><p>Especificações, normas técnicas e segurança estrutural como ponto de partida de toda proposta.</p></div>
        <div class="card-valor anima" data-atraso="1"><i class="fa-solid fa-calendar-check"></i><h3>Prazo</h3><p>Cronograma físico-financeiro realista, acompanhado e comunicado em cada etapa.</p></div>
        <div class="card-valor anima" data-atraso="2"><i class="fa-solid fa-file-invoice-dollar"></i><h3>Preço</h3><p>Orçamento detalhado por etapa, sem letras miúdas.</p></div>
      </div>
    </div>
  </section>
'''),
        "/sobre/reconhecimentos/": ("Reconhecimentos e eventos", "Registros, reconhecimentos e participação da VAFF Engenharia em eventos do setor.", f'''
  <section class="secao">
    <div class="container texto-corrido" style="text-align:center">
      {B.titulo_secao("Reconhecimentos", "Registro e <span>credibilidade</span>", f"A VAFF Engenharia é registrada no {E['crea']}. Em breve publicaremos aqui prêmios, associações e eventos de que participamos.")}
      <a href="https://portal.crea-sc.org.br/" target="_blank" rel="noopener" class="btn btn--base">Consultar no CREA-SC <i class="fa-solid fa-arrow-up-right-from-square"></i></a>
    </div>
  </section>
'''),
        "/sobre/depoimentos/": ("Depoimentos", "O que os clientes dizem sobre a VAFF Engenharia.", f'''
  <section class="secao">
    <div class="container texto-corrido" style="text-align:center">
      {B.titulo_secao("Depoimentos", "O que nossos <span>clientes</span> dizem", "Em breve publicaremos aqui depoimentos de clientes, com autorização de cada um.")}
      <a href="{E["instagram"]}" target="_blank" rel="noopener" class="btn btn--base">Veja nossas obras no Instagram <i class="fa-brands fa-instagram"></i></a>
    </div>
  </section>
'''),
        "/sobre/garantia/": ("Garantia e pós-obra", "Documentação, manual de uso e atendimento pós-obra da VAFF Engenharia.", f'''
  <section class="secao">
    <div class="container sobre__grid">
      <div class="anima">
        {B.titulo_secao("Garantia e pós-obra", "A obra acaba, o <span>compromisso</span> continua", centro=False)}
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
'''),
    }
    for url, (titulo, desc, corpo) in paginas.items():
        html = (B.head(f"{titulo} | VAFF Engenharia", desc, "/sobre/", [B.org_ld(), B.breadcrumb_ld([("Início", "/"), ("Sobre", "/sobre/"), (titulo, url)])],
                       url=url, noindex=url in I.NOINDEX_URLS)
                + B.page_header(titulo, [("Sobre", "/sobre/")]) + "\n  <main>" + corpo + "\n  </main>\n" + B.CTA + B.foot())
        B.escrever(url, html)


def gerar_formularios():
    for s, n in FORM_TIPOS:
        url = f"/solicitar-proposta/{s}/"
        corpo = f'''
  <section class="secao">
    <div class="container contato__grid">
      <div class="anima">
        {B.titulo_secao("Proposta sem compromisso", f"Proposta para <span>{escape(n.lower())}</span>", "Quanto mais detalhes, mais assertiva será a proposta. Fotos, projetos e documentos podem ser enviados depois pelo WhatsApp.", centro=False)}
        {B.form_proposta(tipo_padrao=s)}
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
'''
        html = (B.head(f"Solicitar proposta: {n.lower()} | VAFF Engenharia", f"Solicite uma proposta de {n.lower()} à VAFF Engenharia.", "",
                       [B.org_ld(), B.breadcrumb_ld([("Início", "/"), ("Solicitar proposta", "/solicitar-proposta/"), (n, url)])], url=url)
                + B.page_header(n, [("Solicitar proposta", "/solicitar-proposta/")]) + "\n  <main>" + corpo + "\n  </main>\n" + B.foot())
        B.escrever(url, html)


# ===========================================================================
# Entrada
# ===========================================================================
GERADORES = {
    "Página de subhub": gerar_subhub,
    "Página de serviço": gerar_servico,
    "Página local": gerar_local,
    "Página local de bairro": gerar_local,
    "Página de categoria de marca": gerar_categoria_marca,
    "Página de marca": gerar_marca,
    "Página de marca por serviço": gerar_marca_por_servico,
    "Página de sistema construtivo": gerar_sistema,
    "Página de sistema por serviço": gerar_sistema_por_servico,
    "Guia para download": gerar_guia,
    "Calculadora": gerar_calculadora,
    "Página pilar de conteúdo": gerar_pilar_nbr16280,
}


def gerar(build_module):
    global B
    B = build_module
    gerar_obras_categorias()  # antes, para registrar noindex
    for url, p in I.PAG.items():
        GERADORES[p["tipo"]](url)
    gerar_indices_conteudo()
    gerar_perfis()
    gerar_regioes()
    gerar_sobre_subpaginas()
    gerar_formularios()
