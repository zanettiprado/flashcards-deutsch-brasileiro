# -*- coding: utf-8 -*-
"""
Regras de silabacao alema e de pronuncia aproximada em portugues do Brasil.

Usado por gerar_cards.py para produzir, a partir de uma palavra alema:
  - silabas  : "bit-te"
  - pronuncia: "BIT-te"  (silaba tonica em maiusculas)

As regras cobrem a grande maioria das palavras. Excecoes (compostos,
estrangeirismos, acento irregular) ficam nas tabelas de override abaixo.
"""

VOGAIS = set("aeiouaeiouaouy") | set("äöü")
VOG_SIMPLES = set("aeiouy") | set("äöü")

# nucleos de duas letras (ditongos e vogais longas)
DIG_VOG = ["ei", "ai", "au", "eu", "äu", "ie", "aa", "ee", "oo", "ey", "ay"]

# unidades consonantais indivisiveis na silabacao
TRIG_CONS = ["sch"]
DIG_CONS = ["ch", "ck", "ph", "th", "qu", "sh"]

# prefixos que, na silabacao, se separam do radical
PREFIXOS = [
    "zurück", "gegen", "durch", "hinter", "wieder", "zusammen",
    "über", "unter", "voll", "vorbei", "vor", "nach", "mit", "ent",
    "emp", "zer", "miss", "ver", "auf", "aus", "ein", "ab", "an", "bei",
    "her", "hin", "los", "weg", "zu", "um", "be", "ge", "er", "un",
]

# clusters que so iniciam silaba apos fronteira de morfema -> justificam
# separar o prefixo (ex.: ver-ste-hen, nao vers-te-hen)
# clusters de duas consoantes que abrem silaba e nao se separam
ONSETS_INSEPARAVEIS = [
    "schl", "schm", "schn", "schr", "schw", "str", "spr", "pfl",
    "bl", "br", "dr", "fl", "fr", "gl", "gr", "kl", "kn", "kr",
    "pl", "pr", "tr", "zw", "gn",
]

ONSETS_DUPLOS = [
    "schl", "schm", "schn", "schr", "schw", "str", "spr", "spl",
    "st", "sp", "sch", "pf", "kn", "gn", "gl", "gr", "bl", "br",
    "kl", "kr", "pl", "pr", "tr", "dr", "fl", "fr", "zw", "tsch",
]

# segundos elementos de composto iniciados por s + consoante: a silabacao
# normal erraria a emenda (bahns-teig em vez de bahn-steig)
COMPOSTOS_FINAIS = [
    "schmerzen", "stellung", "stellen", "stimmung", "sprache", "schule",
    "schrift", "straße", "studio", "stunde", "system", "städten", "städte",
    "stadt", "steig", "stelle", "stück", "stand", "stein", "sport",
    "strom", "stuhl", "stock", "start", "stieg", "stau",
]

# sufixos que formam morfema proprio: a silabacao nao os atravessa
SUFIXOS_MORFEMA = [
    "mäßig", "schaft", "weise", "reich", "haft", "keit", "heit",
    "lichen", "liches", "licher", "liche", "lich",
    "sam", "bar", "los", "nis", "voll", "land", "mal",
]

# palavras em que o inicio NAO e prefixo (silabacao normal)
SEM_PREFIXO = {
    "beste", "besten", "bester", "bestes", "best", "bestens",
    "erste", "ersten", "erster", "erstes", "erst", "erstens",
    "gestern", "gestrig", "gestrige", "gestern.",
    "beide", "beiden", "beides", "bequem", "bereit", "bereits",
    "besser", "besonders", "bestimmt", "bestimmte", "bestimmten",
    "einfach", "einfache", "einfacher", "einige", "einigen", "einzig",
    "unten", "unter", "untere", "mitte", "mittel", "mittag", "mittags",
    "mitten", "nachher", "nachmittag", "nachmittags", "nachts",
    "nachbar", "nachbarn", "zuerst", "zufrieden", "zusammen",
    "geld", "gelb", "gern", "gerne", "geschwister", "gesicht",
    "berg", "berge", "beruf", "berufe", "berlin", "ende", "endlich",
    "entweder", "erde", "ernst", "ernsthaft", "verwandte", "verwandten",
    "abend", "abends", "aber", "ander", "andere", "anderen", "anders",
    "angst", "antwort", "arbeit", "augen", "august", "ausland",
    "ausländer", "unser", "unsere", "unseren", "unser e",
    "einmal", "einst", "umsonst", "umgebung", "zuletzt",
    "besseres", "besserung", "bessere", "besten", "bestens",
}

