import sys
from gemini_service import AnthropoGuideBot

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

print("Inicializando AnthropoGuideBot com o modelo gemini-3.6-flash...")
bot = AnthropoGuideBot()

pergunta = "Qual o prazo do envio dos 20 sujeitos pós-curso no ISAKMetry e qual o limite de ETM para dobras?"
print(f"Pergunta: {pergunta}\n")

resposta = bot.send_message(pergunta)
print("Resposta do AnthropoGuide:")
print(resposta)
