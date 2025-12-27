import streamlit as st
from openai import OpenAI
import random

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Trader Mastery Hub", layout="wide")

# --- CLIENTE IA CON FALLBACK ---
client = None
if "OPENAI_API_KEY" in st.secrets:
    try:
        # Intentamos inicializar, pero si no hay saldo, el error saltará después
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    except:
        client = None

# --- BASE DE DATOS TÉCNICA (TAB 1: BLOOMBERG) ---
bloomberg_db = [
    {"cmd": "YAS", "desc": "Yield and Spread Analysis", "context": "Fixed Income", "tip": "Recuerda: El G-Spread es vs Curva Soberana, el I-Spread vs Swaps. ¿Cuál es más relevante hoy?"},
    {"cmd": "WB", "desc": "World Bond Yields", "context": "Macro", "tip": "Usa 'Relative Value' para comparar el 10Y de México vs el 10Y UST."},
    {"cmd": "NIM", "desc": "New Issue Monitor", "context": "Fixed Income", "tip": "Fíjate en el 'Books Open' para ver el momentum de la demanda primaria."},
    {"cmd": "CRAT", "desc": "Credit Rating History", "context": "Credit", "tip": "Busca divergencias entre Moody's y S&P antes de un rebalanceo."},
    {"cmd": "RATC", "desc": "Rating Changes", "context": "Credit", "tip": "Filtra por 'Fallen Angels' para buscar oportunidades de alto rendimiento."},
    {"cmd": "FMC", "desc": "Fiscal Monitor Chart", "context": "Macro", "tip": "Crucial para analizar el déficit fiscal antes de comprar bonos de larga duración."},
    {"cmd": "HP", "desc": "Historical Price", "context": "General", "tip": "Usa la pestaña de 'Seasonality' para ver patrones históricos en FX."},
]

st.title("🏛️ Professional Trading Hub")
tabs = st.tabs(["Bloomberg", "Financial Analysis", "Programming", "Derivatives", "Fixed Income", "Statistics"])

# ==========================================
# TAB 1: BLOOMBERG (IA + MODO OFFLINE)
# ==========================================
with tabs[0]:
    st.header("Terminal Bloomberg Mastery")
    
    if 'fn_bb' not in st.session_state:
        st.session_state.fn_bb = random.choice(bloomberg_db)
        st.session_state.feedback_bb = ""

    fn = st.session_state.fn_bb
    st.info(f"📍 **Contexto:** {fn['context']}")
    st.subheader(f"Explica la función: **{fn['cmd']}**")
    
    user_exp = st.text_area("Explica para qué sirve y cuándo la aplicas:", key="exp_bb", height=150)

    if st.button("Evaluar Explicación"):
        if user_exp:
            with st.spinner("Analizando con IA (o modo de respaldo)..."):
                try:
                    # INTENTO CON IA
                    prompt = f"Actúa como Senior Trader mentor. Evalúa esta explicación de {fn['cmd']} ({fn['desc']}): '{user_exp}'. Detecta huecos técnicos y sé breve."
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "system", "content": "Experto en Bloomberg."}, {"role": "user", "content": prompt}],
                        timeout=4 # No esperar más de 4 seg
                    )
                    st.session_state.feedback_bb = response.choices[0].message.content
                except Exception:
                    # RESPALDO SI FALLA LA API (CUOTA/SALDO)
                    st.session_state.feedback_bb = f"⚠️ **Modo Respaldo (Sin Saldo API):**\n\nTu explicación sobre **{fn['cmd']}** ha sido registrada. Como no hay conexión con la IA, aquí tienes el punto clave: **{fn['tip']}**"
        else:
            st.warning("Escribe tu explicación primero.")

    if st.session_state.feedback_bb:
        st.markdown("---")
        st.markdown("### 🔍 Feedback:")
        st.write(st.session_state.feedback_bb)
        
        if st.button("Siguiente Función ➡️"):
            st.session_state.fn_bb = random.choice(bloomberg_db)
            st.session_state.feedback_bb = ""
            st.rerun()

# ==========================================
# SECCIONES RESTANTES (PLACEHOLDERS)
# ==========================================
with tabs[1]: st.header("Análisis Financiero"); st.write("Sección en construcción...")
with tabs[2]: st.header("Programación para Traders"); st.code("import pandas as pd", language='python')
with tabs[3]: st.header("Derivados"); st.write("Práctica de Griegas y Volatilidad...")
with tabs[4]: st.header("Fixed Income"); st.write("Conceptos de Convexidad y Duración...")
with tabs[5]: st.header("Estadística"); st.write("Modelos VaR y Correlaciones...")
