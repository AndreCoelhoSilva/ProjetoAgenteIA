# pip install python-dotenv langchain langchain-openai langchain-community langchain-chroma chromadb openai pypdf
# Importações atualizadas conforme recomendações do LangChain
# main.py

from dotenv import load_dotenv                           # Carrega variáveis do .env (API Key da OpenAI, etc)
from langchain_community.vectorstores import Chroma     # Banco vetorial Chroma (de documentos)
from langchain_openai.embeddings import OpenAIEmbeddings  # Geração de embeddings com OpenAI
from langchain.prompts import ChatPromptTemplate         # Template para criar o prompt do chat
from langchain_openai import ChatOpenAI                  # Modelo de chat da OpenAI

import gc
gc.collect()  # Libera memória de execuções anteriores (ajuda com erro do Chroma às vezes)

# Carrega as variáveis do arquivo .env
load_dotenv()

# Caminho onde está o banco de vetores
CAMINHO_DB = "database"

# Template para construir o prompt com a pergunta e o conhecimento encontrado
prompt_template = """
Responda a pergunta do usuário:
{pergunta}

com base nessas informações: 

{base_conhecimento}

Se não for encontrada a resposta para a pergunta do usuário nessas informações, 
responda que não foram encontradas.
"""

def perguntar():
    # Entrada do usuário
    pergunta = input("Escreva sua pergunta: ")

    # Gera embeddings da pergunta usando OpenAI
    funcao_embedding = OpenAIEmbeddings()

    # Carrega o banco Chroma usando os embeddings
    db = Chroma(persist_directory=CAMINHO_DB, embedding_function=funcao_embedding)

    # Busca os textos mais parecidos com a pergunta
    resultados = db.similarity_search_with_relevance_scores(pergunta, k=3)

    # Se não encontrar nada relevante
    if len(resultados) == 0 or resultados[0][1] < 0.7:
        print("Não conseguiu encontrar alguma informação relevante na base")
        return

    # Junta os textos em um só bloco
    textos_resultado = [resultado[0].page_content for resultado in resultados]
    base_conhecimento = "\n\n----\n\n".join(textos_resultado)

    # Prepara o prompt com a pergunta + base de conhecimento
    prompt = ChatPromptTemplate.from_template(prompt_template)
    texto_prompt = prompt.format(pergunta=pergunta, base_conhecimento=base_conhecimento)

    # Inicializa o modelo da OpenAI
    modelo = ChatOpenAI()

    # Envia o prompt e recebe a resposta (método correto: invoke)
    resposta = modelo.invoke(texto_prompt)

    # Mostra a resposta da IA
    print("Resposta da IA:", resposta.content)

# Executa
perguntar()





         
    
