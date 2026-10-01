# -*- coding: utf-8 -*-
"""Dados do site VAFF Engenharia.

Fonte: planilha "vaff-engenharia-mapa-de-servicos-marcas-e-arquitetura" (abas
Arquitetura, Menu, Hubs e Mapa de Serviços) e Manual de Marca VAFF 2.1.
Edite aqui e rode `python3 _build/build.py` para regenerar as páginas.
"""

EMPRESA = {
    "nome": "VAFF Engenharia",
    "razao": "VAFF Engenharia Ltda.",
    "cnpj": "27.967.285/0001-90",
    "crea": "CREA-SC 159203-5",
    "tel": "(48) 3375-8253",
    "tel_link": "+554833758253",
    "wpp": "(48) 99905-3954",
    "wpp_link": "5548999053954",
    "email": "contato@vaff.com.br",
    "instagram": "https://www.instagram.com/vaffengenharia/",
    "site": "https://www.vaff.com.br",
    "horario": "Seg a Sex: 07h30 às 17h",
    "end_sj": "Av. Nossa Senhora Aparecida, 746, sala 02 — Barreiros, São José/SC",
    "end_pl": "Rua Geral Morro Agudo, 100 — Paulo Lopes/SC",
    "frase": "Engenharia de alto padrão, livre de dor de cabeça.",
    "desde": 2014,
}

