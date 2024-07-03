from data_preparation.preparing_data import prepare_img, prepare_video, prepare_exercises
import argparse


def main():
    parser = argparse.ArgumentParser(description="Preparação dos dados")
    parser.add_argument(
        "--video-path",
        required=False,
        type=str,
        default="./resources/Dica do professor.mp4",
        help="O caminho para o arquivo contendo o vídeo a ser processado",
    )

    parser.add_argument(
        "--txt-video",
        required=False,
        type=str,
        default="./data/video/video.txt",
        help="O caminho onde o txt criado a partir do vídeo será salvo",
    )

    parser.add_argument(
        "--img-url",
        required=False,
        type=str,
        default="https://raw.githubusercontent.com/grupo-a/challenge-artificial-intelligence/main/resources"
                "/Infografico-1.jpg",
        help="A URL contendo a imagem que vai ser processada",
    )

    parser.add_argument(
        "--txt-img",
        required=False,
        type=str,
        default="./data/image/image.txt",
        help="O caminho onde o txt criado a partir da imagem será salvo",
    )

    parser.add_argument(
        "--exerc-path",
        required=False,
        type=str,
        default="./resources/Exercícios.json",
        help="O caminho para o arquivo contendo os exercícios que vão ser processados",
    )

    parser.add_argument(
        "--txt-exerc",
        required=False,
        type=str,
        default="./data/exercicios/exercicios.txt",
        help="O caminho onde o txt criado a partir dos exercícios será salvo",
    )

    args = parser.parse_args()

    # Rodando a preparação de todos os tipos de dados

    print("Preparando o vídeo...\n")
    prepare_video(args.video_path, args.txt_video)
    print("Preparação do vídeo concluída.\n")

    print("Preparando a imagem...\n")
    prepare_img(args.img_url, args.txt_img)
    print("Preparação da imagem concluída.\n")

    print("Preparando os exercícios...\n")
    prepare_exercises(args.exerc_path, args.txt_exerc)
    print("Preparação dos exercícios concluída.\n")

    print("Todos os dados foram preparados com sucesso!")


if __name__ == '__main__':
    main()
