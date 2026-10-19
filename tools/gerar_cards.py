# -*- coding: utf-8 -*-
"""
Gera data/cards.js a partir das frases (frases_*.py) e do lexico (lexico.py).

Uso:
    python3 tools/gerar_cards.py

O script:
  1. separa cada frase alema em palavras;
  2. busca a traducao de cada palavra no lexico;
  3. calcula silabas e pronuncia pelas regras de regras.py;
  4. monta a pronuncia da frase inteira;
  5. valida ids, campos obrigatorios e frases repetidas;
  6. escreve data/cards.js e imprime o resumo por nivel e categoria.

Se faltar alguma palavra no lexico, o script lista as pendencias em formato
pronto para colar em lexico.py e nao escreve o arquivo.
"""
import io
import json
import os
import re
import sys
import unicodedata
from collections import Counter, OrderedDict

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)

import regras                                    # noqa: E402
import regras_pt                                 # noqa: E402
from lexico import LEXICO                        # noqa: E402
from lexico_pt import LEXICO_PT                  # noqa: E402
from notas_pt import NOTAS_PT                    # noqa: E402

NIVEIS = ["A1", "A2", "B1", "B2", "C1"]

# palavras funcionais ficam em minusculas na pronuncia da frase
ATONAS = {
    "ich", "du", "er", "sie", "es", "wir", "ihr", "mich", "dich", "sich",
    "mir", "dir", "ihm", "ihn", "uns", "euch", "ihnen", "man",
    "der", "die", "das", "den", "dem", "des", "ein", "eine", "einen",
    "einem", "einer", "eines", "kein", "keine", "und", "oder", "aber",
    "in", "im", "an", "am", "auf", "aus", "bei", "mit", "von", "vom",
    "zu", "zum", "zur", "für", "um", "als", "wie", "wo", "ist",
    "bin", "bist", "sind", "war", "hat", "habe", "hast", "haben",
    "nicht", "noch", "nur", "so", "da", "dass", "ob", "zum", "schon",
    "mein", "meine", "dein", "deine", "sein", "seine", "ihre", "mal",
}


# Palavras portuguesas atonas, que ficam em minusculas na pronuncia da frase.
ATONAS_PT = {
    "a", "o", "as", "os", "um", "uma", "uns", "umas",
    "de", "da", "do", "das", "dos", "d", "em", "na", "no", "nas", "nos",
    "ao", "aos", "\u00e0", "\u00e0s", "pelo", "pela", "pelos", "pelas",
    "e", "ou", "que", "se", "com", "por", "para", "pra", "n\u00e3o",
    "me", "te", "lhe", "nos", "vos", "lhes", "o", "a",
    "meu", "minha", "seu", "sua", "teu", "tua", "este", "esta", "esse",
    "essa", "isso", "\u00e9", "foi", "era", "s\u00e3o", "est\u00e1",
    "eu", "voc\u00ea", "ele", "ela", "n\u00f3s", "eles", "elas",
}


def tokenizar(frase):
    """Lista de palavras de uma frase alema, sem pontuacao."""
    bruto = re.findall(r"[A-Za-zÀ-ɏ]+(?:[’'-][A-Za-zÀ-ɏ]+)*", frase)
    return [t for t in bruto if t]


def montar_palavras(frase_de, faltando):
    palavras = []
    for tok in tokenizar(frase_de):
        pt = LEXICO.get(tok) or LEXICO.get(tok.lower())
        if not pt:
            faltando[tok.lower()] += 1
            pt = "?"
        palavras.append(OrderedDict([
            ("de", tok),
            ("pt", pt),
            ("silabas", regras.silabas_str(tok)),
            ("pronuncia", regras.pronunciar(tok)),
        ]))
    return palavras


def pronuncia_frase(palavras, atonas=None, campo="de"):
    atonas = ATONAS if atonas is None else atonas
    saida = []
    for p in palavras:
        pron = p["pronuncia"]
        if p[campo].lower() in atonas and "-" not in pron:
            pron = pron.lower()
        saida.append(pron)
    return " ".join(saida)


def montar_palavras_pt(frase_pt, faltando):
    """Mesma ideia de montar_palavras, mas para o lado portugues."""
    palavras = []
    for tok in tokenizar(frase_pt):
        de = LEXICO_PT.get(tok) or LEXICO_PT.get(tok.lower())
        if not de:
            faltando[tok.lower()] += 1
            de = "?"
        palavras.append(OrderedDict([
            ("pt", tok),
            ("de", de),
            ("silabas", regras_pt.silabas_str(tok)),
            ("pronuncia", regras_pt.pronunciar(tok)),
        ]))
    return palavras


def carregar_frases():
    todas = []
    for nivel in NIVEIS:
        mod = __import__("frases_%s" % nivel.lower())
        for item in mod.FRASES:
            categoria, pt, de = item[0], item[1], item[2]
            gramatica = item[3] if len(item) > 3 else None
            todas.append((nivel, categoria, pt, de, gramatica))
    return todas


