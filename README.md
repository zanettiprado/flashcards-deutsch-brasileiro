# Alemão do zero — flashcards de frases do cotidiano

**▶ Estude agora: <https://zanettiprado.github.io/flashcards-deutsch-brasileiro/>**

Abre direto no navegador do computador ou do celular, sem instalar nada.

Site estático para aprender alemão do zero, com **738 flashcards** de frases
reais distribuídas em cinco níveis (A1 a C1). Cada card traz a frase nos dois
idiomas, a pronúncia aproximada em português, a tradução palavra por palavra
com separação silábica e áudio pela voz do próprio navegador.

Feito em HTML, CSS e JavaScript puros, sem frameworks e sem build: é só abrir o
`index.html` no navegador.

---

## Como abrir

**Jeito mais simples:** dê dois cliques no arquivo `index.html`. Ele abre no seu
navegador padrão e já funciona — não precisa de servidor nem de internet.

No terminal, também dá para abrir assim:

```bash
# macOS
open index.html

# Linux
xdg-open index.html

# Windows
start index.html
```

> Os cards ficam em `data/cards.js` (um arquivo `.js`, não `.json`) justamente
> para que o site funcione ao abrir o arquivo direto, sem servidor. Navegadores
> bloqueiam leitura de `.json` via `file://`, mas carregam `.js` sem problema.

Se preferir servir por HTTP (opcional, só para testar em outro aparelho da
mesma rede):

```bash
python3 -m http.server 8000
# abra http://localhost:8000
```

## Como testar rapidamente

1. Abra o `index.html`.
2. Na tela inicial, escolha o nível **A1** e a direção **Português → Alemão**.
3. Clique em **Começar a estudar**.
4. Aperte <kbd>espaço</kbd> para virar o card: aparecem a frase em alemão, a
   pronúncia entre colchetes e a nota de gramática.
5. Clique em qualquer palavra (por exemplo, **Morgen**): abre um painel com a
   tradução, a separação silábica (`Mor-gen`) e a pronúncia (`MÓR-gen`), e a
   palavra é lida em voz alta.
6. Teste os botões **Ouvir a frase**, **Ouvir devagar** e **Palavra por palavra**.
7. Marque alguns cards com <kbd>1</kbd> (sei) e <kbd>2</kbd> (não sei), volte ao
   início com a seta ← do topo e confira que o progresso do nível foi salvo.
8. Recarregue a página: o progresso e a posição continuam onde estavam.

## Como usar

### Tela inicial

- **Nível**: A1, A2, B1, B2 ou C1. Cada cartão mostra quantos cards o nível tem,
  quantos você já marcou como "eu sei" e a porcentagem concluída.
- **Direção**: *Português → Alemão* (você vê o português e tenta produzir o
  alemão) ou *Alemão → Português* (você vê o alemão e tenta entender).
- O progresso é contado separadamente para cada combinação de nível e direção.

### Durante o estudo

| Ação | Como fazer |
| --- | --- |
| Virar o card | clicar/tocar no card ou <kbd>espaço</kbd> |
| Próximo / anterior | botões ou <kbd>→</kbd> / <kbd>←</kbd> |
| Marcar "eu sei" | botão ou <kbd>1</kbd> |
| Marcar "não sei" | botão ou <kbd>2</kbd> |
| Ver uma palavra | clicar na palavra no verso do card |
| Fechar o painel da palavra | botão × ou <kbd>Esc</kbd> |
| Embaralhar a rodada | botão ⇄ no topo |
| Reiniciar o nível | botão **Reiniciar nível** |

Cards marcados como **"não sei"** voltam a aparecer quatro cards depois, em vez
de só no fim da rodada. O tamanho da rodada não muda.

### Áudio

O som usa a **Web Speech API** do navegador (`speechSynthesis`). A voz vem do
**seu próprio aparelho** (ou, no caso da "Google Deutsch", dos servidores do
Google através do Chrome) — o site apenas pede ao sistema que leia o texto.
Por isso o mesmo card pode soar diferente em cada computador.

