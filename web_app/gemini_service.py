"""
Módulo de Integração com a API do Google Gemini — AnthropoGuide
Carrega o System Prompt v2.4 blindado e os 8 módulos da Base de Conhecimento.
Inclui retentativas automáticas (retry) e tolerância a falhas (fallback) contra erros 503 temporários da API.
"""

import os
import time
from pathlib import Path
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SYSTEM_PROMPT_PATH = BASE_DIR / "SYSTEM_PROMPT_ANTHROPOGUIDE.md"
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"

# Lista de modelos por ordem de estabilidade e capacidade comprovada
PRIMARY_MODEL = "gemini-flash-latest"
FALLBACK_MODELS = ["gemini-3.5-flash", "gemini-3.7-flash", "gemini-3.1-flash-lite", "gemini-3.6-flash"]

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
        self.current_model = PRIMARY_MODEL
        self.chat = None
        self._init_client(self.current_model)

    def _init_client(self, model_name: str = PRIMARY_MODEL):
        if self.api_key:
            try:
                from google import genai
                from google.genai import types
                self.client = genai.Client(api_key=self.api_key)
                self.current_model = model_name
                self.chat = self.client.chats.create(
                    model=model_name,
                    config=types.GenerateContentConfig(
                        system_instruction=self.system_instruction,
                        temperature=0.3,
                    )
                )
            except Exception as e:
                print(f"[AnthropoGuide] Erro ao inicializar cliente Gemini ({model_name}): {e}")

    def send_message(self, message: str) -> str:
        if not self.api_key:
            return (
                "Chave de API do Gemini não configurada!\n\n"
                "Por favor, configure a variável `GEMINI_API_KEY` no arquivo `.env` ou insira a chave no painel administrativo."
            )
        if not self.client or not self.chat:
            self._init_client(self.current_model)
            if not self.client:
                return "Erro na inicialização da IA. Verifique se o pacote `google-genai` está instalado e se sua chave é válida."

        # Lista ordenada de modelos para tentar (começando pelo atual e depois os alternativos)
        modelos_para_tentar = [self.current_model] + [m for m in FALLBACK_MODELS if m != self.current_model]
        
        for modelo in modelos_para_tentar:
            # Se precisou trocar de modelo devido a instabilidade anterior, reinicializa o chat
            if modelo != self.current_model:
                self._init_client(modelo)

            for tentativa in range(3):
                try:
                    response = self.chat.send_message(message)
                    if response and response.text:
                        self.current_model = modelo
                        return response.text
                except Exception as e:
                    erro_str = str(e).lower()
                    # Se for erro 503 (serviço sobrecarregado momentaneamente) ou 429 (rate limit temporário)
                    if "503" in erro_str or "unavailable" in erro_str or "high demand" in erro_str or "429" in erro_str:
                        # Aguarda breve pausa e retenta
                        time.sleep(1.2 * (tentativa + 1))
                        continue
                    elif "404" in erro_str or "not found" in erro_str:
                        # Modelo indisponível, pula para o próximo da lista de fallback
                        break
                    else:
                        # Erro genérico
                        return f"Erro na comunicação com a IA: {str(e)}"

        return (
            "Os servidores do Google estão temporariamente com alta demanda. "
            "Por favor, tente reenviar sua pergunta em alguns instantes."
        )
