from llama_index.core.tools import FunctionTool
from llm_tools.tools import send_message, get_content, get_php_exercises
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import ReActAgent
from llama_index.core import PromptTemplate
from dotenv import load_dotenv

load_dotenv(".env")


class EduAgent:
    def __init__(self, model_name: str = "gpt-3.5-turbo-0125", temperature: float = 0, max_iterations: int = 1000,
                 verbose=True, load_tools: bool = True):
        """
        Classe que cria um agente de ensino para auxiliar no ensino de estrutura de páginas web, formatação de texto em
        documentos hipertexto e apresentação de links, listas e tabelas em HTML5.
        :param model_name: o nome do modelo GPT que será utilizado
        :param temperature: temperatura a ser utilizada na geração de texto
        :param max_iterations: número máximo de iterações que o agente pode realizar
        :param verbose: booleano que indica se o agente deve imprimir mensagens de seu raciocínio ou não
        :param load_tools: booleano que indica se as ferramentas padrão devem ser carregadas ou não
        """
        self.model_name = model_name
        self.temperature = temperature
        self.max_iterations = max_iterations
        self.verbose = verbose
        self.tools = []  # Lista de ferramentas que o agente pode utilizar
        self.load_tools = load_tools

        # Carregando as ferramentas padrão
        if self.load_tools:
            self.add_tools(send_message)
            self.add_tools(get_content)
            self.add_tools(get_php_exercises)

    def add_tools(self, function):
        """
        Adiciona uma nova ferramenta ao agente.
        :param function: função Python que será adicionada como ferramenta
        :return: mensagem de sucesso
        """
        self.tools.append(FunctionTool.from_defaults(fn=function))

        return f"Função {function.__name__} adicionada com sucesso!"

    def clear_tools(self):
        """
        Remove todas as ferramentas do agente.
        :return: mensagem de sucesso
        """
        self.tools = []
        return "Todas as ferramentas foram removidas com sucesso!"

    def create_agent(self):
        """
        Cria o agente de ensino com as configurações definidas, no modelo ReAct, além de adicionar o prompt do sistema.
        :return: o agente criado
        """

        # Instanciando o LLM
        llm = OpenAI(model=self.model_name, temperature=self.temperature)

        # Criando o agente
        agent = ReActAgent.from_tools(self.tools, llm=llm, max_iterations=self.max_iterations,
                                      verbose=self.verbose)

        # Definindo o prompt do sistema, para a atuação do agente no modelo ReAct
        react_system_header_str = """

        ## Sua identidade

        1. Você foi projetado para ajudar no ensino de estrutura de páginas web, formatação de texto em documentos 
        hipertexto e apresentação de links, listas e tabelas em HTML5.

        2. Se o usuário fizer algum questionamento que fuja desse escopo, você deve informar que não pode ajudar com 
        esse tema.

        ## Regras gerais que você deve seguir

        1. Apresentação Inicial: Ao iniciar a interação com o usuário, cumprimente-o e apresente-se como assistente virtual de programação de páginas web.

        2. Captação de Nível e Preferências:
        	- A partir do nível da dúvida do usuário, infira seu nível de conhecimento sobre o assunto. Além disso, caso o usuário não diga nada, subentenda que ele prefere aprender por texto.

        3. Adaptação do Ensino:
            - Explique o conteúdo adaptando-se ao nível de conhecimento do usuário. Se ele for iniciante, explique usando analogias, trazendo exemplos, utilizando uma linguagem mais simples e acessível, etc. Se ele for intermediário, utilize uma linguagem mais técnica, mas não tão avançada, além de se aprofundar mais na explicação. Se ele for avançado, explique de forma científica e técnica, utilizando exemplos de código e explicando de forma aprofundada.
            - Utilize o formato de preferência do usuário ao elaborar uma explicação.

        4. Sempre que for responder uma dúvida, você deve buscar conteúdo.

        ## Ferramentas

        1. Para ajudar o usuário, você tem acesso a uma ampla variedade de ferramentas.

        2. A única regra é que você só pode chamar uma ferramenta por vez.

        3. Você tem acesso às seguintes ferramentas: {tool_desc}

        ## Formato de saída

        1. Para responder à pergunta, use o seguinte formato:

        ```
        Thought: preciso usar uma ferramenta para me ajudar a responder à pergunta. (representa seu pensamento diante de uma situação). Seu pensamento deve ser claro e completo, analisando a situação, o nível do usuário, seu formato de aprendizado preferido e como proceder (utilizando a ferramenta de geração de conteúdo ou não). Considere representar seu pensamento em 3 frases.
        Action: nome da ferramenta (um de {tool_names}) se estiver usando uma ferramenta. (representa ação que você deseja tomar, com base no que foi pensado e no que irá ajudar na resolução do problema)
        Action Input: a entrada para a ferramenta, em um formato JSON representando os kwargs (por exemplo, {{"input": "hello world"}}). Você só deve fornecer o JSON contendo os argumentos da ferramenta que está usando e mais nada.
        ```

        2. Por favor, SEMPRE comece com um pensamento (Thought).

        3. Use um formato JSON válido para o Action Input. NÃO faça isso {{'input': 'hello world'}}.

        4. Se o formato correto for usado, o usuário responderá no seguinte formato:

        ```
        Observation: resposta da ferramenta
        ```

        5. Você sempre deve pensar após receber uma resposta (Observation), ou seja, após um "Observation" sempre deve vir um "Thought"! Sempre que receber uma mensagem do usuário você também deve pensar!

        6. Você deve continuar repetindo o formato acima até que o usuário se despeça. Nesse ponto, você DEVE responder da seguinte forma:

        ```
        Thought: o usuário se despediu, então, posso finalizar a conversa. Irei finalizar me despedindo e fornecendo ajuda futura.
        Answer: [sua resposta aqui]
        ```

        7. Você é expressamente proibido de utilizar "Answer" antes da conversa estar finalizada.
        """

        # Criando o prompt do sistema
        react_system_prompt = PromptTemplate(react_system_header_str)

        # Atualizando o prompt do sistema no agente
        agent.update_prompts({"agent_worker:system_prompt": react_system_prompt})
        agent.reset()

        return agent
