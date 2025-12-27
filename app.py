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
VBA_TASKS = {
    "Automatización BBG": ["BDH (Historical Data)", "BDP (Real Time)", "Reference Data API"],
    "FX / Money Market": ["Calculadora de Forwards", "Interpolación de Tasas", "Conversor de Base 360/365"],
    "Fixed Income": ["Cálculo de Duración/Convexidad", "Bootstrapping de Curvas", "Generador de Cashflow"],
    "Herramientas UI": ["UserForms (Boletas)", "Eventos de Hoja (Auto-Update)", "Módulos de Clase"]
}
R_LIBS = {
    "Reporting & Dashboarding": "rmarkdown, shiny, flexdashboard, kableExtra, DT",
    "Data Wrangling (Tidyverse)": "dplyr, tidyr, readr, purrr, stringr, readxl",
    "Time Series & Finance": "zoo, lubridate, quantmod, bizdays",
    "Financial Engineering": "RiskMetrics, RQuantLib, ggplot2"
}
# --- BASE DE DATOS LOCAL DAX (Ahorro de Tokens) ---
DAX_FUNCTIONS = {
    "Agregación & Iteración": ["SUMX", "AVERAGEX", "SUM", "AVERAGE", "COUNT"],
    "Inteligencia de Tiempo": ["DATEADD", "YEAR", "EOMONTH", "CALENDAR"],
    "Filtros & Contexto": ["CALCULATE", "KEEPFILTERS", "FILTER", "ALL", "ALLEXCEPT", "CALCULATETABLE"],
    "Lógica & Tablas": ["LOOKUPVALUE", "VAR + RETURN", "ADDCOLUMNS", "IF", "SWITCH", "RANKX", "DIVIDE"]
}

# --- BASE DE DATOS LOCAL (0 TOKENS) ---
FINANCIAL_INDICATORS = [
    {"id": "Cartera Pesada", "f": "Deficiente + Dudoso + Pérdida", "uso": "Identificar deterioro estructural."},
    {"id": "Mora Real", "f": "(Cartera Problema + Castigos) / Colocaciones Brutas", "uso": "Riesgo total efectivo incluyendo pérdidas materializadas."},
    {"id": "Compromiso Patrimonial", "f": "(Cartera Problema - Provisión) / Patrimonio", "uso": "Vulnerabilidad del capital ante deterioro extremo."},
    {"id": "LCR", "f": "HQLA / Salidas Netas (30 días)", "uso": "Resiliencia ante shocks de liquidez de corto plazo."},
    {"id": "RCG", "f": "Patrimonio Efectivo / APR", "uso": "Solvencia regulatoria y absorción de pérdidas inesperadas."},
    {"id": "Expected Loss", "f": "PD × LGD × EAD", "uso": "Costo estadístico de crédito y base para pricing."}
    # Se pueden añadir los demás de tu lista aquí para 0 costo
]

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
st.title("Financial Engineer Hub")
tab_bbg, tab_py, tab_vba, tab_r, tab_powerbi, tab_indicators = st.tabs(["🖥️ Bloomberg", "🐍 Python", "📊 VBA Excel", "📉 R", "📊 DAX", "🏥 Ratios"])

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


# --- TAB 3: VBA (NUEVO) ---
with tab_vba:
    col_vba1, col_vba2 = st.columns([1, 2])
    
    with col_vba1:
        st.subheader("VBA for Traders")
        category = st.selectbox("Área Técnica:", list(VBA_TASKS.keys()))
        feature = st.selectbox("Funcionalidad:", VBA_TASKS[category])
        
        if st.button("Generar Macro/Concepto"):
            prompt = f"""Explica cómo implementar {feature} en VBA para un Trader de FX/Fixed Income. 
            Incluye: 1. ¿Usar Módulo o UserForm? 2. Un snippet de código robusto. 
            3. ¿Cómo conectarlo conceptualmente con el API de Bloomberg?"""
            
            with st.spinner("Escribiendo Macro..."):
                res_vba = quick_ai_query("VBA Financial Developer", prompt)
                st.session_state['vba_res'] = res_vba

    with col_vba2:
        st.subheader("Código y Estructura")
        if 'vba_res' in st.session_state:
            st.markdown(st.session_state['vba_res'])
            
            # EL PUENTE TRIPLE: Conexión VBA -> Python -> BBG
            if st.button("🔗 El Puente: ¿Cómo migro esto a Python?"):
                bridge_vba = quick_ai_query("Software Architect", f"Tengo esta lógica en VBA: {feature}. ¿Cómo se traduce a una función eficiente en Python y qué comando de Bloomberg la alimenta?")
                st.success(bridge_vba)