# silabacao explicita (compostos e casos irregulares)
SILABAS_OVERRIDE = {
    "familie": "Fa-mi-li-e", "familien": "Fa-mi-li-en",
    "linie": "Li-ni-e", "ferien": "Fe-ri-en", "italien": "I-ta-li-en",
    "spanien": "Spa-ni-en", "studium": "Stu-di-um", "aktie": "Ak-ti-e",
    "material": "Ma-te-ri-al", "materialien": "Ma-te-ri-a-li-en",
    "theater": "The-a-ter", "museum": "Mu-se-um", "museen": "Mu-se-en",
    "familienstand": "Fa-mi-li-en-stand",
    # compostos cujo segundo elemento comeca por vogal
    "abendessen": "A-bend-es-sen",
    "aufenthaltserlaubnis": "Auf-ent-halts-er-laub-nis",
    "umsatzanstieg": "Um-satz-an-stieg",
    "selbstständigkeit": "Selbst-stän-dig-keit",
    "arbeitsplatz": "Ar-beits-platz",
    "missverständnis": "Miss-ver-ständ-nis",
    "einschränkungen": "Ein-schrän-kun-gen",
    "verjährungsfrist": "Ver-jäh-rungs-frist",
    "vertragsstrafe": "Ver-trags-stra-fe",
    "gesetzentwurf": "Ge-setz-ent-wurf",
    "nichteinhaltung": "Nicht-ein-hal-tung",
    "zusammenleben": "Zu-sam-men-le-ben",
    "zusammenfassend": "Zu-sam-men-fas-send",
    "kausalzusammenhang": "Kau-sal-zu-sam-men-hang",
    "wahlbeteiligung": "Wahl-be-tei-li-gung",
    "krankheitsrisiko": "Krank-heits-ri-si-ko",
    "konzentrationsfähigkeit": "Kon-zen-tra-ti-ons-fä-hig-keit",
    "aufmerksamkeit": "Auf-merk-sam-keit",
    "elternzeit": "El-tern-zeit",
    # estrangeirismos
    "massentourismus": "Mas-sen-tou-ris-mus",
    "ressourcenverbrauch": "Res-sour-cen-ver-brauch",
    "kartellamt": "Kar-tell-amt", "medien": "Me-di-en",
    "mediennutzung": "Me-di-en-nut-zung",
    "mitarbeiter": "Mit-ar-bei-ter",
    "mängelanzeige": "Män-gel-an-zei-ge",
    "pauschalangebot": "Pau-schal-an-ge-bot",
    "privatunterkünfte": "Pri-vat-un-ter-künf-te",
    "einwilligung": "Ein-wil-li-gung",
    "aufmerksam": "auf-merk-sam",
    "serien": "Se-ri-en", "solarenergie": "So-lar-e-ner-gie",
    "vegetarier": "Ve-ge-ta-ri-er", "ursprünglichen": "ur-sprüng-li-chen",
    "verursachen": "ver-ur-sa-chen", "verändert": "ver-än-dert",
    "veröffentlichten": "ver-öf-fent-lich-ten",
    "veröffentlichung": "ver-öf-fent-li-chung",
    "vorurteile": "Vor-ur-tei-le", "welterbe": "Welt-er-be",
    "wochenende": "Wo-chen-en-de", "weitreichende": "weit-rei-chen-de",
    "unaufhaltsam": "un-auf-halt-sam", "unumkehrbar": "un-um-kehr-bar",
    "unersetzlich": "un-er-setz-lich", "ungeachtet": "un-ge-ach-tet",
    "unterbrechen": "un-ter-bre-chen",
    "restaurant": "Res-tau-rant",
    "niveau": "Ni-veau",
    "budget": "Bud-get",
    "manager": "Ma-na-ger",
    "marathon": "Ma-ra-thon",
    "interview": "In-ter-view",
    "verabredet": "Ver-ab-re-det",
    "beeilen": "be-ei-len", "beendet": "be-en-det",
    "blutuntersuchung": "Blut-un-ter-su-chung",
    "brasilien": "Bra-si-li-en", "brasilianer": "Bra-si-li-a-ner",
    "erinnere": "er-in-ne-re", "erinnerte": "er-in-ner-te",
    "eröffnen": "er-öff-nen", "eröffnet": "er-öff-net",
    "eröffnete": "er-öff-ne-te", "englisch": "Eng-lisch",
    "cloud": "Cloud", "begutachtung": "Be-gut-ach-tung",
    "benachrichtigungen": "Be-nach-rich-ti-gun-gen",
    "energien": "E-ner-gi-en", "effizient": "ef-fi-zi-ent",
    "effizienz": "ef-fi-zi-enz", "zuverlässig": "zu-ver-läs-sig",
    "unterlagen": "Un-ter-la-gen", "unternehmen": "Un-ter-neh-men",
    "untersagt": "un-ter-sagt", "unterscheiden": "un-ter-schei-den",
    "unterschiedliche": "un-ter-schied-li-che",
    "unterschrieben": "un-ter-schrie-ben",
    "unterstützung": "Un-ter-stüt-zung",
    "untertiteln": "Un-ter-ti-teln", "unterzogen": "un-ter-zo-gen",
    "verständnis": "Ver-ständ-nis",
    "facharzt": "Fach-arzt", "zahnarzt": "Zahn-arzt",
    "falschnachrichten": "Falsch-nach-rich-ten",
    "fünfundzwanzig": "fünf-und-zwan-zig",
    "zweiundzwanzig": "zwei-und-zwan-zig",
    "großeltern": "Groß-el-tern", "grundrecht": "Grund-recht",
    "hausaufgaben": "Haus-auf-ga-ben", "hausordnung": "Haus-ord-nung",
    "immobilienpreise": "Im-mo-bi-li-en-prei-se",
    "industriell": "in-dus-tri-ell", "genres": "Gen-res",
    "gegenüber": "ge-gen-ü-ber", "wahlrecht": "Wahl-recht",
    "arbeitsmarkt": "Ar-beits-markt", "wohnkosten": "Wohn-kos-ten",
    "auftragswert": "Auf-trags-wert", "beweislast": "Be-weis-last",
    "stadtplan": "Stadt-plan", "stadtproblem": "Stadt-pro-blem",
    "stadtverwaltung": "Stadt-ver-wal-tung",
    "tierschutz": "Tier-schutz", "umwelt": "Um-welt",
    "jahresbeginn": "Jah-res-be-ginn", "monatsmieten": "Mo-nats-mie-ten",
    "verkehrsmittel": "Ver-kehrs-mit-tel",
    "mietvertrag": "Miet-ver-trag", "ressourcenverbrauch": "Res-sour-cen-ver-brauch",
    "service": "Ser-vice",
    "cousin": "Cou-sin",
    "sharing-economy": "Sha-ring-E-co-no-my",
    "fitnessstudio": "Fit-ness-stu-di-o",
}