Na tela inicial, o bloco **3. Voz do alemão** mostra qual voz está em uso e
deixa você trocar e testar com um clique. A escolha fica salva.

O site prefere automaticamente, nesta ordem: `Google Deutsch` (a de melhor
qualidade, a mesma família usada pelo Google Tradutor), depois vozes alemãs
normais do sistema (Anna, Petra, Markus, Hedda…), e por último qualquer outra.
As vozes "de efeito" do macOS (Eddy, Flo, Grandma, Grandpa, Reed, Rocko, Sandy,
Shelley) são marcadas como *evite* na lista: são vozes de brincadeira e algumas
acabam lendo o alemão com pronúncia inglesa.

> **Se o alemão sair com sotaque de inglês** — por exemplo `Abend` soando
> "ÊI-bend" em vez de "Á-bent" — não é sotaque regional: é o sistema lendo
> alemão com uma voz inglesa. Troque a voz no bloco 3 da tela inicial.

Se o navegador não tiver uma voz alemã instalada, a tela inicial mostra um aviso
com as instruções de instalação:

- **macOS**: Ajustes do Sistema → Acessibilidade → Conteúdo Falado → Voz do
  sistema → Gerenciar vozes → baixar uma voz em **Alemão**.
- **Windows**: Configurações → Hora e idioma → Idioma e região → adicionar
  **Deutsch** e instalar o pacote de fala.
- **Android / iOS**: instalar o pacote de voz alemã nas configurações de
  acessibilidade (Conversão de texto em voz / VoiceOver).

Em qualquer caso, cada card tem o link **Ouvir no Google Tradutor**, que abre
`translate.google.com` com a frase já preenchida. É a página oficial do
tradutor — o site não usa nenhum endpoint não oficial do Google.

### Progresso

Tudo fica no `localStorage` do navegador, com uma chave por nível e direção
(`alemao-v1:A1:pt-de`, por exemplo), guardando os cards sabidos, os que faltam
revisar, a ordem da rodada e a posição atual. Não há servidor nem conta: se você
limpar os dados do navegador ou abrir em outro aparelho, o progresso recomeça.
O botão **Zerar todo o progresso**, na tela inicial, apaga tudo de uma vez.

---

## Arquivos

```
index.html          estrutura das duas telas (início e estudo)
css/style.css       estilos: claro, texto grande, mobile-first
js/app.js           lógica: sessão, virada, áudio, progresso, atalhos
data/cards.js       os 738 cards (define a constante global CARDS)
README.md           este arquivo
tools/              scripts que geram data/cards.js (opcional, precisa de Python 3)
  regras.py         silabação alemã e pronúncia aproximada em PT-BR
  lexico.py         1.478 palavras alemãs e suas traduções
  frases_a1.py …    as frases de cada nível
  gerar_cards.py    monta e valida data/cards.js
```

## Formato de um card

```js
{
  "id": 31,
  "nivel": "A1",
  "categoria": "apresentacao",
  "pt": "Meu nome é Anna.",
  "de": "Ich heiße Anna.",
  "palavras": [
    { "de": "Ich",   "pt": "eu",       "silabas": "Ich",    "pronuncia": "ICH" },
    { "de": "heiße", "pt": "chamo-me", "silabas": "hei-ße", "pronuncia": "HAI-sse" },
    { "de": "Anna",  "pt": "Anna (nome)", "silabas": "An-na", "pronuncia": "ÁN-na" }
  ],
  "pronuncia": "ich HAI-sse ÁN-na",
  "gramatica": "O verbo heißen significa chamar-se e não precisa de pronome reflexivo."
}
```

O campo `gramatica` é opcional; todos os outros são obrigatórios. Na pronúncia,
a **sílaba tônica vai em maiúsculas**.

### Convenções da pronúncia aproximada

A transcrição é pensada para quem lê português do Brasil, não é AFI:

| Alemão | Fica | Exemplo |
| --- | --- | --- |
| `sch`, `sp-`, `st-` no início | `ch`, `chp`, `cht` | `Straße` → `CHTRÁ-sse` |
| `ch` depois de a, o, u, au | `rr` | `Buch` → `BURR` |
| `ch` nos demais casos | `ch` | `ich` → `ICH` |
| `z`, `tz` | `ts` | `Zeit` → `TSAIT` |
| `w` | `v` · `v` → `f` | `Wasser` → `VÁS-sa` |
| `ei`, `ai` | `ai` · `eu`, `äu` → `oi` | `heiße` → `HAI-sse` |
| `ü` | `iu` · `ö` → `ê` · `ä` → `é` | `müde` → `MIU-de` |
| `-er` final átono | `a` | `Vater` → `FÁ-ta` |
| `-ig` final | `irr` | `wenig` → `VÊ-nirr` |
| `h` inicial | `h` aspirado, como no inglês *house* | `Haus` → `HAUS` |

---

## Como adicionar novos cards

### Jeito rápido: editar `data/cards.js` à mão

Abra o arquivo e acrescente um objeto no fim do array, antes do `];`:

```js
  {"id":739,"nivel":"A1","categoria":"comida","pt":"Eu quero um chá.","de":"Ich möchte einen Tee.",
   "palavras":[
     {"de":"Ich","pt":"eu","silabas":"Ich","pronuncia":"ICH"},
     {"de":"möchte","pt":"gostaria","silabas":"möch-te","pronuncia":"MÊCH-te"},
     {"de":"einen","pt":"um (acusativo)","silabas":"ei-nen","pronuncia":"AI-nen"},
     {"de":"Tee","pt":"chá","silabas":"Tee","pronuncia":"TÊ"}],
   "pronuncia":"ich MÊCH-te ai-nen TÊ"},
```

Regras: o `id` precisa ser único, o `nivel` precisa ser um de `A1`…`C1`, e o
array `palavras` precisa ter uma entrada por palavra da frase alemã, na ordem.
Salve e recarregue a página.

### Jeito recomendado: usar o gerador (Python 3, sem dependências)

Assim a silabação, a pronúncia e as validações saem prontas e consistentes.

1. **Escreva a frase** no arquivo do nível, por exemplo `tools/frases_a1.py`.
   Cada item é uma tupla `(categoria, português, alemão, nota de gramática)` —
   a nota pode ser `None`:

   ```python
   ("comida", "Eu quero um chá.", "Ich möchte einen Tee.",
    "Möchte é a forma mais educada de pedir algo."),
   ```

2. **Rode o gerador:**

   ```bash
   python3 tools/gerar_cards.py
   ```

3. Se alguma palavra alemã ainda não estiver no léxico, o script **não grava
   nada** e lista o que falta, já no formato para colar em `tools/lexico.py`:

   ```
   Faltam 1 palavras no lexico. Cole em lexico.py:

       "tee":                 "",   # 1x
   ```

   Preencha a tradução (`"tee": "chá",`) e rode de novo.

4. Com o léxico completo, o script escreve `data/cards.js` e imprime o resumo
   por nível e por categoria.

O gerador também recusa o arquivo se houver **ids repetidos, frases repetidas
(em português ou em alemão), campos vazios ou nível inválido** — ou seja, ele é
a verificação do conteúdo, não só o montador.

#### Quando a pronúncia sair errada

As regras de `tools/regras.py` acertam a grande maioria das palavras, mas alemão
tem exceções (compostos, estrangeirismos, acento irregular). Há três tabelas de
ajuste, todas no topo do arquivo:

- `SILABAS_OVERRIDE` — silabação explícita: `"abendessen": "A-bend-es-sen"`.
- `TONICA_OVERRIDE` — índice da sílaba tônica, começando em 0: `"hotel": 1`.
- `PRONUNCIA_OVERRIDE` — a pronúncia inteira, para estrangeirismos:
  `"restaurant": "res-to-RÁN"`.

Depois de editar qualquer uma, rode o gerador de novo.

