import sys
sys.modules['librosa'] = None
sys.modules['scipy'] = None
import streamlit as st

# Configuración del servidor de Render para máxima anchura
st.set_page_config(page_title="Big Bang OS — HitLab AI Core", page_icon="🌌", layout="wide")

# Ocultar menús nativos de Streamlit para que parezca un software propietario y limpio
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div.block-container {padding: 0rem !important;}
</style>
""", unsafe_allow_html=True)

# --- EL NÚCLEO UNIFICADO (HITLAB AI + BIG BANG WORKSPACE) ---
# Inyectamos el HTML interactivo con JavaScript nativo para que corra fluido en el servidor
html_core = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Big Bang - HitLab AI Executive Dashboard</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Syne:wght@700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #05050A;
            --bg-card: #0F0F1C;
            --neon-green: #00FF88;
            --neon-purple: #BC13FE;
            --neon-red: #FF3333;
            --text-main: #ffffff;
            --text-muted: #A0A0C0;
            --font-title: 'Syne', sans-serif;
            --font-body: 'Space Grotesk', sans-serif;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            background-color: var(--bg-main);
            color: var(--text-main);
            font-family: var(--font-body);
            overflow: hidden;
            height: 100vh;
        }

        .dashboard-container { display: flex; height: 100vh; width: 100vw; }

        /* LADO IZQUIERDO: CLICKUP SIDEBAR */
        .left-panel {
            width: 35%;
            background: linear-gradient(180deg, #090912 0%, #05050A 100%);
            border-right: 1px solid rgba(188, 19, 254, 0.2);
            padding: 2rem;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
            overflow-y: auto;
        }

        .brand-header h1 {
            font-family: var(--font-title);
            font-size: 2.3rem;
            font-weight: 800;
            text-transform: uppercase;
            background: linear-gradient(45deg, var(--neon-purple), var(--neon-green));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -1px;
        }

        .brand-header p {
            color: var(--text-muted);
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-top: 2px;
        }

        .section-title {
            font-family: var(--font-title);
            font-size: 1.1rem;
            color: var(--text-main);
            border-left: 3px solid var(--neon-purple);
            padding-left: 0.5rem;
            margin-bottom: 0.5rem;
        }

        .drawer-container { display: flex; flex-direction: column; gap: 0.8rem; }

        .track-drawer {
            background-color: var(--bg-card);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 12px;
            padding: 1.2rem;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .track-drawer::before {
            content: ''; position: absolute; left: 0; top: 0; height: 100%; width: 4px;
        }

        .drawer-success::before { background-color: var(--neon-green); box-shadow: 0 0 10px var(--neon-green); }
        .drawer-alert::before { background-color: var(--neon-red); box-shadow: 0 0 10px var(--neon-red); }

        .track-drawer:hover {
            transform: translateX(6px);
            background: rgba(188, 19, 254, 0.08);
            border-color: rgba(188, 19, 254, 0.3);
        }

        .track-drawer.active {
            background: rgba(188, 19, 254, 0.12);
            border-color: var(--neon-purple);
            box-shadow: 0 0 20px rgba(188, 19, 254, 0.15);
        }

        .drawer-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem; }
        .drawer-title { font-size: 1.05rem; font-weight: 600; }
        .drawer-meta { font-size: 0.8rem; color: var(--text-muted); }
        .drawer-status-tag { font-size: 0.7rem; font-weight: 700; text-transform: uppercase; padding: 0.15rem 0.5rem; border-radius: 20px; }
        .tag-success { background: rgba(0, 255, 136, 0.1); color: var(--neon-green); }
        .tag-alert { background: rgba(255, 51, 51, 0.1); color: var(--neon-red); }

        /* LADO DERECHO: MUSO CREDITS + FORENSIC PACK */
        .right-panel {
            width: 65%; background-color: var(--bg-main); padding: 2.5rem; overflow-y: auto; display: flex; flex-direction: column; gap: 1.8rem;
        }

        .pitch-pack-header { display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 1.2rem; }
        .pitch-title h2 { font-family: var(--font-title); font-size: 2.4rem; line-height: 1.1; margin-bottom: 0.4rem; }
        
        .signal-badge {
            background: linear-gradient(135deg, #0F0F1C 0%, #05050A 100%);
            border: 2px solid var(--neon-green); box-shadow: 0 0 15px rgba(0, 255, 136, 0.2); border-radius: 14px; padding: 0.8rem; text-align: center; min-width: 110px;
        }
        .signal-value { font-family: var(--font-title); font-size: 2rem; color: var(--neon-green); font-weight: 800; display: block; }
        .signal-label { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted); }

        /* REPRODUCTOR ANIMADO "MUÑECO STYLE" */
        .player-showcase { background: #0F0F1C; border-radius: 14px; padding: 1.2rem; position: relative; border: 1px solid rgba(188, 19, 254, 0.15); }
        .animation-track { height: 60px; width: 100%; background: rgba(0, 0, 0, 0.3); border-radius: 8px; position: relative; margin-bottom: 1rem; overflow: hidden; border-bottom: 1px dashed rgba(255, 255, 255, 0.08); }
        
        .avatar-muñeco {
            position: absolute; bottom: 8px; left: 0%; font-size: 2.2rem; transition: left 0.1s linear; transform: translateX(-50%); filter: drop-shadow(0 0 8px var(--neon-purple));
        }

        .player-controls { display: flex; align-items: center; gap: 1.2rem; }
        .play-btn { background: var(--neon-purple); border: none; color: white; width: 44px; height: 44px; border-radius: 50%; font-size: 1.1rem; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: transform 0.2s; }
        .play-btn:hover { transform: scale(1.08); background: #cc3efd; }
        .timeline-container { flex-grow: 1; display: flex; flex-direction: column; gap: 0.3rem; }
        .timeline-bar { width: 100%; height: 5px; background: rgba(255, 255, 255, 0.08); border-radius: 3px; position: relative; cursor: pointer; }
        .timeline-progress { height: 100%; width: 0%; background: linear-gradient(90deg, var(--neon-purple), var(--neon-green)); border-radius: 3px; }
        .time-labels { display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--text-muted); }

        /* GRID DE INTELIGENCIA DE DATOS DE HITLAB AI */
        .data-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.2rem; }
        .data-card { background-color: var(--bg-card); border-radius: 12px; padding: 1.2rem; border: 1px solid rgba(255, 255, 255, 0.02); }
        .card-header-small { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; color: var(--neon-purple); margin-bottom: 0.6rem; font-weight: 600; }
        .archetype-box { font-size: 1.2rem; font-weight: 700; color: var(--text-main); }
        .hook-text { font-style: italic; color: var(--neon-green); border-left: 2px solid var(--neon-green); padding-left: 0.8rem; margin-top: 0.5rem; font-size: 0.9rem; }

        /* SECCIÓN DE NEGOCIO Y ACUERDO EDITORIAL (TRANSPARENCIA TOTAL) */
        .business-panel { background: rgba(15, 15, 28, 0.6); border: 1px solid rgba(0, 255, 136, 0.08); border-radius: 12px; padding: 1.2rem; }
        .split-row { display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.04); font-size: 0.9rem; }
        .split-row:last-child { border-bottom: none; }
        .fee-highlight { color: var(--neon-green); font-weight: 700; }
    </style>
</head>
<body>

    <div class="dashboard-container">
        
        <div class="left-panel">
            <div class="brand-header">
                <h1>Big Bang</h1>
                <p>HitLab AI Integrated Ecosystem</p>
            </div>
            
            <div class="section-title">Catálogo / Monitor de Fricción</div>
            
            <div class="drawer-container">
                <div class="track-drawer drawer-success active" id="track1" onmouseenter="loadTrackData(1)">
                    <div class="drawer-header">
                        <span class="drawer-title">Mi Propio Rescate</span>
                        <span class="drawer-status-tag tag-success">HitLab Ready</span>
                    </div>
                    <div class="drawer-meta">Bachata / Regional • Split 100% Ok</div>
                </div>

                <div class="track-drawer drawer-success" id="track2" onmouseenter="loadTrackData(2)">
                    <div class="drawer-header">
                        <span class="drawer-title">¿Dónde Estabas Tú?</span>
                        <span class="drawer-status-tag tag-success">HitLab Ready</span>
                    </div>
                    <div class="drawer-meta">Norteño Banda • Catálogo Validado</div>
                </div>

                <div class="track-drawer drawer-alert" id="track3" onmouseenter="loadTrackData(3)">
                    <div class="drawer-header">
                        <span class="drawer-title">El Agropecuario</span>
                        <span class="drawer-status-tag tag-alert">Reclamación</span>
                    </div>
                    <div class="drawer-meta">Cumbia Regional • Auditoría Regalías</div>
                </div>

                <div class="track-drawer drawer-alert" id="track4" onmouseenter="loadTrackData(4)">
                    <div class="drawer-header">
                        <span class="drawer-title">Mi Debilidad</span>
                        <span class="drawer-status-tag tag-alert">Contrato</span>
                    </div>
                    <div class="drawer-meta">Regional Pop • Sony Pubcol Restructure</div>
                </div>
            </div>
        </div>

        <div class="right-panel">
            <div class="pitch-pack-header">
                <div class="pitch-title">
                    <p style="color: var(--neon-purple); font-weight: 600; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 1px;">HitLab Pitch Pack Inteligente</p>
                    <h2 id="display-title">Mi Propio Rescate</h2>
                    <p id="display-genre" style="color: var(--text-muted);">Bachata Regional • Arquetipo Femenino Empoderado</p>
                </div>
                <div class="signal-badge">
                    <span class="signal-value" id="display-score">94%</span>
                    <span class="signal-label">Signal Score</span>
                </div>
            </div>

            <div class="player-showcase">
                <div class="animation-track">
                    <div class="avatar-muñeco" id="muñeco">💃</div>
                </div>
                
                <div class="player-controls">
                    <button class="play-btn" id="playBtn" onclick="togglePlayback()">▶</button>
                    <div class="timeline-container">
                        <div class="timeline-bar" onclick="seekTrack(event)">
                            <div class="timeline-progress" id="progressLine"></div>
                        </div>
                        <div class="time-labels">
                            <span id="time-current">0:00</span>
                            <span id="time-total">2:45</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="data-grid">
                <div class="data-card">
                    <div class="card-header-small">Target & Compatibilidad Vocal</div>
                    <div class="archetype-box" id="display-artist">Nicole Vega / Perfil Similar</div>
                    <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.5rem;" id="display-vocal">Vocal Fit Analysis: 95% afinidad tímbrica con frecuencias de alta retención.</p>
                </div>

                <div class="data-card">
                    <div class="card-header-small">Núcleo Emocional & Retención</div>
                    <div class="archetype-box" id="display-emotion">Empoderamiento / Ruptura</div>
                    <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.5rem;">Focalización territorial prioritaria: Colombia, México y USA Latino.</p>
                </div>

                <div class="data-card" style="grid-column: span 2;">
                    <div class="card-header-small">Activación Algorítmica TikTok / Reels (Gancho 0-3 Segundos)</div>
                    <p style="font-weight: 600; font-size: 0.9rem;">Frase de alto impacto predictivo:</p>
                    <div class="hook-text" id="display-hook">"Ya no me fío de tus palabras raras, encontré mi propio rescate..."</div>
                </div>
            </div>

            <div class="business-panel">
                <div class="section-title" style="margin-bottom: 0.8rem;">Estructura de Negocio & Editorial (Sony Music Pub)</div>
                <div class="split-row">
                    <span>Derechos Editoriales (Publishing)</span>
                    <span style="font-weight: 600; color: white;">100% Administrado por Sony Pubcol</span>
                </div>
                <div class="split-row">
                    <span>Split Sheet de Compositores</span>
                    <span id="display-composers" style="color: var(--text-muted);">Cristian Álvarez (50%) / Co-autores (50%)</span>
                </div>
                <div class="split-row">
                    <span>Tech Fee - HitLab Platform</span>
                    <span class="fee-highlight">3.5% sobre regalías del Máster</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        const tracksData = {
            1: { title: "Mi Propio Rescate", genre: "Bachata Regional • Arquetipo Femenino", score: "94%", avatar: "💃", artist: "Nicole Vega / Perfil Similar", vocal: "Vocal Fit Analysis: 95% afinidad tímbrica.", emotion: "Empoderamiento / Ruptura", hook: '"Ya no me fío de tus palabras raras, encontré mi propio rescate..."', composers: "Cristian Álvarez (50%) / Colaboradores (50%)", duration: 165 },
            2: { title: "¿Dónde Estabas Tú?", genre: "Norteño Banda • Despecho Activo", score: "92%", avatar: "🤠", artist: "Jessi Uribe / Pipe Bueno Type", vocal: "Alineación tonal perfecta para rangos de música popular.", emotion: "Despecho / Reclamo Directo", hook: '"¿Dónde estabas tú cuando las noches frías cobraban factura? Ahora no vengas..."', composers: "Cristian Álvarez (100%)", duration: 190 },
            3: { title: "El Agropecuario", genre: "Cumbia Regional • Ritmo Comercial", score: "89%", avatar: "🚜", artist: "Joaquin Guiller / Arquetipo Fiesta", vocal: "Alerta de Auditoría: Sincronización de regalías pendientes.", emotion: "Fiesta / Identidad de Campo", hook: '"Con las botas llenas de barro pero los bolsillos llenos de orgullo..."', composers: "Cristian Álvarez (40%) / Co-autores (60%)", duration: 180 },
            4: { title: "Mi Debilidad", genre: "Regional Pop • Balada Evolucionada", score: "91%", avatar: "💔", artist: "Nicole Vega / Crossover", vocal: "Restructuración contractual Sony Pubcol sugerida.", emotion: "Vulnerabilidad / Desamor", hook: '"Tú sigues siendo mi debilidad, aunque sé que me rompes el alma al volver..."', composers: "Cristian Álvarez (70%) / Sony Catálogo (30%)", duration: 210 }
        };

        let currentTrackId = 1; let isPlaying = false; let playInterval; let currentTime = 0;

        function loadTrackData(id) {
            document.querySelectorAll('.track-drawer').forEach(drawer => drawer.classList.remove('active'));
            document.getElementById(`track${id}`).classList.add('active');
            currentTrackId = id; const data = tracksData[id];
            document.getElementById('display-title').innerText = data.title;
            document.getElementById('display-genre').innerText = data.genre;
            document.getElementById('display-score').innerText = data.score;
            document.getElementById('muñeco').innerText = data.avatar;
            document.getElementById('display-artist').innerText = data.artist;
            document.getElementById('display-vocal').innerText = data.vocal;
            document.getElementById('display-emotion').innerText = data.emotion;
            document.getElementById('display-hook').innerText = data.hook;
            document.getElementById('display-composers').innerText = data.composers;
            resetPlayer(data.duration);
        }

        function togglePlayback() {
            const btn = document.getElementById('playBtn');
            if (isPlaying) { isPlaying = false; btn.innerText = "▶"; clearInterval(playInterval); }
            else { isPlaying = true; btn.innerText = "⏸"; const maxDuration = tracksData[currentTrackId].duration;
                playInterval = setInterval(() => { currentTime++; if (currentTime > maxDuration) { resetPlayer(maxDuration); } else { updatePlayerUI(maxDuration); } }, 1000);
            }
        }

        function resetPlayer(duration) { isPlaying = false; clearInterval(playInterval); currentTime = 0; document.getElementById('playBtn').innerText = "▶"; updatePlayerUI(duration); }

        function updatePlayerUI(maxDuration) {
            const progressPercent = (currentTime / maxDuration) * 100;
            document.getElementById('progressLine').style.width = `${progressPercent}%`;
            document.getElementById('muñeco').style.left = `${progressPercent}%`;
            document.getElementById('time-current').innerText = formatTime(currentTime);
            document.getElementById('time-total').innerText = formatTime(maxDuration);
        }

        function seekTrack(event) {
            const bar = event.currentTarget; const clickX = event.offsetX; const width = bar.offsetWidth;
            const percentage = clickX / width; const maxDuration = tracksData[currentTrackId].duration;
            currentTime = Math.floor(percentage * maxDuration); updatePlayerUI(maxDuration);
        }

        function formatTime(seconds) { const mins = Math.floor(seconds / 60); const secs = seconds % 60; return `${mins}:${secs < 10 ? '0' : ''}${secs}`; }
    </script>
</body>
</html>
"""

# Renderizamos la interfaz líquida en vivo ocupando todo el contenedor de la pantalla de Render
st.components.v1.html(html_core, height=900, scrolling=False)
