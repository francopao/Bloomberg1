import streamlit as st
from openai import OpenAI
import random
# --- CONFIGURACIÓN Y CLIENTE API ---
# Reemplaza con tu KEY o usa st.secrets para mayor seguridad
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error("Error: Configura la API Key en los Secrets de Streamlit.")
    st.stop()

# --- BASE DE DATOS (Muestra) ---
functions_db = [
    {"cmd": "YAS", "desc": "Yield and Spread Analysis", "context": "Fixed Income / Trading"},
    {"cmd": "WB", "desc": "World Bond Yields", "context": "Macro / Sovereign Debt"},
    {"cmd": "NIM", "desc": "New Issue Monitor", "context": "Primary Markets"},
    {"cmd": "CRAT", "desc": "Company Credit Rating", "context": "Credit Research"}
]

st.title("🎓 Método Feynman: Bloomberg Terminal")

if 'fn' not in st.session_state:
    st.session_state.fn = random.choice(functions_db)
    st.session_state.feedback = ""

# --- UI PRINCIPAL ---
fn = st.session_state.fn
st.subheader(f"Explícame como a un junior: ¿Para qué usas **{fn['cmd']}**?")
st.caption(f"Contexto: {fn['context']}")

# Área de explicación del usuario
user_explanation = st.text_area("Escribe tu explicación técnica aquí:", placeholder="Ej: Uso YAS para calcular el yield to worst y ver el spread contra el benchmark del Tesoro...")

if st.button("Evaluar mi explicación"):
    if user_explanation:
        with st.spinner("Analizando huecos conceptuales..."):
            try:
                prompt = f"""
                Actúa como un Senior Trader mentor. El usuario está intentando explicar la función de Bloomberg '{fn['cmd']}' ({fn['desc']}).
                Su explicación es: "{user_explanation}"
                
                Tu objetivo:
                1. Detectar 'huecos' (blind spots) o imprecisiones técnicas.
                2. Hacer una única pregunta punzante que evalúe si entiende el impacto en el portafolio o el riesgo (FX/FI).
                3. Ser extremadamente breve (máximo 3 frases).
                """
                
                response = client.chat.completions.create(
                    model="gpt-4o", # O "gpt-3.5-turbo" para menor costo
                    messages=[{"role": "system", "content": "Eres un experto en Bloomberg Terminal y mercados globales."},
                              {"role": "user", "content": prompt}]
                )
                st.session_state.feedback = response.choices[0].message.content
            except Exception as e:
                st.error(f"Error con la API: {e}")
    else:
        st.warning("Escribe algo primero para poder evaluarte.")

# --- AUTOEVALUACIÓN E IMPACTO ---
if st.session_state.feedback:
    st.markdown("### 🔍 Feedback de la IA (Huecos detectados):")
    st.info(st.session_state.feedback)
    
    st.divider()
    st.markdown("#### Autoevaluación inmediata:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Lo dominé (Siguiente)"):
            st.session_state.fn = random.choice(functions_db)
            st.session_state.feedback = ""
            st.rerun()
    with col2:
        st.button("Necesito repasar esta función")
