from data_indexing.indexing_tools import index_video, index_img, index_exercicios, index_pdf
import argparse


def main():
    parser = argparse.ArgumentParser(description="Preparação dos dados")
    parser.add_argument(
        "--video-path",
        required=False,
        type=str,
        default="./data/video",
        help="O caminho para o diretório que já contém o txt do vídeo processado.",
    )

    parser.add_argument(
        "--persist-video",
        required=False,
        type=str,
        default="results/video",
        help="O caminho onde o índice do vídeo será salvo",
    )

    parser.add_argument(
        "--img-path",
        required=False,
        type=str,
        default="./data/image",
        help="O caminho para o diretório que já contém o txt da imagem processada.",
    )

    parser.add_argument(
        "--persist-img",
        required=False,
        type=str,
        default="results/image",
        help="O caminho onde o índice da imagem será salvo",
    )

    parser.add_argument(
        "--exerc-path",
        required=False,
        type=str,
        default="./data/exercicios",
        help="O caminho para o diretório que já contém o txt dos exercícios processados.",
    )

    parser.add_argument(
        "--persist-exerc",
        required=False,
        type=str,
        default="results/exercicios",
        help="O caminho onde o índice dos exercícios será salvo",
    )

    parser.add_argument(
        "--pdf-path",
        required=False,
        type=str,
        default="./data/pdf",
        help="O caminho para o diretório que contém o PDF",
    )

    parser.add_argument(
        "--persist-pdf",
        required=False,
        type=str,
        default="results/pdf",
        help="O caminho onde o índice do PDF será salvo",
    )

    args = parser.parse_args()

    # Rodando a indexação de todos os tipos de dados

    print("Indexando o vídeo...\n")
    index_video(args.video_path, args.persist_video)
    print("Indexação do vídeo concluída.\n")

    print("Indexando a imagem...\n")
    index_img(args.img_path, args.persist_img)
    print("Indexação da imagem concluída.\n")

    print("Indexando os exercícios...\n")
    index_exercicios(args.exerc_path, args.persist_exerc)
    print("Indexação dos exercícios concluída.\n")

    print("Indexando o PDF...\n")
    index_pdf(args.pdf_path, args.persist_pdf)
    print("Indexação do PDF concluída.\n")

    print("Todos os dados foram indexados com sucesso!")


if __name__ == '__main__':
    main()
