# sussu(rro): CLI educacional com OpenAI Whisper

> Ferramenta de linha de comando focada em educação e IA offline.
> Usa o poder do Whisper da OpenAI pra transcrever áudios e vídeos de forma simples.

Ao rodar este projeto, uma das primeiras coisas que você vai querer fazer é usar o
comando `whisper` para fazer a transcrição inicial de algum vídeo ou áudio. Essa transcrição é um ótimo jeito de ver na prática como o Whisper trabalha e o que esperar dos resultados.

- [Repositório oficial do `whisper`](https://github.com/openai/whisper)

Por isso, vamos começar pela **instalação** do projeto, o que vai disponibilizar os comandos `sussu` e `whisper` no terminal.

## Instalação do `sussu`

Este projeto usa o `Python 3.11.9` por questões de compatibilidade com o Whisper. Evite alterar essa versão caso não saiba o que está fazendo, porque eu **já testei tudo para você**.

Além disso, este projeto também usa o [uv](https://docs.astral.sh/uv/) no gerenciamento geral (pacotes, versão do Python, etc).

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

É necessário ter o [`ffmpeg`](https://ffmpeg.org/), que é um pacote de software open source que contém uma coleção de ferramentas e bibliotecas para lidar com arquivos multimídia, principalmente áudio e vídeo. O `whisper` trabalha com transcrição de arquivos de áudio, mas o `ffmpeg` permite que você não tenha que converter seus vídeos em áudio para fazer a transcrição.

Para instalar o ffmpeg no seu sistema use um dos comandos abaixo. Isso veio diretamente do [repositório oficial do `whisper`](https://github.com/openai/whisper):

```sh
# no Ubuntu ou Debian
sudo apt update && sudo apt install ffmpeg

# no Arch Linux
sudo pacman -S ffmpeg

# no MacOS com Homebrew (https://brew.sh/)
brew install ffmpeg

# no Windows com Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# no Windows usando Scoop (https://scoop.sh/)
scoop install ffmpeg

# Adicional
# no Windows usando winget (https://winstall.app/apps/Gyan.FFmpeg)
winget install --id=Gyan.FFmpeg  -e
```

**Observação:** os únicos comandos que testei da lista acima foram do MacOS e Ubuntu. Aprovados ✅!

---

## Rodando pela primeira vez

Para testar se tudo funcionou perfeitamente você pode tanto **ativar o ambiente virtual** quanto usar **`uv run`**. Teste com `whisper -h`. Isso deve mostrar a `help` completa do `whisper`. Exemplos:

```sh
uv run whisper -h
# Ou se estiver com o ambiente virtual ativo
whisper -h
```

**Observação:** alguns editores como VS Code ou Zed, ativam seu ambiente virtual automaticamente ao abrir uma nova instância do terminal se tudo estiver configurado corretamente, basta sair (`exit`) e abrir novamente o terminal.

---

## `whisper -h`: entendendo alguns argumentos importantes

Ao digitar `whisper -h` ou `whisper --help`, você pode se assustar com a quantidade de argumentos que estão ali, disponíveis para uso. Claro que você não precisa saber o que cada um deles faz, na verdade, a maioria dos argumentos tem valores padrão que já funcionam perfeitamente. Mas, caso queira personalizar um pouco o comportamente, vamos analisar alguns deles.

O `whisper` usa o `argparse` do Python para criar essa `help` maravilhosa. Caso queira aprender mais sobre isso, assista meu vídeo:

- [Python e argparse: Do Zero a uma CLI Profissional (Projeto Real na Prática)](https://www.youtube.com/watch?v=Ad6934NXn4A)

---

### Argumentos essenciais do `whisper`

**`--model MODEL`:** define qual o modelo será utilizado na transcrição do áudio. É opcional, e o valor padrão é `turbo`. Este model funciona muito bem, é rápido e multilíngue, mas requer cerca de **6GB de VRAM** para funcionar.

Talvez você queira usar outros modelos que usam mais ou menos recursos do seu hardware, ou que possuem mais ou menos parâmetros (como `base`, `small`, `medium`, etc).

Abaixo os modelos disponíveis:

- **`tiny`:** 39M, `tiny.en` e `tiny`, VRAM ~1 GB
- **`base`:** 74M, `base.en` e `base`, VRAM ~1 GB
- **`small`:** 244M, `small.en` e `small`, VRAM ~2 GB
- **`medium`:** 769M, `medium.en` e `medium`, VRAM ~5 GB
- **`large`:** 1550M, `large`, `large-v2` e `large-v3`, VRAM ~10 GB
- **`turbo`:** 809M, `turbo`, VRAM ~6 GB

**VRAM** é um tipo especializado de memória RAM usada pelas placas de vídeo (GPUs).
Se o seu computador compartilha a RAM com a GPU, como acontece nos Macs com chip Apple Silicon (M1, M2, M3 e posteriores), você conseguirá usar os modelos do Whisper **mesmo sem uma placa de vídeo dedicada**.

Nesse caso, o fator limitador passa a ser a **quantidade total de memória disponível no sistema**.
Por exemplo: se você tem apenas 8GB de RAM, o ideal é testar os modelos `tiny`, `base` ou `small`.

A partir do modelo `medium`, é bem provável que você perceba uma **queda absurda no desempenho geral da máquina**, já que a memória será completamente consumida.

---