# acento tonico explicito: palavra -> indice da silaba tonica (0 = primeira)
TONICA_OVERRIDE = {
    # radicais que apenas parecem comecar por prefixo atono
    "gehen": 0, "geht": 0, "geben": 0, "gibt": 0, "gegen": 0, "gegend": 0,
    "gern": 0, "gerne": 0, "besser": 0, "besen": 0, "berg": 0, "berge": 0,
    "bein": 0, "beine": 0, "erde": 0, "ernst": 0, "ernte": 0, "beide": 0,
    "beiden": 0, "beides": 0, "gelder": 0, "gegenteil": 0, "gegenueber": 0,
    "familie": 1, "familien": 1, "linie": 1, "ferien": 0, "italien": 1,
    "spanien": 0, "studium": 0, "stadium": 1, "aktie": 0,
    # estrangeirismos e acento irregular
    "hotel": 1, "august": 1, "papier": 1, "klavier": 1, "kaffee": 0,
    "lebendig": 1, "warum": 1, "woher": 1, "wohin": 1, "wieso": 1,
    "vielleicht": 1, "allein": 1, "zusammen": 1, "zufrieden": 1,
    "überhaupt": 2, "sofort": 1, "soweit": 1, "zuerst": 1, "zuletzt": 1,
    "vorbei": 1, "voraus": 1, "bereits": 1, "bequem": 1, "besonders": 1,
    "zurück": 1, "dahin": 1, "daher": 1, "davor": 1, "danach": 1,
    "deshalb": 1, "dennoch": 1, "jedoch": 1, "obwohl": 1, "damit": 1,
    "damals": 0, "wahrscheinlich": 1, "natürlich": 1,
    # estrangeirismos greco-latinos: tonica no radical
    "apotheke": 2, "theater": 1, "museum": 1, "museen": 1, "kamera": 0,
    "tomate": 1, "tomaten": 1, "banane": 1, "bananen": 1, "kartoffel": 1,
    "kartoffeln": 1, "zitrone": 1, "schokolade": 2, "salat": 1,
    "restaurant": 2, "hotel": 1, "balkon": 1, "garage": 1, "etage": 1,
    "toilette": 1, "sofa": 0, "maschine": 1, "maschinen": 1, "minute": 1,
    "minuten": 1, "sekunde": 1, "sekunden": 1, "problem": 1,
    "probleme": 1, "programm": 1, "moment": 1, "termin": 1, "termine": 1,
    "person": 1, "personen": 1, "beruf": 1, "berufe": 1, "idee": 1,
    "ideen": 1, "familie": 1, "kollege": 1, "kollegen": 1, "kollegin": 1,
    "patient": 1, "patienten": 1, "student": 1, "studenten": 1,
    "studentin": 1, "spaziergang": 1, 
    "entscheidung": 1, "erfahrung": 1,
    "verantwortung": 1, "zusammenhang": 0, "gelegenheit": 1,
    "veranstaltung": 1, "voraussetzung": 1, "voraussichtlich": 1,
    "selbstverständlich": 2, "berücksichtigen": 1, "außerdem": 0,
    "allerdings": 1, "einerseits": 0, "andererseits": 2, "trotzdem": 0,
    "inzwischen": 1, "schließlich": 0, "angesichts": 1, "bezüglich": 1,
    "hinsichtlich": 1, "nachdem": 1, "seitdem": 1, "indem": 1,
    "zumindest": 1, "immerhin": 2, "ohnehin": 2, "keineswegs": 0,
    "nachhaltigkeit": 0,  "philosophie": 3,
    "demokratie": 3, "technologie": 3, "energie": 2, "industrie": 2,
    "biologie": 3, "ökonomie": 3, "ökologie": 3, "büro": 1, "büros": 1, "garantie": 2, "fantasie": 2,
    "kritik": 1, "politik": 2, "musik": 1, "republik": 2, "fabrik": 1,
    "physik": 1, "elektrisch": 1, "politisch": 1, "praktisch": 0,
    "logisch": 0, "typisch": 0, "kritisch": 0, "technisch": 0,
    "effekt": 1, "effekte": 1, "empirisch": 1, "hypothese": 2,
    "methodik": 1, "modell": 1, "algorithmus": 2, "aktuell": 2,
    "aktuellen": 2, "automatisch": 2,
    "diagnose": 1, 
    "energien": 2, "intelligenz": 3, "interessant": 3, "interesse": 1,
    "interview": 0, 
    "kontext": 0, "massive": 1, "medizin": 2,
    "negativ": 2, "niveau": 1, "prognose": 1, "prozent": 1,
    "relevanz": 2, "renovierung": 2,
    
    "repräsentativen": 3, "reservierung": 2,
    "restaurierung": 2, "sensibel": 1, "stipendium": 1,
    "vegetarier": 2, "visum": 0, "formular": 2, "ingenieur": 3,
    "manager": 0, "marathon": 0, "budget": 0, "reform": 1,
    "effizient": 2, "effizienz": 2, "kompromiss": 2, "kompromisse": 2,
    "argument": 2, "argumente": 2, "appetit": 2, "autoren": 1,
    "digitale": 1, "individuelles": 3, "industriell": 3, 
    "mobbing": 0, "programm": 1, "projekt": 1,
    "zeitgenössische": 1, "subkultur": 2, "sofa": 0, "taxi": 0,
    "hobby": 0, "baby": 0, "allergisch": 1, "allergie": 2, "adresse": 1,
    "anerkannt": 2, "angesichts": 2, "artikel": 1, "aktiv": 1, "geschwister": 1,
    "bibliothek": 3, "brasilianer": 3, "brasilien": 1, "dafür": 1,
    "dagegen": 1, "darauf": 1, "darüber": 1, "dazu": 1, "dabei": 1,
    "dadurch": 1, "dateien": 1, "debatte": 1, "diagnose": 2,
    "energiewende": 2, "normalerweise": 1, "begutachtung": 2,
    "benachrichtigungen": 2, "erinnere": 1, "erinnerte": 1,
    "eröffnen": 1, "eröffnet": 1, "eröffnete": 1, "woran": 1,
    "worüber": 1, "worauf": 1, "wovon": 1, "hinzufügen": 1,
    "zustande": 1, "zuletzt": 1, "zunächst": 1, "vorbei": 1,
    "flexible": 1, "fehlerquote": 2, "harmonisches": 1, "harmonisch": 1,
    "hotels": 1, "historisch": 1, "historischen": 1, "interesse": 2,
    "individuelles": 4, "individuell": 3, "industriell": 3,
    "immobilienpreise": 2, "gehe": 0, "gehst": 0, "gehend": 0,
    "jahresbeginn": 0, "kollegin": 2, "lebensweise": 0, "mediennutzung": 0,
    "methodisch": 1, "monatsmieten": 0, "perspektive": 2, "pauschalangebot": 0,
    "privatunterkünfte": 1, "regionale": 2, "regionen": 1, "sensibler": 1,
    "spezielle": 1, "struktur": 1, "subkulturen": 2, "symbolisch": 1,
    "tourismus": 1, "vegetarisch": 2, "zentralen": 1, "zentrum": 0,
    "kredit": 1, "methodik": 2, "minister": 1, "missverständnis": 2,
    "monat": 0, "monate": 0, "monaten": 0, "monats": 0, "oktober": 1,
    "persönlichen": 1, "persönliche": 1, "persönlichkeit": 1,
    "plastik": 0, "politische": 1, "portugiesisch": 2, "prioritäten": 3,
    "produkte": 1, "regionale": 3, "regionen": 2, "kartellamt": 1,
    "medien": 0, "lecker": 0, "spanisch": 0, "russisch": 0,
    "sofern": 1, "sowohl": 1, "soziale": 2, "sozialen": 2, "sozial": 1,
    "stadtplan": 0, "systeme": 1, "system": 1, "technik": 0,
    "verjährungsfrist": 1, "serien": 0, "solarenergie": 0,
    "vegetarier": 2, "stipendium": 1, "subkultur": 2,
    "verursachen": 2, "verändert": 1, "veröffentlichten": 1,
    "veröffentlichung": 1, "vorurteile": 0, "welterbe": 0,
    "widerspricht": 2, "widerspruch": 2, "zeitgenössische": 2,
    "zweimal": 0, "dreimal": 0, "übernehme": 2, "übernimmt": 2,
    "übernommen": 2, "übertragen": 2, "übertrieben": 2,
    "überwiesen": 2, "überzeugend": 2, "überzeugende": 2,
    "überzeugt": 2, "überprüfbar": 2, "überrascht": 2,
    "überhaupt": 2, "überwiesen": 2, "übernahme": 2,
    "solarenergie": 1, "wochenende": 0,
    "vorher": 1, "nachher": 1, "bisher": 1, "daher": 1, "dahin": 1, "inflationsrate": 4, "jahrhundert": 1,
    "jahrhunderte": 1, "jahrzehnte": 1, "jahrelang": 0, "cousin": 1, "balkon": 1, "medikament": 3,
    "kausalität": 3, 
    "konzentrationsfähigkeit": 4, "inflationsrate": 2,
    
    "digitalisierung": 4, 
    "inklusive": 2, 
}

