import streamlit as st
import pandas as pd
import io
from reportlab.platypus import Table, TableStyle

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

st.set_page_config(
    page_title="Concreto Têxtil",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    background-color: #0B3D91;
}

h1, h2, h3, h4, h5, h6, p {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

.stButton>button {
    width: 100%;
    background-color: white;
    color: black;
}

</style>
""", unsafe_allow_html=True)
# ======================================================
# CONFIGURAÇÃO DA PÁGINA
# ======================================================

st.set_page_config(page_title="Reforço com Concreto Têxtil", layout="wide")

# Fundo azul
st.markdown("""
<style>
.main {
    background-color: #0B3D91;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# CABEÇALHO PROFISSIONAL
# ======================================================
st.markdown("""
<div style="text-align:center; color:white;">

<h1 style="margin-bottom:0;">
Cálculo de Reforço com Concreto Têxtil
</h1>

<p style="margin-top:5px;">
Universidade Federal de Sergipe<br>
Departamento de Engenharia Civil
</p>

</div>
""", unsafe_allow_html=True)

# ======================================================
# CABEÇALHO
# ======================================================
st.write("Discente: Agatha Ferreira Oliveira")
st.write("Orientador: Profº Dr. Emerson Figueiredo dos Santos")

st.divider()

# ======================================================
# DADOS DE ENTRADA
# ======================================================

st.header("Dados da Viga")

bw = st.number_input("Largura bw (cm)")
h = st.number_input("Altura h (cm)")
d = st.number_input("Altura útil d (cm)")
dc = st.number_input("Altura útil da armadura comprimida dc (cm)")
As = st.number_input("Área de aço tracionado As (cm²)")
Asc = st.number_input("Área de aço comprimido Asc (cm²)")
Ms = st.number_input("Momento resistente necessário Ms (kN.cm)")

st.subheader("Propriedades Mecânicas")

Ec = st.number_input("Módulo de elasticidade do concreto (GPa)")
Es = st.number_input("Módulo de elasticidade do aço (GPa)")
fy = st.number_input("Tensão de escoamento aço tracionado (MPa)")
fyc = st.number_input("Tensão aço comprimido (MPa)")
fck = st.number_input("fck do concreto (MPa)")

st.divider()

# ======================================================
# TIPO DE MÉTODO E TÊXTIL
# ======================================================

metodo = st.selectbox("Escolha o Método", ["Trintin", "Beeber", "Comparar os dois"])

op_textil = st.selectbox("Tipo de têxtil", ["Armo-mesh L500", "AF-0200 BR"])

if op_textil == "Armo-mesh L500":
    if metodo == "Trintin":
        Ef, Af1, ff, ea, et = 240, 0.0105, 800, 0.3, 0.0105
    else:
        Ef, Af1, ff, ea, et = 240000, 0.0105, 4300, 0.3, 0.0105
    nome = "Armo-mesh L500"

elif op_textil == "AF-0200 BR":
    if metodo == "Trintin":
        Ef, Af1, ff, ea, et = 70, 0.0033, 220, 0.2, 0.05
    else:
        Ef, Af1, ff, ea, et = 70000, 0.003269, 1000, 0.2, 0.05
    nome = "AF-0200 BR"

else:
    nome = st.text_input("Nome do têxtil")
    Ef = st.number_input("Ef")
    Af1 = st.number_input("Af1")
    ff = st.number_input("Tensão do têxtil ff")
    ea = st.number_input("Espessura argamassa ea")
    et = st.number_input("Espessura têxtil et")

st.divider()

def gerar_pdf_tcc(titulo, subtitulo, df_resultados):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=A4)

    style_titulo = ParagraphStyle(
        name="Titulo",
        fontSize=18,
        alignment=1,
        spaceAfter=15
    )

    style_sub = ParagraphStyle(
        name="Sub",
        fontSize=12,
        alignment=1,
        spaceAfter=8
    )

    style_normal = ParagraphStyle(
        name="Normal",
        fontSize=11,
        spaceAfter=8
    )

    elements = []

    # =========================
    # CAPA
    # =========================

    elements.append(Paragraph(titulo, style_titulo))
    elements.append(Paragraph(subtitulo, style_sub))

    elements.append(Spacer(1, 1*cm))

    elements.append(Paragraph(
        "Discente: Agatha Ferreira Oliveira",
        style_normal
    ))

    elements.append(Paragraph(
        "Orientador: Profº Dr. Emerson Figueiredo dos Santos",
        style_normal
    ))

    elements.append(Spacer(1, 1*cm))

    # =========================
    # RESULTADOS
    # =========================

    if df_resultados is not None:

        tabela = [df_resultados.columns.tolist()] + df_resultados.astype(str).values.tolist()

        table = Table(tabela)

        table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.grey),
            ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("GRID", (0,0), (-1,-1), 1, colors.black),
            ("FONT", (0,0), (-1,-1), "Helvetica", 10)
        ]))

        elements.append(table)

    doc.build(elements)

    buffer.seek(0)

    return buffer

