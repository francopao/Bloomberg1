import streamlit as st
import random
import pandas as pd
from openai import OpenAI

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mastery Hub: Bloomberg & Python", layout="wide")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- BASES DE DATOS LOCALES (Ahorro de Tokens) ---
BLOOMBERG_DATA = {
    "Renta Fija": ["YAS", "WB", "NIM", "SRCH", "CRAT"],
    "Equity & FX": ["HP", "EE", "DVD", "QR", "GP"],
    "Macro/Riesgo": ["FMC", "RATC", "ECO", "IFR"]
}

PYTHON_LIBS = {
    "Análisis": "pandas, numpy",
    "Visualización": "matplotlib, seaborn",
    "Estadística/ML": "scipy, sklearn",
    "Data": "yfinance, datetime"
}

# --- FUNCIÓN IA OPTIMIZADA ---
def quick_ai_query(system_role, prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Alta eficiencia, bajo costo
            max_tokens=300,
            messages=[
                {"role": "system", "content": f"Eres un experto en {system_role}. Respuestas técnicas, breves y en formato Markdown."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# --- INTERFAZ POR TABS ---
st.title("🚀 Speed Mastery Hub")
tab_bbg, tab_py = st.tabs(["🖥️ Bloomberg Terminal", "🐍 Python for Finance"])

# --- TAB 1: BLOOMBERG ---
with tab_bbg:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Memorización")
        cat = st.selectbox("Categoría:", list(BLOOMBERG_DATA.keys()))
        cmd = st.selectbox("Comando:", BLOOMBERG_DATA[cat])
        
        if st.button("¿Cómo se usa en la vida real?"):
            prompt = f"Explica el comando {cmd} de Bloomberg. Dime qué métrica clave buscar y cuál es su equivalente lógico en análisis de datos."
            with st.spinner("Buscando en Terminal..."):
                res = quick_ai_query("Terminal Bloomberg", prompt)
                st.session_state['bbg_res'] = res
    
    with col2:
        st.subheader("Insight de Mercado")
        if 'bbg_res' in st.session_state:
            st.info(st.session_state['bbg_res'])
            if st.button("Generar Reto Rápido"):
                reto = quick_ai_query("Trader Senior", f"Dame un ejercicio de 1 línea para practicar el comando {cmd}.")
                st.warning(reto)

# --- TAB 2: PYTHON ---
with tab_py:
    col3, col4 = st.columns([1, 2])
    with col3:
        st.subheader("Librerías Útiles")
        lib_choice = st.selectbox("Librería:", list(PYTHON_LIBS.keys()))
        st.write(f"Enfocarse en: `{PYTHON_LIBS[lib_choice]}`")
        
        task = st.text_input("¿Qué quieres calcular? (ej: VaR, Correlación, Optimización)")
        
        if st.button("Obtener Snippet"):
            prompt = f"Escribe un código de máximo 10 líneas usando {PYTHON_LIBS[lib_choice]} para calcular {task}. Usa datos sintéticos de numpy."
            with st.spinner("Codificando..."):
                res_py = quick_ai_query("Python Quant Developer", prompt)
                st.session_state['py_res'] = res_py

    with col4:
        st.subheader("Código y Aplicación")
        if 'py_res' in st.session_state:
            st.markdown(st.session_state['py_res'])
            
            # EL PUENTE: Conexión inmediata
            if st.button("🔗 ¿Con qué comando BBG conecta esto?"):
                bridge = quick_ai_query("Experto Integrador", f"Este código de Python para {task}, ¿con qué funciones de Bloomberg se relaciona y por qué?")
                st.success(bridge)