# consoantes/letras com leitura estrangeira
V_ESTRANGEIRO = set()

SUFIXOS_TONICOS = [
    "ieren", "ierend", "ierung", "ierte", "ierten", "iertes",
    "iert", "iere", "ierst",
    "ismus", "istisch", "ation", "ition", "ution", "ktion", "sion",
    "tät", "ität", "enz", "anz", "ent", "ant", "eur", "ös",
    "ell", "ial", "iell", "abel", "ibel", "iv", "al", "är", "ur",
    "ik", "ei", "ie", "ist", "at", "ut", "om", "on", "an",
]

PREFIXOS_ATONOS = ("be", "ge", "ver", "er", "ent", "emp", "zer", "miss")
PREFIXOS_ATONOS_LONGOS = ("ver", "ent", "emp", "zer", "miss")


# ---------------------------------------------------------------- silabacao

def _unidades(s):
    """Quebra a palavra em unidades: nucleos vocalicos e unidades consonantais."""
    out = []
    i = 0
    n = len(s)
    while i < n:
        tri = s[i:i + 3]
        dig = s[i:i + 2]
        if tri in TRIG_CONS:
            out.append(("C", tri)); i += 3; continue
        if dig in DIG_VOG:
            out.append(("V", dig)); i += 2; continue
        if dig in DIG_CONS:
            out.append(("C", dig)); i += 2; continue
        c = s[i]
        out.append(("V" if c in VOG_SIMPLES else "C", c))
        i += 1
    return out


