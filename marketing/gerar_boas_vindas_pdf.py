"""Script para atualizar e gerar o PDF de Boas-Vindas do AnthropoGuide."""
from pathlib import Path
import fitz

BASE_DIR = Path(__file__).resolve().parent
PDF_ORIGINAL = BASE_DIR / "AnthropoGuide_Boas_Vindas_v1_0.pdf"
FONT_PATH = Path(r"D:\ISAK_Filipe_Instrutor\referencias\MARCA FILIPE BRITO\Gotham-Font\Gotham-Font\GothamBook.ttf")


def atualizar_pdf(prazo_texto="1 ano", suporte_email="sizelab.academy@gmail.com"):
    doc = fitz.open(str(PDF_ORIGINAL))
    page = doc[0]

    # Carrega a fonte da marca
    font = fitz.Font(fontfile=str(FONT_PATH))

    # Áreas a redigir (limpar)
    rect_prazo = fitz.Rect(60, 650, 500, 666)
    rect_suporte = fitz.Rect(250, 764, 535, 776)

    page.add_redact_annot(rect_prazo, fill=(1, 1, 1))
    page.add_redact_annot(rect_suporte, fill=(1, 1, 1))
    page.apply_redactions()

    # Cor cinza oficial da marca (#5C5B5F)
    cor_cinza = (92 / 255, 91 / 255, 95 / 255)

    # Inserir linha 1 atualizada
    texto_prazo = f"O acesso é pessoal e intransferível, com validade de {prazo_texto} a contar da liberação."
    page.insert_text(
        fitz.Point(62.3622, 661.8898),
        texto_prazo,
        fontfile=str(FONT_PATH),
        fontsize=10.0,
        color=cor_cinza,
    )

    # Inserir linha 2 atualizada (alinhada à direita na margem 532.9134)
    texto_suporte = f"Suporte: {suporte_email}"
    t_len = font.text_length(texto_suporte, fontsize=9.0)
    x_suporte = 532.9134 - t_len

    page.insert_text(
        fitz.Point(x_suporte, 773.8583),
        texto_suporte,
        fontfile=str(FONT_PATH),
        fontsize=9.0,
        color=cor_cinza,
    )

    # Salva com overwrite
    doc.save(str(PDF_ORIGINAL), incremental=False, encryption=fitz.PDF_ENCRYPT_KEEP)
    print("PDF atualizado com sucesso!")


if __name__ == "__main__":
    atualizar_pdf()
