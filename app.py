from pathlib import Path
import hashlib
import google.generativeai as genai
from dotenv import load_dotenv
import csv
import streamlit as st
import os

# Instale o pacote usando: pip install google-generativeai
# ou instale diretamente no VS Code.


# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a chave de API do ambiente
api_key = os.getenv("API_KEY")

# Configuração da chave API
genai.configure(api_key=api_key)

# Configuração do modelo
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

# Configuração de segurança
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

# Instrução do sistema
system_instruction = "Você é um assistente conversacional e passa para o usuário informações sobre eventos que vão acontecer em Goiânia-GO. \nNa planilha de input existe informações sobre os eventos, passe as informações solicitadas para o usuário."

# Inicialização do modelo
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              #system_instruction=system_instruction,
                              safety_settings=safety_settings)


def extract_csv_rows(pathname: str) -> list[str]:
    rows = []
    with open(pathname, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for index, row in enumerate(csv_reader):
            rows.append(f"--- ROW {index} ---")
            rows.extend(row)
    return rows

# Configuração da aplicação Streamlit
st.title('Descubra eventos em Goiânia que são a sua cara!')

# Solicita a pergunta do usuário
user_question = st.text_input('O que você procura?')

# Botão para gerar resposta
if st.button('Enviar'):
    # Construir prompt_parts com a pergunta do usuário
    prompt_parts = [
        'Você é um assistente virtual e será procurado por várias pessoas para saber quais eventos aconteceram em Goiânia que mais combina com os gostos dessa pessoa. Retorne sempre, intusiasmado, os eventos que aconteceram de acordo com a lista de eventos disponibilizado e as demais informações contidas na lista',
        user_question,
        #*extract_csv_rows("C:\severina_criativa\poc_severina\eventos.csv")
        *extract_csv_rows(r"C:\severina_criativa\poc_severina\eventos.csv")
        #*extract_csv_rows("C:\\severina_criativa\\poc_severina\\eventos.csv")

    ]

    # Geração de conteúdo
    response = model.generate_content(prompt_parts)

    # Exibir resposta
    st.write('Resposta:')
    st.write(response.text)
