import streamlit as st
from openai import OpenAI
import random

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Trader Mastery App", layout="wide")

# --- CLIENTE IA (CON MANEJO DE ERRORES) ---
client = None
if "OPENAI_API_KEY" in st.secrets:
    try:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    except:
        client = None

# --- BASES DE DATOS ---
# Tab 1: Bloomberg
bloomberg_db = [
    {"cmd": "YAS", "desc": "Yield and Spread Analysis", "context": "FI Trading", "master_tip": "¿Sabes ajustar el 'Price Source' para bonos ilíquidos?"},
    {"cmd": "WB", "desc": "World Bond Yields", "context": "Macro", "master_tip": "Compara spreads soberanos vs UST para medir riesgo país."},
    {"cmd": "NIM", "desc": "New Issue Monitor", "context": "Primario", "master_tip": "Busca los 'Indicated Price Talks' (IPTs) para nuevas emisiones."},
    {"cmd": "FMC", "desc": "Fiscal Monitor Chart", "context": "Macro", "master_tip": "Analiza la sostenibilidad de deuda/PIB antes de entrar en long-term sovereign."},
]

# Puedes ir llenando estas listas según necesites
financial_db = [{"concept": "WACC", "q": "¿Cómo afecta un alza de tasas al WACC de una empresa apalancada?"}]
stats_db = [{"concept": "Kurtosis", "q": "¿Por qué un trader de FX teme a las distribuciones Leptocúrticas?"}]

# --- INTERFAZ DE TABS ---
st.title("🏛️ Professional Trading Hub")
tabs = st.tabs(["Bloomberg", "Financial Analysis", "Programming", "Derivatives", "Fixed Income", "Statistics"])

# ==========================================
# TAB 1: BLOOMBERG (Metodología Feynman)
# ==========================================
with tabs[0]:
    st.header("Terminal Bloomberg")
    
    if 'fn_bb' not in st.session_state:
        st.session_state.fn_bb = random.choice(bloomberg_db)
        st.session_state.feedback_bb = ""

    fn = st.session_state.fn_bb
    st.subheader(f"Explica la función: **{fn['cmd']}**")
    
    user_exp = st.text_area("Tu explicación:", key="exp_bb", placeholder="Para qué sirve y cuándo aplicarla...")

    if st.button("Evaluar Bloomberg"):
        if user_exp:
            with st.spinner("Analizando..."):
                success = False
                if client:
                    try:
                        prompt = f"Actúa como Senior Trader. Evalúa esta explicación de la función {fn['cmd']} ({fn['desc']}): '{user_exp}'. Sé breve y técnico."
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[{"role": "system", "content": "Experto en Bloomberg."}, {"role": "user", "content": prompt}],
                            timeout=5
                        )
                        st.session_state.feedback_bb = response.choices[0].message.content
                        success = True
                    except: success = False
                
                if not success:
                    st.session_state.feedback_bb = f"**[Offline]** Tip: {fn['master_tip']}"
        st.rerun()

    if st.session_state.feedback_bb:
        st.info(st.session_state.feedback_bb)
        if st.button("Siguiente Función"):
            st.session_state.fn_bb = random.choice(bloomberg_db)
            st.session_state.feedback_bb = ""
            st.rerun()

# ==========================================
# TAB 2: FINANCIAL ANALYSIS
# ==========================================
with tabs[1]:
    st.header("Análisis Financiero")
    st.write("Próximamente: Casos de Equity Research y M&A.")

# ==========================================
# TAB 3: PROGRAMMING
# ==========================================
with tabs[2]:
    st.header("Python & SQL for Finance")
    st.code("df['returns'] = df['close'].pct_change()", language='python')
    st.write("Practica scripts para automatizar reportes de portafolio.")

# ==========================================
# TAB 4: DERIVATIVES
# ==========================================
with tabs[3]:
    st.header("Derivados (FX & Rates)")
    st.write("Estrategias de Cobertura (Hedging) y Griegas.")

# ==========================================
# TAB 5: FIXED INCOME
# ==========================================
with tabs[4]:
    st.header("Renta Fija")
    st.write("Curvas de rendimiento, duración, convexidad y spreads.")

# ==========================================
# TAB 6: STATISTICS
# ==========================================
with tabs[5]:
    st.header("Estadística & Econometría")
    st.write("Análisis de volatilidad, correlaciones y VaR.")