# ---------------------------------------------------------------------------
# 12 hubs de serviço (aba Hubs + Arquitetura + Menu)
# ---------------------------------------------------------------------------
HUBS = [
    {
        "slug": "construcao", "nome": "Construção", "icone": "fa-solid fa-house-chimney",
        "pilar": "Construtora de alto padrão em Florianópolis",
        "resumo": "Execução de casas, edifícios e obras comerciais do zero, incluindo sistemas construtivos, fundações e áreas externas.",
        "personas": ["Patrimonialista Ocupado", "Recém-Chegado", "Construtor por Paixão", "Dono que Não Pode Parar", "Incorporador Enxuto"],
        "subhubs": ["Construção de casas de alto padrão", "Sistemas construtivos", "Ambientes e anexos residenciais", "Edifícios residenciais", "Obras comerciais e corporativas", "Obras de saúde", "Obras educacionais e institucionais", "Hotelaria e turismo", "Galpões e obras industriais", "Fundações, contenções e terraplenagem", "Áreas externas e lazer"],
        "destaques": ["Construção de casa de alto padrão", "Construção de casa em condomínio fechado", "Construção de casa de praia", "Construção de casa de campo", "Construção de casa térrea", "Construção de sobrado"],
        "form": "obra-ou-reforma",
        "faq": [
            ("A VAFF constrói a partir do projeto de outro arquiteto?", "Sim. Executamos obras a partir de projetos arquitetônicos de terceiros, fazendo a compatibilização com os projetos complementares antes do início da obra."),
            ("Como é definido o orçamento da construção?", "O orçamento é elaborado a partir dos projetos e do memorial descritivo, com planilha de quantitativos e cronograma físico-financeiro, para que você saiba o que está sendo contratado em cada etapa."),
            ("Quais sistemas construtivos vocês executam?", "Trabalhamos com concreto armado, alvenaria estrutural, estrutura metálica e outros sistemas, indicados conforme o projeto, o terreno, o prazo e o orçamento."),
        ],
    },
    {
        "slug": "reformas", "nome": "Reformas", "icone": "fa-solid fa-paint-roller",
        "pilar": "Empresa de reforma de alto padrão",
        "resumo": "Reformas residenciais, comerciais e por ambiente, retrofit, acessibilidade e acabamentos.",
        "personas": ["Patrimonialista Ocupado", "Recém-Chegado", "Proprietário à Distância", "Dono que Não Pode Parar", "Investidor de Renda"],
        "subhubs": ["Reformas residenciais", "Reformas por ambiente", "Ampliações", "Reformas comerciais", "Reformas de áreas comuns", "Retrofit e revitalização", "Acessibilidade", "Acabamentos de alto padrão", "Demolição"],
        "destaques": ["Reforma de casa", "Reforma de apartamento de alto padrão", "Reforma de escritório", "Reforma de clínica", "Reforma residencial", "Reforma de apartamento"],
        "form": "obra-ou-reforma",
        "faq": [
            ("Reforma de apartamento precisa de laudo ou ART?", "Sim. A NBR 16280 exige plano de reforma com responsável técnico e ART, apresentado ao síndico antes do início da obra. A VAFF elabora toda essa documentação."),
            ("Vocês acompanham a reforma se eu morar fora?", "Sim. Fazemos gestão completa com relatórios, fotos e reuniões on-line, para que você acompanhe tudo sem precisar estar presente."),
            ("É possível reformar com o imóvel ocupado?", "Depende do escopo. Planejamos as etapas para reduzir o impacto no dia a dia e informamos com antecedência quando a desocupação é recomendada."),
        ],
    },
    {
        "slug": "projetos", "nome": "Projetos de Engenharia", "icone": "fa-solid fa-compass-drafting",
        "pilar": "Projetos de engenharia",
        "resumo": "Projetos complementares, estruturais, aprovações, compatibilização, orçamento e planejamento técnico.",
        "personas": ["Travado pela Burocracia", "Arquiteto", "Incorporador Enxuto", "Patrimonialista Ocupado"],
        "subhubs": ["Projetos estruturais", "Projetos elétricos", "Projetos de sistemas e automação", "Projetos hidrossanitários", "Projetos de gás", "Projetos preventivos contra incêndio", "Projetos de climatização e conforto", "Projetos especiais", "Projetos para aprovação", "Coordenação e compatibilização", "Orçamento e planejamento"],
        "destaques": ["Projeto estrutural", "Projeto elétrico", "Projeto de entrada de energia", "Projeto hidrossanitário", "Projeto preventivo contra incêndio", "Orçamento de obra"],
        "form": "projeto",
        "faq": [
            ("Quais projetos são necessários para construir uma casa?", "Em geral: arquitetônico, estrutural, elétrico, hidrossanitário e, conforme o caso, preventivo contra incêndio, gás e climatização. Indicamos exatamente o que a sua obra exige."),
            ("O que é compatibilização de projetos?", "É a verificação cruzada entre todos os projetos para eliminar interferências, como uma tubulação atravessando uma viga, antes que virem retrabalho na obra."),
            ("Vocês aprovam o projeto na prefeitura?", "Sim. Preparamos os projetos para aprovação e acompanhamos o processo junto à prefeitura e ao Corpo de Bombeiros."),
        ],
    },
    {
        "slug": "laudos-tecnicos", "nome": "Laudos Técnicos", "icone": "fa-solid fa-file-signature",
        "pilar": "Laudo técnico de engenharia",
        "resumo": "Laudos de patologias, estrutura, instalações, sinistros, vizinhança e finalidades legais.",
        "personas": ["Assustado", "Comprador Cauteloso", "Vítima de Sinistro", "Síndico Profissional", "Advogado"],
        "subhubs": ["Laudos estruturais", "Laudos de umidade e patologias", "Laudos de instalações", "Laudos de sinistro e seguros", "Laudos de vizinhança", "Laudos de conformidade e desempenho", "Laudos para finalidades legais"],
        "destaques": ["Laudo estrutural", "Laudo de rachaduras", "Laudo de infiltração", "Laudo de vícios construtivos", "Laudo de sinistro", "Laudo de danos por vendaval"],
        "form": "laudo-ou-vistoria",
        "faq": [
            ("Rachadura na parede é perigosa?", "Nem toda fissura indica risco, mas só uma avaliação técnica consegue dizer a causa e a gravidade. O laudo identifica a origem e indica a solução adequada."),
            ("O laudo serve para acionar o seguro ou a construtora?", "Sim. O laudo técnico com ART é o documento que comprova a causa do dano e embasa pedidos à seguradora, à construtora ou ações judiciais."),
            ("Quanto tempo leva para emitir um laudo?", "Depende do tipo e do porte do imóvel. Após a vistoria, informamos o prazo de entrega na proposta."),
        ],
    },
    {
        "slug": "vistorias-e-inspecoes", "nome": "Vistorias e Inspeções", "icone": "fa-solid fa-magnifying-glass",
        "pilar": "Vistoria técnica de imóveis",
        "resumo": "Vistorias de entrega, compra, locação, cautelares, inspeção predial e ensaios técnicos.",
        "personas": ["Recebedor de Chaves", "Comprador Cauteloso", "Síndico Profissional", "Vizinho de Obra"],
        "subhubs": ["Vistorias de entrega e recebimento", "Vistorias de compra e locação", "Vistorias técnicas", "Inspeções prediais e técnicas", "Ensaios e monitoramento"],
        "destaques": ["Vistoria de entrega de apartamento", "Vistoria de imóvel antes da compra", "Vistoria cautelar", "Inspeção predial", "Vistoria de entrega de casa", "Assistência técnica em recebimento de condomínio novo"],
        "form": "laudo-ou-vistoria",
        "faq": [
            ("Por que fazer vistoria antes de receber as chaves?", "Porque é o momento de registrar os defeitos para que a construtora corrija antes da entrega. Depois de assinado o termo de recebimento, a negociação fica mais difícil."),
            ("O que é vistoria cautelar?", "É o registro técnico do estado dos imóveis vizinhos antes de uma obra começar, protegendo quem constrói e quem mora ao lado."),
            ("Condomínio é obrigado a fazer inspeção predial?", "A inspeção periódica é recomendada pela NBR 16747 e exigida por leis municipais em diversas cidades. Ela orienta a manutenção e protege o síndico."),
        ],
    },
    {
        "slug": "pericias-e-avaliacoes", "nome": "Perícias e Avaliações", "icone": "fa-solid fa-scale-balanced",
        "pilar": "Perícia de engenharia",
        "resumo": "Perícias judiciais e extrajudiciais, assistência técnica, pareceres e avaliação de imóveis.",
        "personas": ["Advogado", "Traído", "Herdeiros", "Comprador Cauteloso"],
        "subhubs": ["Perícias judiciais e extrajudiciais", "Pareceres técnicos", "Avaliação de imóveis"],
        "destaques": ["Parecer técnico para ação contra construtora", "Avaliação de imóvel de alto padrão", "Estimativa de custo de reforma para compra de imóvel", "Perícia judicial", "Perícia extrajudicial", "Assistência técnica em perícia judicial"],
        "form": "laudo-ou-vistoria",
        "faq": [
            ("Qual a diferença entre perícia judicial e assistência técnica?", "O perito é nomeado pelo juiz. O assistente técnico é contratado por uma das partes para acompanhar a perícia e defender tecnicamente seus interesses."),
            ("Posso contratar um parecer antes de entrar com a ação?", "Sim. O parecer técnico prévio ajuda o advogado a avaliar a viabilidade do caso e a fundamentar o pedido."),
            ("A avaliação de imóvel segue alguma norma?", "Sim, a NBR 14653, que define os métodos e o grau de fundamentação da avaliação."),
        ],
    },
    {
        "slug": "gestao-de-obras", "nome": "Gestão e Fiscalização de Obras", "icone": "fa-solid fa-list-check",
        "pilar": "Gestão de obras",
        "resumo": "Gestão, administração, fiscalização, auditoria, controle e responsabilidade técnica de obras.",
        "personas": ["Patrimonialista Ocupado", "Proprietário à Distância", "Incorporador Enxuto", "Síndico Profissional", "Traído"],
        "subhubs": ["Gestão e administração de obras", "Fiscalização e acompanhamento", "Auditoria e controle", "Responsabilidade técnica", "Obras paralisadas e retomadas", "Segurança do trabalho em obras", "Pós-obra e garantia", "Gestão de resíduos e obra limpa"],
        "destaques": ["Gestão de obras residenciais", "Gestão de obra à distância", "Gestão de obra para estrangeiros", "Gestão de obra de casa de veraneio", "Administração de obras", "Retomada de obra paralisada"],
        "form": "obra-ou-reforma",
        "faq": [
            ("Qual a diferença entre gestão e fiscalização de obra?", "Na gestão, a VAFF coordena a obra: fornecedores, compras, cronograma e custos. Na fiscalização, verificamos se quem está executando segue o projeto, as normas e o contrato."),
            ("Vocês assumem uma obra que está parada?", "Sim. Fazemos o levantamento do que foi executado, avaliamos a qualidade, refazemos o planejamento e retomamos a obra."),
            ("Como acompanho a obra de longe?", "Com relatórios periódicos, fotos, medições e reuniões on-line, além de um engenheiro responsável como ponto único de contato."),
        ],
    },
    {
        "slug": "condominios", "nome": "Condomínios", "icone": "fa-solid fa-building",
        "pilar": "Engenharia para condomínios",
        "resumo": "Assessoria técnica a síndicos e administradoras, fiscalização, memorial, NBR 16280 e manutenção.",
        "personas": ["Síndico Profissional", "Administradora"],
        "subhubs": ["Assessoria técnica ao síndico", "Fiscalização de obras em condomínio", "Cotação e contratação de obras", "Reformas nas unidades e NBR 16280", "Planejamento de manutenção", "Treinamentos e conteúdo técnico"],
        "destaques": ["Assessoria técnica para síndicos", "Participação técnica em assembleia", "Fiscalização de obras de condomínio", "Fiscalização de reforma de fachada", "Elaboração de memorial descritivo para cotação", "Análise de planos de reforma de unidades"],
        "form": "condominio",
        "faq": [
            ("Como a VAFF ajuda o síndico na NBR 16280?", "Analisamos os planos de reforma enviados pelos condôminos, emitimos parecer e orientamos o síndico sobre o que autorizar, reduzindo a responsabilidade dele."),
            ("Por que fazer memorial descritivo antes de cotar uma obra?", "Porque sem um escopo técnico igual para todos, as propostas não são comparáveis. O memorial garante que o condomínio compare preço do mesmo serviço."),
            ("Vocês participam de assembleias?", "Sim. Apresentamos laudos, orçamentos e planos de manutenção em linguagem clara para os condôminos."),
        ],
    },
    {
        "slug": "consultoria", "nome": "Consultoria Técnica", "icone": "fa-solid fa-comments",
        "pilar": "Consultoria em engenharia civil",
        "resumo": "Consultoria presencial, online e internacional, segunda opinião, viabilidade e treinamentos.",
        "personas": ["Traído", "Recém-Chegado", "Construtor por Paixão", "Incorporador Enxuto", "Arquiteto"],
        "subhubs": ["Consultoria técnica", "Consultoria para decisões de compra e construção", "Consultoria especializada", "Consultoria por segmento", "Viabilidade e due diligence", "Sustentabilidade e eficiência"],
        "destaques": ["Consultoria técnica online", "Consultoria técnica internacional", "Segunda opinião técnica sobre obra em andamento", "Visita técnica", "Revisão técnica de proposta de construtora", "Consultoria técnica presencial"],
        "form": "consultoria",
        "faq": [
            ("Como funciona a consultoria on-line?", "Você envia fotos, projetos ou documentos e fazemos uma reunião por vídeo com um engenheiro, que orienta sobre o problema e os próximos passos."),
            ("O que é segunda opinião técnica?", "É a avaliação independente de uma obra, orçamento ou diagnóstico feito por outro profissional, para você decidir com segurança."),
            ("Vocês analisam a proposta de uma construtora?", "Sim. Revisamos escopo, especificações, cronograma e preços para identificar lacunas antes de você assinar."),
        ],
    },
    {
        "slug": "regularizacao", "nome": "Regularização e Aprovações", "icone": "fa-solid fa-file-shield",
        "pilar": "Regularização de imóveis",
        "resumo": "Alvarás, habite-se, averbação, CNO, Bombeiros, Vigilância Sanitária, ambiental e acessibilidade legal.",
        "personas": ["Travado pela Burocracia", "Patrimonialista Ocupado", "Dono que Não Pode Parar", "Herdeiros"],
        "subhubs": ["Regularização de obras e imóveis", "Alvarás e habite-se", "Registro e obrigações da obra", "Bombeiros e Vigilância Sanitária", "Terreno e ambiental"],
        "destaques": ["Regularização de obra", "Obtenção de habite-se", "Averbação de construção", "Aprovação no Corpo de Bombeiros", "Regularização de construção sem projeto", "Regularização de ampliação"],
        "form": "projeto",
        "faq": [
            ("É possível regularizar uma construção feita sem projeto?", "Na maioria dos casos, sim. Fazemos o levantamento, os projetos de regularização e acompanhamos o processo até a aprovação."),
            ("Para que serve a averbação da construção?", "Para que a área construída conste na matrícula do imóvel, o que é necessário para vender, financiar ou fazer inventário."),
            ("Vocês cuidam da aprovação no Corpo de Bombeiros?", "Sim. Elaboramos o projeto preventivo (PPCI) e acompanhamos a vistoria até a emissão do atestado."),
        ],
    },
    {
        "slug": "recuperacao-e-manutencao", "nome": "Recuperação e Manutenção", "icone": "fa-solid fa-screwdriver-wrench",
        "pilar": "Manutenção e recuperação de edificações",
        "resumo": "Recuperação e reforço estrutural, impermeabilização, fachadas e manutenção predial.",
        "personas": ["Síndico Profissional", "Patrimonialista Ocupado", "Proprietário à Distância", "Assustado"],
        "subhubs": ["Recuperação e reforço estrutural", "Impermeabilização e umidade", "Fachadas", "Manutenção predial"],
        "destaques": ["Impermeabilização", "Reforma de fachada", "Revisão pré-temporada de imóvel", "Recuperação estrutural", "Reforço estrutural", "Reforço de fundação"],
        "form": "obra-ou-reforma",
        "faq": [
            ("Infiltração sempre exige quebrar o piso?", "Não necessariamente. Primeiro identificamos a origem da umidade; a solução pode ser localizada, evitando demolições desnecessárias."),
            ("De quanto em quanto tempo a fachada precisa de manutenção?", "Depende do revestimento e da exposição. Em regiões litorâneas, a inspeção periódica é ainda mais importante por causa da maresia."),
            ("O que é revisão pré-temporada?", "É uma vistoria preventiva no imóvel de veraneio antes da temporada, para corrigir problemas antes da chegada da família ou dos hóspedes."),
        ],
    },
    {
        "slug": "instalacoes", "nome": "Instalações e Sistemas", "icone": "fa-solid fa-plug-circle-bolt",
        "pilar": "Instalações prediais",
        "resumo": "Instalações elétricas, hidráulicas, gás, climatização, automação, energia solar e equipamentos.",
        "personas": ["Patrimonialista Ocupado", "Dono que Não Pode Parar", "Síndico Profissional"],
        "subhubs": ["Instalações elétricas", "Energia solar e eficiência", "Automação e segurança", "Instalações hidráulicas e gás", "Climatização e combate a incêndio", "Elevadores e acessibilidade vertical"],
        "destaques": ["Instalação elétrica", "Reforma de instalação elétrica", "Troca de fiação", "Adequação de quadro elétrico", "Aumento de carga elétrica", "Instalação de gerador"],
        "form": "obra-ou-reforma",
        "faq": [
            ("Quando é preciso trocar a fiação do imóvel?", "Em instalações antigas, com disjuntores desarmando, aquecimento de tomadas ou aumento de equipamentos. Uma avaliação indica se é caso de adequação ou troca completa."),
            ("Preciso de projeto para aumentar a carga elétrica?", "Sim. O aumento de carga exige projeto e solicitação à concessionária, que a VAFF prepara e acompanha."),
            ("Vocês integram automação e energia solar?", "Sim. Projetamos e executamos as instalações de forma integrada, já prevendo a infraestrutura desses sistemas."),
        ],
    },
]
HUB = {h["slug"]: h for h in HUBS}