---

## Fontes consultadas

O conteúdo e a progressão dos níveis foram definidos a partir de material
oficial, não de listas aleatórias:

- **Goethe-Institut — Wortliste do Goethe-Zertifikat A1 (Fit in Deutsch 1).**
  Usei o inventário oficial de *Themenbereiche* para definir as categorias do
  A1: Person, Persönliche Beziehungen, Körper/Gesundheit, Wohnen, Umwelt,
  Essen/Trinken, Kommunikationsmittel, Reisen/Verkehr, Einkaufen, Lernen,
  Freizeit/Unterhaltung, além das listas de números, horas, dias e meses.
- **Goethe-Institut / ÖSD / Universidade de Freiburg — Wortliste do
  Goethe-Zertifikat B1.** Usei as áreas temáticas e o critério declarado da
  lista (relevância no uso cotidiano e atual da língua, no âmbito privado e
  público, mas também em trabalho, escola e formação) para montar as categorias
  do B1: formação, trabalho, saúde, moradia, meio ambiente, mídia, viagem,
  dinheiro, burocracia e conceitos políticos.
- **Goethe-Institut — sumário do curso Deutsch Online B2 (capítulos 1 a 12).**
  O B2 segue diretamente os temas e a gramática desse sumário: Beziehungen,
  Gesundheit/Mobbing, Gesellschaft im Wandel, Wohnen, Alles digital, trabalho e
  igualdade, Kunst und Kultur, Gefühle und Sinne, Reisen heute, Geschichte und
  Zukunft — com `je … desto`, passiva com modal, particípios como adjetivo,
  conectores de duas partes, orações concessivas e discurso indireto.
- **Deutsche Welle — cursos *Nicos Weg* (A1, A2, B1).** Serviram de referência
  para a progressão narrativa do A1 e do A2: chegada ao país, apresentação,
  rotina, compras, moradia e trabalho, com o passado (Perfekt) entrando no A2.
- **Quadro Europeu Comum de Referência (descritores de C1).** O C1 não tem
  Wortliste oficial do Goethe, então segui os descritores do nível — textos
  longos e exigentes, uso flexível e idiomático, registro acadêmico e
  profissional — em ciência, economia, política, direito, cultura,
  sustentabilidade, tecnologia, argumentação e expressões idiomáticas.

Links: [Wortliste A1](https://www.goethe.de/pro/relaunch/prf/sw/Goethe-Zertifikat_A1_Fit1_Wortliste.pdf) ·
[Wortliste B1](https://www.goethe.de/pro/relaunch/prf/da/Goethe-Zertifikat_B1_Wortliste.pdf) ·
[Deutsch Online B2 — sumário](https://lernen.goethe.de/deutschonline/B2/PDF/DT_online_B2_Inhalt_1-12_de.pdf) ·
[DW Deutsch lernen](https://learngerman.dw.com/)

## Publicar as alterações

O site está no GitHub Pages, servido a partir da branch `main`. Para atualizar:

```bash
cd ~/Desktop/"curso de alemao"
git add -A
git commit -m "descrição do que mudou"
git push
```

O Pages republica sozinho em cerca de um minuto.

> **Mudou `css/style.css`, `js/app.js` ou `data/cards.js`?** Suba também o
> número do `?v=` nas tags do `index.html` (`app.js?v=2` → `?v=3`). O GitHub
> Pages envia tudo com `cache-control: max-age=600`, então sem isso quem já
> abriu o site continua carregando os arquivos antigos.
>
> O próprio `index.html` também fica até 10 minutos em cache. Para ver a
> mudança na hora, recarregue com <kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>R</kbd>
> (ou <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>R</kbd> no Windows).

## Compatibilidade

Funciona em Chrome, Edge, Firefox e Safari atuais, em computador e celular.
A leitura em voz alta depende da Web Speech API: ela existe em todos esses
navegadores, mas a qualidade e a disponibilidade da voz alemã dependem do que
está instalado no sistema.
