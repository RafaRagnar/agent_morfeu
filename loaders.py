import os
from time import sleep
from typing import Optional

import streamlit as st
from fake_useragent import UserAgent
from langchain_community.document_loaders import (
    CSVLoader,
    PyPDFLoader,
    TextLoader,
    WebBaseLoader,
    YoutubeLoader,
)


def load_website(url: str) -> str:
    """Carrega o conteúdo de um site.

    Args:
        url: URL do site a ser carregado.

    Returns:
        str: Conteúdo do site em formato de texto.

    Raises:
        st.error: Se não for possível carregar o site após 5 tentativas.
    """
    document = ""
    max_retries = 5

    for i in range(max_retries):
        try:
            os.environ["USER_AGENT"] = UserAgent().random
            loader = WebBaseLoader(url, raise_for_status=True)
            documents_list = loader.load()
            document = "\n\n".join([doc.page_content for doc in documents_list])
            if document:
                break
        except Exception as e:
            print(
                f"Erro ao carregar o site (tentativa {i + 1}/{max_retries}): {str(e)}"
            )
            sleep(3)

    if not document:
        st.error("Não foi possível carregar o site após várias tentativas.")
        st.stop()
    return document


def load_youtube(video_id: str) -> str:
    """Carrega a transcrição de um vídeo do YouTube.

    Args:
        video_id: ID do vídeo do YouTube.

    Returns:
        str: Transcrição do vídeo em formato de texto.

    Raises:
        st.error: Se não for possível carregar a transcrição.
    """
    try:
        loader = YoutubeLoader(video_id, add_video_info=False, language=["pt"])
        documents_list = loader.load()
        document = "\n\n".join([doc.page_content for doc in documents_list])
        if not document:
            st.error("Não foi possível carregar a transcrição do vídeo.")
            st.stop()
        return document
    except Exception as e:
        st.error(f"Erro ao carregar a transcrição do vídeo: {str(e)}")
        st.stop()


def load_csv(path: str) -> str:
    """Carrega o conteúdo de um arquivo CSV.

    Args:
        path: Caminho do arquivo CSV.

    Returns:
        str: Conteúdo do arquivo em formato de texto.

    Raises:
        st.error: Se não for possível carregar o arquivo.
    """
    try:
        loader = CSVLoader(path)
        documents_list = loader.load()
        document = "\n\n".join([doc.page_content for doc in documents_list])
        if not document:
            st.error("O arquivo CSV está vazio ou não pôde ser carregado.")
            st.stop()
        return document
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo CSV: {str(e)}")
        st.stop()


def load_pdf(path: str) -> str:
    """Carrega o conteúdo de um arquivo PDF.

    Args:
        path: Caminho do arquivo PDF.

    Returns:
        str: Conteúdo do arquivo em formato de texto.

    Raises:
        st.error: Se não for possível carregar o arquivo.
    """
    try:
        loader = PyPDFLoader(path)
        documents_list = loader.load()
        document = "\n\n".join([doc.page_content for doc in documents_list])
        if not document:
            st.error("O arquivo PDF está vazio ou não pôde ser carregado.")
            st.stop()
        return document
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo PDF: {str(e)}")
        st.stop()


def load_txt(path: str) -> str:
    """Carrega o conteúdo de um arquivo de texto.

    Args:
        path: Caminho do arquivo de texto.

    Returns:
        str: Conteúdo do arquivo em formato de texto.

    Raises:
        st.error: Se não for possível carregar o arquivo.
    """
    try:
        loader = TextLoader(path)
        documents_list = loader.load()
        document = "\n\n".join([doc.page_content for doc in documents_list])
        if not document:
            st.error("O arquivo de texto está vazio ou não pôde ser carregado.")
            st.stop()
        return document
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo de texto: {str(e)}")
        st.stop()


if __name__ == "__main__":
    # Teste com um vídeo do YouTube
    url_you = "r_p_t9IRc0A"
    document = load_youtube(url_you)
    print(document)