def main():
    frases = carregar_frases()
    faltando = Counter()
    faltando_pt = Counter()
    cards = []
    vistos_de, vistos_pt = {}, {}
    erros = []

    for i, (nivel, categoria, pt, de, gramatica) in enumerate(frases, start=1):
        chave_de = de.strip().lower()
        if chave_de in vistos_de:
            erros.append("frase alema repetida: %r (ids %d e %d)"
                         % (de, vistos_de[chave_de], i))
        vistos_de[chave_de] = i
        chave_pt = pt.strip().lower()
        if chave_pt in vistos_pt:
            erros.append("frase portuguesa repetida: %r (ids %d e %d)"
                         % (pt, vistos_pt[chave_pt], i))
        vistos_pt[chave_pt] = i

        palavras = montar_palavras(de, faltando)
        palavras_pt = montar_palavras_pt(pt, faltando_pt)
        card = OrderedDict([
            ("id", i),
            ("nivel", nivel),
            ("categoria", categoria),
            ("pt", pt),
            ("de", de),
            ("palavras", palavras),
            ("pronuncia", pronuncia_frase(palavras)),
            ("palavrasPt", palavras_pt),
            ("pronunciaPt", pronuncia_frase(palavras_pt, ATONAS_PT, "pt")),
        ])
        if gramatica:
            card["gramatica"] = gramatica
        if NOTAS_PT.get(i):
            card["gramatikPt"] = NOTAS_PT[i]
        cards.append(card)

    if faltando:
        print("Faltam %d palavras no lexico. Cole em lexico.py:\n" % len(faltando))
        for palavra, n in sorted(faltando.items()):
            print('    %-22s "",   # %dx' % ('"%s":' % palavra, n))
        return 1

    if faltando_pt:
        print("Faltam %d palavras no lexico PT. Cole em lexico_pt.py:\n"
              % len(faltando_pt))
        for palavra, n in sorted(faltando_pt.items()):
            print('    %-22s "",   # %dx' % ('"%s":' % palavra, n))
        return 1

    # validacoes
    ids = [c["id"] for c in cards]
    if len(set(ids)) != len(ids):
        erros.append("ids repetidos")
    for c in cards:
        for campo in ("id", "nivel", "categoria", "pt", "de", "pronuncia"):
            if not c.get(campo):
                erros.append("card %s sem campo %s" % (c["id"], campo))
        if not c["palavras"]:
            erros.append("card %s sem palavras" % c["id"])
        for p in c["palavras"]:
            for campo in ("de", "pt", "silabas", "pronuncia"):
                if not p.get(campo) or p[campo] == "?":
                    erros.append("card %s: palavra %r sem %s"
                                 % (c["id"], p["de"], campo))
        if not c["palavrasPt"]:
            erros.append("card %s sem palavrasPt" % c["id"])
        for p in c["palavrasPt"]:
            for campo in ("de", "pt", "silabas", "pronuncia"):
                if not p.get(campo) or p[campo] == "?":
                    erros.append("card %s: palavra PT %r sem %s"
                                 % (c["id"], p["pt"], campo))
        if c["nivel"] not in NIVEIS:
            erros.append("card %s com nivel invalido" % c["id"])

    if erros:
        print("ERROS:")
        for e in erros[:40]:
            print("  -", e)
        print("total de erros:", len(erros))
        return 1

    # escreve data/cards.js
    linhas = [
        "/* Base de cards do curso de alemao.",
        " * Gerado por tools/gerar_cards.py - nao edite a mao se for regerar.",
        " * Total de cards: %d" % len(cards),
        " */",
        "const CARDS = [",
    ]
    for c in cards:
        linhas.append("  " + json.dumps(c, ensure_ascii=False) + ",")
    linhas.append("];")
    linhas.append("")
    linhas.append("if (typeof window !== 'undefined') { window.CARDS = CARDS; }")
    linhas.append("")
    destino = os.path.join(RAIZ, "data", "cards.js")
    io.open(destino, "w", encoding="utf-8").write("\n".join(linhas))

    # resumo
    print("data/cards.js escrito com %d cards.\n" % len(cards))
    por_nivel = Counter(c["nivel"] for c in cards)
    print("Por nivel:")
    for n in NIVEIS:
        print("  %-3s %4d cards" % (n, por_nivel[n]))
    print("\nPor nivel e categoria:")
    for n in NIVEIS:
        cats = Counter(c["categoria"] for c in cards if c["nivel"] == n)
        print("  %s:" % n)
        for cat, qtd in sorted(cats.items(), key=lambda x: (-x[1], x[0])):
            print("     %-28s %3d" % (cat, qtd))
    palavras_unicas = set()
    for c in cards:
        for p in c["palavras"]:
            palavras_unicas.add(p["de"].lower())
    print("\nPalavras alemas distintas: %d" % len(palavras_unicas))
    print("Entradas no lexico: %d" % len(LEXICO))
    return 0


if __name__ == "__main__":
    sys.exit(main())
