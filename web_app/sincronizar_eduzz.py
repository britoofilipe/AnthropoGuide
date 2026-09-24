"""Sincroniza vendas da Eduzz com os acessos do AnthropoGuide (tarefa agendada)."""
import datetime
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

import auth
from integracao_eduzz import eduzz_api, email_envio, liberacao

BASE = Path(__file__).resolve().parent
logging.basicConfig(
    filename=BASE / "sincronizacao_eduzz.log",
    level=logging.INFO,
    encoding="utf-8",
    format="%(asctime)s %(levelname)s %(message)s",
)


def sincronizar(config: dict, enviar_email) -> dict:
    hoje = datetime.date.today()
    inicio = hoje - datetime.timedelta(days=config["dias_janela"])
    resultado = {"liberados": 0, "bloqueados": 0, "erros": []}

    for venda in eduzz_api.listar_vendas(
        config["token"], config["product_id"], inicio, hoje, "paid"
    ):
        try:
            novo = liberacao.liberar(venda, config["prazo_dias"])
            if novo is None:
                continue
            enviar_email({**novo, "validade": novo["validade"].strftime("%d/%m/%Y")})
            resultado["liberados"] += 1
            logging.info("Acesso liberado para a venda %s", venda.get("id"))
        except Exception as erro:
            resultado["erros"].append(f"venda {venda.get('id')}: {erro}")
            logging.exception("Falha ao liberar a venda %s", venda.get("id"))

    for status in ("refunded", "canceled"):
        for venda in eduzz_api.listar_vendas(
            config["token"], config["product_id"], inicio, hoje, status
        ):
            try:
                if liberacao.bloquear(venda):
                    resultado["bloqueados"] += 1
                    logging.info("Acesso bloqueado para a venda %s", venda.get("id"))
            except Exception as erro:
                resultado["erros"].append(f"venda {venda.get('id')}: {erro}")
                logging.exception("Falha ao bloquear a venda %s", venda.get("id"))

    return resultado


def main() -> int:
    load_dotenv(BASE / ".env")
    auth.init_db()
    config = {
        "token": os.environ["EDUZZ_TOKEN"],
        "product_id": int(os.environ["EDUZZ_PRODUCT_ID"]),
        "prazo_dias": int(os.environ["PRAZO_ACESSO_DIAS"]),
        "url_plataforma": os.environ["URL_PLATAFORMA"],
        "dias_janela": int(os.getenv("EDUZZ_DIAS_JANELA", "3")),
    }

    def enviar(dados):
        email_envio.enviar(
            email_envio.montar(dados, config["url_plataforma"], os.environ["EMAIL_REMETENTE"]),
            os.environ["SMTP_HOST"],
            int(os.environ["SMTP_PORT"]),
            os.environ["SMTP_USUARIO"],
            os.environ["SMTP_SENHA"],
        )

    resultado = sincronizar(config, enviar)
    logging.info("Resumo: %s", resultado)
    print(resultado)
    return 1 if resultado["erros"] else 0


if __name__ == "__main__":
    sys.exit(main())
