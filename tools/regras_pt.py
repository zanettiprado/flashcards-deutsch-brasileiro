# -*- coding: utf-8 -*-
"""
Regras de silabacao do portugues e de pronuncia aproximada escrita para
quem le ALEMAO.

Espelho de regras.py. A partir de uma palavra portuguesa produz:
  - silabas  : "co-ra-cao"  (com os acentos reais: "co-ra-cao" -> "co-ra-cao")
  - pronuncia: "ko-ra-SSAUNG"  (silaba tonica em maiusculas)

A transcricao e pensada para um leitor alemao: "ss" porque o s simples alemao
entre vogais soa [z], "sch" para o nosso ch, "w" para o nosso v, "zh" para o
som do j, "ng" para marcar vogal nasal, e assim por diante. A legenda completa
fica no README e na propria pagina.
"""

VOGAIS = set("aeiouáéíóúâêôãõà")
ACENTO_FORTE = set("áéíóúâêô")   # a e i o u com acento
TIL = set("ãõ")
FRACAS = set("iu")                                                        # formam ditongo

# digrafos consonantais que NAO se separam e abrem silaba
DIG_INSEPARAVEIS = ["ch", "lh", "nh"]

# digrafos que SE SEPARAM: car-ro, pas-sar, nas-cer, ex-ce-to
DIG_SEPARAVEIS = ["rr", "ss", "sc", "sç", "xc", "xs"]

# grupos consoante + l/r que abrem silaba juntos
ONSETS = [
    "bl", "br", "cl", "cr", "dl", "dr", "fl", "fr", "gl", "gr",
    "pl", "pr", "tl", "tr", "vl", "vr", "ps", "pn", "mn",
]

SILABAS_OVERRIDE = {
    # i/u nasal que forma silaba propria, contra a regra do ditongo
    "ainda": "a-in-da", "ruim": "ru-im", "rainha": "ra-i-nha",
    "moinho": "mo-i-nho", "bainha": "ba-i-nha",
}
TONICA_OVERRIDE = {}
PRONUNCIA_OVERRIDE = {
    "muito": "MUING-tu", "muitos": "MUING-tuss",
    "muita": "MUING-ta", "muitas": "MUING-tass",
    # monossilabos atonos: no Brasil o -e final soa [i] e o -o final soa [u]
    "de": "dschi", "me": "mi", "te": "tschi", "se": "ssi", "que": "ki",
    "lhe": "lji", "e": "i", "o": "u", "os": "uss", "do": "du",
    "dos": "duss", "no": "nu", "nos": "nuss", "ao": "au", "aos": "auss",
    "pelo": "PE-lu", "pelos": "PE-luss",
}

# "x" tem quatro leituras; o padrao aqui e [sch] e o resto vem por excecao
X_COMO_KS = {"táxi", "fixo", "tóxico", "léxico", "anexo", "sexo", "oxigênio"}
X_COMO_Z = {"exame", "exato", "exemplo", "exercício", "existe", "existem",
            "exigir", "exige", "exato", "exílio", "êxito", "executar"}
X_COMO_SS = {"próximo", "próxima", "máximo", "máxima",
             "aproximar", "trouxe", "auxílio", "sexta", "sextas",
             "sexto", "texto", "textos", "contexto", "extra", "externo"}


# ---------------------------------------------------------------- silabacao

def _unidades(s):
    """Quebra em unidades: nucleos vocalicos e unidades consonantais."""
    out = []
    i = 0
    n = len(s)
    while i < n:
        dig = s[i:i + 2]
        if dig in DIG_INSEPARAVEIS:
            out.append(("C", dig)); i += 2; continue
        # gu / qu antes de vogal formam uma unidade: guar-dar, a-gua, que
        if dig in ("gu", "qu") and i + 2 < n and s[i + 2] in VOGAIS:
            out.append(("C", dig)); i += 2; continue
        c = s[i]
        out.append(("V" if c in VOGAIS else "C", c))
        i += 1
    return out


