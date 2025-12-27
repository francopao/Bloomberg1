import streamlit as st
import random

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Trader Mastery Hub", layout="wide")

# --- BASES DE DATOS OFFLINE (Sin dependencia de API) ---
bloomberg_db = [
    {"cmd": "YAS", "desc": "Yield and Spread Analysis", "tip": "Recuerda: El G-Spread es vs Curva Soberana, el I-Spread vs Swaps."},
    {"cmd": "WB", "desc": "World Bond Yields", "tip": "Usa 'Relative Value' para comparar curvas soberanas."},
    {"cmd": "NIM", "desc": "New Issue Monitor", "tip": "Fíjate en el 'Books Open' para ver el momentum de demanda."},
    {"cmd": "CRAT", "desc": "Credit Rating History", "tip": "Busca divergencias entre agencias (Moody's, S&P, Fitch)."},
    {"cmd": "RATC", "desc": "Rating Changes", "tip": "Filtra por 'Fallen Angels' para buscar oportunidades."},
    {"cmd": "FMC", "desc": "Fiscal Monitor Chart", "tip": "Analiza Déficit/PIB antes de comprar bonos de larga duración."},
    {"cmd": "HP", "desc": "Historical Price", "tip": "Usa 'Seasonality' para ver patrones históricos en FX."}
]

fin_analysis_db = [
    {"formula": "Cartera Pesada / Crítica", "calc": "Crédito Deficiente + Crédito Dudoso + Crédito en Pérdida"},
    {"formula": "Mora Real", "calc": "(Cartera Problema + Flujos Castigados) / Colocaciones Brutas"},
    {"formula": "Compromiso Patrimonial", "calc": "(Cartera Problema - Provisión) / Patrimonio"},
    {"formula": "Expected Loss (EL)", "calc": "PD × LGD × EAD"},
    {"formula": "RCG (Ratio de Capital Global)", "calc": "Patrimonio Efectivo / Activos Ponderados por Riesgo"},
    {"formula": "LCR", "calc": "HQLA / Total Net Cash Outflows (30 days)"},
    {"formula": "NSFR", "calc": "Financiación Estable Disponible / Financiación Estable Requerida"},
    {"formula": "Debt Service Coverage", "calc": "(EBITDA - cash taxes) / (interest + principal)"},
    {"formula": "EBITDA", "calc": "Operating Profit + Depreciation + Amortization"},
    {"formula": "CapEx", "calc": "(PPE Final - PPE Inicial) + Depreciación"}
]

# --- INICIALIZACIÓN DE ESTADOS ---
if 'fn_bb' not in st.session_state: st.session_state.fn_bb = random.choice(bloomberg_db)
if 'show_bb' not in st.session_state: st.session_state.show_bb = False

if 'fn_fin' not in st.session_state: st.session_state.fn_fin = random.choice(fin_analysis_db)
if 'show_fin' not in st.session_state: st.session_state.show_fin = False

# --- UI PRINCIPAL ---
st.title("🏛️ Professional Trading Hub")
tabs = st.tabs(["Bloomberg", "Financial Analysis", "Programming", "Derivatives", "Fixed Income", "Statistics"])

# ==========================================
# TAB 1: BLOOMBERG
# ==========================================
with tabs[0]:
    st.header("Terminal Bloomberg Mastery")
    item = st.session_state.fn_bb
    st.subheader(f"¿Para qué sirve la función: **{item['cmd']}**?")
    
    st.text_area("Tu explicación:", key="input_bb")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Verificar Bloomberg"): st.session_state.show_bb = True
    with col2:
        if st.button("Siguiente Comando ➡️"):
            st.session_state.fn_bb = random.choice(bloomberg_db)
            st.session_state.show_bb = False
            st.rerun()

    if st.session_state.show_bb:
        st.success(f"**Punto Clave:** {item['tip']}")

# ==========================================
# TAB 2: FINANCIAL ANALYSIS
# ==========================================
with tabs[1]:
    st.header("Análisis Financiero y de Crédito")
    item_f = st.session_state.fn_fin
    
    st.subheader(f"Define la fórmula de: **{item_f['formula']}**")
    st.text_area("Escribe la fórmula y su interpretación:", key="input_fin")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Verificar Fórmula"): st.session_state.show_fin = True
    with col2:
        if st.button("Siguiente Fórmula ➡️"):
            st.session_state.fn_fin = random.choice(fin_analysis_db)
            st.session_state.show_fin = False
            st.rerun()

    if st.session_state.show_fin:
        st.warning(f"**Cálculo Correcto:** {item_f['calc']}")

# ==========================================
# OTROS TABS
# ==========================================
with tabs[2]: st.header("Programación"); st.code("import pandas as pd")
with tabs[3]: st.header("Derivados"); st.write("Contenido de Griegas...")
with tabs[4]: st.header("Fixed Income"); st.write("Contenido de Duración...")
with tabs[5]: st.header("Estadística"); st.write("Contenido de Correlación...")


with tabs[2]: st.header("Programación para Traders"); st.code("import pandas as pd", language='python')
with tabs[3]: st.header("Derivados"); st.write("Práctica de Griegas y Volatilidad...")
with tabs[4]: st.header("Fixed Income"); st.write("Conceptos de Convexidad y Duración...")
with tabs[5]: st.header("Estadística"); st.write("Modelos VaR y Correlaciones...")
