
import streamlit as st
import pandas as pd
import joblib
import os

# Cargar modelo y encoder
modelo = joblib.load("modelo_regresion_logistica.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# Configurar estilo y página
st.set_page_config(page_title="Recomendador de Seguros", layout="centered")
st.markdown("""
    <style>
        .stApp {
            background-color: #cce6ff;
        }
        h1, h3 {
            color: #003366 !important;
        }
        .titulo-principal {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-top: 20px;
        }
        .titulo-principal img {
            width: 40px;
            height: 40px;
        }
        .tarjeta-imagen {
            width: 80px;
            height: 80px;
            margin-bottom: 5px;
        }
        .stButton > button {
            background-color: #003366;
            color: white;
            font-size: 16px;
            font-weight: bold;
            padding: 12px;
            border-radius: 12px;
            width: 100%;
            height: 60px;
        }
        .stButton > button:hover {
            background-color: #005bbb;
        }
        .stProgress > div > div > div > div {
            background-color: #005bbb;
        }
    </style>
""", unsafe_allow_html=True)

# Título con ícono
st.markdown("""
    <div class="titulo-principal">
        <img src="https://cdn-icons-png.flaticon.com/512/942/942748.png" />
        <h1>Encuentra tu seguro ideal</h1>
    </div>
""", unsafe_allow_html=True)

# Estado
if "indice" not in st.session_state:
    st.session_state.indice = 0
    st.session_state.respuestas = {}

PREGUNTAS = [
    ("edad", "Selecciona tu rango de edad:", ["18-21", "22-25", "26-29", "30-33", "34-37", "38-41", "42-45", "46-49", "50-53", "54-57", "58-61", "62-65", "66-70"]),
    ("genero", "Selecciona tu género:", ["Masculino", "Femenino"]),
    ("nivel_educativo", "¿Cuál es tu nivel educativo?", ["Bachiller", "Técnico", "Tecnólogo", "Profesional", "Postgrado"]),
    ("ocupacion", "¿Cuál es tu ocupación actual?", ["Empleado", "Independiente", "Desempleado", "Estudiante", "Pensionado"]),
    ("tiene_hijos", "¿Tienes hijos?", ["Sí", "No"]),
]

indice = st.session_state.indice

if indice < len(PREGUNTAS):
    clave, pregunta, opciones = PREGUNTAS[indice]
    st.markdown(f"### {pregunta}")
    cols = st.columns(len(opciones))
    for i, op in enumerate(opciones):
        with cols[i]:
            ruta = f"static/icon_{op.lower().replace(' ', '_')}.png"
            if os.path.exists(ruta):
                st.image(ruta, use_container_width=True)
            if st.button(op, key=f"{clave}_{op}"):
                st.session_state.respuestas[clave] = op
                st.session_state.indice += 1
                st.rerun()

    st.progress(indice / len(PREGUNTAS))

else:
    respuestas = st.session_state.respuestas
    if "edad" in respuestas:
        try:
            ini, fin = map(int, respuestas["edad"].split("-"))
            respuestas["edad"] = (ini + fin) // 2
        except:
            respuestas["edad"] = 30

    mapa_ingresos = {
        "<1M": 500_000, "1-2M": 1_500_000, "2-4M": 3_000_000,
        "4-6M": 5_000_000, "6-8M": 7_000_000, "8-10M": 9_000_000, ">10M": 12_000_000
    }
    if "ingresos_mensuales" in respuestas:
        respuestas["ingresos_mensuales"] = mapa_ingresos.get(respuestas["ingresos_mensuales"], 3_000_000)

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
