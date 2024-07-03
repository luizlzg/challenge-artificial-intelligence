from openai import OpenAI
import os
import json
import pandas as pd

from dotenv import load_dotenv

load_dotenv(".env")


def prepare_video(video_path: str = "./resources/Dica do professor.mp4",
                  txt_to_save: str = "./data/video/video.txt") -> None:
    """
    Função que prepara o conteúdo do vídeo para ser utilizado em um modelo de geração de texto (LLM). A função irá transcrever o áudio do vídeo, segmentar o texto em frases e, em seguida, agrupar as frases em parágrafos. Por fim, a função irá salvar o conteúdo em um arquivo txt, que conterá o texto do parágrafo, os timestamps de início e fim do parágrafo e um link para o vídeo, que já estará na minutagem do conteúdo em questão.
    :param video_path: o caminho do vídeo que será utilizado para transcrição
    :param txt_to_save: o caminho do arquivo txt que irá armazenar o conteúdo do vídeo
    :return: None
    """

    # Obtendo a transcrição do vídeo em segmentos, juntamente com os timestamps de cada segmento.
    client = OpenAI()

    audio_file = open(video_path, "rb")
    transcript = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-1",
        response_format="verbose_json",
        timestamp_granularities=["segment"],
        language='pt'
    )

    # Organizando os segmentos e os timestamps em uma lista
    segmentos = []
    for t in transcript.segments:
        segmentos.append([t['text'], t['start'], t['end']])

    # Juntando os segmentos que não terminam com ponto final com os segmentos que terminam com ponto final, formando,
    # assim, frases.
    frases = []  # criando a lista para armazenar as frases
    frase = ''  # string que irá representar as frases que serão formadas
    inicio = 0  # variável que irá armazenar o timestamp de início de cada frase

    # Iterando sobre os segmentos para formar as frases
    for i, r in enumerate(segmentos):

        # Se o segmento não terminar com ponto final, adicione-o à frase
        if not r[0].endswith('.'):
            frase += r[0] + ' '

        # Se o segmento terminar com ponto final, adicione-o à frase e armazene a frase formada na lista de frases.
        # Em seguida, reinicie a variável frase e capte o timestamp de início da próxima frase.
        else:
            frase += r[0]
            frases.append([frase, inicio, r[2]])
            inicio = segmentos[i + 1][1]
            frase = ''

    # Acumulando 4 frases para formar um parágrafo
    paragrafos = []

    # Iterando sobre as frases para formar os parágrafos, de 4 em 4. Além disso, armazenando o timestamp de início e
    # fim de cada parágrafo.
    for i in range(0, len(frases), 4):
        if i + 4 <= len(frases):
            paragrafo = frases[i][0] + ' ' + frases[i + 1][0] + ' ' + frases[i + 2][0] + ' ' + frases[i + 3][0]
            paragrafos.append([paragrafo, frases[i][1], frases[i + 3][2]])
        else:
            paragrafo = frases[i][0] + ' ' + frases[i + 1][0] + ' ' + frases[i + 2][0]
            paragrafos.append([paragrafo, frases[i][1], frases[i + 2][2]])

    # Criando uma string que irá ser armazenado em um txt, representando o conteúdo do vídeo.
    string_video = ''

    # Nessa string, terá o texto do parágrafo, os timestamps de início e fim do parágrafo e um link para o vídeo,
    # que já estará na minutagem do conteúdo em questão.
    for i in range(len(paragrafos)):
        inicio = paragrafos[i][1]
        fim = paragrafos[i][2]
        texto = paragrafos[i][0]

        link = f"(Para acessar o conteúdo, clique no link https://youtu.be/w3L27GhWLog&t={round(inicio)}. O vídeo já está na minutagem do conteúdo em questão e ele dura cerca de {round(fim - inicio)} segundos.)"

        string_video += f"O seguinte texto foi dito entre os segundos {round(inicio)} e {round(fim)} do vídeo: {texto}\n{link}\n\n\n"

    # Verifica se a pasta que o txt vai ser salvo existe
    caminho = '/'.join(txt_to_save.split('/')[:-1])
    if not os.path.exists(caminho):
        # Se não existir, cria o caminho
        os.makedirs(caminho)

    # Salvando a string resultante em um txt
    with open(txt_to_save, 'w', encoding='utf-8') as arquivo:
        arquivo.write(string_video)


def prepare_img(
        image_url: str = "https://raw.githubusercontent.com/grupo-a/challenge-artificial-intelligence/main/resources"
                         "/Infografico-1.jpg",
        txt_to_save: str = './data/image/image.txt') -> None:
    """
    Função que prepara o conteúdo da imagem para ser utilizado em um modelo de geração de texto (LLM). A função irá extrair o texto da imagem e salva em um txt.
    :param image_url: a URL da imagem que será utilizada para extração de texto
    :param txt_to_save: o caminho do arquivo txt que irá armazenar o conteúdo da imagem
    :return: None
    """

    # Enviando a imagem para o GPT-4o para a extração de informações da imagem.
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Descreva, em detalhes, o que há na imagem."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=512,
    )

    img_text = response.choices[0].message.content  # obtendo o texto da imagem

    # Verifica se a pasta que o txt vai ser salvo existe
    caminho = '/'.join(txt_to_save.split('/')[:-1])
    if not os.path.exists(caminho):
        # Se não existir, cria o caminho
        os.makedirs(caminho)

    # Salvando o texto da imagem em um txt
    with open(txt_to_save, 'w', encoding='utf-8') as arquivo:
        arquivo.write(img_text)


