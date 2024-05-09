from pathlib import Path
import hashlib
import google.generativeai as genai

genai.configure(api_key="AIzaSyBcb_FFOKNi-hUfkI5zvN1g5uF7HAkpXq8")

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

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

system_instruction = "Você é um assistente conversacional e passa para o usuário informações sobre eventos que vão acontecer em Goiânia-GO. \nNa planilha de input existe informações sobre os eventos, passe as informações solicitadas para o usuário."

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              system_instruction=system_instruction,
                              safety_settings=safety_settings)

def extract_pdf_pages(pathname: str) -> list[str]:
  parts = [f"--- START OF PDF ${pathname} ---"]
  # Add logic to read the PDF and return a list of pages here.
  pages = []
  for index, page in enumerate(pages):
    parts.append(f"--- PAGE {index} ---")
    parts.append(page)
  return parts

prompt_parts = [
  *extract_pdf_pages("<path>/document0.pdf"),
  "Olá, gostaria de saber quais eventos de música clássica aconteceram em Goiânia neste final de semana?",
]

response = model.generate_content(prompt_parts)
print(response.text)