# ======================================================
# BOTÃO CALCULAR
# ======================================================

if st.button("Calcular"):

    try:

        from calculos_web import metodo_trintin_web, metodo_beeber_web

        if metodo == "Trintin":

            resultado = metodo_trintin_web(bw, h, d, dc, As, Asc, Ms,Ec, Es, fy, fyc, fck,Ef, Af1, ff, ea, et, nome)

            st.success("Resultado - Trintin")

            st.metric("Linha neutra (x)", f"{resultado['x']:.3f} cm")
            st.metric("Momento resistente", f"{resultado['Mr']:.3f} kN.cm")
            st.metric("Camadas", resultado["camadas"])

            linhas_pdf = [
                "Método: Trintin",
                f"Linha neutra (x): {resultado['x']:.3f} cm",
                f"Momento resistente: {resultado['Mr']:.3f} kN.cm",
                f"Camadas: {resultado['camadas']}"
            ]

            pdf = gerar_pdf_tcc(
                "Cálculo de Reforço com Concreto Têxtil",
                "Universidade Federal de Sergipe",
                pd.DataFrame({"Resultados": linhas_pdf})
            )

            st.download_button(
                "📄 Exportar PDF",
                data=pdf,
                file_name="trintin.pdf",
                mime="application/pdf"
            )


        elif metodo == "Beeber":

            resultado = metodo_beeber_web(
                bw, h, d, dc, As, Asc, Ms,
                Ec, Es, fy, fyc, fck,
                Ef, Af1, ff, ea, et, nome
            )

            st.success("Resultado - Beeber")

            st.metric("Linha neutra (x)", f"{resultado['x']:.3f} cm")
            st.metric("Momento resistente", f"{resultado['Mu']:.3f} kN.cm")
            f"Camadas: {resultado['camadas']}"

            linhas_pdf = [
                "Método: Beeber",
                f"Linha neutra (x): {resultado['x']:.3f} cm",
                f"Momento resistente: {resultado['Mu']:.3f} kN.cm",
                f"Camadas: {resultado['camadas']}"
            ]

            linhas_pdf = [
                "Método: Beeber",
                f"Linha neutra (x): {resultado['x']:.3f} cm",
                f"Momento resistente: {resultado['Mu']:.3f} kN.cm",
                f"Camadas: {resultado['camadas']}"
            ]

            pdf = gerar_pdf_tcc(
                "Cálculo de Reforço com Concreto Têxtil",
                "Universidade Federal de Sergipe",
                pd.DataFrame({"Resultados": linhas_pdf})
            )

            st.download_button(
                "📄 Exportar PDF",
                data=pdf,
                file_name="beeber.pdf",
                mime="application/pdf"
            )



        else:

            res_t = metodo_trintin_web(
                bw, h, d, dc, As, Asc, Ms,
                Ec, Es, fy, fyc, fck,
                Ef, Af1, ff, ea, et, nome
            )

            res_b = metodo_beeber_web(
                bw, h, d, dc, As, Asc, Ms,
                Ec, Es, fy, fyc, fck,
                Ef, Af1, ff, ea, et, nome
            )

            df = pd.DataFrame({
                "Parâmetro": ["Linha neutra", "Momento", "Camadas"],
                "Trintin": [res_t["x"], res_t["Mr"], res_t["camadas"]],
                "Beeber": [res_b["x"], res_b["Mu"], res_b["camadas"]]
            })

            st.subheader("Comparação")
            st.dataframe(df, use_container_width=True, hide_index=True)

            pdf = gerar_pdf_tcc(
                "Comparação entre Métodos",
                "Universidade Federal de Sergipe",
                df
            )

            st.download_button(
                "📄 Exportar PDF",
                data=pdf,
                file_name="comparacao.pdf",
                mime="application/pdf"
            )


    except Exception as e:
        st.error(str(e))

# ======================================================

st.markdown("""
<hr>
<p style='text-align:center;color:white;'>
Desenvolvido por Agatha Ferreira Oliveira
<br>
Orientador: Profº Dr. Emerson Figueiredo dos Santos
</p>
""", unsafe_allow_html=True)