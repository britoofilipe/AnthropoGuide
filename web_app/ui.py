"""
Identidade visual FilipeBrito para o AnthropoGuide (Streamlit).
Cores, CSS, cabeçalhos, cartões de status e avatares — ver BC_MARCA_FILIPEBRITO.md.
"""

import base64
import io
from functools import lru_cache
from pathlib import Path

import streamlit as st
from PIL import Image, ImageDraw, ImageFont

ASSETS = Path(__file__).parent / "assets"
FAVICON = str(ASSETS / "favicon.png")
AVATAR_TUTOR = str(ASSETS / "avatar_tutor.png")

VERDE = "#7FB961"
TURQUESA = "#01978F"
MAGENTA = "#C40B7B"
AZUL = "#014393"
CINZA = "#5C5B5F"


@lru_cache(maxsize=None)
def _img_b64(nome: str) -> str:
    return base64.b64encode((ASSETS / nome).read_bytes()).decode()


CSS = f"""
<style>
:root {{
  --fb-verde: {VERDE}; --fb-turquesa: {TURQUESA}; --fb-magenta: {MAGENTA};
  --fb-azul: {AZUL}; --fb-cinza: {CINZA};
  --fb-gradiente: linear-gradient(120deg, {VERDE} 0%, {TURQUESA} 100%);
}}

/* Títulos: contraste de peso (Light + Bold), como na marca */
h1, h2, h3 {{ color: var(--fb-cinza); letter-spacing: -0.01em; }}

/* ---------- Login ---------- */
.fb-hero {{
  position: relative; overflow: hidden;
  background: var(--fb-gradiente);
  border-radius: 1rem; padding: 2.2rem 1.8rem 2rem;
  margin: 0.5rem 0 1.8rem; color: #fff;
}}
/* padrão pontilhado discreto no canto, longe do texto */
.fb-hero::after {{
  content: ""; position: absolute; right: -10px; bottom: -10px;
  width: 190px; height: 130px; opacity: 0.22; pointer-events: none;
  background-image: radial-gradient(#fff 1.6px, transparent 1.7px);
  background-size: 14px 14px;
  -webkit-mask-image: linear-gradient(135deg, transparent 20%, #000 90%);
          mask-image: linear-gradient(135deg, transparent 20%, #000 90%);
}}
.fb-hero img {{ height: 40px; width: auto; display: block; margin-bottom: 1.6rem; }}
.fb-hero .fb-produto {{
  font-family: "Montserrat", sans-serif; font-size: 2.1rem; line-height: 1.1;
  margin: 0; color: #fff;
}}
.fb-hero .fb-produto b {{ font-weight: 800; }}
.fb-hero .fb-produto span {{ font-weight: 300; }}
.fb-hero .fb-sub {{ margin: 0.6rem 0 0; font-size: 1.02rem; opacity: 0.95; }}
.fb-hero .fb-frase {{
  margin: 1.4rem 0 0; font-size: 0.85rem; letter-spacing: 0.04em; opacity: 0.85;
}}
.fb-autoria {{ text-align: center; font-size: 0.85rem; color: var(--fb-cinza); margin-top: 1.5rem; }}

/* ---------- Cabeçalho do chat ---------- */
.fb-header {{
  display: flex; align-items: center; gap: 0.9rem; flex-wrap: wrap;
  padding-bottom: 0.9rem; margin-bottom: 0.4rem;
  border-bottom: 3px solid transparent;
  border-image: var(--fb-gradiente) 1;
}}
.fb-header img {{ height: 34px; width: auto; }}
.fb-header .fb-sep {{ width: 1px; height: 28px; background: #D5DAD8; }}
.fb-header .fb-produto {{ font-family: "Montserrat", sans-serif; font-size: 1.25rem; color: var(--fb-cinza); }}
.fb-header .fb-produto b {{ font-weight: 800; }}
.fb-header .fb-produto span {{ font-weight: 300; }}
.fb-aviso {{ font-size: 0.82rem; color: var(--fb-cinza); margin: 0.5rem 0 1rem; }}
.fb-aviso b {{ font-weight: 600; }}

/* ---------- Cartão de status ---------- */
.fb-status {{
  background: #fff; border: 1px solid #DCE5E1; border-left: 5px solid var(--fb-cor);
  border-radius: 0.6rem; padding: 0.85rem 1rem; margin: 0.4rem 0 0.6rem;
}}
.fb-status .fb-rotulo {{
  font-family: "Montserrat", sans-serif; font-weight: 700; font-size: 0.78rem;
  text-transform: uppercase; letter-spacing: 0.06em; color: var(--fb-cor); margin: 0;
}}
.fb-status .fb-titulo {{ font-weight: 600; color: var(--fb-cinza); margin: 0.2rem 0 0.5rem; }}
.fb-status .fb-dias {{ font-family: "Montserrat", sans-serif; font-size: 1.9rem; font-weight: 800; color: var(--fb-cinza); line-height: 1; }}
.fb-status .fb-dias small {{ font-size: 0.8rem; font-weight: 600; color: var(--fb-cinza); }}
.fb-status .fb-ponto {{ color: var(--fb-magenta); }}
.fb-status .fb-data {{ font-size: 0.84rem; margin: 0.45rem 0 0; color: var(--fb-cinza); }}

/* ---------- Painel do instrutor ---------- */
.fb-selo {{
  display: inline-block; font-size: 0.78rem; font-weight: 600; padding: 0.2rem 0.6rem;
  border-radius: 999px; background: color-mix(in srgb, var(--fb-cor) 12%, #fff);
  color: var(--fb-cor); border: 1px solid color-mix(in srgb, var(--fb-cor) 35%, #fff);
}}
.fb-dias-admin {{ font-family: "Montserrat", sans-serif; font-weight: 800; font-size: 1.3rem; color: var(--fb-cinza); margin-top: 0.4rem; }}
.fb-dias-admin small {{ font-family: "Inter", sans-serif; font-weight: 400; font-size: 0.78rem; }}
</style>
"""

