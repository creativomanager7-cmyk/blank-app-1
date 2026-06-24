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

# --- MAQUETACIÓN ESTÉTICA DE ALTA GAMA (DARK VIP INTERFACE) ---
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #080711 !important;
        color: #E2E8F0 !important;
    }
    .main-header {
        background: linear-gradient(135deg, #1E1B4B 0%, #311042 100%);
        padding: 35px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 30px;
        border: 1px solid #4338CA;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .kpi-card {
        background: #111022;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #06B6D4;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .track-card {
        background: #121124;
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #23214A;
        margin-bottom: 10px;
    }
    .badge-green { background: #065F46; color: #34D399; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: bold; }
    .badge-red { background: #7F1D1D; color: #FCA5A5; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: bold; }
    .badge-yellow { background: #78350F; color: #FCD34D; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1 style="color: #00F2FE; font-size: 42px; margin-bottom: 5px; font-family: 'Helvetica Neue', sans-serif;">🌌 BIG BANG OS</h1>
    <p style="color: #94A3B8; font-size: 18px; letter-spacing: 1px;">A&R Copilot & Digital Royalty Forensic Suite • B2B Enterprise</p>
</div>
""", unsafe_allow_html=True)

# --- BASE DE DATOS REAL DE CRISTIAN ÁLVAREZ ---
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
    "📊 Bóveda de Control Forense", "🔬 Oráculo Inteligente A&R", "🤝 Mesa de Negociación Sony"
])

with tab1:
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown('<div class="kpi-card"><p style="color:#94A3B8; margin:0;">Tracks Protegidos</p><h2 style="color:#00F2FE; margin:0;">47 Works</h2></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="kpi-card" style="border-left-color:#F59E0B;"><p style="color:#94A3B8; margin:0;">Alertas en Caja Negra</p><h2 style="color:#F59E0B; margin:0;">21 Fricciones</h2></div>', unsafe_allow_html=True)
    with col_c:
        st.markdown('<div class="kpi-card" style="border-left-color:#EF4444;"><p style="color:#94A3B8; margin:0;">Estatus General</p><h2 style="color:#EF4444; margin:0;">Mesa de Trabajo</h2></div>', unsafe_allow_html=True)
        
    st.markdown("<br><h3 style='color:#6366F1;'>🧬 Despliegue de Control Territorial Estructural</h3>", unsafe_allow_html=True)
    
    for i, cancion in enumerate(canciones):
        artista = artistas[i]
        isrc = f"CO-SMP-26-{i+1001:04d}"
        
        if cancion == "Mi Debilidad" and artista == "Francy":
            exe_b = '<span class="badge-red">🔴 Conflicto de Reclamación</span>'
            mec_b = '<span class="badge-yellow">🚨 Publisher Share Volátil</span>'
            say_b = "⚠️ Retención Directa por Coautorías"
        elif cancion == "¿Dónde Estabas Tú?" and artista == "Paola Jara":
            exe_b = '<span class="badge-red">🔴 Conflicto de Reclamación</span>'
            mec_b = '<span class="badge-red">🔴 Retenido Territorial</span>'
            say_b = "❌ Fondos Congelados en Caja Negra"
        elif cancion == "Amores de un ratico" and artista == "Sofi Piñan":
            exe_b = '<span class="badge-green">🟢 Reclamado</span>'
            mec_b = '<span class="badge-yellow">🚨 Alerta: Publisher Share?</span>'
            say_b = "⚠️ Pendiente Conciliación"
        elif cancion == "La bandida" and artista == "Hanna Rivas":
            exe_b = '<span class="badge-green">🟢 Reclamado</span>'
            mec_b = '<span class="badge-green">🟢 Aligned</span>'
            say_b = "✅ Liquidado Estricto"
        elif "Nicol Vega" in artista or "Joaquin Guiller" in artista or "Jhon Alex" in artista:
            exe_b = '<span class="badge-green">🟢 Reclamado</span>'
            mec_b = '<span class="badge-yellow">🚨 Alerta: Verificar Historial</span>'
            say_b = "⚠️ Auditoría de Distribución Activa"
        else:
            exe_b = '<span class="badge-green">🟢 Reclamado</span>'
            mec_b = '<span class="badge-green">🟢 Aligned</span>'
            say_b = "✅ Sincronizado Completamente"
            
        # Diseño Estructural Con Carátula Optimizada (Fila por Canción)
        st.markdown(f'<div class="track-card">', unsafe_allow_html=True)
        
        c_img, c_info, c_alerts = st.columns([1, 4, 4])
        
        with c_img:
            # Placeholder Estético de Carátula (Disco de vinilo / Álbum VIP)
            st.image("https://images.unsplash.com/photo-1539635278303-d4002c07eae3?q=80&w=200&auto=format&fit=crop", use_container_width=True)
            
        with c_info:
            st.markdown(f"""
            <h4 style="color:#00F2FE; margin:0; font-size:20px;">{cancion}</h4>
            <p style="color:#94A3B8; margin:5px 0 0 0; font-size:14px;">🎙️ Artista: <b>{artista}</b></p>
            <p style="color:#64748B; margin:2px 0 0 0; font-size:11px;">🆔 ISRC: {isrc}</p>
            """, unsafe_allow_html=True)
            
        with c_alerts:
            st.markdown(f"""
            <div style="font-size:13px; margin-top:5px;">
                <div style="margin-bottom:4px;"><b>Ejecución:</b> {exe_b}</div>
                <div style="margin-bottom:4px;"><b>Mecánica:</b> {mec_b}</div>
                <div><b>SAYCO:</b> <span style="color:#94A3B8;">{say_b}</span></div>
            </div>
            """, unsafe_allow_html=True)
            
        # Fila de Botones Nativos de Verificación Segura e Interactivos
        st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
        c_btn1, c_btn2, _ = st.columns([1.5, 1.5, 5])
        with c_btn1:
            st.link_button("🟩 Spotify Audit", f"https://open.spotify.com/search/{cancion.replace(' ', '%20')}%20{artista.replace(' ', '%20')}", use_container_width=True)
        with c_btn2:
            st.link_button("🟥 YouTube Video", f"https://www.youtube.com/results?search_query={cancion.replace(' ', '+')}+{artista.replace(' ', '+')}", use_container_width=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.header("🔬 Oráculo A&R e Ingeniería de Catálogo")
    st.info("Ingresa tus llaves operacionales en la terminal para habilitar auditorías profundas.")

with tab3:
    st.header("🤝 Estrategia para Mesa de Trabajo (Sony Music Publishing)")
    if st.button("📋 Generar Minuta de Reclamo Legal para Sony", type="primary"):
        st.markdown("### 📄 MEMORANDO DE RECLAMO FORMAL DE METADATA")
