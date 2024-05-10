from pathlib import Path
import hashlib
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Use the API key from the .env file
api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api_key)

# Set up the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

system_instruction = ("Você é um assistente conversacional e passa para o usuário informações sobre eventos que vão acontecer em Goiânia-GO. "
                      "Na planilha de input existem informações sobre os eventos, passe as informações solicitadas para o usuário.")

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              system_instruction=system_instruction,
                              safety_settings=safety_settings)

def extract_pdf_pages(pathname: str) -> list[str]:
    parts = [f"--- START OF PDF {pathname} ---"]
    # Add logic to read the PDF and return a list of pages here.
    pages = []
    for index, page in enumerate(pages):
        parts.append(f"--- PAGE {index} ---")
        parts.append(page)
    return parts

# Streamlit user interface
st.title("Consulta de Eventos em Goiânia")
uploaded_file = st.file_uploader("Carregue o PDF com as informações dos eventos")

if uploaded_file is not None:
    path = uploaded_file.name
    prompt_parts = extract_pdf_pages(path)
    prompt_parts.append(st.text_input("Digite sua pergunta sobre os eventos:"))
    if st.button("Gerar Resposta"):
        response = model.generate_content(prompt_parts)
        st.write(response.text)