# Status do aluno → (cor, rótulo, título)
STATUS = {
    "acreditado": (TURQUESA, "Acreditado", "ISAK Nível 1 — acesso estendido"),
    "pos_curso": (VERDE, "Pós-curso", "Coleta dos 20 perfis"),
    "expirado": ("#B3261E", "Expirado", "Acesso encerrado"),
}


def aplicar_css() -> None:
    st.html(CSS)


def hero_login() -> None:
    st.html(f"""
    <div class="fb-hero">
      <img src="data:image/png;base64,{_img_b64('logo_horizontal_branca.png')}" alt="FilipeBrito">
      <p class="fb-produto"><span>Anthropo</span><b>Guide</b></p>
      <p class="fb-sub">Tutor de cineantropometria para alunos da certificação ISAK Nível 1</p>
      <p class="fb-frase">Transformando medidas em propósito</p>
    </div>
    """)


def autoria() -> None:
    st.html('<p class="fb-autoria">Coordenação: <b>Prof. Filipe Brito</b>, Instrutor Internacional ISAK Nível 3</p>')


def cabecalho_chat(aviso: bool = True) -> None:
    texto_aviso = """<p class="fb-aviso">Orientação didática sobre protocolo ISAK, qualidade da medida, equações e referências.
    <b>Não substitui a avaliação profissional nem emite laudos.</b> Descreva os casos sem dados que identifiquem o avaliado.</p>""" if aviso else ""
    st.html(f"""
    <div class="fb-header">
      <img src="data:image/png;base64,{_img_b64('logo_horizontal_colorida.png')}" alt="FilipeBrito">
      <div class="fb-sep"></div>
      <div class="fb-produto"><span>Anthropo</span><b>Guide</b></div>
    </div>
    {texto_aviso}
    """)


def cartao_status(status: str, dias: int, data_exp: str) -> None:
    cor, rotulo, titulo = STATUS.get(status, STATUS["pos_curso"])
    prazo = "Acesso válido até" if status == "acreditado" else "Prazo ISAKMetry até"
    st.html(f"""
    <div class="fb-status" style="--fb-cor:{cor}">
      <p class="fb-rotulo">{rotulo}</p>
      <p class="fb-titulo">{titulo}</p>
      <div class="fb-dias">{dias}<span class="fb-ponto">.</span> <small>dias restantes</small></div>
      <p class="fb-data">{prazo} <b>{data_exp}</b></p>
    </div>
    """)


def selo(status: str, texto: str) -> str:
    cor = STATUS.get(status, STATUS["pos_curso"])[0]
    return f'<span class="fb-selo" style="--fb-cor:{cor}">{texto}</span>'


@lru_cache(maxsize=256)
def _avatar_iniciais_png(iniciais: str) -> bytes:
    s = 256
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((0, 0, s - 1, s - 1), fill=(0xE4, 0xE6, 0xE5, 255))
    fonte = ImageFont.truetype(str(ASSETS / "fonts" / "Montserrat-SemiBold.ttf"), int(s * 0.38))
    d.text((s / 2, s / 2), iniciais, font=fonte, fill=CINZA, anchor="mm")
    buf = io.BytesIO()
    im.save(buf, format="PNG")
    return buf.getvalue()


def avatar_usuario(nome: str) -> Image.Image:
    """Iniciais do usuário em círculo cinza (primeiro e último nome)."""
    partes = [p for p in nome.replace("Prof.", "").split() if p[:1].isalpha()]
    iniciais = (partes[0][0] + (partes[-1][0] if len(partes) > 1 else "")).upper() if partes else "?"
    return Image.open(io.BytesIO(_avatar_iniciais_png(iniciais)))
