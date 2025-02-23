from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from transformers import pipeline
from typing import List, Tuple
import uvicorn

app = FastAPI(
    title="Clinical NER BIO API",
    description="API for clinical named entity recognition in BIO format",
    version="1.0.0"
)

# Configurar templates
templates = Jinja2Templates(directory="templates")

# Inicializar el modelo globalmente
pipe = pipeline("token-classification",
                model="anvorja/xlm-roberta-large-clinical-ner-breast-cancer-sp")

def convert_to_bio_format(texto, pipe):
    """
    Convierte la salida del pipeline de NER a formato BIO, reconstruyendo palabras completas
    y preservando todas las palabras del texto original
    """
    # Obtener predicciones
    resultados = pipe(texto)

    # Dividir el texto original en palabras manteniendo la puntuación
    palabras_originales = []
    palabra_actual = ""
    for char in texto:
        if char.isspace():
            if palabra_actual:
                palabras_originales.append(palabra_actual)
                palabra_actual = ""
        elif char in ".,;:!?":
            if palabra_actual:
                palabras_originales.append(palabra_actual)
            palabras_originales.append(char)
            palabra_actual = ""
        else:
            palabra_actual += char
    if palabra_actual:
        palabras_originales.append(palabra_actual)

    # Reconstruir palabras etiquetadas del pipeline
    palabras_etiquetadas = {}
    palabra_actual = ""
    tag_actual = None

    for resultado in resultados:
        token = resultado['word'].replace('▁', ' ').strip()
        tag = resultado['entity']

        if token.startswith(' '):
            token = token[1:]

        if '▁' in resultado['word'] and palabra_actual:
            if palabra_actual:
                palabra_limpia = palabra_actual.strip().lower()
                palabras_etiquetadas[palabra_limpia] = tag_actual
            palabra_actual = token
            tag_actual = tag
        else:
            palabra_actual += token
            tag_actual = tag

    if palabra_actual:
        palabra_limpia = palabra_actual.strip().lower()
        palabras_etiquetadas[palabra_limpia] = tag_actual

    # Crear la salida final en formato BIO
    bio_tokens = []
    for palabra in palabras_originales:
        if palabra.strip():
            if palabra in ".,;:!?":
                bio_tokens.append((palabra, 'O'))
            else:
                # Buscar la etiqueta correspondiente
                palabra_lower = palabra.lower()
                tag = palabras_etiquetadas.get(palabra_lower, 'O')
                bio_tokens.append((palabra, tag))

    return bio_tokens

# Modelos Pydantic para la API
class TextInput(BaseModel):
    text: str

class TokenTag(BaseModel):
    token: str
    tag: str

class BIOOutput(BaseModel):
    bio_format: List[TokenTag]
    original_text: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/get_bio", response_model=BIOOutput)
async def get_bio_format(input_data: TextInput):
    try:
        # Obtener el formato BIO
        bio_results = convert_to_bio_format(input_data.text, pipe)
        
        # Convertir los resultados al formato de salida
        formatted_results = [
            TokenTag(token=token, tag=tag)
            for token, tag in bio_results
        ]
        
        return BIOOutput(
            bio_format=formatted_results,
            original_text=input_data.text
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": "anvorja/xlm-roberta-large-clinical-ner-breast-cancer-sp"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
