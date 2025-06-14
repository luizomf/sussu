# sussu(rro): CLI educacional com OpenAI Whisper

> Ferramenta de linha de comando focada em educação e IA offline.
> Usa o poder do Whisper da OpenAI pra transcrever áudios e vídeos de forma simples.

Ao rodar este projeto, uma das primeiras coisas que você vai querer fazer é usar o
comando `whisper` para fazer a transcrição inicial de algum vídeo ou áudio. Essa transcrição é um ótimo jeito de ver na prática como o Whisper trabalha e o que esperar dos resultados.

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

## Rodando pela primeira vez

Para testar se tudo funcionou perfeitamente você pode tanto **ativar o ambiente virtual** quanto usar **`uv run`**. Teste com `whisper -h`. Isso deve mostrar a `help` completa do `whisper`. Exemplos:

```sh
uv run whisper -h
# Ou se estiver com o ambiente virtual ativo
whisper -h
```

**Observação:** alguns editores como VS Code ou Zed, ativam seu ambiente virtual automaticamente ao abrir uma nova instância do terminal se tudo estiver configurado corretamente, basta sair (`exit`) e abrir novamente o terminal.

---
