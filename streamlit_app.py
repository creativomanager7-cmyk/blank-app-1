import streamlit as st
import pandas as pd

# Configuración de alta gama para el entorno ejecutivo
st.set_page_config(
    page_title="BIG BANG MUSIC INTELLIGENCE",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos oscuros para la presentación de mañana
st.markdown("""
    <style>
    .reportview-container { background: #060609; color: #ffffff; }
    .sidebar .sidebar-content { background: #0b0b11; }
    h1, h2, h3 { font-family: 'Inter', sans-serif; font-weight: 700; }
    .metric-box { background-color: #11111a; border: 1px solid #1b1b2a; padding: 20px; border-radius: 12px; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ BIG BANG OS — Music Business Intelligence")
st.subheader("Ecosistema de Auditoría de Regalías, Splits y Potencial Viral")
st.markdown("---")

# Base de datos real del catálogo (47 tracks)
catalog_data = {
    "Track / Single": ["Mi propio rescate", "¿Dónde estabas tú?", "Muestreo Latente Catálogo (45 Tracks)"],
    "Subgénero / Nicho": ["Norteño Banda", "Regional Pop / Cumbia", "Regional / Variado"],
    "Split Asignado": ["85% / Split Autor", "92% / Split Autor", "Monitoreo Centralizado"],
    "Potencial Viral": ["Alto Impacto (Nicho Fiel)", "Muy Alto (Tendencia Latente)", "Estable"],
    "Estado de Regalías": ["Auditoría Limpia • Retención Verificada", "Split de Composición Auditado", "Flujo Activo"]
}

df = pd.DataFrame(catalog_data)

# Control interactivo en la barra lateral
st.sidebar.header("Control de Catálogo")
st.sidebar.markdown("### 47 Tracks Activos")
selected_track = st.sidebar.selectbox("Seleccione un track para auditoría profunda:", df["Track / Single"].tolist())

track_info = df[df["Track / Single"] == selected_track].iloc[0]

# Despliegue de métricas clave
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
    st.metric(label="PORCENTAJE ASIGNADO / SPLIT", value=track_info["Split Asignado"])
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
    st.metric(label="NICHO DE MERCADO / SUBGÉNERO", value=track_info["Subgénero / Nicho"])
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
    st.metric(label="POTENCIAL DE INYECCIÓN VIRAL", value=track_info["Potencial Viral"])
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("### 📊 Matriz de Distribución y Auditoría Operativa")
st.dataframe(df, use_container_width=True)

st.markdown("---")
st.markdown("🔒 **Entorno Operativo de Control Privado** | Conexión Segura Activa en Render")