# ---------------------------------------------------------------------------
# Marcas e sistemas (aba Menu). Sem logotipos e sem sugerir parceria.
# ---------------------------------------------------------------------------
MARCAS = [
    ("Materiais básicos e estruturais", [
        ("tubos-e-conexoes", "Tubos e conexões", "fa-solid fa-faucet", "Tigre, Amanco, Krona", ["projetos", "instalacoes"]),
        ("cimento-e-concreto", "Cimento e concreto", "fa-solid fa-cubes", "Votorantim, Itambé, InterCement, CSN Cimentos", ["construcao", "recuperacao-e-manutencao"]),
        ("aco-para-construcao", "Aço para construção", "fa-solid fa-bars-staggered", "Gerdau, ArcelorMittal, CSN", ["construcao", "laudos-tecnicos"]),
    ]),
    ("Acabamentos", [
        ("revestimentos-ceramicos", "Revestimentos cerâmicos", "fa-solid fa-border-all", "Portobello, Eliane, Portinari, Decortiles, Incepa, Roca Cerâmica", ["reformas", "laudos-tecnicos"]),
        ("metais-e-loucas", "Metais e louças", "fa-solid fa-sink", "Deca, Docol, Lorenzetti, Tramontina, Celite, Roca, Grohe, Hansgrohe, Kohler", ["reformas", "instalacoes"]),
        ("argamassas-e-rejuntes", "Argamassas e rejuntes", "fa-solid fa-trowel", "Quartzolit, Votomassa", ["reformas", "recuperacao-e-manutencao"]),
        ("tintas", "Tintas", "fa-solid fa-fill-drip", "Suvinil, Coral, Sherwin-Williams, Lukscolor", ["reformas", "recuperacao-e-manutencao"]),
        ("drywall-e-forros", "Drywall e forros", "fa-solid fa-table-cells-large", "Placo, Knauf", ["reformas", "construcao"]),
        ("pisos-madeira-e-vinilicos", "Pisos de madeira e vinílicos", "fa-solid fa-grip-lines", "Durafloor, Eucafloor, Indusparquet, Tarkett, Quick-Step", ["reformas"]),
        ("superficies-e-pedras", "Superfícies e pedras", "fa-solid fa-gem", "Dekton, Silestone, Neolith", ["reformas"]),
        ("vidros", "Vidros", "fa-solid fa-window-maximize", "Cebrace, Guardian, Saint-Gobain Glass", ["construcao", "reformas"]),
        ("paineis-madeira", "Painéis de madeira", "fa-solid fa-layer-group", "Duratex, Arauco, Berneck", ["reformas"]),
    ]),
    ("Proteção e cobertura", [
        ("impermeabilizantes", "Impermeabilizantes", "fa-solid fa-droplet-slash", "Viapol, Vedacit, Sika, Quartzolit, Denver Impermeabilizantes, MC-Bauchemie", ["recuperacao-e-manutencao", "laudos-tecnicos"]),
        ("telhas-e-coberturas", "Telhas e coberturas", "fa-solid fa-house", "Brasilit, Eternit, Tégula, Owens Corning, IKO, Kingspan Isoeste", ["construcao", "laudos-tecnicos"]),
    ]),
    ("Equipamentos", [
        ("elevadores", "Elevadores", "fa-solid fa-elevator", "TK Elevator, Otis, Atlas Schindler, Daiken", ["instalacoes", "condominios"]),
        ("climatizacao", "Climatização", "fa-solid fa-snowflake", "Daikin, LG, Samsung, Midea, Carrier, Fujitsu, Gree, Trane", ["projetos", "instalacoes"]),
        ("aquecimento-a-gas", "Aquecimento a gás", "fa-solid fa-fire-flame-simple", "Rinnai, Komeco, Bosch", ["projetos", "instalacoes"]),
        ("geradores", "Geradores", "fa-solid fa-car-battery", "WEG, Cummins, Stemac", ["instalacoes"]),
        ("energia-solar", "Energia solar", "fa-solid fa-solar-panel", "WEG, Canadian Solar, Jinko Solar, Fronius, Growatt", ["instalacoes", "projetos"]),
        ("automacao", "Automação", "fa-solid fa-microchip", "Control4, Crestron, Savant, Lutron, Intelbras", ["projetos", "instalacoes"]),
        ("seguranca-eletronica", "Segurança eletrônica", "fa-solid fa-video", "Intelbras, Hikvision", ["instalacoes"]),
        ("material-eletrico", "Material elétrico", "fa-solid fa-bolt", "Schneider Electric, Legrand, Pial Legrand, Siemens, WEG", ["projetos", "instalacoes"]),
        ("piscinas", "Piscinas", "fa-solid fa-water-ladder", "Sodramar, Nautilus, Jacuzzi, Dancor", ["construcao", "instalacoes"]),
    ]),
    ("Sistemas construtivos", [
        ("sistemas-construtivos", "Sistemas construtivos", "fa-solid fa-building-columns", "Steel frame, Wood frame, Estrutura metálica, Concreto armado, Alvenaria estrutural, Madeira laminada cruzada, Pré-moldado de concreto, Paredes de concreto, Concreto protendido, Laje nervurada", ["construcao", "projetos"]),
    ]),
]

