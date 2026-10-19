/* Alemão do zero / Portugiesisch von null — lógica dos flashcards.
 *
 * O mesmo arquivo serve aos dois cursos. A página define window.CURSO antes
 * de carregar este script:
 *
 *   'de' — para quem fala português e aprende ALEMÃO   (index.html)
 *   'pt' — para quem fala alemão e aprende PORTUGUÊS   (portugiesisch.html)
 *
 * Depende de data/cards.js, que define a constante global CARDS.
 * Todo o estado fica no localStorage, separado por curso, nível e direção.
 */
(function () {
  'use strict';

  var CARDS = window.CARDS || [];
  var CURSO = window.CURSO === 'pt' ? 'pt' : 'de';
  var NIVEIS = ['A1', 'A2', 'B1', 'B2', 'C1'];
  var INTERVALO_REVISAO = 4;
  var VERSAO_ARMAZENAMENTO = 'alemao-v1';

  // ---------------------------------------------------------------- textos

  var TEXTOS = {
    de: {
      lang: 'pt-BR',
      idiomaAlvo: 'de',          // língua que o aluno está aprendendo
      idiomaBase: 'pt',          // língua que o aluno já fala
      titulo: 'Alemão do zero',
      saudacao: 'Vamos lá, Felipe, aprender alemão!',
      subtitulo: 'Frases do cotidiano em flashcards, do A1 ao C1, com ' +
        'pronúncia aproximada em português.',
      passo1: '1. Escolha o nível',
      passo2: '2. Escolha a direção',
      passo3: '3. Voz do alemão',
      explicaVoz: 'A voz vem do seu próprio aparelho, não do site. Se o ' +
        'alemão sair com sotaque de inglês, é porque o sistema caiu numa ' +
        'voz inglesa — troque aqui e teste.',
      rotuloVoz: 'Voz usada no alemão',
      testarVoz: '🔊 Testar: “Guten Abend”',
      fraseTeste: 'Guten Abend',
      comecar: 'Começar a estudar',
      zerar: 'Zerar todo o progresso',
      voltar: 'Voltar ao início',
      embaralhar: 'Embaralhar',
      dicaVirar: 'toque no card ou aperte <kbd>espaço</kbd> para virar',
      rotuloAlvo: 'Deutsch',
      rotuloBase: 'Português',
      silabas: 'Sílabas',
      pronuncia: 'Pronúncia',
      ouvirPalavra: '🔊 Ouvir a palavra',
      ouvirFrase: '🔊 Ouvir a frase',
      ouvirDevagar: '🐢 Ouvir devagar',
      ouvirPalavras: '🔉 Palavra por palavra',
      tradutor: '↗ Ouvir no Google Tradutor',
      vozEmUso: 'Voz do alemão:',
      trocarVoz: 'trocar',
      sei: 'Eu sei',
      naoSei: 'Não sei',
      anterior: '← Anterior',
      proximo: 'Próximo →',
      reiniciar: 'Reiniciar nível',
      atalhos: 'Atalhos: <kbd>espaço</kbd> virar · <kbd>←</kbd> <kbd>→</kbd> ' +
        'navegar · <kbd>1</kbd> sei · <kbd>2</kbd> não sei',
      outroCurso: 'Deutsche Muttersprachler? → Portugiesisch lernen',
      outroLink: 'portugiesisch.html',
      niveis: {
        A1: 'Primeiros passos', A2: 'Dia a dia', B1: 'Independência',
        B2: 'Fluência', C1: 'Domínio'
      },
      direcoes: [
        ['pt-de', 'Português → Alemão',
         'Você vê a frase em português e tenta dizer em alemão'],
        ['de-pt', 'Alemão → Português',
         'Você vê a frase em alemão e tenta entender']
      ],
      cards: function (n) { return n + ' cards'; },
      jaSei: function (n, p) { return n + ' já sei (' + p + '%)'; },
      contador: function (a, b, cat) { return a + ' de ' + b + ' · ' + cat; },
      progresso: function (f, t, nivel, rev) {
        return f + ' de ' + t + ' cards do nível ' + nivel +
          ' marcados como “eu sei”' +
          (rev ? ' · ' + rev + ' para revisar' : '');
      },
      sessao: function (nivel, dir) { return nivel + ' · ' + dir; },
      confirmaReiniciar: function (n) {
        return 'Apagar o progresso do nível ' + n +
          ' nesta direção e começar de novo?';
      },
      confirmaZerar: 'Apagar o progresso de todos os níveis e direções?',
      semVoz: '<strong>Nenhuma voz alemã instalada.</strong> O áudio em ' +
        'alemão vai sair com sotaque errado ou não funcionar. No macOS: ' +
        'Ajustes do Sistema → Acessibilidade → Conteúdo Falado → Voz do ' +
        'sistema → Gerenciar vozes → baixe uma voz em Alemão. No Windows: ' +
        'Configurações → Hora e idioma → Idioma e região → adicione ' +
        '“Deutsch” e instale a fala. Enquanto isso, use o link “Ouvir no ' +
        'Google Tradutor”.',
      semFala: '<strong>Este navegador não tem leitura em voz alta.</strong> ' +
        'Use o link “Ouvir no Google Tradutor” em cada card.',
      semVozLista: 'nenhuma voz alemã encontrada',
      vozEfeito: ' — voz de efeito, evite',
      emUso: function (nome, lang, local) {
        return 'Em uso: ' + nome + ' (' + lang + '), ' +
          (local ? 'instalada no aparelho' : 'vinda da internet') + '.';
      },
      semVozCurta: 'Nenhuma voz alemã disponível neste aparelho.',
      semFalaCurta: 'Este navegador não lê em voz alta.',
      semCards: 'Nenhum card neste nível.',
      erroCards: '<main class="tela"><h1>Falha ao carregar os cards</h1>' +
        '<p>O arquivo <code>data/cards.js</code> não foi encontrado. ' +
        'Mantenha a pasta <code>data</code> ao lado do ' +
        '<code>index.html</code>.</p></main>'
    },

    pt: {
      lang: 'de-DE',
      idiomaAlvo: 'pt',
      idiomaBase: 'de',
      titulo: 'Portugiesisch von null',
      saudacao: 'Hallo Giulia, lernen wir Portugiesisch? \u2764\ufe0f',
      subtitulo: 'Alltagssätze als Karteikarten, von A1 bis C1, mit einer ' +
        'Lautschrift, die sich für deutsche Augen lesen lässt.',
      passo1: '1. Niveau wählen',
      passo2: '2. Richtung wählen',
      passo3: '3. Portugiesische Stimme',
      explicaVoz: 'Die Stimme kommt von deinem eigenen Gerät, nicht von ' +
        'dieser Seite. Klingt das Portugiesische deutsch oder englisch, ' +
        'ist das System auf eine falsche Stimme ausgewichen — hier ' +
        'wechseln und ausprobieren.',
      rotuloVoz: 'Stimme für Portugiesisch',
      testarVoz: '🔊 Test: „Boa noite“',
      fraseTeste: 'Boa noite',
      comecar: 'Lernen anfangen',
      zerar: 'Allen Fortschritt löschen',
      voltar: 'Zurück zum Anfang',
      embaralhar: 'Mischen',
      dicaVirar: 'tippe auf die Karte oder drücke <kbd>Leertaste</kbd> ' +
        'zum Umdrehen',
      rotuloAlvo: 'Português',
      rotuloBase: 'Deutsch',
      silabas: 'Silben',
      pronuncia: 'Aussprache',
      ouvirPalavra: '🔊 Wort anhören',
      ouvirFrase: '🔊 Satz anhören',
      ouvirDevagar: '🐢 Langsam anhören',
      ouvirPalavras: '🔉 Wort für Wort',
      tradutor: '↗ Bei Google Übersetzer anhören',
      vozEmUso: 'Portugiesische Stimme:',
      trocarVoz: 'wechseln',
      sei: 'Weiß ich',
      naoSei: 'Weiß ich nicht',
      anterior: '← Zurück',
      proximo: 'Weiter →',
      reiniciar: 'Niveau zurücksetzen',
      atalhos: 'Tasten: <kbd>Leertaste</kbd> umdrehen · <kbd>←</kbd> ' +
        '<kbd>→</kbd> blättern · <kbd>1</kbd> weiß ich · <kbd>2</kbd> ' +
        'weiß ich nicht',
      outroCurso: 'Fala português? → Aprender alemão',
      outroLink: 'index.html',
      niveis: {
        A1: 'Erste Schritte', A2: 'Alltag', B1: 'Selbstständig',
        B2: 'Sicher', C1: 'Souverän'
      },
      direcoes: [
        ['de-pt', 'Deutsch → Portugiesisch',
         'Du siehst den Satz auf Deutsch und versuchst, ihn auf ' +
         'Portugiesisch zu sagen'],
        ['pt-de', 'Portugiesisch → Deutsch',
         'Du siehst den portugiesischen Satz und versuchst, ihn zu verstehen']
      ],
      cards: function (n) { return n + ' Karten'; },
      jaSei: function (n, p) { return n + ' gekonnt (' + p + '%)'; },
      contador: function (a, b, cat) { return a + ' von ' + b + ' · ' + cat; },
      progresso: function (f, t, nivel, rev) {
        return f + ' von ' + t + ' Karten auf Niveau ' + nivel +
          ' als „weiß ich“ markiert' +
          (rev ? ' · ' + rev + ' zum Wiederholen' : '');
      },
      sessao: function (nivel, dir) { return nivel + ' · ' + dir; },
      confirmaReiniciar: function (n) {
        return 'Den Fortschritt auf Niveau ' + n +
          ' in dieser Richtung löschen und neu anfangen?';
      },
      confirmaZerar: 'Den Fortschritt aller Niveaus und Richtungen löschen?',
      semVoz: '<strong>Keine portugiesische Stimme installiert.</strong> ' +
        'Der Ton klingt dann falsch oder bleibt stumm. Unter macOS: ' +
        'Systemeinstellungen → Bedienungshilfen → Gesprochene Inhalte → ' +
        'Systemstimme → Stimmen verwalten → eine Stimme auf ' +
        '„Portugiesisch (Brasilien)“ laden. Unter Windows: Einstellungen → ' +
        'Zeit und Sprache → Sprache und Region → „Português (Brasil)“ ' +
        'hinzufügen und die Sprachausgabe installieren. Solange hilft der ' +
        'Link „Bei Google Übersetzer anhören“.',
      semFala: '<strong>Dieser Browser liest nichts vor.</strong> ' +
        'Nutze auf jeder Karte den Link „Bei Google Übersetzer anhören“.',
      semVozLista: 'keine portugiesische Stimme gefunden',
      vozEfeito: ' — Effektstimme, lieber meiden',
      emUso: function (nome, lang, local) {
        return 'Aktiv: ' + nome + ' (' + lang + '), ' +
          (local ? 'auf dem Gerät installiert' : 'aus dem Internet') + '.';
      },
      semVozCurta: 'Auf diesem Gerät gibt es keine portugiesische Stimme.',
      semFalaCurta: 'Dieser Browser liest nichts vor.',
      semCards: 'Auf diesem Niveau gibt es keine Karten.',
      erroCards: '<main class="tela"><h1>Karten konnten nicht geladen ' +
        'werden</h1><p>Die Datei <code>data/cards.js</code> wurde nicht ' +
        'gefunden. Der Ordner <code>data</code> muss neben der ' +
        'HTML-Datei liegen.</p></main>'
    }
  };

  var T = TEXTOS[CURSO];

  var CATEGORIAS = {
    de: {
      ambiente: 'meio ambiente', apresentacao: 'apresentação',
      argumentacao: 'argumentação', burocracia: 'burocracia',
      ciencia: 'ciência', cidade: 'cidade', clima: 'clima', comida: 'comida',
      compras: 'compras', comunicacao: 'comunicação', cultura: 'cultura',
      cumprimentos: 'cumprimentos', descricao: 'descrição',
      digital: 'vida digital', dinheiro: 'dinheiro', direito: 'direito',
      economia: 'economia', educacao: 'educação', escola: 'escola e trabalho',
      familia: 'família', historia: 'história e futuro',
      idiomatico: 'expressões idiomáticas', lazer: 'lazer', midia: 'mídia',
      moradia: 'moradia', numeros: 'números', opiniao: 'opinião',
      passado: 'passado', planos: 'planos', politica: 'política',
      relacoes: 'relações', restaurante: 'restaurante', rotina: 'rotina',
      saude: 'saúde', sentidos: 'sentidos e sentimentos',
      sentimentos: 'sentimentos', servicos: 'serviços', sociedade: 'sociedade',
      sustentabilidade: 'sustentabilidade', tecnologia: 'tecnologia',
      tempo: 'tempo e horas', trabalho: 'trabalho', viagem: 'viagem'
    },
    pt: {
      ambiente: 'Umwelt', apresentacao: 'Sich vorstellen',
      argumentacao: 'Argumentieren', burocracia: 'Behörden',
      ciencia: 'Wissenschaft', cidade: 'Stadt', clima: 'Wetter',
      comida: 'Essen', compras: 'Einkaufen', comunicacao: 'Kommunikation',
      cultura: 'Kultur', cumprimentos: 'Begrüßung', descricao: 'Beschreiben',
      digital: 'Digitales', dinheiro: 'Geld', direito: 'Recht',
      economia: 'Wirtschaft', educacao: 'Ausbildung', escola: 'Schule',
      familia: 'Familie', historia: 'Geschichte und Zukunft',
      idiomatico: 'Redewendungen', lazer: 'Freizeit', midia: 'Medien',
      moradia: 'Wohnen', numeros: 'Zahlen', opiniao: 'Meinung',
      passado: 'Vergangenheit', planos: 'Pläne', politica: 'Politik',
      relacoes: 'Beziehungen', restaurante: 'Restaurant', rotina: 'Alltag',
      saude: 'Gesundheit', sentidos: 'Sinne und Gefühle',
      sentimentos: 'Gefühle', servicos: 'Dienstleistungen',
      sociedade: 'Gesellschaft', sustentabilidade: 'Nachhaltigkeit',
      tecnologia: 'Technik', tempo: 'Zeit und Uhrzeit', trabalho: 'Arbeit',
      viagem: 'Reisen'
    }
  };

  // -------------------------------------------------------------- utilidades

  function $(id) { return document.getElementById(id); }

  function cardsDoNivel(nivel) {
    return CARDS.filter(function (c) { return c.nivel === nivel; });
  }

  function chave(nivel, direcao) {
    return VERSAO_ARMAZENAMENTO + ':' + CURSO + ':' + nivel + ':' + direcao;
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
    } catch (e) { /* modo privado: segue sem salvar */ }
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
    direcao: T.direcoes[0][0],
    deck: [],
    pos: 0,
    virado: false,
    sabidos: {},
    naoSabidos: {}
  };

  function cardAtual() {
    var id = estado.deck[estado.pos];
    for (var i = 0; i < CARDS.length; i++) {
      if (CARDS[i].id === id) { return CARDS[i]; }
    }
    return null;
  }

  /* Dados do card no idioma que o aluno está aprendendo. */
  function ladoAlvo(card) {
    return CURSO === 'de'
      ? { frase: card.de, palavras: card.palavras, pronuncia: card.pronuncia,
          campo: 'de' }
      : { frase: card.pt, palavras: card.palavrasPt,
          pronuncia: card.pronunciaPt, campo: 'pt' };
  }

  function ladoBase(card) {
    return CURSO === 'de' ? card.pt : card.de;
  }

  function notaGramatical(card) {
    return CURSO === 'de' ? card.gramatica : card.gramatikPt;
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

  var voz = { alvo: null, base: null };
  var CHAVE_VOZ = VERSAO_ARMAZENAMENTO + ':voz-' + CURSO;

  var VOZES_NOVIDADE = [
    'eddy', 'flo', 'grandma', 'grandpa', 'reed', 'rocko', 'sandy', 'shelley',
    'bubbles', 'bells', 'boing', 'jester', 'organ', 'superstar', 'trinoids',
    'whisper', 'wobble', 'bahh', 'bad news', 'good news', 'albert', 'cellos',
    'zarvox', 'novelty', 'eloquence'
  ];

  var VOZES_BOAS = {
    de: ['google deutsch', 'anna', 'petra', 'markus', 'yannick', 'helena',
         'viktor', 'katja', 'hedda', 'stefan', 'conrad', 'amala', 'killian'],
    pt: ['google português do brasil', 'google portugues', 'luciana',
         'joana', 'felipe', 'fernanda', 'daniel', 'maria', 'raquel',
         'catarina', 'helo', 'brasil']
  };

  function ehNovidade(nome) {
    var n = (nome || '').toLowerCase();
    for (var i = 0; i < VOZES_NOVIDADE.length; i++) {
      if (n.indexOf(VOZES_NOVIDADE[i]) === 0 ||
          n.indexOf('(' + VOZES_NOVIDADE[i]) >= 0) { return true; }
    }
    return false;
  }

  function vozesDoIdioma(prefixo) {
    if (!('speechSynthesis' in window)) { return []; }
    var todas = window.speechSynthesis.getVoices() || [];
    return todas.filter(function (v) {
      return (v.lang || '').toLowerCase().replace('_', '-')
        .indexOf(prefixo) === 0;
    });
  }

  function pontuarVoz(v, idioma) {
    var nome = (v.name || '').toLowerCase();
    var lista = VOZES_BOAS[idioma] || [];
    for (var i = 0; i < lista.length; i++) {
      if (nome.indexOf(lista[i]) >= 0) { return 100 - i; }
    }
    // pt-BR é preferível a pt-PT neste curso
    var bonus = (idioma === 'pt' &&
      (v.lang || '').toLowerCase().indexOf('pt-br') === 0) ? 20 : 0;
    return (ehNovidade(v.name) ? -10 : 10) + bonus;
  }

  function lerVozSalva() {
    try { return localStorage.getItem(CHAVE_VOZ) || ''; } catch (e) { return ''; }
  }

  function gravarVozSalva(uri) {
    try { localStorage.setItem(CHAVE_VOZ, uri || ''); } catch (e) {}
  }

  function escolherVozes() {
    if (!('speechSynthesis' in window)) { return; }
    var alvo = vozesDoIdioma(T.idiomaAlvo);
    var salva = lerVozSalva();

    voz.alvo = null;
    if (salva) {
      for (var i = 0; i < alvo.length; i++) {
        if (alvo[i].voiceURI === salva || alvo[i].name === salva) {
          voz.alvo = alvo[i];
          break;
        }
      }
    }
    if (!voz.alvo && alvo.length) {
      voz.alvo = alvo.slice().sort(function (a, b) {
        return pontuarVoz(b, T.idiomaAlvo) - pontuarVoz(a, T.idiomaAlvo);
      })[0];
    }

    var base = vozesDoIdioma(T.idiomaBase);
    voz.base = base.length ? base.slice().sort(function (a, b) {
      return pontuarVoz(b, T.idiomaBase) - pontuarVoz(a, T.idiomaBase);
    })[0] : null;

    preencherSeletorVoz(alvo);
    mostrarAvisoVoz(
      (window.speechSynthesis.getVoices() || []).length > 0, alvo.length);
    mostrarVozAtual();
  }

  function preencherSeletorVoz(disponiveis) {
    var sel = $('seletor-voz');
    if (!sel) { return; }
    var atual = voz.alvo ? voz.alvo.voiceURI : '';
    if (sel.dataset.qtd === String(disponiveis.length) &&
        sel.value === atual) { return; }
    sel.innerHTML = '';
    if (!disponiveis.length) {
      var vazio = document.createElement('option');
      vazio.textContent = T.semVozLista;
      sel.appendChild(vazio);
      sel.disabled = true;
      return;
    }
    sel.disabled = false;
    disponiveis.slice().sort(function (a, b) {
      return pontuarVoz(b, T.idiomaAlvo) - pontuarVoz(a, T.idiomaAlvo);
    }).forEach(function (v) {
      var op = document.createElement('option');
      op.value = v.voiceURI;
      op.textContent = v.name + ' (' + v.lang + ')' +
        (ehNovidade(v.name) ? T.vozEfeito : '');
      sel.appendChild(op);
    });
    sel.value = atual;
    sel.dataset.qtd = String(disponiveis.length);
  }

  function mostrarAvisoVoz(vozesCarregadas, quantas) {
    var alvo = $('aviso-voz');
    if (!alvo) { return; }
    if (!('speechSynthesis' in window)) {
      alvo.innerHTML = T.semFala;
      alvo.hidden = false;
      return;
    }
    if (vozesCarregadas && (!voz.alvo || quantas === 0)) {
      alvo.innerHTML = T.semVoz;
      alvo.hidden = false;
    } else {
      alvo.hidden = true;
    }
  }

  function mostrarVozAtual() {
    var alvo = $('voz-atual');
    if (alvo) {
      alvo.textContent = voz.alvo ? voz.alvo.name : T.semVozCurta;
    }
    var diag = $('diagnostico-voz');
    if (!diag) { return; }
    if (!('speechSynthesis' in window)) {
      diag.textContent = T.semFalaCurta;
    } else if (!voz.alvo) {
      diag.textContent = T.semVozCurta;
    } else {
      diag.textContent = T.emUso(voz.alvo.name, voz.alvo.lang,
        voz.alvo.localService);
    }
  }

  function falar(texto, qual, velocidade) {
    if (!('speechSynthesis' in window)) { return; }
    if ((qual === 'base' && !voz.base) || (qual !== 'base' && !voz.alvo)) {
      escolherVozes();
    }
    window.speechSynthesis.cancel();
    var fala = new SpeechSynthesisUtterance(texto);
    var escolhida = qual === 'base' ? voz.base : voz.alvo;
    var idioma = qual === 'base' ? T.idiomaBase : T.idiomaAlvo;
    fala.lang = escolhida ? escolhida.lang
      : (idioma === 'pt' ? 'pt-BR' : 'de-DE');
    if (escolhida) { fala.voice = escolhida; }
    fala.rate = velocidade || 1;
    window.speechSynthesis.speak(fala);
  }

  function falarPalavras(palavras, campo) {
    if (!('speechSynthesis' in window)) { return; }
    if (!voz.alvo) { escolherVozes(); }
    window.speechSynthesis.cancel();
    palavras.forEach(function (p) {
      var fala = new SpeechSynthesisUtterance(p[campo]);
      fala.lang = voz.alvo ? voz.alvo.lang
        : (T.idiomaAlvo === 'pt' ? 'pt-BR' : 'de-DE');
      if (voz.alvo) { fala.voice = voz.alvo; }
      fala.rate = 0.75;
      window.speechSynthesis.speak(fala);
    });
  }

  // ------------------------------------------------------------ tela inicial

  function aplicarTextos() {
    document.documentElement.lang = T.lang;
    document.title = T.titulo;
    var mapa = {
      'txt-titulo': T.titulo, 'txt-saudacao': T.saudacao,
      'txt-subtitulo': T.subtitulo,
      'txt-passo1': T.passo1, 'txt-passo2': T.passo2, 'txt-passo3': T.passo3,
      'txt-explica-voz': T.explicaVoz, 'rotulo-voz': T.rotuloVoz,
      'btn-testar-voz': T.testarVoz, 'btn-comecar': T.comecar,
      'btn-zerar-tudo': T.zerar, 'btn-ouvir': T.ouvirFrase,
      'btn-ouvir-devagar': T.ouvirDevagar,
      'btn-ouvir-palavras': T.ouvirPalavras, 'link-tradutor': T.tradutor,
      'painel-ouvir': T.ouvirPalavra, 'txt-silabas': T.silabas,
      'txt-pronuncia': T.pronuncia, 'txt-voz-em-uso': T.vozEmUso,
      'btn-trocar-voz': T.trocarVoz, 'btn-reiniciar': T.reiniciar,
      'btn-anterior': T.anterior, 'btn-proximo': T.proximo,
      'link-outro-curso': T.outroCurso
    };
    Object.keys(mapa).forEach(function (id) {
      var el = $(id);
      if (el) { el.textContent = mapa[id]; }
    });
    var comHtml = { 'txt-dica': T.dicaVirar, 'txt-atalhos': T.atalhos };
    Object.keys(comHtml).forEach(function (id) {
      var el = $(id);
      if (el) { el.innerHTML = comHtml[id]; }
    });
    $('btn-sei').innerHTML = T.sei + ' <kbd>1</kbd>';
    $('btn-nao-sei').innerHTML = T.naoSei + ' <kbd>2</kbd>';
    $('btn-voltar').setAttribute('aria-label', T.voltar);
    $('btn-embaralhar').setAttribute('aria-label', T.embaralhar);
    $('btn-embaralhar').title = T.embaralhar;
    $('link-outro-curso').href = T.outroLink;
  }

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
          '<span class="nivel-titulo">' + T.niveis[nivel] + '</span>' +
          '<span class="nivel-detalhe">' + T.cards(total) + ' · ' +
            T.jaSei(feitos, pct) + '</span>' +
          '<span class="nivel-progresso"><span style="width:' + pct +
            '%"></span></span>' +
        '</span>';
      botao.addEventListener('click', function () {
        estado.nivel = nivel;
        desenharNiveis();
      });
      alvo.appendChild(botao);
    });
  }

  function desenharDirecoes() {
    var alvo = $('lista-direcoes');
    if (!alvo) { return; }
    alvo.innerHTML = '';
    T.direcoes.forEach(function (d) {
      var botao = document.createElement('button');
      botao.type = 'button';
      botao.className = 'direcao';
      botao.setAttribute('data-direcao', d[0]);
      botao.setAttribute('aria-pressed', d[0] === estado.direcao ? 'true' : 'false');
      botao.innerHTML = '<strong>' + d[1] + '</strong><small>' + d[2] + '</small>';
      botao.addEventListener('click', function () {
        estado.direcao = d[0];
        desenharDirecoes();
        desenharNiveis();
      });
      alvo.appendChild(botao);
    });
  }

  function rotuloDirecao() {
    for (var i = 0; i < T.direcoes.length; i++) {
      if (T.direcoes[i][0] === estado.direcao) { return T.direcoes[i][1]; }
    }
    return '';
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
      $('frase-frente').textContent = T.semCards;
      return;
    }

    var alvo = ladoAlvo(card);
    var base = ladoBase(card);
    // a direção diz qual idioma aparece na FRENTE
    var alvoNaFrente = estado.direcao.indexOf(T.idiomaAlvo) === 0;

    $('rotulo-sessao').textContent = T.sessao(estado.nivel, rotuloDirecao());
    $('contador').textContent = T.contador(estado.pos + 1, estado.deck.length,
      CATEGORIAS[CURSO][card.categoria] || card.categoria);

    $('etiqueta-frente').textContent = alvoNaFrente ? T.rotuloAlvo : T.rotuloBase;
    $('frase-frente').textContent = alvoNaFrente ? alvo.frase : base;
    $('etiqueta-verso').textContent = alvoNaFrente ? T.rotuloBase : T.rotuloAlvo;
    $('frase-verso').textContent = alvoNaFrente ? base : alvo.frase;
    $('pronuncia-frase').textContent = '[ ' + alvo.pronuncia + ' ]';

    var gram = $('gramatica');
    var nota = notaGramatical(card);
    if (nota) {
      gram.textContent = nota;
      gram.hidden = false;
    } else {
      gram.hidden = true;
    }

    desenharPalavras(alvo);
    fecharPainelPalavra();

    var de = T.idiomaAlvo === 'pt' ? 'pt' : 'de';
    var para = T.idiomaBase === 'pt' ? 'pt' : 'de';
    $('link-tradutor').href = 'https://translate.google.com/?sl=' + de +
      '&tl=' + para + '&text=' + encodeURIComponent(alvo.frase) +
      '&op=translate';

    $('card').classList.toggle('virado', estado.virado);
    $('btn-anterior').disabled = estado.pos === 0;
    ajustarAlturaCard();

    var feitos = Object.keys(estado.sabidos).length;
    var pct = total ? Math.round((feitos / total) * 100) : 0;
    $('progresso-barra').style.width = pct + '%';
    $('progresso').setAttribute('aria-valuenow', String(pct));
    $('progresso-texto').textContent = T.progresso(feitos, total, estado.nivel,
      Object.keys(estado.naoSabidos).length);
  }

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

  function desenharPalavras(alvo) {
    var lista = $('palavras');
    lista.innerHTML = '';
    (alvo.palavras || []).forEach(function (palavra) {
      var botao = document.createElement('button');
      botao.type = 'button';
      botao.className = 'palavra';
      botao.textContent = palavra[alvo.campo];
      botao.addEventListener('click', function (ev) {
        ev.stopPropagation();
        abrirPainelPalavra(palavra, alvo.campo, botao);
      });
      lista.appendChild(botao);
    });
  }

  function abrirPainelPalavra(palavra, campo, botao) {
    var ativos = document.querySelectorAll('.palavra.ativa');
    for (var i = 0; i < ativos.length; i++) { ativos[i].classList.remove('ativa'); }
    if (botao) { botao.classList.add('ativa'); }

    var outro = campo === 'de' ? 'pt' : 'de';
    $('painel-de').textContent = palavra[campo];
    $('painel-pt').textContent = palavra[outro];
    $('painel-silabas').textContent = palavra.silabas;
    $('painel-pronuncia').textContent = palavra.pronuncia;
    $('painel-palavra').hidden = false;
    $('painel-ouvir').onclick = function (ev) {
      ev.stopPropagation();
      falar(palavra[campo], 'alvo', 0.75);
    };
    falar(palavra[campo], 'alvo', 0.8);
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
    if (!window.confirm(T.confirmaReiniciar(estado.nivel))) { return; }
    try { localStorage.removeItem(chave(estado.nivel, estado.direcao)); } catch (e) {}
    montarDeck();
    desenharCard();
  }

  function zerarTudo() {
    if (!window.confirm(T.confirmaZerar)) { return; }
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

    var seletor = $('seletor-voz');
    if (seletor) {
      seletor.addEventListener('change', function () {
        gravarVozSalva(this.value);
        escolherVozes();
        falar(T.fraseTeste, 'alvo', 0.9);
      });
    }
    var testar = $('btn-testar-voz');
    if (testar) {
      testar.addEventListener('click', function () {
        falar(T.fraseTeste, 'alvo', 0.9);
      });
    }
    var trocar = $('btn-trocar-voz');
    if (trocar) { trocar.addEventListener('click', voltarAoInicio); }

    $('btn-comecar').addEventListener('click', iniciarSessao);
    $('btn-zerar-tudo').addEventListener('click', zerarTudo);
    $('btn-voltar').addEventListener('click', voltarAoInicio);

    $('card').addEventListener('click', virar);
    $('card').addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter') { ev.preventDefault(); virar(); }
    });

    $('fechar-painel').addEventListener('click', function (ev) {
      ev.stopPropagation();
      fecharPainelPalavra();
    });
    $('painel-palavra').addEventListener('click', function (ev) {
      ev.stopPropagation();
    });

    $('btn-ouvir').addEventListener('click', function () {
      var c = cardAtual();
      if (c) { falar(ladoAlvo(c).frase, 'alvo', 1); }
    });
    $('btn-ouvir-devagar').addEventListener('click', function () {
      var c = cardAtual();
      if (c) { falar(ladoAlvo(c).frase, 'alvo', 0.55); }
    });
    $('btn-ouvir-palavras').addEventListener('click', function () {
      var c = cardAtual();
      if (c) {
        var alvo = ladoAlvo(c);
        falarPalavras(alvo.palavras || [], alvo.campo);
      }
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
      if (alvo && (alvo.tagName === 'INPUT' || alvo.tagName === 'TEXTAREA' ||
          alvo.tagName === 'SELECT')) { return; }
      switch (ev.key) {
        case ' ':
        case 'Spacebar':
          ev.preventDefault(); virar(); break;
        case 'ArrowRight':
          ev.preventDefault(); proximo(); break;
        case 'ArrowLeft':
          ev.preventDefault(); irPara(estado.pos - 1); break;
        case '1': marcar(true); break;
        case '2': marcar(false); break;
        case 'Escape': fecharPainelPalavra(); break;
        default: break;
      }
    });
  }

  // ------------------------------------------------------------------ início

  function iniciar() {
    if (!CARDS.length) {
      document.body.innerHTML = T.erroCards;
      return;
    }
    aplicarTextos();
    desenharNiveis();
    desenharDirecoes();
    ligarEventos();

    if ('speechSynthesis' in window) {
      escolherVozes();
      window.speechSynthesis.onvoiceschanged = escolherVozes;
      window.setTimeout(escolherVozes, 400);
      window.setTimeout(escolherVozes, 1500);
    } else {
      mostrarAvisoVoz(false, 0);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', iniciar);
  } else {
    iniciar();
  }
}());