def _junta_ditongos(un, tem_acento=False):
    """Agrupa vogais que ficam na mesma silaba (ditongos e nasais)."""
    out = []
    i = 0
    while i < len(un):
        t, v = un[i]
        if t != "V":
            out.append((t, v)); i += 1; continue
        nucleo = v
        # encadeia vogais seguintes enquanto formarem ditongo
        while i + 1 < len(un) and un[i + 1][0] == "V":
            prox = un[i + 1][1]
            ult = nucleo[-1]
            # i/u com acento proprio sempre abrem hiato: sa-i-da, ru-i-na
            if prox in ACENTO_FORTE and prox in "íú":
                break
            # ditongo decrescente: vogal + i/u atonos  (pai, lei, meu, mau)
            if prox in FRACAS:
                nucleo += prox; i += 1; continue
            # Ditongo crescente (his-to-ria) so em palavra que ja tem acento
            # grafico. Sem acento, o i/u e que leva a tonica e abre hiato:
            # di-a, Ma-ri-a, pi-a-no, i-di-o-ma.
            if (ult in FRACAS and len(nucleo) == 1
                    and tem_acento and prox not in ACENTO_FORTE):
                nucleo += prox; i += 1; continue
            # til + vogal: mae, poe, pao
            if ult in TIL and prox in "eo":
                nucleo += prox; i += 1; continue
            break
        out.append(("V", nucleo)); i += 1
    return out


def _silabar_simples(s):
    tem_acento = any(c in ACENTO_FORTE or c in TIL for c in s)
    un = _junta_ditongos(_unidades(s), tem_acento)
    idx_v = [k for k, (t, _) in enumerate(un) if t == "V"]
    if len(idx_v) <= 1:
        return ["".join(v for _, v in un)]

    cortes = []
    for a, b in zip(idx_v, idx_v[1:]):
        meio = un[a + 1:b]
        if not meio:
            cortes.append(b)                       # hiato: sa-i-da
        elif len(meio) == 1:
            cortes.append(b - 1)                   # uma consoante vai adiante
        else:
            dois = "".join(v for _, v in meio[-2:])
            if dois in DIG_SEPARAVEIS:
                cortes.append(b - 1)               # car-ro, pas-sar, nas-cer
            elif dois in ONSETS:
                cortes.append(b - 2)               # a-bra-co, re-gra
            else:
                cortes.append(b - 1)               # por-ta, cam-po
    silabas, ini = [], 0
    for c in cortes:
        silabas.append("".join(v for _, v in un[ini:c]))
        ini = c
    silabas.append("".join(v for _, v in un[ini:]))
    return [x for x in silabas if x]


def silabar(palavra):
    base = palavra.strip()
    chave = base.lower()
    if chave in SILABAS_OVERRIDE:
        return SILABAS_OVERRIDE[chave].split("-")
    if "-" in base:
        partes = []
        for p in base.split("-"):
            if p:
                partes.extend(silabar(p))
        return partes
    silabas = _silabar_simples(chave)
    if base[:1].isupper() and silabas:
        silabas[0] = silabas[0][:1].upper() + silabas[0][1:]
    return silabas


def silabas_str(palavra):
    return "-".join(silabar(palavra))


# -------------------------------------------------------------- tonicidade

FINAIS_PAROXITONAS = ("a", "as", "e", "es", "o", "os", "em", "ens", "am")


def indice_tonico(palavra, silabas):
    """Regra padrao do portugues, que e bem regular."""
    chave = palavra.lower()
    if chave in TONICA_OVERRIDE:
        return min(TONICA_OVERRIDE[chave], len(silabas) - 1)
    if len(silabas) == 1:
        return 0

    # 1) acento grafico manda
    for i in range(len(silabas) - 1, -1, -1):
        if any(c in ACENTO_FORTE for c in silabas[i].lower()):
            return i
    for i in range(len(silabas) - 1, -1, -1):
        if any(c in TIL for c in silabas[i].lower()):
            return i

    # 2) terminacao decide
    if chave.endswith(FINAIS_PAROXITONAS):
        return len(silabas) - 2
    return len(silabas) - 1