def _silabar_simples(s):
    """Silabacao de um morfema (sem prefixos)."""
    if len(s) < 2:
        return [s] if s else []
    un = _unidades(s)
    idx_v = [k for k, (t, _) in enumerate(un) if t == "V"]
    if len(idx_v) <= 1:
        return ["".join(v for _, v in un)]

    cortes = []  # indices de unidade onde comeca uma nova silaba
    for a, b in zip(idx_v, idx_v[1:]):
        meio = un[a + 1:b]
        if not meio:                       # duas vogais seguidas: Fa-mi-li-e
            cortes.append(b)
        elif len(meio) == 1:               # uma consoante vai para a proxima
            cortes.append(b - 1)
        else:
            tres = "".join(v for _, v in meio[-3:])
            dois = "".join(v for _, v in meio[-2:])
            if len(meio) >= 3 and tres in ONSETS_INSEPARAVEIS:
                cortes.append(b - 3)       # ab-ge-schlos-sen
            elif dois in ONSETS_INSEPARAVEIS:
                cortes.append(b - 2)       # Pro-gramm, e-lek-trisch
            else:
                cortes.append(b - 1)       # ultima unidade abre a nova silaba
    silabas, ini = [], 0
    for c in cortes:
        silabas.append("".join(v for _, v in un[ini:c]))
        ini = c
    silabas.append("".join(v for _, v in un[ini:]))
    return [x for x in silabas if x]


def _tem_vogal(s):
    return any(c in VOG_SIMPLES for c in s)


def _separar_prefixos(s, prof=0):
    """Separa prefixos quando o radical comeca por cluster ou outro prefixo."""
    if prof >= 3 or s in SEM_PREFIXO:
        return [s]
    for p in PREFIXOS:
        if s.startswith(p) and len(s) > len(p) + 2:
            resto = s[len(p):]
            if not _tem_vogal(resto) or not _tem_vogal(p):
                continue
            abre_cluster = any(resto.startswith(o) for o in ONSETS_DUPLOS)
            abre_prefixo = any(resto.startswith(p2) and len(resto) > len(p2) + 2
                               for p2 in PREFIXOS)
            if abre_cluster or abre_prefixo:
                return [p] + _separar_prefixos(resto, prof + 1)
    return [s]


def _separar_sufixos(s):
    """Separa sufixos derivacionais, que nao se misturam com o radical."""
    for suf in SUFIXOS_MORFEMA:
        if s.endswith(suf) and len(s) - len(suf) >= 3:
            inicio = s[:-len(suf)]
            if _tem_vogal(inicio):
                return _separar_prefixos(inicio) + [suf]
    return _separar_prefixos(s)


def _separar_compostos(s):
    """Separa o segundo elemento de compostos iniciados por s + consoante."""
    for fim in COMPOSTOS_FINAIS:
        if s.endswith(fim) and len(s) - len(fim) >= 3:
            inicio = s[:-len(fim)]
            if _tem_vogal(inicio):
                return _separar_sufixos(inicio) + [fim]
    return _separar_sufixos(s)


