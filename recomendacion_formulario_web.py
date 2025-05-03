import streamlit as st
import pandas as pd
import joblib
from PIL import Image
import os

# Cargar modelo y encoder
modelo = joblib.load("modelo_regresion_logistica.pkl")
label_encoder = joblib.load("label_encoder.pkl")

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

st.set_page_config(page_title="Recomendador de Seguros", layout="centered")
st.markdown(
    '<h1 style="color:#003366; font-weight:800;">🛡️ Encuentra tu seguro ideal</h1>',
    unsafe_allow_html=True
)

# Estilos personalizados
st.markdown(
    """
    <style>
        /* Fondo general */
        body, .stApp {
            background-color: #cce6ff;
        }

        /* Título */
        h1 {
            color: black;
            font-weight: 800;
        }

        /* Texto de las preguntas */
        h3, .stMarkdown h3 {
            color: #003366 !important;
            font-weight: 700;
        }


        /* Botones (cuadros de selección) */
        button[kind="secondary"] {
            background-color: white !important;
            color: black !important;
            border: 2px solid #003366 !important;
            border-radius: 10px !important;
            padding: 0.5em 1em;
            transition: background-color 0.3s ease;
        }

        button[kind="secondary"]:hover {
            background-color: #e6f0ff !important;
        }

        /* Botón activo (ya seleccionado) */
        button:focus:not(:active) {
            background-color: #005bbb !important;
            color: white !important;
        }

        /* Estilo de barra de progreso */
        .stProgress > div > div > div > div {
            background-color: #005bbb;
        }
    </style>
    """,
    unsafe_allow_html=True
)
# Inicializar estado
if "indice" not in st.session_state:
    st.session_state.indice = 0
    st.session_state.respuestas = {}

indice = st.session_state.indice

# Preguntas restantes
if indice < len(PREGUNTAS):
    clave, pregunta, opciones = PREGUNTAS[indice]
    st.markdown(f"### {pregunta}")

    MAX_COLS = 5
    filas = [opciones[i:i + MAX_COLS] for i in range(0, len(opciones), MAX_COLS)]
    for fila in filas:
        cols = st.columns(len(fila))
        for i, op in enumerate(fila):
            with cols[i]:
                icon_path = f"icon_{op.lower().replace(' ', '_')}.png"
                if os.path.exists(icon_path):
                    st.image(icon_path, width=60)
                if st.button(op, key=f"{clave}_{op}"):
                    st.session_state.respuestas[clave] = op
                    st.session_state.indice += 1
                    st.rerun()

    st.progress(indice / len(PREGUNTAS))

# Resultado
else:
    respuestas = st.session_state.respuestas

    # Convertir edad
    if "edad" in respuestas:
        try:
            ini, fin = map(int, respuestas["edad"].split("-"))
            respuestas["edad"] = (ini + fin) // 2
        except:
            respuestas["edad"] = 30

    # Convertir ingreso
    mapa_ingresos = {
        "<1M": 500_000, "1-2M": 1_500_000, "2-4M": 3_000_000,
        "4-6M": 5_000_000, "6-8M": 7_000_000,
        "8-10M": 9_000_000, ">10M": 12_000_000
    }
    if "ingresos_mensuales" in respuestas:
        respuestas["ingresos_mensuales"] = mapa_ingresos.get(
            respuestas["ingresos_mensuales"], 3_000_000
        )

    # Predecir
    df_usuario = pd.DataFrame([respuestas])
    try:
        pred = modelo.predict(df_usuario)
        resultado = label_encoder.inverse_transform(pred)[0]
        st.success(f"✅ Seguro recomendado: **{resultado}**")
    except Exception as e:
        st.error(f"❌ Error en la predicción: {str(e)}")

    if st.button("🔁 Volver a comenzar"):
        st.session_state.indice = 0
        st.session_state.respuestas = {}
        st.rerun()
