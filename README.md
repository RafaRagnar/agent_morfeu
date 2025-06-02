# 🤖 Morfeu - Assistente Virtual Inteligente

Morfeu é um assistente virtual inteligente que pode processar diferentes tipos de documentos e responder perguntas baseadas no conteúdo deles. O assistente utiliza modelos de linguagem avançados da Groq e Google Gemini para fornecer respostas precisas e contextuais.

## ✨ Funcionalidades

- Processamento de múltiplos formatos de arquivo:
  - Sites web
  - Vídeos do YouTube
  - Arquivos PDF
  - Arquivos de texto (TXT)
  - Arquivos CSV
- Interface amigável com Streamlit
- Suporte a múltiplos modelos de linguagem:
  - Groq (llama-3.3-70b-versatile, meta-lhama/lhama-guarda-4-12B, gemma2-9b-it)
  - Google Gemini (gemini-1.5-flash, gemini-1.5-pro)
- Histórico de conversas
- Limpeza de histórico

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/morfeu.git
cd morfeu
```

2. Crie um ambiente virtual e ative-o:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 🔧 Configuração

1. Obtenha suas chaves de API:
   - [Groq API](https://console.groq.com/)
   - [Google Gemini API](https://ai.google.dev/)

2. Configure as chaves de API na interface do Morfeu

## 🎮 Uso

1. Inicie a aplicação:
```bash
streamlit run home_page.py
```

2. Na interface:
   - Selecione o tipo de arquivo que deseja processar
   - Faça upload do arquivo ou insira a URL
   - Escolha o provedor e modelo de linguagem
   - Inicialize o Morfeu
   - Comece a fazer perguntas!

## 📦 Estrutura do Projeto

```
morfeu/
├── home_page.py      # Interface principal
├── loaders.py        # Funções de carregamento de arquivos
├── requirements.txt  # Dependências do projeto
└── README.md         # Este arquivo
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.