def silabar(palavra):
    """Retorna a lista de silabas de uma palavra alema."""
    base = palavra.strip()
    chave = base.lower()
    if chave in SILABAS_OVERRIDE:
        return SILABAS_OVERRIDE[chave].split("-")
    if "-" in base:  # composto com hifen: trata cada parte
        partes = []
        for p in base.split("-"):
            partes.extend(silabar(p) if p else [])
        return partes
    silabas = []
    for morf in _separar_compostos(chave):
        silabas.extend(_silabar_simples(morf))
    # devolve a capitalizacao original
    if base[:1].isupper() and silabas:
        silabas[0] = silabas[0][:1].upper() + silabas[0][1:]
    return silabas


def silabas_str(palavra):
    return "-".join(silabar(palavra))


# -------------------------------------------------------------- tonicidade

def indice_tonico(palavra, silabas):
    chave = palavra.lower()
    if chave in TONICA_OVERRIDE:
        return min(TONICA_OVERRIDE[chave], len(silabas) - 1)
    if len(silabas) == 1:
        return 0
    if chave in SEM_PREFIXO:
        return 0
    # -tion, -sion: a tonica recai sempre na ultima silaba
    if chave.endswith(("tion", "sion", "tionen", "sionen")):
        return len(silabas) - 1 if not chave.endswith("en") else len(silabas) - 2
    # sufixos tonicos
    for suf in SUFIXOS_TONICOS:
        if chave.endswith(suf) and len(chave) > len(suf) + 1:
            pos = len(chave) - len(suf)
            acc = 0
            for i, s in enumerate(silabas):
                prox = acc + len(s)
                if prox > pos:
                    return i
                acc = prox
            return len(silabas) - 1
    # prefixos atonos
    if chave.startswith(PREFIXOS_ATONOS_LONGOS) or (
        chave.startswith(("be", "ge", "er")) and len(silabas) > 1
    ):
        pref = next((p for p in PREFIXOS_ATONOS if chave.startswith(p)), "")
        if silabas[0].lower().startswith(pref) and len(silabas[0]) <= len(pref) + 1:
            return 1
    return 0


# -------------------------------------------------------------- pronuncia

# palavras em que "v" soa [v] (estrangeirismos) em vez de [f]
V_COMO_V = {
    "vase", "villa", "klavier", "vitamin", "vitamine", "visum", "video",
    "videos", "vegetarisch", "vegetarier", "vulkan", "vokal", "variante",
    "version", "virus", "vision", "vital", "privat", "privaten", "privater",
    "november", "aktiv", "aktive", "aktiven", "positiv", "negativ", "kreativ",
    "intensiv", "effektiv", "motivation", "motiviert", "investition",
    "investieren", "revolution", "individuell", "universitaet", "universum",
    "interview", "service", "advent", "evangelisch", "eva", "revision",
    "provokant", "provozieren", "nerv", "nerven", "serviette", "niveau",
    "perspektive", "alternative", "initiative", "relativ", "subjektiv",
    "objektiv", "attraktiv", "produktiv", "konservativ", "innovativ",
    "individuelles", "inklusive", "investiert", "investitionen",
    "massive", "nervös", "intensive", "relative", "relativieren",
    "relevanz", "renoviert", "renovierung", "reserviert", "reservierung",
    "repräsentativen", "vegetarier", "universität", "vokal",
    "universitäten", "aktiven", "privatunterkünfte", "vegetarier",
    "vokabeln", "videos", "niveau",
}

# radicais em que "chs" soa [ks]; em nächste ou höchste soa [çs]
CHS_COMO_KS = {
    "sechs", "sechste", "sechsten", "wachsen", "wächst", "wachstum",
    "fuchs", "achse", "achsel", "büchse", "lachs", "ochse", "wechsel",
    "wechseln", "wechselt",
}

# "s" surdo no inicio de palavra (estrangeirismos): City, Sofa -> z normal
S_SURDO = {"sofa"}

VOG_LONGAS_H = ("ah", "eh", "ih", "oh", "uh", "äh", "öh", "üh")


# palavras em que o h continua muda mesmo depois de ge-/be- (sem prefixo real)
H_MUDA_APOS_PREFIXO = {
    "gehen", "gehe", "geht", "gehend", "gehst", "behende",
}

# palavras em que o h soa mesmo depois de vogal (emenda de morfema)
H_SONORO = {
    "woher", "wohin", "daher", "dahin", "bisher", "vorher", "nachher",
    "umher", "seither", "woraufhin", "wieherte", "freiheit",
}


def _ch_apos_posterior(prev):
    """Decide entre ach-Laut (rr) e ich-Laut (ch)."""
    if not prev:
        return False
    if prev.endswith(("eu", "äu", "i", "e")):
        return False               # bräuchte, Bücher: ich-Laut
    return prev[-1] in ("a", "o", "u")


