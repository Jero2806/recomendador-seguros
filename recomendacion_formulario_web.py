import streamlit as st
import pandas as pd
import joblib
from PIL import Image
import os

# Cargar modelo y encoder
modelo = joblib.load("modelo_regresion_logistica.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# Preguntas
PREGUNTAS = [
    ("tiene_hijos", "¿Tienes hijos?", ["Sí", "No"]),
    ("vive_con_familia", "¿Vives con tu familia?", ["Sí", "No"]),
    ("responsable_otros", "¿Eres responsable de otros familiares?", ["Sí", "No"]),
    # Agrega las demás preguntas...
]

# Configurar página
st.set_page_config(page_title="Recomendador de Seguros", layout="centered")
st.markdown(
    """
    <style>
        .stApp {
            background-color: #cce6ff;
        }
        h1 {
            color: #003366;
            font-weight: 800;
        }
        h3 {
            color: #003366;
        }
        .tarjeta-opcion {
            border: 2px solid #003366;
            border-radius: 12px;
            background-color: white;
            padding: 10px;
            text-align: center;
            cursor: pointer;
            transition: 0.2s;
        }
        .tarjeta-opcion:hover {
            background-color: #e6f0ff;
        }
        .tarjeta-imagen {
            width: 50px;
            height: auto;
            margin-bottom: 5px;
        }
        .stProgress > div > div > div > div {
            background-color: #005bbb;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🛡️ Encuentra tu seguro ideal")

# Inicializar estado
if "indice" not in st.session_state:
    st.session_state.indice = 0
    st.session_state.respuestas = {}

indice = st.session_state.indice

if indice < len(PREGUNTAS):
    clave, pregunta, opciones = PREGUNTAS[indice]
    st.markdown(f"### {pregunta}")

    MAX_COLS = 5
    filas = [opciones[i:i + MAX_COLS] for i in range(0, len(opciones), MAX_COLS)]

    for fila in filas:
        cols = st.columns(len(fila))
        for i, op in enumerate(fila):
            with cols[i]:
                boton_html = f"""
                <div class="tarjeta-opcion" onclick="document.getElementById('{clave}_{op}').click()">
                    <img src="app/static/icon_{op.lower().replace(' ', '_')}.png" class="tarjeta-imagen" onerror="this.style.display='none';"/>
                    <div>{op}</div>
                </div>
                """
                clicked = st.button(op, key=f"{clave}_{op}", help=op)
                st.markdown(boton_html, unsafe_allow_html=True)
                if clicked:
                    st.session_state.respuestas[clave] = op
                    st.session_state.indice += 1
                    st.rerun()

    st.progress(indice / len(PREGUNTAS))

else:
    # Resultado final
    respuestas = st.session_state.respuestas
    df_usuario = pd.DataFrame([respuestas])

    try:
        pred = modelo.predict(df_usuario)
        resultado = label_encoder.inverse_transform(pred)[0]
        st.success(f"✅ Seguro recomendado: **{resultado}**")
    except Exception as e:
        st.error(f"❌ Error en la predicción: {e}")

    if st.button("🔁 Volver a comenzar"):
        st.session_state.indice = 0
        st.session_state.respuestas = {}
        st.rerun()