# ---------------------------------------------------------------------------
# Personas (aba Arquitetura: Para você)
# ---------------------------------------------------------------------------
PERFIS = [
    ("proprietarios", "Proprietários", "fa-solid fa-house-user", "Quer construir, reformar ou resolver um problema no imóvel com segurança e sem dor de cabeça.", ["construcao", "reformas", "laudos-tecnicos", "gestao-de-obras"]),
    ("sindicos", "Síndicos e administradoras", "fa-solid fa-building-user", "Precisa de respaldo técnico para decidir obras, manutenções e reformas das unidades.", ["condominios", "vistorias-e-inspecoes", "recuperacao-e-manutencao"]),
    ("empresas", "Empresas", "fa-solid fa-briefcase", "Não pode parar a operação e precisa de obras, regularização e instalações dentro do prazo.", ["reformas", "regularizacao", "instalacoes"]),
    ("incorporadores", "Incorporadores e investidores", "fa-solid fa-chart-line", "Busca viabilidade, projetos compatibilizados e gestão enxuta para proteger o retorno.", ["projetos", "consultoria", "gestao-de-obras"]),
    ("arquitetos", "Arquitetos", "fa-solid fa-pen-ruler", "Precisa de um parceiro de engenharia para complementares, compatibilização e execução fiel ao projeto.", ["projetos", "construcao", "consultoria"]),
    ("advogados", "Advogados", "fa-solid fa-gavel", "Precisa de perícia, parecer ou assistência técnica para fundamentar e defender o caso.", ["pericias-e-avaliacoes", "laudos-tecnicos"]),
    ("corretores", "Corretores", "fa-solid fa-key", "Quer dar segurança ao comprador com vistoria, avaliação e regularização do imóvel.", ["vistorias-e-inspecoes", "pericias-e-avaliacoes", "regularizacao"]),
    ("quem-mora-fora", "Quem mora fora", "fa-solid fa-plane", "Tem obra ou imóvel em SC e precisa de quem cuide de tudo com transparência à distância.", ["gestao-de-obras", "consultoria", "recuperacao-e-manutencao"]),
]

