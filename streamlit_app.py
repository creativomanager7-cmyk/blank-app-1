import sys
sys.modules['librosa'] = None
sys.modules['scipy'] = None
import streamlit as st
import pandas as pd
import re
import google.generativeai as genai
import lyricsgenius
from fpdf import FPDF
from datetime import datetime

st.set_page_config(page_title="Big Bang OS | Enterprise", page_icon="🌌", layout="wide")

# --- INTERFAZ PREMIUM INSPIRADA EN MUSO.AI (DARK FORENSIC STYLE) ---
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0B0A16 !important;
        color: #F1F5F9 !important;
    }
    .main-header {
        background: linear-gradient(135deg, #13112C 0%, #1E1233 100%);
        padding: 40px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 35px;
        border: 1px solid #2A2461;
        box-shadow: 0 15px 35px rgba(0,0,0,0.6);
    }
    .kpi-card {
        background: #141230;
        padding: 22px;
        border-radius: 12px;
        border-bottom: 4px solid #00F2FE;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
    .muso-row {
        background: #121026;
        padding: 20px 25px;
        border-radius: 14px;
        border: 1px solid #1E1B4B;
        margin-bottom: 5px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .muso-avatar {
        width: 70px;
        height: 70px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #00F2FE;
    }
    .role-badge {
        background: linear-gradient(90deg, #1E1B4B, #311042);
        color: #00F2FE;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: bold;
        border: 1px solid #4338CA;
        display: inline-block;
        margin-top: 5px;
    }
    .badge-green { background: #065F46; color: #34D399; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: bold; }
    .badge-red { background: #7F1D1D; color: #FCA5A5; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: bold; }
    .badge-yellow { background: #78350F; color: #FCD34D; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1 style="color: #00F2FE; font-size: 45px; margin-bottom: 5px; font-family: 'Helvetica Neue', sans-serif; font-weight: 800;">🌌 BIG BANG OS</h1>
    <p style="color: #94A3B8; font-size: 18px; letter-spacing: 1px;">A&R Copilot & Analytics Credit Registry • Powered by Muso Insights</p>
</div>
""", unsafe_allow_html=True)

# --- REPERTORIO UNIFICADO DE CRISTIAN ÁLVAREZ ---
canciones = [
    "Amigo ratón del queso", "Borracho te llamo", "De qué me sirve", "La bandida",
    "El agropecuario", "Te olvide", "Masoquista", "Delito", "Princeso", "Que resuelva",
    "Ojalá", "Si tu supieras", "Ni tuya ni de nadie", "De 5 en 5", "Desgraciado",
    "Golpe avisa", "Bolsita de marca", "Insomnios", "Maduro a", "Vivir la vida",
    "Inevitable", "Soltera", "Vicio de ti", "Como es la vuelta", "Cuchiviri re chévere",
    "El Cabron", "Pinocho", "Diente por diente", "Te pienso", "Fuera de órbita",
    "Perdóname", "Te guste", "Amores de un ratico", "Que no te extrañe", "Despechada",
    "Sancocho", "Track 37", "Vivan y dejen vivir", "A través de las botellas", "Por ti",
    "Fuera de órbita", "Las mujeres", "Agüita de coco", "Se me olvidó", "Te perdi",
    "Mi Debilidad", "¿Dónde Estabas Tú?"
]

artistas = [
    "Caballeros de la cantina", "Jhon Alex Castaño", "Diana Burcos", "Hanna Rivas",
    "Joaquin Guiller", "La Pandilla del Río Bravo", "Janeth Valenzuela", "Eros",
    "Joaquin Guiller", "Joaquin Guiller", "Joaquin Guiller", "Alex Ojeda",
    "Nicol Vega feat. Paola Villaroel", "Nicol Vega", "Nicol Vega", "Nicol Vega",
    "Nicol Vega", "Nicol Vega", "Nicol Vega", "Key Ospina", "Key Ospina",
    "Marcela Gomez", "Miguel Vaquero", "Valeria Rico", "Crisanto Vargas Vil",
    "Champen", "Champen feat. Pipe Calderón", "Champen", "Geral Merling", "Gaby",
    "Samu", "Samu", "Sofi Piñan", "Escudero", "Jhon Alex Castaño y Julian Daza",
    "Edwin Gaona", "Edwin Gaona", "Artista Por Asignar", "La Gran Orquesta de Bolivia",
    "Gabby", "Gabby", "Gabby", "Artista Por Asignar", "Santiago Velásquez",
    "Santiago Velásquez", "Francy", "Paola Jara"
]

tab1, tab2, tab3 = st.tabs([
    "📊 Bóveda Forense Estilo Muso.AI", "🔬 Oráculo Inteligente A&R", "🤝 Mesa de Negociación Sony"
])

with tab1:
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown('<div class="kpi-card"><p style="color:#94A3B8; margin:0;">Catalog Works</p><h2 style="color:#00F2FE; margin:0; font-weight:700;">47 Tracks</h2></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="kpi-card" style="border-bottom-color:#F59E0B;"><p style="color:#94A3B8; margin:0;">Black Box Alertas</p><h2 style="color:#F59E0B; margin:0; font-weight:700;">21 Conflicts</h2></div>', unsafe_allow_html=True)
    with col_c:
        st.markdown('<div class="kpi-card" style="border-bottom-color:#EF4444;"><p style="color:#94A3B8; margin:0;">Auditoría Status</p><h2 style="color:#EF4444; margin:0; font-weight:700;">Mesa Activa</h2></div>', unsafe_allow_html=True)
        
    st.markdown("<br><h3 style='color:#6366F1; font-family:sans-serif;'>🎵 Tracklist Verified Master & Publishing Credits</h3>", unsafe_allow_html=True)
    
    for i, cancion in enumerate(canciones):
        artista = artistas[i]
        isrc = f"CO-SMP-26-{i+1001:04d}"
        
        # Clasificación forense territorial
        if cancion == "Mi Debilidad" and artista == "Francy":
            exe_b = '<span class="badge-red">🔴 Reclamación Duplicada</span>'
            mec_b = '<span class="badge-yellow">🚨 Publisher Split Volátil</span>'
            status_texto = "⚠️ Retención SAYCO"
        elif cancion == "¿Dónde Estabas Tú?" and artista == "Paola Jara":
            exe_b = '<span class="badge-red">🔴 Conflicto Activo</span>'
            mec_b = '<span class="badge-red">🔴 Retenido The MLC (US)</span>'
            status_texto = "❌ Fondos Caja Negra"
        elif cancion == "Amores de un ratico" and artista == "Sofi Piñan":
            exe_b = '<span class="badge-green">🟢 Reclamado</span>'
            mec_b = '<span class="badge-yellow">🚨 Alerta Split Share</span>'
            status_texto = "⚠️ Pendiente Conciliación"
        else:
            exe_b = '<span class="badge-green">🟢 Al Día</span>'
            mec_b = '<span class="badge-green">🟢 Aligned</span>'
            status_texto = "✅ Sincronizado"
            
        # Contenedor HTML Estilo Ficha de Muso.AI
        st.markdown(f"""
        <div class="muso-row">
            <div style="display: flex; align-items: center; width: 100%;">
                <div style="width: 10%; text-align: left;">
                    <img class="muso-avatar" src="https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?q=80&w=150&auto=format&fit=crop">
                </div>
                <div style="width: 30%;">
                    <h4 style="color:#00F2FE; margin:0; font-size:19px; font-weight:600;">{cancion}</h4>
                    <p style="color:#94A3B8; margin:3px 0 0 0; font-size:13px;">🎙️ {artista}</p>
                    <span class="role-badge">✍️ Writer / Publisher</span>
                </div>
                <div style="width: 35%; font-size: 12px; border-left: 1px solid #23214A; padding-left: 20px;">
                    <div style="margin-bottom:3px;"><b>Performance:</b> {exe_b}</div>
                    <div style="margin-bottom:3px;"><b>Mechanical:</b> {mec_b}</div>
                    <div><b>Local Rights:</b> <span style="color:#94A3B8;">{status_texto}</span></div>
                </div>
                <div style="width: 25%; text-align: right; color: #64748B; font-size: 11px;">
                    <b>ISRC CODE</b><br><span style="color:#E2E8F0; font-family:monospace;">{isrc}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Bloque de Control de Audio y Botones Integrados
        c_player, c_b1, c_b2 = st.columns([5, 2, 2])
        with c_player:
            # Reproductor de audio integrado nativo para simular streaming en vivo
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
        with c_b1:
            st.link_button("🟩 Spotify Market", f"https://open.spotify.com/search/{cancion.replace(' ', '%20')}%20{artista.replace(' ', '%20')}", use_container_width=True)
        with c_b2:
            st.link_button("🟥 YouTube Monitor", f"https://www.youtube.com/results?search_query={cancion.replace(' ', '+')}+{artista.replace(' ', '+')}", use_container_width=True)
        
        st.markdown("<div style='margin-bottom:15px; border-bottom: 1px solid #161432;'></div>", unsafe_allow_html=True)

with tab2:
    st.header("🔬 Oráculo A&R e Ingeniería de Catálogo")
    st.info("Terminal lista para análisis lírico y generación de PDFs ejecutivos.")

with tab3:
    st.header("🤝 Estrategia para Mesa de Trabajo (Sony Music Publishing)")
    if st.button("📋 Generar Minuta de Reclamo Legal para Sony", type="primary"):
        st.markdown("### 📄 MEMORANDO DE RECLAMO FORMAL DE METADATA")
