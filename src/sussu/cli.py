# ruff: noqa: E402
from dotenv import load_dotenv

load_dotenv()

import argparse
from pathlib import Path

import rich_argparse

from sussu.basic_logger import logger

# Example commands:
#
# sussu whisper ~/Desktop/videos/part_0004.mp4 --temperature 0 --beam_size 1 \
# --device cpu --fp16 False --output_format srt --model tiny --language pt \
# --output_dir ~/Desktop/videos/
#
# sussu one ~/Desktop/videos/part_0004.mp4 --temperature 0 --beam_size 1 \
# --device cpu --fp16 False --output_format srt --model tiny --language pt \
# --output_dir ~/Desktop/videos/
#
# sussu batch --input_dir ~/Desktop/videos/ --temperature 0 --beam_size 1
# --device cpu --fp16 False --output_format srt --model tiny --language pt
# -s video.mp4 part_0000.mp4 --skip_files part_0001.mp4
# --output_dir 'this wont do anything here'


# Essa função é basicamente um jeito de "enganar" o cli do `whisper`
# para que ele "entenda" que está sendo chamado com determinados argumentos.
def whisper_cli_runner(whisper_args: list[str]) -> None:
    import sys

    # `whisper` não tem stub, por isso o pyright vai gerar erro (ignorado)
    from whisper.transcribe import cli as whisper_cli  # pyright: ignore

    # Aqui está a malícia. Vamos fingir que o python está recebendo os argumento
    # via sys.argv. Com isso o argparse entra em ação da mesma forma que
    # entraria se estivesse sendo executado via linha de comando.
    sys.argv = ["whisper", *whisper_args]
    whisper_cli()


# Essa é a nossa função que vai processar os arquivos usando o whisper original
def batch_whisper(
    input_dir: Path, whisper_raw_args: list[str], skip_files: list[str] | None = None
) -> None:
    # Vamos preencher essa lista com os dados que precisamos
    whisper_args: list[str] = []

    # As extensões abaixo podem não conter todas as extensões suportadas pelo
    # ffmpeg, sinta-se à vontade para adicionar novas extensões
    # fmt: off
    allowed_extensions =  {
        ".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg", ".opus", ".mp4", ".mkv",
        ".webm", ".mov", ".avi", ".3gp", ".wmv",
    }
    # fmt: on

    # Às vezes tem alguns arquivos na mesma pasta que são válidos, mas não
    # queremos transcrever (eu só queria agilizar meus testes manuais)
    if not skip_files:
        skip_files = []

    # Passamos em todos os arquivos da pasta enviada pelo usuário
    for file in input_dir.iterdir():
        skip_loop = False
        ########## VAMOS PULAR ALGUNS ARQUIVOS PARA EVITAR ERROS ##########

        # Pulamos quando é um subdiretório
        if file.is_dir():
            logger.warning(f"Directory not allowed: {file.name}")
            continue

        # Pulamos se a extensão não for permitida
        if file.suffix not in allowed_extensions:
            logger.error(f"File extension not allowed: {file.name}")
            continue

        # Pulamos também quando o usuário pede para pular aquele arquivo via -s
        for skip_file in skip_files:
            if str(file).endswith(skip_file):
                logger.info(f"File skipped: {file.name}")
                skip_loop = True

        if skip_loop:
            skip_loop = False
            continue

        ############ DAQUI EM DIANTE VAI PARA O WHISPER ##########

        # O argumento posicional vai sozinho no primeiro índice
        # depois os argumentos desconhecidos
        whisper_args.extend([str(file), *whisper_raw_args])
        logger.debug(f"audio set as {file!s}")

        # Por fim, adicionamos o outdir para ser sempre a pasta onde está
        # o arquivo original. Isso gera um arquivo de mesmo nome com a extensão
        # `.srt`.
        logger.debug(f"--output_dir set to {file.parent}")
        whisper_args.extend(["--output_dir", str(file.parent)])

        # Desativa o modo verboso do `whisper` por padrão para que a gente possa
        # ver nossos logs. Se o user passar algo, usa o que ele passar.
        if "--verbose" not in whisper_args:
            whisper_args += ["--verbose", "False"]
            logger.debug("--verbose set to False by default")

        # Agora só chamar o whisper com os argumentos que montamos
        logger.debug(f"whisper commands are: {whisper_args}")
        logger.debug(f"Final command: whisper {' '.join(whisper_args)}")
        whisper_cli_runner(whisper_args)

        # Zeramos os argumentos para o próximo loop
        whisper_args = []


