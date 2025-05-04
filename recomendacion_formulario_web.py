from pathlib import Path
import streamlit as st
import pandas as pd
import joblib
import os
import base64

# ---------------- CONFIGURACIÓN GENERAL ----------------

st.set_page_config(page_title="Recomendador de Seguros", layout="centered")

# Estilo CSS
st.markdown("""
    <style>
        .stApp {
            background-color: #cce6ff;
        }
        h1, h3 {
            color: #003366 !important;
        }
        .tarjeta {
            border: 2px solid #003366;
            border-radius: 12px;
            padding: 10px;
            background-color: white;
            text-align: center;
            transition: 0.2s;
            cursor: pointer;
        }
        .tarjeta:hover {
            background-color: #e6f0ff;
        }
        .tarjeta img {
            width: 80px;
            height: auto;
            margin-bottom: 8px;
        }
        .tarjeta-texto {
            font-size: 18px;
            font-weight: bold;
            color: #003366;
        }
        .titulo-principal {
            font-size: 32px;
            font-weight: bold;
            color: #003366;
            text-align: center;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------- CARGAR MODELOS ----------------

modelo = joblib.load("modelo_regresion_logistica.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# ---------------- UTILIDADES ----------------

def imagen_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# ---------------- ESTADO DE SESIÓN ----------------

if "indice" not in st.session_state:
    st.session_state.indice = 0
    st.session_state.respuestas = {}

# ---------------- PREGUNTAS ----------------

PREGUNTAS = [
    ("edad", "Selecciona tu rango de edad:", ["18-21", "22-25", "26-29", "30-33", "34-37", "38-41", "42-45", "46-49", "50-53", "54-57", "58-61", "62-65", "66-70"]),
    ("genero", "Selecciona tu género:", ["Masculino", "Femenino"]),
    ("ciudad", "Selecciona tu ciudad de residencia:", ["Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena", "Bucaramanga", "Pereira", "Manizales", "Santa Marta", "Cúcuta"]),
    ("nivel_educativo", "¿Cuál es tu nivel educativo?", ["Bachiller", "Técnico", "Tecnólogo", "Profesional", "Postgrado"]),
    ("ocupacion", "¿Cuál es tu ocupación actual?", ["Empleado", "Independiente", "Desempleado", "Estudiante", "Pensionado"]),
    ("tiene_hijos", "¿Tienes hijos?", ["Sí", "No"]),
    ("vive_con_familia", "¿Vives con tu familia?", ["Sí", "No"]),
    ("responsable_otros", "¿Eres responsable de otros familiares?", ["Sí", "No"]),
    ("dependientes_discapacidad", "¿Tienes personas con discapacidad a tu cargo?", ["Sí", "No"]),
    ("condicion_preexistente", "¿Tienes condiciones de salud preexistentes?", ["Sí", "No"]),
    ("medicacion_permanente", "¿Tomas medicación permanente?", ["Sí", "No"]),
    ("antecedentes_familiares", "¿Tienes antecedentes familiares de enfermedades graves?", ["Sí", "No"]),
    ("chequeos_periodicos", "¿Te haces chequeos médicos periódicos?", ["Sí", "No"]),
    ("ingresos_mensuales", "¿Cuál es tu ingreso mensual aproximado? (COP)", ["<1M", "1-2M", "2-4M", "4-6M", "6-8M", "8-10M", ">10M"]),
    ("ingresos_adicionales", "¿Tienes ingresos adicionales?", ["Sí", "No"]),
    ("vivienda_propia", "¿Tienes vivienda propia?", ["Sí", "No"]),
    ("tiene_deudas", "¿Tienes deudas actuales?", ["Sí", "No"]),
    ("plan_ahorro", "¿Tienes un plan de ahorro?", ["Sí", "No"]),
    ("planes_futuros", "¿Tienes planes futuros definidos?", ["Sí", "No"]),
    ("ejercicio_fisico", "¿Con qué frecuencia haces ejercicio?", ["Nunca", "1-2 veces por semana", "3-5 veces por semana", "Diario"]),
    ("fuma", "¿Fumas regularmente?", ["Sí", "No"]),
    ("alcohol", "¿Consumes alcohol regularmente?", ["Sí", "No"]),
    ("actividad", "Describe tu nivel de actividad física diaria:", ["Activa", "Sedentaria"]),
    ("medio_transporte", "¿Cuál es tu medio de transporte habitual?", ["Transporte público", "Vehículo propio", "Bicicleta", "Moto", "Caminando"]),
    ("tiempo_transporte", "¿Cuánto tiempo gastas en transporte al día?", ["Menos de 1 hora", "1-2 horas", "Más de 2 horas"]),
    ("actividades_riesgo", "¿Realizas actividades de riesgo?", ["Sí", "No"]),
    ("prioridad_actual", "¿Cuál es tu prioridad financiera actual?", ["Protección familiar", "Ahorro futuro", "Cobertura médica", "Educación"]),
    ("paga_mas_cobertura", "¿Pagarías más por mejor cobertura?", ["Sí", "No"]),
    ("preferencia_seguro", "¿Qué tipo de seguro prefieres?", ["Alta cobertura", "Baja cobertura"]),
    ("preocupacion_economica", "¿Tu mayor preocupación económica?", ["Salud", "Educación", "Ingreso", "Futuro"]),
    ("gasto_preferido", "¿En qué prefieres gastar tu dinero?", ["Educación", "Salud", "Viajes", "Inversión"]),
    ("nivel_investigacion", "¿Cuánto investigas antes de comprar un seguro?", ["Nada", "Poco", "Regular", "Mucho"]),
    ("lee_sobre_finanzas", "¿Lees sobre temas financieros?", ["Sí", "No"]),
]

# ---------------- ENCABEZADO PRINCIPAL ----------------

st.markdown("<div class='titulo-principal'>🛡️ Encuentra tu seguro ideal</div>", unsafe_allow_html=True)

# ---------------- FORMULARIO INTERACTIVO ----------------

indice = st.session_state.indice

if indice < len(PREGUNTAS):
    clave, pregunta, opciones = PREGUNTAS[indice]
    st.markdown(f"### {pregunta}")

    MAX_COLS = 4
    filas = [opciones[i:i + MAX_COLS] for i in range(0, len(opciones), MAX_COLS)]

    for fila in filas:
        cols = st.columns(len(fila))
        for i, op in enumerate(fila):
            with cols[i]:
                ruta = f"static/icon_{op.lower().replace(' ', '_')}.png"
                if os.path.exists(ruta):
                    img_b64 = imagen_base64(ruta)
                    img_html = f"<img src='data:image/png;base64,{img_b64}'/>"
                else:
                    img_html = ""

                button_id = f"{clave}_{op}"
                html_boton = f"""
                    <div class="tarjeta" onclick="document.getElementById('{button_id}').click();">
                        {img_html}
                        <div class="tarjeta-texto">{op}</div>
                    </div>
                """
                st.markdown(html_boton, unsafe_allow_html=True)
                if st.button("", key=button_id):
                    st.session_state.respuestas[clave] = op
                    st.session_state.indice += 1
                    st.rerun()

    st.progress(indice / len(PREGUNTAS))

# ---------------- RESULTADO FINAL ----------------

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
