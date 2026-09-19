import os
import sys
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"Chave carregada: {api_key[:6]}...{api_key[-4:] if api_key else 'None'}")

try:
    from google import genai
    client = genai.Client(api_key=api_key)
    print("Tentando chamada de teste ao modelo gemini-2.5-flash ou gemini-2.0-flash...")
    
    for m in ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-3.6-flash"]:
        try:
            print(f"Testando modelo: {m}...")
            response = client.models.generate_content(
                model=m,
                contents="Responda apenas: 'AnthropoGuide online!'"
            )
            print(f"Sucesso com {m}: {response.text}")
            break
        except Exception as err:
            print(f"Falha com {m}: {err}")
except Exception as e:
    print(f"Erro no teste: {e}")