def build_argparse() -> argparse.ArgumentParser:
    # Nosso main parser e o subparser para os comandos
    parser = argparse.ArgumentParser(
        prog="sussu", formatter_class=rich_argparse.RawDescriptionRichHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    ########## WHISPER PARSER ##########

    # Esse subparse só será usado como um wrapper do argparse do whisper.
    # No final das contas, ele só vai chamar `whisper.transcribe.cli()`
    whisper_parser = subparsers.add_parser(
        "whisper",
        help="Calls `whisper` directly",
        conflict_handler="resolve",
        aliases=["one"],
        formatter_class=rich_argparse.RawDescriptionRichHelpFormatter,
    )
    whisper_parser.set_defaults(command="whisper")

    # Esse argumento aqui é pra garantir que vamos chamar o help do whisper e
    # não do nosso parser
    whisper_parser.add_argument(
        "-h", "--help", help="Shows `whisper` help.", action="store_true"
    )

    ########## NOSSOS PARSERS ##########
    # Minha ideia aqui é criar um subparser `batch` que vai receber um diretório
    # com arquivos de vídeo. Vamos passar em todos os arquivos do diretório e
    # usar o whisper para transcrever cada um deles.

    batch_parser = subparsers.add_parser(
        "batch",
        help="Process files with `whisper` in batch mode",
        formatter_class=rich_argparse.RawDescriptionRichHelpFormatter,
    )

    # Só coloquei essa função aqui para ficar próxima do argumento e facilitar
    # minha explicação na hora de gravar.
    def parse_input_dir(path_str: str) -> Path:
        path = Path(path_str)

        if not path.is_dir():
            msg = f"{path_str!r} is not a directory"
            raise argparse.ArgumentTypeError(msg)

        return path.resolve()

    # Isso deverá ser uma pasta que contém arquivos de vídeo ou áudio
    batch_parser.add_argument(
        "--input_dir",
        help="Directory with files to work with",
        type=parse_input_dir,
        required=True,
    )

    # Para testar, eu estava pulando um monte de arquivos para ir mais rápido
    batch_parser.add_argument(
        "-s",
        "--skip_files",
        help="Name of file(s) to skip",
        action="extend",
        nargs="+",
        default=[],
    )

    # Essa foi a maneira mais simples e direta de remover output_dir dos
    # unknown_args. Se isso fosse para o whisper, geraria conflito
    batch_parser.add_argument("-o", "--output_dir", help=argparse.SUPPRESS)
    return parser


def run() -> None:
    ########## PARSE KNOWN ARGS ##########

    # Vamos receber argumentos que são conhecidos (os nossos), e desconhecidos.
    # Argumentos desconhecidos serão repassados para o whisper cli.
    parser = build_argparse()
    args, unknown_args = parser.parse_known_args()

    # Se o comando for whisper, passamos tudo direto para o whisper
    if args.command == "whisper":
        # Simula -h e --help
        if args.help:
            whisper_cli_runner(["--help"])
            return

        # Executa o whisper normal, só que por baixo de `sussu`
        # Ex.: `sussu whisper audio.mp3` chama o cli original do `whisper` com
        # o argumento `audio.mp3` (ou qualquer outro argumento)
        whisper_cli_runner(unknown_args)
        return

    # Se o comando for `batch`, fazemos nosso trabalho
    if args.command == "batch":
        batch_whisper(args.input_dir, unknown_args, args.skip_files)


if __name__ == "__main__":
    run()
