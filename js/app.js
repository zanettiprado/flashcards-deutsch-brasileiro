/* Alemão do zero — lógica dos flashcards.
 *
 * Depende de data/cards.js, que define a constante global CARDS.
 * Todo o estado fica no localStorage, separado por nível e direção.
 */
(function () {
  'use strict';

  var CARDS = window.CARDS || [];
  var NIVEIS = ['A1', 'A2', 'B1', 'B2', 'C1'];

  var NOMES_NIVEL = {
    A1: 'Primeiros passos',
    A2: 'Dia a dia',
    B1: 'Independência',
    B2: 'Fluência',
    C1: 'Domínio'
  };

  var DESCRICOES = {
    A1: 'Cumprimentos, apresentação, família, números, horas, comida, compras.',
    A2: 'Rotina, passado, trabalho, serviços, saúde, viagem, opiniões simples.',
    B1: 'Formação, carreira, moradia, meio ambiente, mídia, dinheiro, burocracia.',
    B2: 'Sociedade, vida digital, cultura, sentimentos, história e futuro.',
    C1: 'Ciência, economia, direito, argumentação e expressões idiomáticas.'
  };

  /* Nomes das categorias na tela (os dados usam identificadores sem acento). */
  var NOMES_CATEGORIA = {
    ambiente: 'meio ambiente', apresentacao: 'apresentação',
    argumentacao: 'argumentação', burocracia: 'burocracia',
    ciencia: 'ciência', cidade: 'cidade', clima: 'clima', comida: 'comida',
    compras: 'compras', comunicacao: 'comunicação', cultura: 'cultura',
    cumprimentos: 'cumprimentos', descricao: 'descrição', digital: 'vida digital',
    dinheiro: 'dinheiro', direito: 'direito', economia: 'economia',
    educacao: 'educação', escola: 'escola e trabalho', familia: 'família',
    historia: 'história e futuro', idiomatico: 'expressões idiomáticas',
    lazer: 'lazer', midia: 'mídia', moradia: 'moradia', numeros: 'números',
    opiniao: 'opinião', passado: 'passado', planos: 'planos',
    politica: 'política', relacoes: 'relações', restaurante: 'restaurante',
    rotina: 'rotina', saude: 'saúde', sentidos: 'sentidos e sentimentos',
    sentimentos: 'sentimentos', servicos: 'serviços', sociedade: 'sociedade',
    sustentabilidade: 'sustentabilidade', tecnologia: 'tecnologia',
    tempo: 'tempo e horas', trabalho: 'trabalho', viagem: 'viagem'
  };

  /* Quantos cards à frente um card marcado como "não sei" volta a aparecer. */
  var INTERVALO_REVISAO = 4;

  var VERSAO_ARMAZENAMENTO = 'alemao-v1';

  // -------------------------------------------------------------- utilidades

  function $(id) { return document.getElementById(id); }

  function cardsDoNivel(nivel) {
    return CARDS.filter(function (c) { return c.nivel === nivel; });
  }

  function chave(nivel, direcao) {
    return VERSAO_ARMAZENAMENTO + ':' + nivel + ':' + direcao;
  }

  function lerProgresso(nivel, direcao) {
    var vazio = { sabidos: [], naoSabidos: [], ordem: null, pos: 0 };
    try {
      var bruto = localStorage.getItem(chave(nivel, direcao));
      if (!bruto) { return vazio; }
      var dados = JSON.parse(bruto);
      return {
        sabidos: Array.isArray(dados.sabidos) ? dados.sabidos : [],
        naoSabidos: Array.isArray(dados.naoSabidos) ? dados.naoSabidos : [],
        ordem: Array.isArray(dados.ordem) ? dados.ordem : null,
        pos: typeof dados.pos === 'number' ? dados.pos : 0
      };
    } catch (e) {
      return vazio;
    }
  }

  function gravarProgresso(nivel, direcao, dados) {
    try {
      localStorage.setItem(chave(nivel, direcao), JSON.stringify(dados));
    } catch (e) {
      /* modo privado ou armazenamento cheio: segue sem salvar */
    }
  }

  function embaralhar(lista) {
    var copia = lista.slice();
    for (var i = copia.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = copia[i]; copia[i] = copia[j]; copia[j] = t;
    }
    return copia;
  }

  // ------------------------------------------------------------------- estado

  var estado = {
    nivel: 'A1',
    direcao: 'pt-de',
    deck: [],        // ids de cards, na ordem da sessão
    pos: 0,
    virado: false,
    sabidos: {},     // id -> true
    naoSabidos: {}   // id -> true
  };

  function cardAtual() {
    var id = estado.deck[estado.pos];
    for (var i = 0; i < CARDS.length; i++) {
      if (CARDS[i].id === id) { return CARDS[i]; }
    }
    return null;
  }

  function salvar() {
    gravarProgresso(estado.nivel, estado.direcao, {
      sabidos: Object.keys(estado.sabidos).map(Number),
      naoSabidos: Object.keys(estado.naoSabidos).map(Number),
      ordem: estado.deck,
      pos: estado.pos
    });
    desenharNiveis();
  }

  // --------------------------------------------------------------------- voz

  var voz = { de: null, pt: null, avisado: false };

  function escolherVozes() {
    if (!('speechSynthesis' in window)) { return; }
    var vozes = window.speechSynthesis.getVoices() || [];
    voz.de = null;
    voz.pt = null;
    for (var i = 0; i < vozes.length; i++) {
      var lang = (vozes[i].lang || '').toLowerCase().replace('_', '-');
      if (!voz.de && lang.indexOf('de') === 0) { voz.de = vozes[i]; }
      if (!voz.pt && lang.indexOf('pt') === 0) { voz.pt = vozes[i]; }
    }
    mostrarAvisoVoz(vozes.length > 0);
  }

  function mostrarAvisoVoz(vozesCarregadas) {
    var alvo = $('aviso-voz');
    if (!alvo) { return; }
    if (!('speechSynthesis' in window)) {
      alvo.innerHTML = '<strong>Este navegador não tem leitura em voz alta.</strong>' +
        ' Use o link “Ouvir no Google Tradutor” em cada card.';
      alvo.hidden = false;
      return;
    }
    if (vozesCarregadas && !voz.de) {
      alvo.innerHTML = '<strong>Nenhuma voz alemã instalada.</strong>' +
        ' O áudio em alemão vai sair com sotaque errado ou não funcionar.' +
        ' No macOS: Ajustes do Sistema → Acessibilidade → Conteúdo Falado →' +
        ' Voz do sistema → Gerenciar vozes → baixe uma voz em Alemão.' +
        ' No Windows: Configurações → Hora e idioma → Idioma e região →' +
        ' adicione “Deutsch” e instale a fala. No Android/iOS, instale o' +
        ' pacote de voz alemã nas configurações de acessibilidade.' +
        ' Enquanto isso, use o link “Ouvir no Google Tradutor”.';
      alvo.hidden = false;
    } else {
      alvo.hidden = true;
    }
  }

  function falar(texto, idioma, velocidade) {
    if (!('speechSynthesis' in window)) { return; }
    window.speechSynthesis.cancel();
    var fala = new SpeechSynthesisUtterance(texto);
    fala.lang = idioma === 'pt' ? 'pt-BR' : 'de-DE';
    var escolhida = idioma === 'pt' ? voz.pt : voz.de;
    if (escolhida) { fala.voice = escolhida; }
    fala.rate = velocidade || 1;
    window.speechSynthesis.speak(fala);
  }

  function falarPalavras(palavras) {
    if (!('speechSynthesis' in window)) { return; }
    window.speechSynthesis.cancel();
    palavras.forEach(function (p) {
      var fala = new SpeechSynthesisUtterance(p.de);
      fala.lang = 'de-DE';
      if (voz.de) { fala.voice = voz.de; }
      fala.rate = 0.75;
      window.speechSynthesis.speak(fala);
    });
  }

  // ------------------------------------------------------------ tela inicial

  function desenharNiveis() {
    var alvo = $('lista-niveis');
    if (!alvo) { return; }
    alvo.innerHTML = '';
    NIVEIS.forEach(function (nivel) {
      var total = cardsDoNivel(nivel).length;
      var salvo = lerProgresso(nivel, estado.direcao);
      var feitos = salvo.sabidos.length;
      var pct = total ? Math.round((feitos / total) * 100) : 0;

      var botao = document.createElement('button');
      botao.type = 'button';
      botao.className = 'nivel';
      botao.setAttribute('aria-pressed', nivel === estado.nivel ? 'true' : 'false');
      botao.innerHTML =
        '<span class="nivel-sigla">' + nivel + '</span>' +
        '<span class="nivel-info">' +
          '<span class="nivel-titulo">' + NOMES_NIVEL[nivel] + '</span>' +
          '<span class="nivel-detalhe">' + total + ' cards · ' +
            feitos + ' já sei (' + pct + '%)</span>' +
          '<span class="nivel-progresso"><span style="width:' + pct + '%"></span></span>' +
        '</span>';
      botao.title = DESCRICOES[nivel];
      botao.addEventListener('click', function () {
        estado.nivel = nivel;
        desenharNiveis();
      });
      alvo.appendChild(botao);
    });
  }

  function desenharDirecoes() {
    var botoes = document.querySelectorAll('.direcao');
    for (var i = 0; i < botoes.length; i++) {
      var b = botoes[i];
      b.setAttribute('aria-pressed',
        b.getAttribute('data-direcao') === estado.direcao ? 'true' : 'false');
    }
  }

  // ----------------------------------------------------------------- sessão

  function montarDeck() {
    var doNivel = cardsDoNivel(estado.nivel).map(function (c) { return c.id; });
    var salvo = lerProgresso(estado.nivel, estado.direcao);

    estado.sabidos = {};
    salvo.sabidos.forEach(function (id) { estado.sabidos[id] = true; });
    estado.naoSabidos = {};
    salvo.naoSabidos.forEach(function (id) { estado.naoSabidos[id] = true; });

    var deck;
    if (salvo.ordem && salvo.ordem.length) {
      // mantém a ordem salva, descartando ids que não existem mais
      var validos = {};
      doNivel.forEach(function (id) { validos[id] = true; });
      deck = salvo.ordem.filter(function (id) { return validos[id]; });
      var presentes = {};
      deck.forEach(function (id) { presentes[id] = true; });
      doNivel.forEach(function (id) {
        if (!presentes[id]) { deck.push(id); }
      });
    } else {
      deck = doNivel;
    }

    estado.deck = deck;
    estado.pos = Math.min(Math.max(salvo.pos, 0), Math.max(deck.length - 1, 0));
    estado.virado = false;
  }

  function iniciarSessao() {
    montarDeck();
    $('tela-inicio').hidden = true;
    $('tela-estudo').hidden = false;
    window.scrollTo(0, 0);
    desenharCard();
  }

  function voltarAoInicio() {
    if ('speechSynthesis' in window) { window.speechSynthesis.cancel(); }
    $('tela-estudo').hidden = true;
    $('tela-inicio').hidden = false;
    desenharNiveis();
    window.scrollTo(0, 0);
  }

  // -------------------------------------------------------------- desenhar

  function desenharCard() {
    var card = cardAtual();
    var total = cardsDoNivel(estado.nivel).length;

    if (!card) {
      $('frase-frente').textContent = 'Nenhum card neste nível.';
      return;
    }

    var ptPrimeiro = estado.direcao === 'pt-de';
    var frente = ptPrimeiro ? card.pt : card.de;
    var verso = ptPrimeiro ? card.de : card.pt;

    $('rotulo-sessao').textContent = estado.nivel + ' · ' +
      (ptPrimeiro ? 'Português → Alemão' : 'Alemão → Português');
    $('contador').textContent = (estado.pos + 1) + ' de ' + estado.deck.length +
      ' · ' + (NOMES_CATEGORIA[card.categoria] || card.categoria);

    $('etiqueta-frente').textContent = ptPrimeiro ? 'Português' : 'Deutsch';
    $('frase-frente').textContent = frente;
    $('etiqueta-verso').textContent = ptPrimeiro ? 'Deutsch' : 'Português';
    $('frase-verso').textContent = verso;
    $('pronuncia-frase').textContent = '[ ' + card.pronuncia + ' ]';

    var gram = $('gramatica');
    if (card.gramatica) {
      gram.textContent = card.gramatica;
      gram.hidden = false;
    } else {
      gram.hidden = true;
    }

    desenharPalavras(card);
    fecharPainelPalavra();

    $('link-tradutor').href = 'https://translate.google.com/?sl=de&tl=pt&text=' +
      encodeURIComponent(card.de) + '&op=translate';

    $('card').classList.toggle('virado', estado.virado);
    $('btn-anterior').disabled = estado.pos === 0;
    ajustarAlturaCard();

    var feitos = Object.keys(estado.sabidos).length;
    var pct = total ? Math.round((feitos / total) * 100) : 0;
    $('progresso-barra').style.width = pct + '%';
    $('progresso').setAttribute('aria-valuenow', String(pct));
    $('progresso-texto').textContent = feitos + ' de ' + total +
      ' cards do nível ' + estado.nivel + ' marcados como “eu sei”' +
      (Object.keys(estado.naoSabidos).length
        ? ' · ' + Object.keys(estado.naoSabidos).length + ' para revisar'
        : '');
  }

  /* As duas faces sao absolutas, entao a altura do card precisa ser calculada
     a partir do lado mais alto; sem isso a nota de gramatica fica cortada. */
  function ajustarAlturaCard() {
    var medir = function () {
      var frente = document.querySelector('.card-frente');
      var verso = document.querySelector('.card-verso');
      if (!frente || !verso) { return; }
      // +2 por causa da borda de 1px de cada face, que o scrollHeight ignora
      var altura = Math.max(300, frente.scrollHeight, verso.scrollHeight) + 2;
      $('card').style.height = altura + 'px';
      $('card-inner').style.height = altura + 'px';
    };
    if (window.requestAnimationFrame) {
      window.requestAnimationFrame(medir);
    } else {
      medir();
    }
  }

  function desenharPalavras(card) {
    var alvo = $('palavras');
    alvo.innerHTML = '';
    (card.palavras || []).forEach(function (palavra) {
      var botao = document.createElement('button');
      botao.type = 'button';
      botao.className = 'palavra';
      botao.textContent = palavra.de;
      botao.addEventListener('click', function (ev) {
        ev.stopPropagation();
        abrirPainelPalavra(palavra, botao);
      });
      alvo.appendChild(botao);
    });
  }

  function abrirPainelPalavra(palavra, botao) {
    var ativos = document.querySelectorAll('.palavra.ativa');
    for (var i = 0; i < ativos.length; i++) { ativos[i].classList.remove('ativa'); }
    if (botao) { botao.classList.add('ativa'); }

    $('painel-de').textContent = palavra.de;
    $('painel-pt').textContent = palavra.pt;
    $('painel-silabas').textContent = palavra.silabas;
    $('painel-pronuncia').textContent = palavra.pronuncia;
    $('painel-palavra').hidden = false;
    $('painel-ouvir').onclick = function (ev) {
      ev.stopPropagation();
      falar(palavra.de, 'de', 0.75);
    };
    falar(palavra.de, 'de', 0.8);
  }

  function fecharPainelPalavra() {
    $('painel-palavra').hidden = true;
    var ativos = document.querySelectorAll('.palavra.ativa');
    for (var i = 0; i < ativos.length; i++) { ativos[i].classList.remove('ativa'); }
  }

  // ------------------------------------------------------------------ ações

  function virar() {
    estado.virado = !estado.virado;
    $('card').classList.toggle('virado', estado.virado);
    if (!estado.virado) { fecharPainelPalavra(); }
  }

  function irPara(novaPos) {
    if (!estado.deck.length) { return; }
    estado.pos = Math.min(Math.max(novaPos, 0), estado.deck.length - 1);
    estado.virado = false;
    if ('speechSynthesis' in window) { window.speechSynthesis.cancel(); }
    salvar();
    desenharCard();
  }

  function proximo() {
    if (estado.pos >= estado.deck.length - 1) {
      irPara(estado.deck.length - 1);
      return;
    }
    irPara(estado.pos + 1);
  }

  function marcar(sei) {
    var card = cardAtual();
    if (!card) { return; }
    if (sei) {
      estado.sabidos[card.id] = true;
      delete estado.naoSabidos[card.id];
      proximo();
      return;
    }

    estado.naoSabidos[card.id] = true;
    delete estado.sabidos[card.id];

    // O card sai da posicao atual e volta poucos cards adiante, para ser
    // revisto antes dos outros. O tamanho da rodada nao muda.
    estado.deck.splice(estado.pos, 1);
    var destino = Math.min(estado.pos + INTERVALO_REVISAO, estado.deck.length);
    estado.deck.splice(destino, 0, card.id);

    if (estado.pos >= estado.deck.length) { estado.pos = estado.deck.length - 1; }
    estado.virado = false;
    if ('speechSynthesis' in window) { window.speechSynthesis.cancel(); }
    salvar();
    desenharCard();
  }

  function embaralharDeck() {
    estado.deck = embaralhar(estado.deck);
    estado.pos = 0;
    estado.virado = false;
    salvar();
    desenharCard();
  }

  function reiniciarNivel() {
    if (!window.confirm('Apagar o progresso do nível ' + estado.nivel +
        ' nesta direção e começar de novo?')) { return; }
    try { localStorage.removeItem(chave(estado.nivel, estado.direcao)); } catch (e) {}
    montarDeck();
    desenharCard();
  }

  function zerarTudo() {
    if (!window.confirm('Apagar o progresso de todos os níveis e direções?')) { return; }
    NIVEIS.forEach(function (nivel) {
      ['pt-de', 'de-pt'].forEach(function (d) {
        try { localStorage.removeItem(chave(nivel, d)); } catch (e) {}
      });
    });
    desenharNiveis();
  }

  // ------------------------------------------------------------------ ligação

  function ligarEventos() {
    window.addEventListener('resize', ajustarAlturaCard);
    $('btn-comecar').addEventListener('click', iniciarSessao);
    $('btn-zerar-tudo').addEventListener('click', zerarTudo);
    $('btn-voltar').addEventListener('click', voltarAoInicio);

    var direcoes = document.querySelectorAll('.direcao');
    for (var i = 0; i < direcoes.length; i++) {
      direcoes[i].addEventListener('click', function () {
        estado.direcao = this.getAttribute('data-direcao');
        desenharDirecoes();
        desenharNiveis();
      });
    }

    $('card').addEventListener('click', virar);
    $('card').addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter') { ev.preventDefault(); virar(); }
    });

    $('fechar-painel').addEventListener('click', function (ev) {
      ev.stopPropagation();
      fecharPainelPalavra();
    });
    $('painel-palavra').addEventListener('click', function (ev) { ev.stopPropagation(); });

    $('btn-ouvir').addEventListener('click', function () {
      var c = cardAtual();
      if (c) { falar(c.de, 'de', 1); }
    });
    $('btn-ouvir-devagar').addEventListener('click', function () {
      var c = cardAtual();
      if (c) { falar(c.de, 'de', 0.55); }
    });
    $('btn-ouvir-palavras').addEventListener('click', function () {
      var c = cardAtual();
      if (c) { falarPalavras(c.palavras || []); }
    });

    $('btn-sei').addEventListener('click', function () { marcar(true); });
    $('btn-nao-sei').addEventListener('click', function () { marcar(false); });
    $('btn-anterior').addEventListener('click', function () { irPara(estado.pos - 1); });
    $('btn-proximo').addEventListener('click', proximo);
    $('btn-embaralhar').addEventListener('click', embaralharDeck);
    $('btn-reiniciar').addEventListener('click', reiniciarNivel);

    document.addEventListener('keydown', function (ev) {
      if ($('tela-estudo').hidden) { return; }
      var alvo = ev.target;
      if (alvo && (alvo.tagName === 'INPUT' || alvo.tagName === 'TEXTAREA')) { return; }
      switch (ev.key) {
        case ' ':
        case 'Spacebar':
          ev.preventDefault(); virar(); break;
        case 'ArrowRight':
          ev.preventDefault(); proximo(); break;
        case 'ArrowLeft':
          ev.preventDefault(); irPara(estado.pos - 1); break;
        case '1':
          marcar(true); break;
        case '2':
          marcar(false); break;
        case 'Escape':
          fecharPainelPalavra(); break;
        default:
          break;
      }
    });
  }

  // ------------------------------------------------------------------ início

  function iniciar() {
    if (!CARDS.length) {
      document.body.innerHTML =
        '<main class="tela"><h1>Falha ao carregar os cards</h1>' +
        '<p>O arquivo <code>data/cards.js</code> não foi encontrado. ' +
        'Mantenha a pasta <code>data</code> ao lado do <code>index.html</code>.</p></main>';
      return;
    }
    desenharNiveis();
    desenharDirecoes();
    ligarEventos();

    if ('speechSynthesis' in window) {
      escolherVozes();
      window.speechSynthesis.onvoiceschanged = escolherVozes;
      // Safari e Chrome às vezes só preenchem a lista depois de um instante
      window.setTimeout(escolherVozes, 400);
      window.setTimeout(escolherVozes, 1500);
    } else {
      mostrarAvisoVoz(false);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', iniciar);
  } else {
    iniciar();
  }
}());
