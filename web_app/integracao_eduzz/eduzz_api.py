"""Cliente da API pública da Eduzz — apenas leitura de vendas."""
import datetime
import time
import requests

BASE = "https://api.eduzz.com/myeduzz/v1/sales"
PAUSA_ENTRE_PAGINAS = 2.1  # limite documentado: 30 requisições por minuto


def listar_vendas(token: str, product_id: int, inicio: datetime.date, fim: datetime.date, status: str) -> list[dict]:
    """Lista vendas da API Eduzz com paginação automática.

    Retorna todos os objetos 'items' de todas as páginas concatenados em uma lista.
    Pausa entre requisições para respeitar limite de rate-limit.

    Args:
        token: Token de autenticação da API Eduzz
        product_id: ID do produto a filtrar
        inicio: Data inicial do período (inclusiva)
        fim: Data final do período (inclusiva)
        status: Status da venda ('paid', 'refunded', etc.)

    Returns:
        Lista de dicionários com os dados das vendas
    """
    vendas, pagina, total_paginas = [], 1, 1
    while pagina <= total_paginas:
        resposta = requests.get(
            BASE,
            headers={"authorization": f"bearer {token}"},
            params={
                "startDate": inicio.isoformat(),
                "endDate": fim.isoformat(),
                # Para vendas pagas, usa data do pagamento; para reembolso/cancelamento,
                # usa data da última atualização (quando o status mudou).
                "referenceDate": "paidAt" if status == "paid" else "updatedAt",
                "productId": product_id,
                "status": status,
                "page": pagina,
                "itemsPerPage": 100,
            },
            timeout=30,
        )
        resposta.raise_for_status()
        dados = resposta.json()
        vendas.extend(dados.get("items", []))
        total_paginas = dados.get("pages", 1)
        pagina += 1
        if pagina <= total_paginas:
            time.sleep(PAUSA_ENTRE_PAGINAS)
    return vendas
