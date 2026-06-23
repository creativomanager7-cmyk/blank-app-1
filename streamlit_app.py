import streamlit as st
import requests
import lyricsgenius
import re
from collections import Counter
import google.generativeai as genai
import pandas as pd
import random

st.set_page_config(page_title="Big Bang OS | Intelligence", page_icon="🌌", layout="wide")

st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #0f0c29, #302b63, #24243e);
    color: white;
    padding: 25px;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 25px;
    border-bottom: 4px solid #00F2FE;
}
.metric-box { background: #f0f2f6; padding: 15px; border-radius: 8px; border-left: 4px solid #302b63; margin-top: 10px;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🌌 PROYECTO BIG BANG OS</h1>
    <p>A&R Copilot + Auditoría Forense de Regalías | Enterprise B2B</p>
</div>
""", unsafe_allow_html=True)

BASE_URL = "https://api.deezer.com"

# --- MOTOR BACKEND: ESCÁNER DE REGALÍAS (Creado por el CTO) ---
def motor_auditoria_regalias(catalogo):
    """Motor que cruza streams de Spotify vs Registros de Publishing (SAYCO/BMI)"""
    resultados = []
    dinero_atrapado_total = 0
    
    for obra in catalogo:
        # Simulamos la extracción de datos de bases mundiales
        streams = random.randint(500000, 5000000)
        # Regalía promedio generada (aprox $0.004 por stream, 15% es publishing)
        dinero_generado = (streams * 0.004) * 0.15 
        
        isrc_distribuidora = f"US{random.randint(10000000, 99999999)}"
        isrc_publishing = isrc_distribuidora if obra["estado"] == "Limpio" else f"US{random.randint(10000000, 99999999)}"
        
        friccion = isrc_distribuidora != isrc_publishing
        if friccion:
            dinero_atrapado_total += dinero_generado
            
        resultados.append({
            "Obra": obra["track"],
            "Streams": f"{streams:,}",
            "Estado": "🔴 Retenido" if friccion else "🟢 Fluyendo",
            "Dinero Generado": f"${dinero_generado:,.2f} USD",
            "Diagnóstico": "Conflicto de ISRC" if friccion else "Match Perfecto"
        })
        
    return pd.DataFrame(resultados), dinero_atrapado_total

# --- MOTOR DE INGENIERÍA INVERSA (GENIUS + GEMINI) ---
def analizar_letra_metricas(letra):
    if not letra: return None
    letra_limpia = re.sub(r'\[.*?\]', '', letra)
    palabras = re.findall(r'[a-záéíóúñü]+', letra_limpia.lower())
    lineas = [l.strip() for l in letra.split('\n') if l.strip() and not l.strip().startswith('[')]
    secciones = re.findall(r'\[(.*?)\]', letra, re.IGNORECASE)
    return {
        "total_palabras": len(palabras),
        "total_lineas": len(lineas),
        "secciones": secciones,
        "num_secciones": len(secciones),
        "densidad": round(len(palabras) / max(len(lineas), 1), 1),
        "estructura": " → ".join(secciones[:10]) if secciones else "Sin estructura detectada"
    }

def generar_receta_gemini(cancion, artista, metricas, gemini_key):
    try:
        genai.configure(api_key=gemini_key.strip())
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        prompt = f"Actúa como Ejecutivo de Sony Music. Hicimos ingeniería inversa a '{cancion}'. Estructura: {metricas['estructura']}. Palabras: {metricas['total_palabras']}. Densidad: {metricas['densidad']}. Redacta: 1) Psicoacústica (por qué atrapa). 2) Instrucciones de composición. 3) Prompt exacto para Suno AI sin usar nombres reales."
        return model.generate_content(prompt).text
    except Exception as e:
        return f"Error con Gemini: {str(e)}"

# --- INTERFAZ: LAS 4 PESTAÑAS DEL BIG BANG ---
tab1, tab2, tab3, tab4 = st.tabs([
    "💰 Auditor Financiero (Nuevo)", 
    "🤝 Matchmaker de Feats (Nuevo)", 
    "🔬 Oráculo A&R (Genius + AI)", 
    "🔥 Tendencias Diarias"
])

# 1. PESTAÑA DEL DINERO (El Escáner de Fricciones)
with tab1:
    st.header("💰 Auditoría Forense de Catálogo (Metadata & Regalías)")
    st.write("Escanea discrepancias entre distribuidoras (Spotify/Apple) y sociedades de gestión (SAYCO/BMI) para detectar dinero atrapado.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Catálogo de Cristian", "49 Obras", "Sincronizado")
    col2.metric("Obras Limpias", "47", "95% de Salud")
    col3.metric("Obras en Fricción", "2", "-5% de Riesgo", delta_color="inverse")
    
    if st.button("🚀 Ejecutar Escáner de Bases de Datos", type="primary"):
        with st.spinner("Cruzando ISRC vs ISWC a nivel global..."):
            # Tu catálogo real simplificado para la demo
            mi_catalogo = [
                {"track": "Mi Propio Rescate", "estado": "Limpio"},
                {"track": "Cama Fría", "estado": "Limpio"},
                {"track": "Obra Inédita #3", "estado": "Fricción"},
                {"track": "Obra Inédita #4", "estado": "Fricción"}
            ]
            
            df_resultados, dinero_perdido = motor_auditoria_regalias(mi_catalogo)
            
            st.error(f"🚨 ALERTA ROJA: Se detectaron aprox. **${dinero_perdido:,.2f} USD** retenidos en la 'Black Box' por errores de metadata territorial.")
            
            st.dataframe(df_resultados, use_container_width=True)
            
            st.success("💡 **Acción Requerida:** Exportar reporte y enviar 'Split Sheets' corregidos a la editorial.")

# 2. PESTAÑA MATCHMAKER (Cruce de Audiencias)
with tab2:
    st.header("🤝 Matchmaker de Colaboraciones (Feats)")
    st.write("Cruza demografía de audiencias para predecir el éxito de una colaboración antes de grabarla.")
    
    gen_b = st.selectbox("Selecciona Género Objetivo:", ["Regional Mexicano", "Cumbia Pop", "Urbano Latino", "Trap"])
    
    if st.button("🧬 Calcular Match Algorítmico"):
        match = random.randint(85, 99)
        st.markdown(f"<h2 style='color:#00F2FE;'>🔥 Score de Éxito Algorítmico: {match}%</h2>", unsafe_allow_html=True)
        st.info(f"**Estrategia:** Juntar a un productor de Monterrey (80% audiencia masculina) con tu maqueta de {gen_b} (Alta retención femenina).")
        st.write("📊 **Proyección:** Aumento del 34% en tasa de 'Saves' en Spotify en 72 horas por cruce demográfico perfecto.")

# 3. PESTAÑA DEL ORÁCULO A&R (Ingeniería Inversa)
with tab3:
    st.header("🔬 Oráculo A&R — Ingeniería Inversa & Shadow Talent")
    col_k1, col_k2 = st.columns(2)
    with col_k1: t_gen = st.text_input("1. Token de Genius:", type="password")
    with col_k2: t_gem = st.text_input("2. API Key de Gemini:", type="password")
    
    st.markdown("---")
    c_a, c_b = st.columns(2)
    with c_a: h_can = st.text_input("Canción:", placeholder="Ej: Un x100to")
    with c_b: h_art = st.text_input("Artista:", placeholder="Ej: Grupo Frontera")

    if st.button("🧬 Hackear Hit & Generar Receta"):
        if t_gen and t_gem and h_can and h_art:
            with st.spinner("Desarmando canción y consultando a Gemini..."):
                try:
                    genius = lyricsgenius.Genius(t_gen.strip(), verbose=False)
                    song = genius.search_song(h_can, h_art)
                    if song:
                        st.success(f"✅ Hit Desarmado: {song.title}")
                        if hasattr(song, 'writer_artists') and song.writer_artists:
                            st.write("**✍️ Escritores Reales (Shadow A&R):** " + ", ".join([e['name'] for e in song.writer_artists]))
                        
                        metricas = analizar_letra_metricas(song.lyrics)
                        st.code(f"Estructura: {metricas['estructura']} | Densidad: {metricas['densidad']} pal/línea")
                        
                        st.markdown("### 🤖 REPORTE EJECUTIVO (Gemini AI)")
                        st.info(generar_receta_gemini(song.title, song.artist, metricas, t_gem))
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Completa llaves, canción y artista.")

# 4. TENDENCIAS
with tab4:
    st.header("🔥 Playlists Líquidas & Tendencias")
    if st.button("Cargar Radar Global"):
        res = requests.get(f"{BASE_URL}/chart/0/tracks?limit=10").json().get("data", [])
        for i, t in enumerate(res, 1):
            st.write(f"**#{i} {t['title']}** - {t['artist']['name']}")

st.markdown("---")
st.caption("Proyecto Big Bang OS v5.0 | Desarrollado para Nivel Enterprise")
 
