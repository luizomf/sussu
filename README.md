# sussu(rro): CLI educacional com OpenAI Whisper

> Ferramenta de linha de comando focada em educação e IA offline.
> Usa o poder do Whisper da OpenAI para transcrever áudios e vídeos de forma simples.

Ao rodar este projeto, uma das primeiras coisas que você vai querer fazer é usar o comando `whisper` para fazer a transcrição inicial de algum vídeo ou áudio. Essa transcrição é um ótimo jeito de ver na prática como o **Whisper** trabalha e o que esperar dos resultados.

- [Repositório oficial do `whisper`](https://github.com/openai/whisper)

Por isso, vamos começar pela **instalação** do projeto, o que vai disponibilizar os comandos `sussu` e `whisper` no terminal.

## Instalação do `sussu`

Se você encontrar alguma dificuldade com o ambiente, recomendo meu tutorial completo:

- [Ambiente Python Moderno 2025: UV, Ruff, Pyright, pyproject.toml e VS Code](https://www.youtube.com/watch?v=HuAc85cLRx0)

Este projeto utiliza o **Python 3.11.9** por questões de compatibilidade com o **Whisper**. Evite alterar essa versão se não souber o que está fazendo, pois **eu já testei tudo para você**.

Além disso, este projeto usa o [`uv`](https://docs.astral.sh/uv/) para o gerenciamento geral (pacotes, versão do Python, etc.).

Para instalar tudo, basta rodar o comando:

```sh
uv sync  # é só isso mesmo 😅
```

`uv sync` é suficiente para:

- Baixar e instalar o `python 3.11.9`
- Criar o ambiente virtual em `.venv`
- Instalar os pacotes necessários
- Buildar o `whisper` e o `sussu`

---

## `ffmpeg`

Você também precisará ter o **`ffmpeg`** instalado. Ele é um software de código aberto com várias ferramentas e bibliotecas para trabalhar com arquivos multimídia, especialmente áudio e vídeo. Embora o `whisper` foque na transcrição de áudio, o `ffmpeg` é quem permite que você transcreva seus vídeos diretamente, sem precisar convertê-los para áudio antes.

Para instalar o `ffmpeg` no seu sistema, você pode usar um dos comandos abaixo. Eles foram retirados diretamente do [repositório oficial do `whisper`](https://github.com/openai/whisper):

```bash
# No Ubuntu ou Debian
sudo apt update && sudo apt install ffmpeg

# No Arch Linux
sudo pacman -S ffmpeg

# No macOS com Homebrew (https://brew.sh/)
brew install ffmpeg

# No Windows com Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# No Windows usando Scoop (https://scoop.sh/)
scoop install ffmpeg

# Adicional: No Windows usando winget (https://winstall.app/apps/Gyan.FFmpeg)
winget install --id=Gyan.FFmpeg -e
```

**Observação:** Dos comandos listados, os únicos que testei e aprovei (✅) foram os para **macOS** e **Ubuntu**.

---

## Rodando pela Primeira Vez

Para verificar se tudo foi instalado corretamente, você tem duas opções: **ativar o ambiente virtual** ou usar o comando **`uv run`**. Sugiro que você teste com `whisper -h`. Esse comando deve exibir a ajuda completa do `whisper`, indicando que ele está funcionando. Veja os exemplos:

```bash
uv run whisper -h
# Ou, se você já ativou o ambiente virtual
whisper -h
```

**Observação:** Editores de código como **VS Code** ou **Zed** podem ativar o ambiente virtual automaticamente ao abrir um novo terminal, desde que estejam configurados corretamente. Se for o seu caso, basta fechar e abrir o terminal novamente para que as mudanças façam efeito.

---

## `whisper -h`: Entendendo Alguns Argumentos Importantes

Ao digitar `whisper -h` ou `whisper --help`, você pode se surpreender com a quantidade de argumentos disponíveis. Mas não se preocupe! Você não precisa saber o que cada um deles faz. Na verdade, a maioria dos argumentos já vem com valores padrão que funcionam perfeitamente. No entanto, se você quiser personalizar um pouco o comportamento da ferramenta, vamos analisar alguns dos mais importantes.

O `whisper` utiliza a biblioteca `argparse` do Python para gerar essa documentação de ajuda (`help`) completa e bem organizada. Se você tiver interesse em aprender mais sobre como criar interfaces de linha de comando profissionais com Python, confira meu vídeo:

- [Python e argparse: Do Zero a uma CLI Profissional (Projeto Real na Prática)](https://www.youtube.com/watch?v=Ad6934NXn4A)

---

### Argumentos Essenciais do `whisper`

Vamos começar com os argumentos que você usará com mais frequência:

**`audio`**: Este é o **argumento posicional** principal. Ele representa o caminho completo (localização) do arquivo de áudio ou vídeo que você quer transcrever.

**Exemplo:**

```bash
whisper /caminho/do/seu/arquivo.mp4
```

No exemplo acima, você notou que especificamos apenas o caminho do arquivo de vídeo. Nas próximas seções, vou detalhar as opções que mais utilizo para personalizar a transcrição.

---

**`--model MODEL`**: Este argumento serve para **definir qual modelo será usado na transcrição** do seu áudio ou vídeo. Ele é opcional, e o valor padrão é `turbo`. O modelo `turbo` é excelente: rápido e multilíngue, mas requer cerca de **6GB de VRAM** para rodar.

Talvez você queira usar outros modelos que exigem mais ou menos recursos do seu hardware, ou que possuem mais ou menos parâmetros (como `base`, `small`, `medium`, etc.).

Aqui estão os modelos disponíveis e seus requisitos aproximados de VRAM:

- **`tiny`**: 39M parâmetros, `tiny.en` e `tiny`, VRAM ~1 GB
- **`base`**: 74M parâmetros, `base.en` e `base`, VRAM ~1 GB
- **`small`**: 244M parâmetros, `small.en` e `small`, VRAM ~2 GB
- **`medium`**: 769M parâmetros, `medium.en` e `medium`, VRAM ~5 GB
- **`large`**: 1550M parâmetros, `large`, `large-v2` e `large-v3`, VRAM ~10 GB
- **`turbo`**: 809M parâmetros, `turbo`, VRAM ~6 GB

**VRAM** é um tipo de memória RAM especializada que as placas de vídeo (GPUs) usam. Mas não se preocupe se você não tiver uma placa de vídeo dedicada! Se seu computador compartilha a RAM com a GPU, o que acontece em Macs com chips Apple Silicon (M1, M2, M3 e posteriores), por exemplo, você conseguirá usar os modelos do Whisper normalmente.

Nesses casos, o que realmente limita é a **quantidade total de memória RAM disponível no seu sistema**. Por exemplo: se você tem apenas 8GB de RAM, o ideal é testar os modelos `tiny`, `base` ou `small`.

A partir do modelo `medium`, é bem provável que você perceba uma **queda drástica no desempenho geral da sua máquina**, já que a memória será completamente consumida.

**Exemplo:**

```bash
whisper /caminho/do/seu/arquivo.mp4 --model large-v2
```

---

**`--device DEVICE`**: Este argumento é para você que possui uma **placa de vídeo NVIDIA com drivers CUDA** e uma versão compatível com o PyTorch. Se for o seu caso, vale a pena usar `--device cuda` para aproveitar o processamento da GPU. Caso contrário, não se preocupe em alterar esta opção, o padrão é `cpu` (processamento pela CPU) e funcionará perfeitamente.

**Exemplo:**

```bash
whisper /caminho/do/seu/arquivo.mp4 --model large-v2 --device cpu
```

---

**`--output_dir` ou `-o`**: Define o **caminho da pasta onde as transcrições serão salvas**. Por padrão, os arquivos serão salvos na raiz do projeto (`.`).

**`--output_format` ou `-f`**: Permite que você escolha o **formato da transcrição ou legenda** gerada. As opções disponíveis são: `txt`, `vtt`, `srt`, `tsv`, `json` e `all` (que gera todos os formatos). O padrão é `all`.


**Exemplo:**

O arquivo de saída será `srt` (SubRip) na pasta indicada em `-o`. Essa pasta será criada caso não exista.

```bash
whisper /caminho/do/seu/arquivo.mp4 --model turbo -o caminho/da/pasta_de_saida -f srt
```

---

**`--task`**: Com este argumento, você pode escolher entre **transcrever o áudio** no idioma original ou **traduzir para o inglês**. As opções são `transcribe` (o padrão, que transcreve no idioma falado no áudio) ou `translate` (que traduz o conteúdo para o inglês).

**Exemplo:**

```bash
whisper /caminho/do/seu/arquivo.mp4 --model turbo --task transcribe
```

---

**`--language`**: Este argumento permite que você **especifique o idioma falado no áudio ou vídeo**. Existem muitas opções de idiomas disponíveis. Se você não informar esse argumento, o `whisper` é inteligente o suficiente para detectar automaticamente o idioma do conteúdo.

Forma curta (language code):

```python
["af", "am", "ar", "as", "az", "ba", "be", "bg", "bn", "bo", "br", "bs", "ca",
"cs", "cy", "da", "de", "el", "en", "es", "et", "eu", "fa", "fi", "fo", "fr",
"gl", "gu", "ha", "haw", "he", "hi", "hr", "ht", "hu", "hy", "id", "is", "it",
"ja", "jw", "ka", "kk", "km", "kn", "ko", "la", "lb", "ln", "lo", "lt", "lv",
"mg", "mi", "mk", "ml", "mn", "mr", "ms", "mt", "my", "ne", "nl", "nn", "no",
"oc", "pa", "pl", "ps", "pt", "ro", "ru", "sa", "sd", "si", "sk", "sl", "sn",
"so", "sq", "sr", "su", "sv", "sw", "ta", "te", "tg", "th", "tk", "tl", "tr",
"tt", "uk", "ur", "uz", "vi", "yi", "yo", "yue", "", "zh"]
```

- Exemplo para português do Brasil: `--language pt`

Forma longa (language name):

```python
["Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian", "Assamese",
"Azerbaijani", "Bashkir", "Basque", "Belarusian", "Bengali", "Bosnian",
"Breton", "Bulgarian", "Burmese", "Cantonese", "Castilian", "Catalan",
"Chinese", "Croatian", "Czech", "Danish", "Dutch", "English", "Estonian",
"Faroese", "Finnish", "Flemish", "French", "Galician", "Georgian", "German",
"Greek", "Gujarati", "Haitian", "Haitian Creole", "Hausa", "Hawaiian", "Hebrew",
"Hindi", "Hungarian", "Icelandic", "Indonesian", "Italian", "Japanese",
"Javanese", "Kannada", "Kazakh", "Khmer", "Korean", "Lao", "Latin", "Latvian",
"Letzeburgesch", "Lingala", "Lithuanian", "Luxembourgish", "Macedonian",
"Malagasy", "Malay", "Malayalam", "Maltese", "Mandarin", "Maori", "Marathi",
"Moldavian", "Moldovan", "Mongolian", "Myanmar", "Nepali", "Norwegian",
"Nynorsk", "Occitan", "Panjabi", "Pashto", "Persian", "Polish", "Portuguese",
"Punjabi", "Pushto", "Romanian", "Russian", "Sanskrit", "Serbian", "Shona",
"Sindhi", "Sinhala", "Sinhalese", "Slovak", "Slovenian", "Somali", "Spanish",
"Sundanese", "Swahili", "Swedish", "Tagalog", "Tajik", "Tamil", "Tatar",
"Telugu", "Thai", "Tibetan", "Turkish","Turkmen", "Ukrainian", "Urdu", "Uzbek",
"Valencian", "Vietnamese", "Welsh", "Yiddish", "Yoruba"]
```

- Exemplo para português do Brasil: `--language Portuguese`

Se precisar de um dicionário completo com todos os idiomas e seus códigos, ele está disponível em `whisper.tokenizer.LANGUAGES` dentro do código do `whisper`.


**Exemplo:**

```bash
# Para o comando ficar menor, vou manter tudo padrão
# model turbo (padrão)
# task transcribe (padrão)
# etc...
# Idioma falado no vídeo "Português"
whisper /caminho/do/seu/arquivo.mp4 --language pt
```


---

**`--temperature`:** controla a "criatividade" do modelo. Vai de `0.0` a `1.0`. Quanto mais alto, mais liberdade o modelo tem pra decidir os próximos tokens. Esse parâmetro interage com `--beam_size`, `--patience` e `--best_of`.

**`--beam_size`:** número de hipóteses que o modelo mantém em paralelo. Pensa como se ele testasse vários caminhos ao mesmo tempo e no fim escolhesse o melhor. O padrão é `5` e **só funciona se `--temperature == 0.0`**.

**`--patience`:** fator de tolerância que faz o modelo continuar explorando novas hipóteses mesmo depois de achar uma aceitável. Requer `--temperature == 0.0` e `--beam_size > 1`.

**`--best_of`:** número de amostras diferentes geradas antes de escolher a melhor. Funciona apenas quando `--temperature > 0.0`.

**Cola rápida:**

```
- temperature > 0 → usa sampling
  ✅ --best_of 5 (5 amostras)
  🔴 --beam_size (ignorado)
  🔴 --patience (ignorado)

- temperature == 0 → usa beam search
  ✅ --beam_size 5 (5 hipóteses)
  ✅ --patience 2 (2 x 5 = 10 hipóteses)
  🔴 --best_of (ignorado)

- temperature == 0 → greedy
  ✅ --beam_size 1 (1 hipótese)
  🔴 --patience (não faz diferença)
  🔴 --best_of (ignorado)
```

**Importante:** Quanto maiores os valores de `--beam_size`, `--patience` e `--best_of`, mais lento e "indeciso" o modelo tende a ficar. Isso acontece porque ele precisa gerar mais hipóteses ou amostras e, em seguida, tomar uma decisão entre elas. Faça testes rápidos para confirmar esse comportamento.

**Observação sincera:**

Na prática, o modelo vai responder como foi treinado, independente do seu capricho nas configs. Trocar `temperature`, `beam_size`, `patience` e afins pode virar desperdício de tempo.

**Recomendação direta:** só mexa nessas opções se:

- o modelo começar a repetir palavras (loop)
- estiver errando demais em blocos grandes

Se for só por causa de uma ou duas palavras... aceita e segue. Ou então faz igual eu: **testa tudo por uma semana e conclui que o padrão já era bom** 😅

**Exemplo:**

O arquivo de saída será `srt` (SubRip) na pasta indicada em `-o`. Essa pasta será criada caso não exista.

```bash
# Greedy: Mais rápido, mas pode errar mais por considerar apenas uma hipótese por vez.
whisper /caminho/do/seu/arquivo.mp4 --temperature 0.0 --beam_size 1

# Beam Search: Utiliza 3 hipóteses em paralelo.
# O 'patience' padrão é 1.
whisper /caminho/do/seu/arquivo.mp4 --temperature 0.0 --beam_size 3

# Sampling: Gera 5 amostras diferentes para escolher a melhor.
whisper /caminho/do/seu/arquivo.mp4 --temperature 0.7 --best_of 5
```

**`--temperature_increment_on_fallback`**: Este argumento permite que você **aumente a temperatura do modelo em casos de falha na transcrição**. Se o modelo encontrar dificuldades na temperatura `0.0`, ele fará um "fallback" e tentará com a temperatura incrementada. O valor também varia de `0.0` a `1.0`. No entanto, **cuidado: definir `0.0` para este argumento causará um erro `ZeroDivisionError: float division by zero`** (isso pode ser um pequeno "bugzinho" 🫣, mas, de fato, não faria muito sentido usar zero aqui, já que o objetivo é justamente *incrementar* a temperatura). O valor padrão é `0.2`.

---
