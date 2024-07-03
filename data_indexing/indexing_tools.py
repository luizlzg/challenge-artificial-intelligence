from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.core.indices.base import BaseIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import QueryBundle
import shutil
from typing import List

import os
from dotenv import load_dotenv

load_dotenv(".env")


def index_pdf(path_to_pdf: str = './data/pdf', persist_dir: str = 'results/pdf') -> None:
    """
    Indexa os documentos PDF em path_to_pdf e persiste o índice em persist_dir.
    :param path_to_pdf: o caminho para os documentos PDF
    :param persist_dir: o diretório onde o índice será persistido
    :return: None
    """

    # Copiando o PDF para um diretório que contenha só ele, para evitar que outros arquivos sejam indexados
    caminho_origem = "./resources/Capítulo do Livro.pdf"
    if not os.path.exists(path_to_pdf):
        # Se não existir, cria o caminho
        os.makedirs(path_to_pdf)

    # Copia o arquivo de origem para o destino
    shutil.copy(caminho_origem, path_to_pdf)

    # Carregando os documentos
    documents = SimpleDirectoryReader(path_to_pdf).load_data()

    # Indexando os documentos
    index = VectorStoreIndex.from_documents(documents,
                                            transformations=[SentenceSplitter(chunk_size=256, chunk_overlap=0)])

    # Persistindo o índice
    index.storage_context.persist(persist_dir=persist_dir)


def index_img(path_to_img: str = './data/imagem', persist_dir: str = 'results/imagem') -> None:
    """
    Indexa o texto da imagem, que está em path_to_img, e persiste o índice em persist_dir.
    :param path_to_img: o caminho para o texto da imagem
    :param persist_dir: o diretório onde o índice será persistido
    :return: None
    """

    # Carregando os documentos
    documents = SimpleDirectoryReader(path_to_img).load_data()

    # Indexando os documentos
    index = VectorStoreIndex.from_documents(documents,
                                            transformations=[SentenceSplitter(chunk_size=128, chunk_overlap=0)])

    # Persistindo o índice
    index.storage_context.persist(persist_dir=persist_dir)


def index_exercicios(path_to_txt: str = './data/exercicio', persist_dir: str = 'results/exercicio') -> None:
    """
    Indexa o texto dos exercícios, que está em path_to_txt, e persiste o índice em persist_dir.
    :param path_to_txt: o caminho para o texto dos exercícios
    :param persist_dir: o diretório onde o índice será persistido
    :return: None
    """

    # Carregando os documentos
    documents = SimpleDirectoryReader(path_to_txt).load_data()

    # Indexando os documentos
    index = VectorStoreIndex.from_documents(documents,
                                            transformations=[SentenceSplitter(chunk_size=256, chunk_overlap=0)])

    # Persistindo o índice
    index.storage_context.persist(persist_dir=persist_dir)


def index_video(path_to_txt: str = './data/video', persist_dir: str = 'results/video') -> None:
    """
    Indexa o texto do vídeo, que está em path_to_txt, e persiste o índice em persist_dir.
    :param path_to_txt: o caminho para o texto do vídeo
    :param persist_dir: o diretório onde o índice será persistido
    :return: None
    """

    # Carregando os documentos
    documents = SimpleDirectoryReader(path_to_txt).load_data()

    # Indexando os documentos
    index = VectorStoreIndex.from_documents(documents,
                                            transformations=[SentenceSplitter(chunk_size=256, chunk_overlap=0)])

    # Persistindo o índice
    index.storage_context.persist(persist_dir=persist_dir)


def get_index(persist_dir: str = 'results/pdf') -> BaseIndex:
    """
    Carrega o índice persistido em persist_dir.
    :param persist_dir: o diretório onde o índice foi persistido
    :return: o índice carregado
    """

    # Verificando se a indexação já foi feita e o índice foi persistido no diretório indicado.
    if not os.path.exists(persist_dir):
        raise ValueError(
            f"Index não encontrado em {persist_dir}. Certifique-se de indexar os documentos primeiro e persistir o "
            f"índice em {persist_dir}.")

    # Carregando o índice, caso o índice já tenha sido persistido.
    else:
        storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
        index = load_index_from_storage(storage_context)

    return index


def get_retriever(index) -> RetrieverQueryEngine:
    """
    Configura o retriever e a query engine que retornará os documentos mais similares à query.
    :param index: o índice a ser utilizado
    :return: a query engine configurada
    """

    # Configurando o retriever
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=3,  # retornando o top 3 nós mais similares
    )

    # Criando a engine que irá retornar os nós a partir da query do usuário.
    query_engine = RetrieverQueryEngine(
        retriever=retriever,
    )

    return query_engine


def retrieve_nodes(retriever: RetrieverQueryEngine, query: str) -> List[str]:
    """
    Recupera os nós mais similares à query.
    :param retriever: o retriever configurado
    :param query: a query do usuário
    :return: uma lista com os nós mais similares à query
    """

    # Recuperando os nós mais similares à query
    recuperado = retriever.retrieve(QueryBundle(query))

    # Armazenando os materiais recuperados
    materiais = []

    for r in recuperado:
        # Garantindo que apenas nós com mais de 75% de similaridade sejam retornados
        if r.score >= 0.75:
            materiais.append(r.text)

    return materiais
