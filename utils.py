import os
import json
from llama_index.core.agent import ReActAgent
import time


def create_message_broker(user_json_path: str = './message_broker/user_msgs.json',
                          assistant_json_path: str = './message_broker/assistant_msgs.json'):
    """
    Função que cria os arquivos JSON que armazenarão as mensagens do usuário e do assistente.
    :param user_json_path: caminho do JSON que armazenará as mensagens do usuário
    :param assistant_json_path: caminho do JSON que armazenará as mensagens do assistente
    :return:
    """

    # Criando diretório para armazenar os JSONs
    diretorio = './message_broker'
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
        print(f'Diretório {diretorio} criado com sucesso.')
    else:
        print(f'O diretório {diretorio} já existe.')

    # Criando json que armazenará as mensagens do usuário
    if os.path.exists(user_json_path):
        print('JSON do user já existente!')
    else:
        # Cria uma nova estrutura de dados JSON, caso não exista
        user_msgs = {"user": []}
        with open(user_json_path, 'w') as arquivo:
            json.dump(user_msgs, arquivo, indent=4)
        print('Caminho do user criado!')

    # Criando json que armazenará as mensagens do assistente
    if os.path.exists(assistant_json_path):
        print('Caminho do assistant já existente!')
    else:
        # Cria uma nova estrutura de dados JSON, caso não exista
        assistant_msgs = {"assistant": []}
        with open(assistant_json_path, 'w') as arquivo:
            json.dump(assistant_msgs, arquivo, indent=4)
        print('JSON do assistant criado!')


def start_chat(agent: ReActAgent, user_json_path: str = './message_broker/user_msgs.json',
               assistant_json_path: str = './message_broker/assistant_msgs.json'):
    """
    Função que inicia o chat do agente com o usuário. É nessa função que o agente responde às mensagens do usuário, atuando no modelo ReAct.
    :param agent: agente de ensino que responderá às mensagens do usuário
    :param user_json_path: caminho do JSON que armazena as mensagens do usuário
    :param assistant_json_path: caminho do JSON que armazena as mensagens do assistente
    :return:
    """

    # Abrindo o JSON que armazena as mensagens do usuário
    with open(user_json_path, 'r', encoding='utf-8') as arquivo:
        user_msgs = json.load(arquivo)

    # Analisando o número de mensagens do usuário, antes do agente começar a responder
    old_user_msgs = len(user_msgs["user"])

    # Loop que verifica se há novas mensagens do usuário e responde a elas
    while True:
        time.sleep(1)  # Espera 1 segundo antes de verificar se há novas mensagens do usuário,
        # para que dê tempo de abrir o arquivo JSON

        # Abrindo o JSON que armazena as mensagens do usuário
        with open(user_json_path, 'r', encoding='utf-8') as arquivo:
            user_msgs2 = json.load(arquivo)

        # Captando o número de mensagens do usuário
        new_user_msgs = len(user_msgs2["user"])
        resposta = ""  # variável que armazenará a resposta final do agente

        # Verificando se há novas mensagens do usuário
        if new_user_msgs > old_user_msgs:
            # Iniciando o chat do agente com o usuário, a partir da última mensagem do usuário
            response = agent.chat(user_msgs2["user"][-1] + ("\n(Aviso 1 do Sistema: caso essa mensagem seja uma "
                                                            "dúvida, explique em seus"
                                                            "pensamentos qual o nível do usuário e seu formato de aprendizado preferido.)\n(Aviso "
                                                            "2 do Sistema: caso essa mensagem seja uma dúvida, utilize a ferramenta de obtenção de "
                                                            "conteúdo para basear sua resposta.)"))

            # Armanezando a última resposta do agente, quando o ciclo ReAct se encerra
            resposta = response.response

        # Se a resposta não for vazia, armazena a resposta no JSON do assistente
        if resposta:
            # Abrindo o JSON que armazena as mensagens do assistente
            with open(assistant_json_path, 'r', encoding='utf-8') as arquivo:
                assistant_msgs = json.load(arquivo)

            # Adicionando a mensagem do assistente ao JSON
            assistant_msgs["assistant"].append(resposta)

            # Salvando a mensagem do assistente no JSON
            with open(assistant_json_path, 'w') as arquivo:
                json.dump(assistant_msgs, arquivo, indent=4)

            # Atualizando o número de mensagens do usuário
            old_user_msgs = new_user_msgs + 1
            agent.reset()