def _transcrever_silaba(sil, idx, total, silabas, tonica):
    s = sil.lower()
    primeira = idx == 0
    ultima = idx == total - 1
    anterior = silabas[idx - 1].lower() if idx > 0 else ""
    seguinte = silabas[idx + 1].lower() if idx < total - 1 else ""
    palavra = "".join(silabas).lower()

    # h muda entre vogais (ge-hen -> GE-en, Ru-he -> RU-e)
    palavra_toda = "".join(silabas).lower()
    h_muda = (s.startswith("h") and not primeira
              and palavra_toda not in H_SONORO
              and anterior[-1:] in VOG_SIMPLES
              and (anterior not in PREFIXOS or palavra_toda in H_MUDA_APOS_PREFIXO)
              and not anterior.endswith(("ei", "ai", "au", "eu", "äu")))
    if h_muda:
        s = s[1:]

    # sch / ch / chs
    s = s.replace("sch", "§")                     # marcador temporario de "ch" (PT)
    if "chs" in s and palavra in CHS_COMO_KS:
        s = s.replace("chs", "ks")
    out = []
    i = 0
    while i < len(s):
        if s[i:i + 2] == "ch":
            antes = "".join(out) or anterior
            out.append("rr" if _ch_apos_posterior(antes) else "ch")
            i += 2
            continue
        out.append(s[i]); i += 1
    s = "".join(out)

    # "ti" antes de "on"/"onen" soa [tsi]: Informa-ti-on
    if s == "ti" and seguinte.startswith("o"):
        s = "tsi"

    if s.endswith("igt") and s[-4:-3] not in VOG_SIMPLES:
        s = s[:-3] + "icht"

    if s.endswith("ig") and seguinte in ("keit", "keiten", "lich"):
        s = s[:-2] + "irr"

    # -ig final -> irr
    if (ultima and s.endswith("ig") and len(s) > 2
            and s[-3] not in VOG_SIMPLES):
        s = s[:-2] + "irr"

    # "sit-zen" -> ZI-tsen: o t final cai porque o z seguinte ja soa [ts]
    if s.endswith("t") and seguinte.startswith("z"):
        s = s[:-1]

    # grupos consonantais
    s = s.replace("ck", "k").replace("ph", "f").replace("th", "t")
    s = s.replace("qu", "k¥").replace("tz", "ts").replace("z", "ts")
    s = s.replace("ß", "ss")
    s = s.replace("pf", "pf").replace("ng", "ng")

    # st- / sp- no inicio de silaba -> cht- / chp-
    if s.startswith("st"):
        s = "§t" + s[2:]
    elif s.startswith("sp"):
        s = "§p" + s[2:]

    # s sonoro (inicio de silaba antes de vogal) -> z
    if (s.startswith("s") and len(s) > 1 and s[1] in VOG_SIMPLES
            and palavra not in S_SURDO
            and anterior[-1:] not in ("s", "\u00df")):
        s = "z" + s[1:]

    # v / w / j
    if palavra in V_COMO_V:
        s = s.replace("v", "v")
    else:
        s = s.replace("v", "f")
    s = s.replace("w", "v")
    s = s.replace("j", "¤")          # marcador: sera lido como "i"
    s = s.replace("y", "ü")

    # vogais longas com h -> cai o h
    for dig in VOG_LONGAS_H:
        s = s.replace(dig, dig[0])

    # ditongos e vogais duplas
    s = s.replace("äu", "oi").replace("eu", "oi")
    s = s.replace("ei", "ai").replace("ai", "ai")
    s = s.replace("ie", "i").replace("aa", "a").replace("ee", "ê").replace("oo", "ô")

    # vogais com trema
    s = s.replace("ä", "é").replace("ö", "ê").replace("ü", "iu")

    if s.endswith("dt"):
        s = s[:-2] + "t"
    elif s.endswith("gt"):
        s = s[:-2] + "kt"
    elif s.endswith("bst"):
        s = s[:-3] + "pst"
    elif s.endswith("bt"):
        s = s[:-2] + "pt"

    # consoantes finais ensurdecem
    if ultima or (seguinte and seguinte[0] not in VOG_SIMPLES):
        ensurdeceu = False
        if s.endswith("b"):
            s = s[:-1] + "p"; ensurdeceu = True
        elif s.endswith("d"):
            s = s[:-1] + "t"; ensurdeceu = True
        elif s.endswith("g") and not s.endswith("ng"):
            s = s[:-1] + "k"; ensurdeceu = True
        # Stad-te -> CHTÁ-te: o som ensurdecido nao se repete na emenda
        if ensurdeceu and seguinte and s[-1] == seguinte[0]:
            s = s[:-1]

    # r final de silaba: -er final soa [a], mas so em palavras polissilabicas
    # a reducao de -er para [a] so ocorre em silaba atona (Va-ter, mas wo-HER)
    if (total > 1 and ultima and idx != tonica
            and sil.lower().endswith("er") and s.endswith("er")):
        s = s[:-2] + "a"           # Va-ter -> FA-ta, Be-su-cher -> be-ZU-rra

    # abertura da vogal tonica
    if idx == tonica and not any(d in s for d in ("ai", "au", "oi")):
        fechada = bool(s) and s[-1] not in VOG_SIMPLES and s[-1] not in "éêóôá"
        mapa_fechada = {"a": "á", "e": "é", "o": "ó"}
        mapa_aberta = {"a": "á", "e": "ê", "o": "ô"}
        mapa = mapa_fechada if fechada else mapa_aberta
        for k, v in mapa.items():
            if k in s:
                s = s.replace(k, v, 1)
                break

    s = s.replace("§", "ch").replace("¤", "i").replace("¥", "v")
    return s


