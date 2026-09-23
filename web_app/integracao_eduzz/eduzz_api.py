"""Cliente da API pública da Eduzz — apenas leitura de vendas."""
import datetime
import time
import requests

BASE = "https://api.eduzz.com/myeduzz/v1/sales"
PAUSA_ENTRE_PAGINAS = 2.1  # limite documentado: 30 requisições por minuto


def listar_vendas(token, product_id, inicio, fim, status):
    vendas, pagina, total_paginas = [], 1, 1
    while pagina <= total_paginas:
        resposta = requests.get(
            BASE,
            headers={"authorization": f"bearer {token}", "content-type": "application/json"},
            params={
                "startDate": inicio.isoformat(),
                "endDate": fim.isoformat(),
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
