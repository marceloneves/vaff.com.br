/* VAFF Engenharia — interações do site */
(function () {
  'use strict';

  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));
  const reduzMovimento = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Header fixo + voltar ao topo ---------- */
  const cabecalho = $('.cabecalho');
  const voltarTopo = $('.voltar-topo');
  let espacador = null;

  function aoRolar() {
    const y = window.scrollY;
    if (cabecalho) {
      const limite = 300;
      if (y > limite && !cabecalho.classList.contains('fixo')) {
        espacador = espacador || document.createElement('div');
        espacador.style.height = cabecalho.offsetHeight + 'px';
        cabecalho.after(espacador);
        cabecalho.classList.add('fixo');
      } else if (y <= limite && cabecalho.classList.contains('fixo')) {
        cabecalho.classList.remove('fixo');
        espacador && espacador.remove();
      }
    }
    if (voltarTopo) voltarTopo.classList.toggle('visivel', y > 600);
  }
  window.addEventListener('scroll', aoRolar, { passive: true });
  aoRolar();

  if (voltarTopo) {
    voltarTopo.addEventListener('click', () => window.scrollTo({ top: 0, behavior: reduzMovimento ? 'auto' : 'smooth' }));
  }

  /* ---------- Menu mobile ---------- */
  const menuMobile = $('.menu-mobile');
  const menuToggle = $('.menu-toggle');
  function alternarMenu(abrir) {
    if (!menuMobile) return;
    menuMobile.classList.toggle('aberto', abrir);
    menuMobile.setAttribute('aria-hidden', String(!abrir));
    menuToggle && menuToggle.setAttribute('aria-expanded', String(abrir));
    document.body.style.overflow = abrir ? 'hidden' : '';
    if (abrir) $('.menu-mobile__fechar', menuMobile).focus();
  }
  menuToggle && menuToggle.addEventListener('click', () => alternarMenu(true));
  if (menuMobile) {
    $$('.menu-mobile__fechar, .menu-mobile__fundo, nav a', menuMobile).forEach((el) =>
      el.addEventListener('click', () => alternarMenu(false))
    );
  }

  /* ---------- Hero slider ---------- */
  const hero = $('.hero');
  if (hero) {
    const slides = $$('.hero__slide', hero);
    const pontosWrap = $('.hero__pontos', hero);
    let atual = 0;
    let timer = null;

    const pontos = slides.map((_, i) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('aria-label', 'Ir para o slide ' + (i + 1));
      b.addEventListener('click', () => { irPara(i); reiniciar(); });
      pontosWrap && pontosWrap.appendChild(b);
      return b;
    });

    function irPara(i) {
      slides[atual].classList.remove('ativo');
      pontos[atual].classList.remove('ativo');
      atual = (i + slides.length) % slides.length;
      slides[atual].classList.add('ativo');
      pontos[atual].classList.add('ativo');
    }
    function reiniciar() {
      clearInterval(timer);
      if (!reduzMovimento && slides.length > 1) timer = setInterval(() => irPara(atual + 1), 7000);
    }

    const prev = $('[data-hero="anterior"]', hero);
    const next = $('[data-hero="proximo"]', hero);
    prev && prev.addEventListener('click', () => { irPara(atual - 1); reiniciar(); });
    next && next.addEventListener('click', () => { irPara(atual + 1); reiniciar(); });

    pontos[0] && pontos[0].classList.add('ativo');
    reiniciar();
  }

  /* ---------- Animações ao rolar + contadores ---------- */
  function animarContador(el) {
    const alvo = parseInt(el.dataset.alvo, 10) || 0;
    if (reduzMovimento) { el.textContent = alvo; return; }
    const duracao = 2000;
    const inicio = performance.now();
    function passo(agora) {
      const p = Math.min((agora - inicio) / duracao, 1);
      el.textContent = Math.floor(alvo * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(passo);
    }
    requestAnimationFrame(passo);
  }

  const anima = $$('.anima');
  const contadores = $$('[data-alvo]');
  if ('IntersectionObserver' in window) {
    const obs = new IntersectionObserver((entradas) => {
      entradas.forEach((e) => {
        if (!e.isIntersecting) return;
        if (e.target.dataset.alvo !== undefined) animarContador(e.target);
        else e.target.classList.add('visivel');
        obs.unobserve(e.target);
      });
    }, { threshold: 0.15 });
    anima.forEach((el) => obs.observe(el));
    contadores.forEach((el) => obs.observe(el));
  } else {
    anima.forEach((el) => el.classList.add('visivel'));
    contadores.forEach((el) => (el.textContent = el.dataset.alvo));
  }

  /* ---------- Filtro de projetos ---------- */
  const filtros = $$('.filtros button');
  const projetos = $$('.card-projeto');
  filtros.forEach((btn) => {
    btn.addEventListener('click', () => {
      filtros.forEach((b) => { b.classList.remove('ativo'); b.setAttribute('aria-pressed', 'false'); });
      btn.classList.add('ativo');
      btn.setAttribute('aria-pressed', 'true');
      const cat = btn.dataset.filtro;
      projetos.forEach((p) => p.classList.toggle('oculto', cat !== '*' && p.dataset.categoria !== cat));
    });
  });

  /* ---------- Carrossel de depoimentos ---------- */
  $$('.carrossel').forEach((car) => {
    const trilho = $('.carrossel__trilho', car);
    const itens = $$('.depoimento', car);
    const wrap = car.parentElement;
    let i = 0;
    let timer = null;
    const mover = (n) => {
      i = (n + itens.length) % itens.length;
      trilho.style.transform = 'translateX(' + -i * 100 + '%)';
      itens.forEach((it, k) => it.setAttribute('aria-hidden', String(k !== i)));
    };
    const reiniciar = () => {
      clearInterval(timer);
      if (!reduzMovimento) timer = setInterval(() => mover(i + 1), 6000);
    };
    const prev = $('[data-carrossel="anterior"]', wrap);
    const next = $('[data-carrossel="proximo"]', wrap);
    prev && prev.addEventListener('click', () => { mover(i - 1); reiniciar(); });
    next && next.addEventListener('click', () => { mover(i + 1); reiniciar(); });
    mover(0);
    reiniciar();
  });

  /* ---------- Modal de vídeo ---------- */
  const modal = $('.modal');
  if (modal) {
    const frameWrap = $('.modal__conteudo', modal);
    const fechar = () => {
      modal.classList.remove('aberto');
      const f = $('iframe', frameWrap);
      f && f.remove();
      document.body.style.overflow = '';
    };
    $$('[data-video]').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const iframe = document.createElement('iframe');
        iframe.src = btn.dataset.video + (btn.dataset.video.includes('?') ? '&' : '?') + 'autoplay=1';
        iframe.allow = 'autoplay; encrypted-media; picture-in-picture';
        iframe.allowFullscreen = true;
        iframe.title = 'Vídeo institucional VAFF Engenharia';
        frameWrap.appendChild(iframe);
        modal.classList.add('aberto');
        document.body.style.overflow = 'hidden';
        $('.modal__fechar', modal).focus();
      });
    });
    $('.modal__fechar', modal).addEventListener('click', fechar);
    modal.addEventListener('click', (e) => { if (e.target === modal) fechar(); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && modal.classList.contains('aberto')) fechar(); });
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && menuMobile && menuMobile.classList.contains('aberto')) alternarMenu(false);
  });

  /* ---------- FAQ (acordeão) ---------- */
  $$('.faq__item').forEach((item) => {
    const btn = $('.faq__pergunta', item);
    const resp = $('.faq__resposta', item);
    btn.addEventListener('click', () => {
      const abrir = !item.classList.contains('aberto');
      $$('.faq__item.aberto').forEach((o) => {
        o.classList.remove('aberto');
        $('.faq__resposta', o).style.maxHeight = null;
        $('.faq__pergunta', o).setAttribute('aria-expanded', 'false');
      });
      if (abrir) {
        item.classList.add('aberto');
        resp.style.maxHeight = resp.scrollHeight + 'px';
        btn.setAttribute('aria-expanded', 'true');
      }
    });
  });
  const faqAberto = $('.faq__item.aberto .faq__resposta');
  if (faqAberto) faqAberto.style.maxHeight = faqAberto.scrollHeight + 'px';

  /* ---------- Formulários (sem backend: abre o e-mail do cliente) ---------- */
  $$('form[data-mailto]').forEach((form) => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const dados = new FormData(form);
      const linhas = [];
      dados.forEach((v, k) => { if (v) linhas.push(k + ': ' + v); });
      const assunto = encodeURIComponent('Contato pelo site - ' + (dados.get('Nome') || ''));
      const corpo = encodeURIComponent(linhas.join('\n'));
      window.location.href = 'mailto:' + form.dataset.mailto + '?subject=' + assunto + '&body=' + corpo;
      const msg = $('.form-msg', form);
      msg && msg.classList.add('visivel');
      form.reset();
    });
  });


  /* ---------- Mega menu (clique/teclado) ---------- */
  $$('.menu > li.tem-mega').forEach((li) => {
    const link = $('a', li);
    link.addEventListener('click', (e) => {
      // primeiro clique abre o painel em telas de toque; o segundo segue o link
      if (window.matchMedia('(hover: none)').matches && !li.classList.contains('aberto')) {
        e.preventDefault();
        $$('.menu > li.aberto').forEach((o) => o !== li && o.classList.remove('aberto'));
        li.classList.add('aberto');
        link.setAttribute('aria-expanded', 'true');
      }
    });
    li.addEventListener('mouseleave', () => { li.classList.remove('aberto'); link.setAttribute('aria-expanded', 'false'); });
    li.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') { li.classList.remove('aberto'); link.focus(); }
    });
  });
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.menu > li.tem-mega')) $$('.menu > li.aberto').forEach((o) => o.classList.remove('aberto'));
  });

  /* ---------- Acordeão do menu mobile ---------- */
  $$('.acordeao').forEach((ac) => {
    const btn = $('.acordeao__botao', ac);
    const painel = $('.acordeao__painel', ac);
    btn.addEventListener('click', () => {
      const abrir = !ac.classList.contains('aberto');
      ac.classList.toggle('aberto', abrir);
      btn.setAttribute('aria-expanded', String(abrir));
      painel.style.maxHeight = abrir ? painel.scrollHeight + 'px' : null;
    });
  });

  /* ---------- Formulário de proposta: tipo vindo da URL (?tipo=) ---------- */
  const tipo = new URLSearchParams(window.location.search).get('tipo');
  if (tipo) {
    $$('select[data-tipo]').forEach((sel) => {
      const op = Array.from(sel.options).find((o) => o.dataset.slug === tipo);
      if (op) sel.value = op.value;
    });
  }

  /* ---------- Ano no rodapé ---------- */
  $$('[data-ano]').forEach((el) => (el.textContent = new Date().getFullYear()));
})();