def prepare_exercises(exercise_path: str = "./resources/Exercícios.json",
                      txt_to_save: str = './data/exercicios/exercicios.txt') -> None:
    """
    Função que prepara o conteúdo dos exercícios para ser utilizado em um modelo de geração de texto (LLM). A função irá extrair o enunciado dos exercícios, juntamente com as opções de resposta, a opção correta, o feedback e, então, salvará tudo em um txt.
    :param exercise_path: o caminho do arquivo que contém os exercícios
    :param txt_to_save: o caminho do arquivo txt que irá armazenar o conteúdo dos exercícios
    :return: None
    """

    # Abrindo o arquivo JSON que contém os exercícios
    with open(exercise_path, 'r', encoding='utf-8') as file:
        json_aux = json.load(file)

    # Organizando todas as informações dos exercícios em um DataFrame pandas.
    exercicios = json_aux['content']
    data_exercicios = {'exercicio': [], 'enunciado': [], 'opcao_1': [], 'opcao_2': [], 'opcao_3': [], 'opcao_4': [],
                       'opcao_5': [], 'correta': [], 'feedback': []}

    # Iterando sobre os exercícios
    for exerc in exercicios:

        # Obtendo qual é o exercício
        data_exercicios['exercicio'].append(exerc['title'])

        # Captando o enunciado, filtrando tags HTML que poderiam atrapalhar o LLM
        enunciado = exerc['content']['html'].split('<div class="question"><p></p><p><strong>')[1].split(
            '</strong></p><p></p></div>')[0]
        data_exercicios['enunciado'].append(f"Enunciado: {enunciado}")

        # Captando as opções de resposta, filtrando tags HTML que poderiam atrapalhar o LLM
        opcao1 = exerc['content']['options'][0]['content']['html'].split('<div class="question-option"><p>')[1].split(
            '</p></div>')[0].strip()
        data_exercicios['opcao_1'].append(f"Opção 1: {opcao1}")

        opcao2 = exerc['content']['options'][1]['content']['html'].split('<div class="question-option"><p>')[1].split(
            '</p></div>')[0].strip()
        data_exercicios['opcao_2'].append(f"Opção 2: {opcao2}")

        opcao3 = exerc['content']['options'][2]['content']['html'].split('<div class="question-option"><p>')[1].split(
            '</p></div>')[0].strip()
        data_exercicios['opcao_3'].append(f"Opção 3: {opcao3}")

        opcao4 = exerc['content']['options'][3]['content']['html'].split('<div class="question-option"><p>')[1].split(
            '</p></div>')[0].strip()
        data_exercicios['opcao_4'].append(f"Opção 4: {opcao4}")

        opcao5 = exerc['content']['options'][4]['content']['html'].split('<div class="question-option"><p>')[1].split(
            '</p></div>')[0].strip()
        data_exercicios['opcao_5'].append(f"Opção 5: {opcao5}")

        # Obtendo a opção correta do exercício
        for i in range(len(exerc['content']['options'])):
            if exerc['content']['options'][i]['correct']:
                data_exercicios['correta'].append(f"Opção correta: {i + 1}")

        # Captando o feedback do exercício, filtrando tags HTML que poderiam atrapalhar o LLM
        feedback = \
            exerc['content']['options'][0]['feedback']['html'].split('<div class="question-feedback"> <p>')[1].split(
                '</p></div>')[0].strip()
        data_exercicios['feedback'].append(f"Feedback do exercício: {feedback}")

    # Gerando o DataFrame
    df_exercicios = pd.DataFrame(data_exercicios)

    # Inserindo informações de área, curso e matéria de cada exercício no DataFrame
    area = [f"Área de estudo do exercício: {json_aux['tags'][0]['area']['name']}" for _ in range(len(df_exercicios))]

    curso = [f"Curso referente ao exercício: {json_aux['tags'][0]['course']['name']}" for _ in
             range(len(df_exercicios))]

    materia = [f"Disciplina estudada no exercício: {json_aux['tags'][0]['subject']['name']}" for _ in
               range(len(df_exercicios))]

    df_exercicios['area'] = area
    df_exercicios['curso'] = curso
    df_exercicios['materia'] = materia

    # Com todas as informações anteriores, preparamos uma string que contém todas as informações de todos os exercícios
    string_resultante = ''

    # Iterando sobre o DataFrame e preparando a string
    for index, row in df_exercicios.iterrows():
        string_resultante += f"{row['exercicio']}\n{row['enunciado']}\n{row['opcao_1']}\n{row['opcao_2']}\n{row['opcao_3']}\n{row['opcao_4']}\n{row['opcao_5']}\n{row['correta']}\n{row['feedback']}\n{row['area']}\n{row['curso']}\n{row['materia']}\n\n\n\n"

    # Verifica se a pasta que o txt vai ser salvo existe
    caminho = '/'.join(txt_to_save.split('/')[:-1])
    if not os.path.exists(caminho):
        # Se não existir, cria o caminho
        os.makedirs(caminho)

    # Salvando a string resultante em um txt
    with open(txt_to_save, 'w', encoding='utf-8') as arquivo:
        arquivo.write(string_resultante)
