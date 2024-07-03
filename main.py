import gradio as gr
import time
import json
from utils import create_message_broker, start_chat
from llm.educational_agent import EduAgent
import threading


def talk_to_agent(message: str, history):
    """
    Função que realiza a conversa entre o usuário e o agente.
    :param message: mensagem do usuário
    :param history: histórico de mensagens
    :return:
    """
    # Abrindo o JSON que armazena as mensagens do usuário
    caminho_user = './message_broker/user_msgs.json'
    with open(caminho_user, 'r') as arquivo:
        user_msgs = json.load(arquivo)

    # Adicionando a mensagem do usuário ao JSON
    user_msgs["user"].append(message)
    with open(caminho_user, 'w') as arquivo:
        json.dump(user_msgs, arquivo, indent=4)

    # Abrindo o JSON que armazena as mensagens do assistente
    caminho_assistant = './message_broker/assistant_msgs.json'
    with open(caminho_assistant, 'r') as arquivo:
        assistant_msgs = json.load(arquivo)

    # Analisando o número de mensagens do agente, antes do usuário começar a responder
    old_assistant_msgs = len(assistant_msgs["assistant"])

    # Loop que verifica se há novas mensagens do agente
    while True:
        time.sleep(1)  # Espera 1 segundo antes de verificar se há novas mensagens do usuário,
        # para que dê tempo de abrir o arquivo JSON

        # Abrindo o JSON que armazena as mensagens do assistente
        with open(caminho_assistant, 'r') as arquivo:
            assistant_msgs2 = json.load(arquivo)

        # Captando o número de mensagens do assistente
        new_assistant_msgs = len(assistant_msgs2["assistant"])

        # Verificando se há novas mensagens do assistente
        if new_assistant_msgs > old_assistant_msgs:
            break

    # Se há novas mensagens do assistente, ela é retornada, simulando o retorno em streaming
    resposta = assistant_msgs2["assistant"][-1].replace('<', '').replace('>', '')
    for i in range(len(resposta)):
        time.sleep(0.01)
        yield resposta[: i + 7]


if __name__ == '__main__':
    # Criando o message broker
    create_message_broker()

    # Instanciando o agente de ensino
    agent = EduAgent()
    agent = agent.create_agent()

    # Função para iniciar o chat em um thread separado
    def start_chat_thread(agent):
        start_chat(agent)


    # Iniciando o chat entre o usuário e o agente em um novo thread
    chat_thread = threading.Thread(target=start_chat_thread, args=(agent,))
    chat_thread.start()

    # Iniciando a interface de chat, através do Gradio
    gr.ChatInterface(talk_to_agent).launch(share=True)
