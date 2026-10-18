from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI(title="MenuMitra AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranslationRequest(BaseModel):
    restaurant: str
    menu: list
    language: str = "Marathi"

@app.get("/")
def home():
    return {"message": "MenuMitra AI API is running!"}

@app.post("/translate")
def translate_menu(data: TranslationRequest):
    prompt = (
        f"Translate this restaurant menu into {data.language}. "
        f"Keep dish prices unchanged. Menu: {data.menu}"
    )

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma3:4b",
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
    )
    response.raise_for_status()

    return {"translation": response.json()["response"]}

