import os
import tempfile
from typing import Dict, List, Optional, Type, Union

import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from loaders import load_csv, load_pdf, load_txt, load_website, load_youtube

# Constantes
VALID_FILE_TYPES: List[str] = ["Site", "Youtube", "PDF", "TXT", "CSV"]

VALID_MODELS: Dict[str, Dict[str, Union[List[str], Type]]] = {
    "Groq": {
        "modelos": [
            "llama-3.3-70b-versatile",
            "meta-lhama/lhama-guarda-4-12B",
            "gemma2-9b-it",
        ],
        "chat": ChatGroq,
    },
    "Google-Gemini": {
        "modelos": ["models/gemini-1.5-flash", "models/gemini-1.5-pro"],
        "chat": ChatGoogleGenerativeAI,
    },
}

MEMORY = ConversationBufferMemory()


def load_arquivos(file_type: str, files: Optional[Union[str, bytes]]) -> Optional[str]:
    """Carrega o conteúdo de diferentes tipos de arquivos.

    Args:
        file_type: Tipo do arquivo a ser carregado.
        files: Conteúdo do arquivo ou URL.

    Returns:
        Optional[str]: Conteúdo do arquivo em formato de texto ou None se houver erro.
    """
    document = None
    if files is not None:
        if file_type == "Site":
            document = load_website(files)
        elif file_type == "Youtube":
            document = load_youtube(files)
        elif file_type == "PDF":
            temp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
            # Ensure files is bytes for writing to temp file
            file_content = (
                files.read() if hasattr(files, "read") else files.encode("utf-8")
            )
            temp.write(file_content)
            temp_name = temp.name
            temp.close()
            document = load_pdf(temp_name)
            # Clean up temporary file
            os.remove(temp_name)
        elif file_type == "TXT":
            temp = tempfile.NamedTemporaryFile(suffix=".txt", delete=False)
            # Ensure files is bytes for writing to temp file
            file_content = (
                files.read() if hasattr(files, "read") else files.encode("utf-8")
            )
            temp.write(file_content)
            temp_name = temp.name
            temp.close()
            document = load_txt(temp_name)
            # Clean up temporary file
            os.remove(temp_name)
        elif file_type == "CSV":
            temp = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
            # Ensure files is bytes for writing to temp file
            file_content = (
                files.read() if hasattr(files, "read") else files.encode("utf-8")
            )
            temp.write(file_content)
            temp_name = temp.name
            temp.close()
            document = load_csv(temp_name)
            # Clean up temporary file
            os.remove(temp_name)

    # Escape curly braces in the document content
    if document is not None:
        document = document.replace("{", "{{").replace("}", "}}")

    return document


def load_model(
    provider: str,
    model: str,
    api_key: str,
    file_type: str,
    files: Optional[Union[str, bytes]],
) -> None:
    """Inicializa o modelo de chat com o documento carregado.

    Args:
        provider: Provedor do modelo (Groq ou Google-Gemini).
        model: Nome do modelo a ser usado.
        api_key: Chave de API do provedor.
        file_type: Tipo do arquivo carregado.
        files: Conteúdo do arquivo ou URL.
    """
    document = load_arquivos(file_type, files)

    system_message = f"""Você é um assistente amigável chamado Oráculo.
    Você possui acesso às seguintes informações vindas 
    de um documento {file_type}: 

    ####
    {document}
    ####

    Histórico da conversa:
    {MEMORY.buffer_as_str}

    Utilize as informações fornecidas e o histórico da conversa para basear as suas respostas.

    Sempre que houver $ na sua saída, substitua por S.

    Se a informação do documento for algo como "Just a moment...Enable
    JavaScript and cookies to continue" sugira ao usuário carregar novamente
    o Oráculo!"""

    template = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            ("user", "{input}"),
        ]
    )

    chat = VALID_MODELS[provider]["chat"](model=model, api_key=api_key)
    chain = template | chat
    st.session_state["chain"] = chain


def chat_page() -> None:
    """Renderiza a página principal do chat."""
    st.header("🤖 Bem-vindo ao Morfeu", divider="rainbow")

    chat_model = st.session_state.get("chain")
    memory = st.session_state.get("memory", MEMORY)

    if chat_model is None:
        st.info(
            "Por favor, inicialize o Morfeu na barra lateral " "'Seleção do modelo'."
        )
        return

    for msg in memory.buffer_as_messages:
        chat = st.chat_message(msg.type)
        chat.markdown(msg.content)

    input_user = st.chat_input("Digite uma mensagem")
    if input_user:
        memory.chat_memory.add_user_message(input_user)
        chat = st.chat_message("human")
        chat.markdown(input_user)

        chat = st.chat_message("ai")
        response = chat.write_stream(
            chat_model.stream(
                {"input": input_user, "chat_history": memory.buffer_as_messages}
            )
        )
        memory.chat_memory.add_ai_message(response)
        st.session_state["memory"] = memory


def side_bar() -> None:
    """Renderiza a barra lateral com opções de upload e seleção de modelo."""
    with st.sidebar:
        tabs = st.tabs(["Upload de Arquivos", "Seleção de Modelos"])
        with tabs[0]:
            file_type = st.selectbox("Selecione o tipo de arquivo", VALID_FILE_TYPES)
            files = None
            if file_type == "Site":
                url = st.text_input("Digite o URL do site")
                if url:
                    if not url.startswith(("http://", "https://")):
                        url = "https://" + url
                    files = url
            elif file_type == "Youtube":
                files = st.text_input("Digite o URL do Youtube")
            elif file_type == "PDF":
                files = st.file_uploader("Upload de PDF", type=".pdf")
            elif file_type == "TXT":
                files = st.file_uploader("Upload de TXT", type=".txt")
            elif file_type == "CSV":
                files = st.file_uploader("Upload de CSV", type=".csv")
        with tabs[1]:
            provider = st.selectbox(
                "Selecione o provedor do modelo", VALID_MODELS.keys()
            )
            model = st.selectbox(
                "Selecione o modelo", VALID_MODELS[provider]["modelos"]
            )
            api_key = st.text_input(
                f"Adicione a api key para o provedor {provider}",
                value=st.session_state.get(f"api_key_{provider}"),
            )
            st.session_state[f"api_key_{provider}"] = api_key

        if st.button("Inicializar Morfeu", use_container_width=True):
            load_model(provider, model, api_key, file_type, files)

        if st.button(
            "🗑️ Limpar Histórico de Conversa",
            use_container_width=True,
            help="Apaga todo o histórico de conversa atual",
        ):
            st.session_state["memory"] = MEMORY


def main() -> None:
    """Função principal que inicializa a aplicação."""
    chat_page()
    side_bar()


if __name__ == "__main__":
    main()