# ---------------------------------------------------------------------------
# Obras (categorias do portfólio)
# ---------------------------------------------------------------------------
OBRAS_CATEGORIAS = [("residenciais", "Residenciais"), ("comerciais", "Comerciais"), ("saude", "Saúde"), ("educacao", "Educação"), ("condominios", "Condomínios"), ("edificios", "Edifícios"), ("galpoes", "Galpões")]
OBRAS = [  # placeholders: substituir por obras reais com fotos autorizadas
    ("projeto-1", "residenciais", "Residência de alto padrão"),
    ("projeto-5", "condominios", "Recuperação de fachada em condomínio"),
    ("projeto-3", "comerciais", "Reforma de loja"),
    ("projeto-4", "galpoes", "Galpão logístico"),
    ("projeto-2", "edificios", "Edifício residencial"),
    ("projeto-6", "saude", "Reforma de clínica"),
]

# ---------------------------------------------------------------------------
# Regiões atendidas
# ---------------------------------------------------------------------------
REGIOES = [
    ("Florianópolis", "Grande Florianópolis"), ("São José", "Grande Florianópolis"), ("Palhoça", "Grande Florianópolis"),
    ("Biguaçu", "Grande Florianópolis"), ("Governador Celso Ramos", "Grande Florianópolis"), ("Santo Amaro da Imperatriz", "Grande Florianópolis"),
    ("Paulo Lopes", "Sul da Grande Florianópolis"),
    ("Balneário Camboriú", "Litoral Norte"), ("Itajaí", "Litoral Norte"), ("Itapema", "Litoral Norte"),
    ("Joinville", "Norte de SC"), ("Blumenau", "Vale do Itajaí"),
]

# Tipos do formulário qualificado (/solicitar-proposta/)
FORM_TIPOS = [
    ("obra-ou-reforma", "Obra ou reforma"),
    ("laudo-ou-vistoria", "Laudo ou vistoria"),
    ("projeto", "Projeto"),
    ("condominio", "Condomínio"),
    ("consultoria", "Consultoria"),
]

# Menu principal (aba Menu)
MENU = [
    ("/servicos/", "Serviços", "servicos"),
    ("/marcas-e-sistemas/", "Marcas e Sistemas", "marcas"),
    ("/para-voce/", "Para você", None),
    ("/obras/", "Obras", None),
    ("/sobre/", "Sobre", None),
    ("/blog/", "Conteúdo", None),
    ("/contato/", "Contato", None),
]