PRONUNCIA_OVERRIDE = {
    "ber\u00fccksichtigen": "be-RIUK-sich-ti-gen",
    "selbst": "ZÉLPST",
    "sechs": "ZÉKS",
    "sechzehn": "ZÉCH-tsên",
    "sechzig": "ZÉCH-tsirr",
    "eins": "ÁINS",
    "zwei": "TSVAI",
    "drei": "DRAI",
    "vier": "FIR",
    "f\u00fcnf": "FIUNF",
    "sieben": "ZI-ben",
    "acht": "ÁRRT",
    "neun": "NÓIN",
    "zehn": "TSÊN",
    "elf": "ÉLF",
    "zw\u00f6lf": "TSVÊLF",
    "siebzehn": "ZIP-tsên",
    "siebzig": "ZIP-tsirr",
    "achtzehn": "ÁRRT-tsên",
    "achtzig": "ÁRRT-tsirr",
    "haben": "HÁ-ben",
    "sein": "ZAIN",
    "ist": "IST",
    "sind": "ZINT",
    "war": "VÁR",
    "waren": "VÁ-ren",
    "hatte": "HÁT-te",
    "w\u00fcrde": "VIUR-de",
    "m\u00f6chte": "MÊCH-te",
    "nat\u00fcrlich": "na-TIUR-lich",
    "wirklich": "VIRK-lich",
    "deshalb": "DÉS-halp",
    "obwohl": "op-VÔL",
    "trotzdem": "TRÓTS-dêm",
    "au\u00dferdem": "ÁU-sser-dêm",
    "massentourismus": "mas-sen-tu-RIS-mus",
    "restaurant": "res-to-RÁN",
    "niveau": "ni-VÔ",
    "budget": "biu-DCHÊ",
    "manager": "MÉ-ned-ja",
    "interview": "IN-ter-viu",
    "service": "SÖR-vis",
    "cousin": "ku-ZÄN",
    "ressourcenverbrauch": "re-SUR-sen-fer-braurr",
    "sharing-economy": "CHÉ-ring-i-KÓ-no-mi",
    "team": "TIM",
    "cloud": "KLAUD",
    "live": "LAIF",
    "app": "ÉP",
    "apps": "ÉPS",
    "gesundheits-apps": "ge-ZUNT-haits-eps",
    "baby": "BÊ-bi",
    "hobby": "HÓ-bi",
    "t-shirt": "TI-chört",
    "wlan-passwort": "VÊ-lan-pass-vort",
    "e-mail": "I-mêil",
    "e-mail-adresse": "I-mêil-a-DRÉS-se",
    "mobbing": "MÓ-bing",
    "chatbots": "TCHÉT-bots",
    "fitnessstudio": "FIT-nes-chtu-di-o",
    "marathon": "MÁ-ra-ton",
    "documenta": "do-ku-MÉN-ta",
    "chancen": "CHÁN-sen",
    "computer": "kom-PIU-ta",
    "engagement": "an-gaj-MÁN",
    "engagieren": "an-ga-ZCHI-ren",
    "garage": "ga-RÁ-je",
    "etage": "e-TÁ-je",
    "orange": "o-RÁN-je",
    "flexible": "fle-KSI-ble",
    "genres": "ZCHÁN-res",
    "geruchssinn": "ge-RURRS-zin",
    "handy": "HÉN-di",
    "ingenieur": "in-jen-i-ÊR",
    "experiment": "eks-pe-ri-MÉNT",
    "exportiert": "eks-por-TIRT",
    "immunsystem": "i-MUN-zius-têm",
    "sharing-economy": "CHÉ-ring-i-KÓ-no-mi",
    "nebensaison": "NÊ-ben-ze-zon",
    "recycelt": "re-TSAI-kelt",
    "taxi": "TÁ-ksi",
    "verwechselt": "fer-VÉK-selt",
    "wechsel": "VÉK-sel",
    "t-shirt": "TI-chört",
}


def pronunciar(palavra):
    """Pronuncia aproximada em PT-BR, com a silaba tonica em maiusculas."""
    chave = palavra.lower()
    if chave in PRONUNCIA_OVERRIDE:
        return PRONUNCIA_OVERRIDE[chave]
    silabas = silabar(palavra)
    if not silabas:
        return ""
    tonica = indice_tonico(palavra, silabas)
    partes = [
        _transcrever_silaba(s, i, len(silabas), silabas, tonica)
        for i, s in enumerate(silabas)
    ]
    partes[tonica] = partes[tonica].upper()
    return "-".join(p for p in partes if p)