# --- TAB 4: RSTUDIO (NUEVO) ---
with tab_r:
    col_r1, col_r2 = st.columns([1, 2])
    
    with col_r1:
        st.subheader("Financial R Mastery")
        category_r = st.selectbox("Especialidad R:", list(R_LIBS.keys()))
        libraries = R_LIBS[category_r]
        
        st.write(f"**Librerías clave:** `{libraries}`")
        
        target = st.text_input("Objetivo (ej: Stress Test FX, Curva de Tasas, Reporte PDF):")
        
        if st.button("Generar Solución en R"):
            prompt = f"""Crea un ejemplo de ingeniería financiera para {target} usando las librerías {libraries}.
            Enfócate en: 1. Estructura de datos (dplyr/zoo). 2. Visualización o Reporte (ggplot2/Shiny).
            3. Si aplica, usa RiskMetrics o RQuantLib para el cálculo técnico."""
            
            with st.spinner("Analizando modelos en R..."):
                res_r = quick_ai_query("R-Quant Developer", prompt)
                st.session_state['r_res'] = res_r

    with col_r2:
        st.subheader("Script & Engineering Output")
        if 'r_res' in st.session_state:
            st.markdown(st.session_state['r_res'])
            
            # EL PUENTE: Conexión R -> Python/BBG
            if st.button("🔗 El Puente: ¿Cuándo usar R en lugar de Python?"):
                bridge_r = quick_ai_query("Head of Quantitative Research", 
                    f"Para este caso de {target}, compara la eficiencia de R (Shiny/RMarkdown) frente a Python y cómo se alimentaría de Bloomberg.")
                st.success(bridge_r)
 # --- TAB 5: BI & DAX (NUEVO) ---
with tab_powerbi:
    col_dax1, col_dax2 = st.columns([1, 2])
    
    with col_dax1:
        st.subheader("Financial BI (DAX)")
        cat_dax = st.selectbox("Categoría DAX:", list(DAX_FUNCTIONS.keys()))
        func_dax = st.selectbox("Función clave:", DAX_FUNCTIONS[cat_dax])
        
        target_dax = st.text_input("Objetivo (ej: P&L acumulado, Atribución de Retorno, Ranking de Traders):")
        
        if st.button("Generar Medida DAX"):
            prompt = f"""Explica la función {func_dax} aplicada a finanzas para {target_dax}.
            Proporciona: 1. La sintaxis de la Medida (DAX). 2. Explicación del 'Contexto de Filtro'.
            3. Un consejo de optimización (performance)."""
            
            with st.spinner("Calculando medida..."):
                res_dax = quick_ai_query("Power BI Financial Architect", prompt)
                st.session_state['dax_res'] = res_dax

    with col_dax2:
        st.subheader("DAX Expression & Model Insight")
        if 'dax_res' in st.session_state:
            st.markdown(st.session_state['dax_res'])
            
            # EL PUENTE: Conexión DAX -> Python/VBA
            if st.button("🔗 El Puente: ¿Cuándo usar DAX y cuándo Python/VBA?"):
                bridge_dax = quick_ai_query("CTO Financiero", 
                    f"Para {target_dax}, compara la ventaja de usar DAX en un Dashboard frente a procesar los datos en Python o VBA.")
                st.success(bridge_dax) 
# --- TAB 6: RISK & SOLVENCY (Basado en tu imagen/lista) ---
with tab_indicators:
    col_r1, col_r2 = st.columns([1, 2])
    
    with col_r1:
        st.subheader("Entrenamiento de Indicadores")
        ind = st.selectbox("Indicador a dominar:", [i["id"] for i in FINANCIAL_INDICATORS])
        
        # Seleccionamos los datos locales para pasarlos como contexto rápido
        data_ind = next(item for item in FINANCIAL_INDICATORS if item["id"] == ind)
        
        if st.button("Generar Caso de Cálculo"):
            prompt = f"""Crea un micro-caso numérico breve para calcular {ind}. 
            Dame solo 3 datos numéricos y pídeme el resultado. 
            No des la respuesta todavía."""
            
            with st.spinner("Generando escenario..."):
                res_caso = quick_ai_query("Analista de Riesgos", prompt)
                st.session_state['caso_risk'] = res_caso

    with col_r2:
        st.subheader("Escenario y Aplicación")
        if 'caso_risk' in st.session_state:
            st.info(st.session_state['caso_risk'])
            
            with st.expander("Ver Fórmula y Utilidad (Memoria)"):
                st.write(f"**Fórmula:** {data_ind['f']}")
                st.write(f"**¿Para qué sirve?:** {data_ind['uso']}")
            
            if st.button("🔗 El Puente: ¿Cómo monitoreo esto en vivo?"):
                bridge_risk = quick_ai_query("Chief Risk Officer", 
                    f"¿Qué función de Bloomberg me da los inputs para {ind} y cómo lo automatizo en un dashboard de R o Python?")
                st.success(bridge_risk)