# -------------------------------------------------------------- pronuncia

# Vogais nasais: o m/n que fecha a silaba vira "ng" para o leitor alemao.
NASAIS = {"a": "ang", "e": "eng", "i": "ing", "o": "ong", "u": "ung",
          "â": "ang", "ê": "eng", "ô": "ong",
          "á": "ang", "é": "eng", "í": "ing",
          "ó": "ong", "ú": "ung"}

# Ditongos e vogais, em ordem de tentativa (os maiores primeiro).
DITONGOS = [
    ("ão", "aung"), ("õe", "oing"), ("ãe", "aing"),
    ("ã", "ang"), ("õ", "ong"),
    ("ou", "o"),
    ("ei", "ej"), ("éi", "äj"), ("êi", "ej"),
    ("oi", "oj"), ("ói", "oj"), ("ôi", "oj"),
    ("ui", "uj"),
    ("ai", "ai"), ("ái", "ai"),
    ("au", "au"), ("áu", "au"),
    ("eu", "ehu"), ("êu", "ehu"), ("éu", "äu"),
    ("iu", "ihu"),
]

VOGAIS_SIMPLES = {
    "a": "a", "á": "a", "â": "a", "à": "a",
    "e": "e", "é": "ä", "ê": "e",
    "i": "i", "í": "i",
    "o": "o", "ó": "o", "ô": "o",
    "u": "u", "ú": "u",
}


def _eh_vogal(c):
    return c in VOGAIS


