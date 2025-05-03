# recomendacion_formulario_web.py adaptado a tarjetas visuales con iconos

import streamlit as st
import pandas as pd
import joblib
import base64
from PIL import Image
import os

# Cargar modelo y encoder
modelo = joblib.load("modelo_regresion_logistica.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# Configuracion de la pagina
st.set_page_config(page_title="Recomendador de Seguros", page_icon="🛡️", layout="centered")
st.image("logo_global.png", width=150)
st.image("recomendacion.png", width=100)
st.title("\U0001F6E1️ Encuentra tu seguro ideal")

# Preguntas
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

# Función para codificar imágenes a base64
def codificar_imagen(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Función para mostrar tarjetas

def mostrar_tarjetas(clave, pregunta, opciones, seleccion_actual):
    st.markdown(f"### {pregunta}")
    cols = st.columns(len(opciones))
    seleccion = seleccion_actual
    for i, op in enumerate(opciones):
        icono_path = f"icon_{op.lower().replace(' ', '_')}.png"
        icono = codificar_imagen(icono_path)
        color_borde = "#005BBB" if seleccion_actual == op else "#cccccc"
        with cols[i]:
            st.markdown(f"""
                <div style='border:2px solid {color_borde}; border-radius:10px; padding:10px; text-align:center;'>
                    <img src='data:image/png;base64,{icono}' width='60'><br>
                    <strong style='color:white'>{op}</strong>
                </div>
            """, unsafe_allow_html=True)
            if st.button(op, key=f"{clave}_{op}"):
                seleccion = op
    return seleccion

# Estado de sesión para avanzar paso a paso
if 'indice' not in st.session_state:
    st.session_state.indice = 0
if 'respuestas' not in st.session_state:
    st.session_state.respuestas = {}

indice = st.session_state.indice
clave, texto, opciones = PREGUNTAS[indice]

# Mostrar barra de progreso
st.progress((indice + 1) / len(PREGUNTAS))

# Mostrar pregunta
respuesta_actual = st.session_state.respuestas.get(clave, None)
respuesta = mostrar_tarjetas(clave, texto, opciones, respuesta_actual)
if respuesta:
    st.session_state.respuestas[clave] = respuesta

    if st.button("Siguiente"):
        if indice + 1 < len(PREGUNTAS):
            st.session_state.indice += 1
            st.rerun()
        else:
            # Procesamiento especial
            r = st.session_state.respuestas
            if "edad" in r:
                try:
                    ini, fin = map(int, r["edad"].split("-"))
                    r["edad"] = (ini + fin) // 2
                except:
                    r["edad"] = 30

            ingresos_map = {
                "<1M": 500_000, "1-2M": 1_500_000, "2-4M": 3_000_000,
                "4-6M": 5_000_000, "6-8M": 7_000_000,
                "8-10M": 9_000_000, ">10M": 12_000_000
            }
            if "ingresos_mensuales" in r:
                r["ingresos_mensuales"] = ingresos_map.get(r["ingresos_mensuales"], 3_000_000)

            df_usuario = pd.DataFrame([r])
            try:
                pred = modelo.predict(df_usuario)
                resultado = label_encoder.inverse_transform(pred)[0]
                st.success(f"✅ Seguro recomendado: **{resultado}**")
            except Exception as e:
                st.error(f"❌ Error en la predicción: {str(e)}")
