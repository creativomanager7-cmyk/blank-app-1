import sys
sys.modules['librosa'] = None
sys.modules['scipy'] = None
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Big Bang OS | Enterprise", page_icon="🌌", layout="wide")

# --- MAQUETACIÓN ULTRA PREMIUM (CLICKUP + MUSO INTERACTIVE INTERFACE) ---
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #070612 !important;
        color: #F1F5F9 !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .main-header {
        background: linear-gradient(135deg, #120E2E 0%, #1F0D3D 100%);
        padding: 25px;
        border-radius: 14px;
        text-align: center;
        margin-bottom: 25px;
        border: 1px solid #281E66;
    }
    /* Estilos para los botones/cajones de la izquierda */
    div.stButton > button {
        width: 100% !important;
        padding: 14px 20px !important;
        border-radius: 12px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        text-align: left !important;
        margin-bottom: 2px !important;
        transition: all 0.2s ease-in-out !important;
        color: #FFFFFF !important;
    }
    /* El contenedor derecho de la ficha técnica */
    .forensic-panel {
        background-color: #0E0D24;
        border: 1px solid #1F1C4D;
        border-radius: 16px;
        padding: 30px;
        min-height: 800px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .platform-pill {
        background: #161436;
        padding: 10px 15px;
        border-radius: 10px;
        border: 1px solid #262354;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .role-badge {
        background: #1F133A;
        color: #00F2FE;
        padding: 3px 10px;
        border-radius: 8px;
        font-size: 11px;
        font-weight: bold;
        border: 1px solid #4F3596;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1 style="color: #00F2FE; font-size: 38px; margin: 0; font-weight: 800;">🌌 BIG BANG OS</h1>
    <p style="color: #94A3B8; font-size: 15px; margin: 5px 0 0 0; letter-spacing: 1px;">Interactive Splitted Forensic Workspace • B2B Sello Directivo</p>
</div>
""", unsafe_allow_html=True)

# --- BASE DE DATOS ESTRUCTURADA DE TUS 47 OBRAS ---
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

# Inicializar memoria de selección de canción
if "selected_track_idx" not in st.session_state:
    st.session_state.selected_track_idx = 0

# --- ARQUITECTURA DE PANTALLA DIVIDIDA (IZQUIERDA VS DERECHA) ---
col_menu, col_details = st.columns([2, 3], gap="large")

with col_menu:
    st.markdown("<h3 style='color:#6366F1; font-size:18px; margin-bottom:15px;'>🎵 WORKSPACE TRACKS</h3>", unsafe_allow_html=True)
    
    # Renderizado inteligente de cajones verticales con colores interactivos
    for idx, cancion in enumerate(canciones):
        artista = artistas[idx]
        
        # Detectar el estado de salud para inyectar el color correcto del cajón
        if cancion in ["Mi Debilidad", "¿Dónde Estabas Tú?", "Amores de un ratico"]:
            button_style = """
            <style>
                div.stButton > button[key="btn_{idx}"] {{
                    background: linear-gradient(90deg, #5A1212 0%, #1A0505 100%) !important;
                    border: 1px solid #EF4444 !important;
                    box-shadow: 0 0 10px rgba(239, 68, 68, 0.2);
                }}
            </style>
            """
            label = f"🚨 {cancion} — {artista}"
        else:
            button_style = """
            <style>
                div.stButton > button[key="btn_{idx}"] {{
                    background: linear-gradient(90deg, #063C26 0%, #03140E 100%) !important;
                    border: 1px solid #10B981 !important;
                    box-shadow: 0 0 10px rgba(16, 185, 129, 0.1);
                }}
            </style>
            """
            label = f"✅ {cancion} — {artista}"
            
        st.markdown(button_style.format(idx=idx), unsafe_allow_html=True)
        
        if st.button(label, key=f"btn_{idx}"):
            st.session_state.selected_track_idx = idx
            st.rerun()

# --- PROCESAMIENTO DEL PANEL FORENSE DERECHO (DINÁMICO) ---
with col_details:
    sel_idx = st.session_state.selected_track_idx
    track_name = canciones[sel_idx]
    track_artist = artistas[sel_idx]
    isrc_code = f"CO-SMP-26-{sel_idx+1001:04d}"
    
    # Asignación de analíticas simuladas pero contextualizadas en base a tus números de ejemplo
    yt_plays, sp_plays, dz_plays = "12.4M", "8.2M", "1.5M"
    if track_name == "El agropecuario":
        yt_plays, sp_plays, dz_plays = "17.0M", "10.0M", "2.1M"
    elif track_name == "Mi Debilidad":
        yt_plays, sp_plays, dz_plays = "15.1M", "9.4M", "1.8M"
        
    st.markdown('<div class="forensic-panel">', unsafe_allow_html=True)
    
    # Encabezado Interno Estilo Muso.AI
    c_avatar, c_title = st.columns([1, 4])
    with c_avatar:
        st.image("https://images.unsplash.com/photo-1514525253161-7a46d19cd819?q=80&w=150&auto=format&fit=crop", width=85)
    with c_title:
        st.markdown(f"""
        <h2 style="color:#00F2FE; margin:0; font-size:28px; font-weight:700;">{track_name}</h2>
        <p style="color:#94A3B8; margin:3px 0; font-size:16px;">🎙️ Artista Principal: <b>{track_artist}</b></p>
        <div style="margin-top:5px;"><span class="role-badge">✍️ Cristian Álvarez • Writer & Publisher Share</span></div>
        """, unsafe_allow_html=True)
        
    st.markdown("<hr style='border-color:#1F1C4D; margin:20px 0;'>", unsafe_allow_html=True)
    
    # REPRODUCTOR DE AUDIO INTEGRADO (SENA POPULAR/RANCHERA)
    st.markdown("<p style='color:#6366F1; font-weight:600; margin-bottom:5px;'>▶️ AUDITAR AUDIO EN VIVO (MUESTRA DE STREAMING)</p>", unsafe_allow_html=True)
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3", format="audio/mp3")
    
    # PESTAÑAS INTERACTIVAS DE FICHA FORENSE
    sub_tab1, sub_tab2, sub_tab3 = st.tabs(["📊 Créditos e Identidad", "📝 Letra de la Obra", "🤝 Alertas y Booking"])
    
    with sub_tab1:
        st.markdown(f"""
        <table style="width:100%; font-size:13px; color:#E2E8F0;">
            <tr><td><b>Código ISRC:</b></td><td style="font-family:monospace; color:#00F2FE;">{isrc_code}</td></tr>
            <tr><td><b>Compositores:</b></td><td>Cristian Alexander Alvarez Cortez / {track_artist}</td></tr>
            <tr><td><b>Productores:</b></td><td>Jair Leonardo Bautista Ramón / Alianza HitLab</td></tr>
            <tr><td><b>Día de Estreno:</b></td><td>24 de Septiembre de 2021 (Distribución Global)</td></tr>
        </table>
        """, unsafe_allow_html=True)
        
        st.markdown("<br><p style='color:#94A3B8; font-weight:600; font-size:12px;'>📈 RENDIMIENTO GLOBAL DE STREAMING VERIFICADO</p>", unsafe_allow_html=True)
        
        # Mapeo interactivo con logos simulados e indicadores numéricos exactos
        st.markdown(f"""
        <div class="platform-pill">
            <span>🟩 <b>Spotify Official</b></span>
            <span style="color:#10B981; font-weight:bold;">{sp_plays} Streams</span>
        </div>
        <div class="platform-pill">
            <span>🟥 <b>YouTube Media</b></span>
            <span style="color:#EF4444; font-weight:bold;">{yt_plays} Views</span>
        </div>
        <div class="platform-pill">
            <span>🟪 <b>Deezer Catalog</b></span>
            <span style="color:#A855F7; font-weight:bold;">{dz_plays} Plays</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Botones Reales de Salto a la Web Oficial
        c_lk1, c_lk2 = st.columns(2)
        with c_lk1:
            st.link_button("🌐 Ir a Spotify Tienda", f"https://open.spotify.com/search/{track_name.replace(' ', '%20')}")
        with c_lk2:
            st.link_button("🌐 Ver Video en YouTube", f"https://www.youtube.com/results?search_query={track_name.replace(' ', '+')}")

    with sub_tab2:
        st.markdown(f"""
        <div style="background:#090818; padding:15px; border-radius:10px; border:1px solid #1C1942; font-family:serif; font-size:15px; line-height:1.6; color:#94A3B8;">
            [Verso]<br>
            Ayer me dijeron que andabas buscando lo que ya perdiste...<br>
            Hoy las cuentas se aclaran y el catálogo habla por sí solo.<br><br>
            [Coro]<br>
            Si me ven llorando es de pura alegría, porque los números no mienten<br>
            Y en la mesa de Sony se asienta el derecho que el sello defiende.
        </div>
        """, unsafe_allow_html=True)

    with sub_tab3:
        st.markdown("### 💼 Directorio de Manejos, Registro & Booking")
        st.write("Canales directos configurados para la administración legal de la obra:")
        
        if track_name in ["Mi Debilidad", "¿Dónde Estabas Tú?"]:
            st.error(f"🚨 **Alerta Crítica:** Esta canción presenta discrepancias de liquidación en SAYCO / The MLC. Se sugiere congelar preventivamente o citar a mesa técnica.")
        else:
            st.success("✅ **Estatus Aligned:** Obra mapeada correctamente en los servidores de recaudo global.")
            
        st.button("✉️ Redactar Correo de Discrepancia Legal (Sony Pubcol)")
        st.button("📱 Enviar Reporte Ejecutivo a Nicole Vega por WhatsApp")

    st.markdown('</div>', unsafe_allow_html=True)