def _transcrever_silaba(sil, idx, total, silabas, tonica, palavra):
    s = sil.lower()
    primeira = idx == 0
    ultima = idx == total - 1
    anterior = silabas[idx - 1].lower() if idx > 0 else ""
    seguinte = silabas[idx + 1].lower() if idx < total - 1 else ""

    # ---- 1. vogal nasal: o m/n que fecha a silaba nao soa, nasaliza a vogal
    cauda = ""
    sufixo_s = ""
    seguinte_bruta = silabas[idx + 1].lower() if idx < total - 1 else ""
    if len(s) >= 3 and s.endswith("s") and s[-2] in "mn" and _eh_vogal(s[-3]):
        sufixo_s = "ss"          # pa-ra-BEINGSS, al-GUNGSS
        s = s[:-1]
    dobrada = seguinte_bruta[:1] == s[-1:] and s[-1:] in "mn"
    if dobrada and len(s) >= 2 and _eh_vogal(s[-2]):
        s = s[:-1]               # An-na: o n soa so na silaba seguinte
    if len(s) >= 2 and s[-1] in "mn" and _eh_vogal(s[-2]) and not dobrada:
        vogal = s[-2]
        if ultima and vogal in "eéê" and (s[-1] == "m" or sufixo_s):
            cauda = "eing"              # bem, tem, quem, alguem
        else:
            cauda = NASAIS.get(vogal, vogal + "ng")
        s = s[:-2]                      # tira vogal + m/n; a cauda os substitui

    out = []
    i = 0
    while i < len(s):
        c = s[i]
        prox = s[i + 1] if i + 1 < len(s) else ""
        par = s[i:i + 2]
        fim_da_silaba = (i + 1 == len(s)) and not cauda
        # o que vem depois, olhando tambem a proxima silaba
        depois = prox or (cauda[:1] if cauda else (seguinte[:1] if seguinte else ""))

        # ------------------------------------------------ digrafos
        if par == "ch":
            out.append("sch"); i += 2; continue
        if par == "lh":
            out.append("lj"); i += 2; continue
        if par == "nh":
            out.append("nj"); i += 2; continue
        if par in ("gu", "qu"):
            terceiro = s[i + 2] if i + 2 < len(s) else ""
            if terceiro in "eiéêí":
                out.append("g" if c == "g" else "k")
            else:
                out.append("gw" if c == "g" else "kw")
            i += 2; continue

        # ------------------------------------------------ vogais
        achou = False
        for seq, som in DITONGOS:
            if s[i:i + len(seq)] == seq:
                out.append(som); i += len(seq); achou = True; break
        if achou:
            continue
        if c in VOGAIS_SIMPLES:
            som = VOGAIS_SIMPLES[c]
            # vogal final atona reduz: -e vira [i], -o vira [u]
            if ultima and idx != tonica and not cauda:
                resto = s[i + 1:]
                if resto in ("", "s"):
                    if c == "e":
                        som = "i"
                    elif c == "o":
                        som = "u"
            out.append(som); i += 1; continue

        # ------------------------------------------------ consoantes
        if c == "h":
            i += 1; continue                      # h nao soa

        if c == "ç":
            out.append("ss"); i += 1; continue

        if c == "c":
            out.append("ss" if depois in "eiéêí" else "k")
            i += 1; continue

        if c == "g":
            out.append("zh" if depois in "eiéêí" else "g")
            i += 1; continue

        if c == "j":
            out.append("zh"); i += 1; continue

        if c == "x":
            if palavra in X_COMO_KS:
                out.append("ks")
            elif palavra in X_COMO_Z:
                out.append("s")
            elif palavra in X_COMO_SS:
                out.append("ss")
            else:
                out.append("sch")
            i += 1; continue

        if c == "r":
            if primeira and i == 0:
                out.append("rr")                  # r inicial e forte
            elif fim_da_silaba and seguinte[:1] == "r":
                pass                              # car-ro: o rr vem na proxima
            elif i == 0 and anterior[-1:] == "r":
                out.append("rr")                  # segunda metade de rr
            else:
                out.append("r")
            i += 1; continue

        if c == "s":
            prox_vira_ss = (
                seguinte[:1] in ("s", "ç")
                or (seguinte[:1] == "c" and seguinte[1:2] in "eiéêí"))
            if fim_da_silaba and prox_vira_ss:
                pass                              # pas-sar, nas-cer: nao dobra
            elif i == 0 and anterior[-1:] in ("s",):
                out.append("ss")
            elif (i > 0 and _eh_vogal(s[i - 1]) and _eh_vogal(prox)) or \
                 (i == 0 and anterior[-1:] and _eh_vogal(anterior[-1]) and _eh_vogal(prox)):
                out.append("s")                   # entre vogais soa [z]
            else:
                out.append("ss")
            i += 1; continue

        if c == "z":
            if fim_da_silaba and not seguinte:
                out.append("ss")                  # feliz, rapaz
            else:
                out.append("s")                   # fazer, doze
            i += 1; continue

        if c == "v":
            out.append("w"); i += 1; continue

        if c == "l":
            # So vira [u] quando fecha a silaba depois de vogal (Bra-sil,
            # al-to). Em inicio de silaba continua [l]: fa-lam, lo-go.
            if i > 0 and _eh_vogal(s[i - 1]):
                out.append("u")
            else:
                out.append("l")
            i += 1; continue

        if c in "td":
            # antes de [i] o brasileiro palataliza: dia, noite, grande
            vira_i = depois in "ií" or (
                ultima and idx != tonica and s[i + 1:] in ("e", "es"))
            if vira_i:
                out.append("tsch" if c == "t" else "dsch")
            else:
                out.append(c)
            i += 1; continue

        out.append(c); i += 1

    return "".join(out) + cauda + sufixo_s


def pronunciar(palavra):
    """Pronuncia do portugues escrita para quem le alemao."""
    chave = palavra.lower()
    if chave in PRONUNCIA_OVERRIDE:
        return PRONUNCIA_OVERRIDE[chave]
    silabas = silabar(palavra)
    if not silabas:
        return ""
    tonica = indice_tonico(palavra, silabas)
    partes = [
        _transcrever_silaba(s, i, len(silabas), silabas, tonica, chave)
        for i, s in enumerate(silabas)
    ]
    partes[tonica] = partes[tonica].upper()
    return "-".join(p for p in partes if p)
