"""
Módulo de Integração com a API do Google Gemini — AnthropoGuide
Carrega o System Prompt v2.4 blindado e os 8 módulos da Base de Conhecimento.
"""

import os
from pathlib import Path
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SYSTEM_PROMPT_PATH = BASE_DIR / "SYSTEM_PROMPT_ANTHROPOGUIDE.md"
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"

def load_system_context() -> str:
    """Carrega o System Prompt v2.4 e concatena os 8 módulos da Base de Conhecimento."""
    system_text = ""
    if SYSTEM_PROMPT_PATH.exists():
        system_text += SYSTEM_PROMPT_PATH.read_text(encoding="utf-8") + "\n\n"
        
    system_text += "# BASE DE CONHECIMENTO CIENTÍFICA E PROTOCOLAR OFICIAL (ISAK N1)\n\n"
    
    if KNOWLEDGE_BASE_DIR.exists():
        modules = sorted(list(KNOWLEDGE_BASE_DIR.glob("*.md")))
        for mod in modules:
            system_text += f"## MÓDULO: {mod.name}\n"
            system_text += mod.read_text(encoding="utf-8") + "\n\n---\n\n"
            
    return system_text

class AnthropoGuideBot:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.system_instruction = load_system_context()
        self.client = None
        self.chat = None
        
        if self.api_key:
            try:
                from google import genai
                from google.genai import types
                self.client = genai.Client(api_key=self.api_key)
                self.chat = self.client.chats.create(
                    model="gemini-3.6-flash",
                    config=types.GenerateContentConfig(
                        system_instruction=self.system_instruction,
                        temperature=0.3,
                    )
                )
            except Exception as e:
                print(f"[AnthropoGuide] Erro ao inicializar cliente Gemini: {e}")

    def send_message(self, message: str) -> str:
        if not self.api_key:
            return (
                "**Chave de API do Gemini não configurada!**\n\n"
                "Por favor, configure a variável `GEMINI_API_KEY` no arquivo `.env` ou insira a chave no painel administrativo."
            )
        if not self.chat:
            return (
                "**Erro na inicialização da IA.**\n\n"
                "Verifique se o pacote `google-genai` está instalado e se sua chave é válida."
            )
            
        try:
            response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            return f"Erro na comunicação com a IA: {str(e)}"
