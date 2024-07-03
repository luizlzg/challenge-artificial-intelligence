import json
from typing import List, Union
from data_indexing.indexing_tools import get_index, get_retriever, retrieve_nodes
import time


def send_message(message: str) -> str:
    """
    Função "Enviar Mensagem": esta função envia uma mensagem para o usuário.
    :param message: a mensagem a ser enviada
    :return: a resposta do usuário após receber a mensagem
    """

    # Verifica se o arquivo JSON existe
    caminho_assistant = './message_broker/assistant_msgs.json'
    with open(caminho_assistant, 'r', encoding='utf-8') as arquivo:
        assistant_msgs = json.load(arquivo)

    assistant_msgs["assistant"].append(message)
    with open(caminho_assistant, 'w', encoding='utf-8') as arquivo:
        json.dump(assistant_msgs, arquivo, indent=4)

    caminho_user = './message_broker/user_msgs.json'
    with open(caminho_user, 'r', encoding='utf-8') as arquivo:
        user_msgs = json.load(arquivo)

    num_user_msgs = len(user_msgs["user"])
    while True:
        time.sleep(1)
        with open(caminho_user, 'r', encoding='utf-8') as arquivo:
            user_msgs = json.load(arquivo)
        num_user_msgs2 = len(user_msgs["user"])

        if num_user_msgs2 > num_user_msgs:
            break

    resposta_usuario = user_msgs["user"][-1]

    return resposta_usuario + ("\n(Aviso 1 do Sistema: caso essa mensagem seja uma dúvida, explique em seus "
                               "pensamentos qual o nível do usuário e seu formato de aprendizado preferido.)\n(Aviso "
                               "2 do Sistema: caso essa mensagem seja uma dúvida, utilize a ferramenta de obtenção de "
                               "conteúdo para basear sua resposta.)")


def get_content(user_msg: str, content_format: str) -> Union[str, List[str]]:
    """
    Função "Obter Conteúdo": esta função busca conteúdo com base na dúvida do usuário, no formato de conteúdo preferido do usuário.
    Lembre-se que essa função não gera respostas, apenas o conteúdo para te apoiar na sua geração de resposta.
    Essa função não adapta o conteúdo ao nível do usuário, você é responsável por isso. Sendo assim, ao pesquisar a mesma coisa, buscando níveis de conteúdos diferentes, você não terá sucesso.
    :param user_msg: mensagem do usuário, contendo sua dúvida
    :param content_format: formato do conteúdo que o usuário prefere. Deve ser um dos valores a seguir: ['texto', 'video', 'imagem'], que representam, respectivamente, conteúdo em texto, vídeo e imagem.
    :return: uma lista com os conteúdos e materiais correspondentes à dúvida do usuário. Caso a lista esteja vazia, a função retorna uma mensagem informando que não foi possível encontrar conteúdo.
    """

    # Mapeando o formato de conteúdo preferido para o seu respectivo índice do RAG
    map_format_to_index = {'texto': get_index('results/pdf'), 'video': get_index('results/video'),
                           'imagem': get_index('results/image')}

    # Instanciando o retriever que irá recuperar os conteúdos do RAG
    retriever = get_retriever(map_format_to_index[content_format])

    # Recuperando os nós, que representam o conteúdo, do RAG
    rag_return = retrieve_nodes(retriever, user_msg)

    # Se o RAG retornar algum conteúdo, retorna esse conteúdo
    if rag_return:
        # Se o conteúdo for de imagem, anexa o link da imagem ao conteúdo
        if content_format == 'imagem':
            rag_return_img = []
            for r in rag_return:
                rag_return_img.append(
                    r + "\n(Este é o link para acessar a imagem a qual o texto se refere https://raw.githubusercontent.com/grupo-a/challenge-artificial-intelligence/main/resources"
                        "/Infografico-1.jpg)\n")

            return f"Adapte o seguinte conteúdo ao nível do usuário (veja se é iniciante, intermediário ou avançado): {rag_return_img}\nVocê deve utilizar esse conteúdo apenas como base, você deve criar a resposta com suas palavras e adaptando ao nível do usuário. Restrinja-se em apenas responder o que o usuário perguntou, não forneça informações que fuja de sua dúvida. Além disso, envie para o usuário o link da imagem que irá auxiliar na dúvida dele. Você é proibido de responder sem enviar o link."

        elif content_format == "video":
            return f"Adapte o seguinte conteúdo ao nível do usuário (veja se é iniciante, intermediário ou avançado): {rag_return}\nVocê deve utilizar esse conteúdo apenas como base, você deve criar a resposta com suas palavras e adaptando ao nível do usuário. Restrinja-se em apenas responder o que o usuário perguntou, não forneça informações que fuja de sua dúvida. Além disso, envie para o usuário o link do vídeo que irá auxiliar na dúvida dele. Você é proibido de responder sem enviar o link."
        else:
            return f"Adapte o seguinte conteúdo ao nível do usuário (veja se é iniciante, intermediário ou avançado): {rag_return}\nVocê deve utilizar esse conteúdo apenas como base, você deve criar a resposta com suas palavras e adaptando ao nível do usuário. Restrinja-se em apenas responder o que o usuário perguntou, não forneça informações que fuja de sua dúvida."
    else:
        return ("Não foi possível encontrar conteúdo. Talvez em outros formatos possa haver conteúdos relacionados à "
                "dúvida do usuário. Explique para ele essa possibilidade.")


def get_php_exercises(user_msg: str) -> Union[str, List[str]]:
    """
    Função "Obter Exercícios de PHP": esta função busca exercícios de PHP com base na dúvida do usuário, caso seja uma dúvida relacionada a desenvolvimento de sistemas com PHP.
    :param user_msg: mensagem do usuário, contendo sua dúvida
    :return: uma lista com os exercícios correspondentes à dúvida do usuário. Caso a lista esteja vazia, a função retorna uma mensagem informando que não foi possível encontrar exercícios.
    """

    # Instanciando o retriever que irá recuperar os conteúdos do RAG
    retriever = get_retriever(get_index('results/exercicios'))

    # Recuperando os nós, que representam o conteúdo, do RAG
    rag_return = retrieve_nodes(retriever, user_msg)

    # Se o RAG retornar algum conteúdo, retorna esse conteúdo
    if rag_return:
        return rag_return
    else:
        return ("Não foi possível encontrar conteúdo. Talvez em outros formatos possa haver conteúdos relacionados à "
                "dúvida do usuário. Explique para ele essa possibilidade.")
