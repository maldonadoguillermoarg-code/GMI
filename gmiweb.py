import streamlit as st
import datetime
import time
import base64

# 1. Configuración de página
st.set_page_config(layout="wide", page_title="GMI | Negocios Inmobiliarios")

# 2. Control de estado
if 'estado' not in st.session_state:
    st.session_state.estado = 'intro'
if 'categoria_actual' not in st.session_state:
    st.session_state.categoria_actual = None

# Función para convertir archivos a Base64
def get_file_base64(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

# CARGA DE ASSETS
ricoso_b64 = get_file_base64("ricoso.gif")
pepinillo_b64 = get_file_base64("pepinillo.gif")
audio_b64 = get_file_base64("Ricoo.mp3")

# --- ESTILOS GLOBALES ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&family=Nunito+Sans:wght@300;400;600&display=swap');
    @import url('https://fonts.cdnfonts.com/css/seven-segment');

    html, body {{ scrollbar-width: none; }}
    body::-webkit-scrollbar {{ display: none; }}
    
    @keyframes blinker {{ 50% {{ opacity: 0.1; }} }}

    @keyframes dvdBounce {{
        0%   {{ top: 0%; left: 0%; transform: rotate(0deg); }}
        25%  {{ top: 85%; left: 10%; transform: rotate(90deg); }}
        50%  {{ top: 5%; left: 80%; transform: rotate(180deg); }}
        75%  {{ top: 80%; left: 40%; transform: rotate(270deg); }}
        100% {{ top: 0%; left: 0%; transform: rotate(360deg); }}
    }}

    .pepinillo-dvd {{ position: fixed; width: 140px; z-index: 10000; animation: dvdBounce 14s linear infinite; pointer-events: none; }}
    .ricoso-fijo {{ position: fixed; bottom: 0; right: 0; width: 160px; z-index: 10001; pointer-events: none; }}

    /* Estilo del Botón Ponte Rickoso! */
    .music-control {{
        position: fixed;
        top: 25px;
        right: 25px;
        z-index: 10005;
        background: linear-gradient(45deg, #ff0000, #8b0000);
        color: white;
        padding: 12px 24px;
        border-radius: 5px;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        cursor: pointer;
        box-shadow: 0 0 20px rgba(255,0,0,0.4);
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }}
    .music-control:hover {{
        transform: scale(1.05);
        box-shadow: 0 0 30px rgba(255,0,0,0.6);
    }}
    </style>

    <div class="pepinillo-dvd"><img src="data:image/gif;base64,{pepinillo_b64}" width="100%"></div>
    <div class="ricoso-fijo"><img src="data:image/gif;base64,{ricoso_b64}" width="100%"></div>
    """, unsafe_allow_html=True)

# REPRODUCTOR Y LÓGICA RICKOSA
if audio_b64:
    st.markdown(f"""
        <audio id="audioRicoo" loop>
            <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
        </audio>
        
        <div id="musicBtn" class="music-control" onclick="toggleMusic()">
            🚀 Ponte Rickoso!
        </div>

        <script>
            function toggleMusic() {{
                var audio = document.getElementById("audioRicoo");
                var btn = document.getElementById("musicBtn");
                if (audio.paused) {{
                    audio.play();
                    btn.innerHTML = "🔇 Silenciar";
                    btn.style.background = "#333";
                }} else {{
                    audio.pause();
                    btn.innerHTML = "🚀 Ponte Rickoso!";
                    btn.style.background = "linear-gradient(45deg, #ff0000, #8b0000)";
                }}
            }}
        </script>
        """, unsafe_allow_html=True)

# --- PANTALLAS ---
if st.session_state.estado == 'intro':
    st.markdown("<style>.stApp { background-color: #000000 !important; }</style>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; margin-top: 5vh;'><h1 style='font-size: 100px; margin-bottom: 0px; color: white;'><span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span></h1><p style='letter-spacing: 8px; color: #333; font-size: 14px; font-weight: 800; margin-bottom: 50px;'>NEGOCIOS INMOBILIARIOS</p></div>", unsafe_allow_html=True)

    # RELOJ
    futuro = datetime.datetime(2026, 10, 31, 0, 0)
    dif = futuro - datetime.datetime.now()
    d, h, res = dif.days, *divmod(dif.seconds, 3600)
    m, s = divmod(res, 60)
    
    st.markdown(f"""
        <div style="text-align: center;">
            <div style="font-family: 'Seven Segment'; color: #FF0000; font-size: 90px; text-shadow: 0 0 15px rgba(255,0,0,0.7); letter-spacing: 5px;">
                {d:02d}:{h:02d}:{m:02d}:{s:02d}
            </div>
            <div style="color: #8B0000; letter-spacing: 12px; font-size: 14px; font-weight: 800; text-transform: uppercase; margin-top: 15px;">
                DÍAS HORAS MINUTOS SEGUNDOS
            </div>
            <div style="color: #FF0000; font-family: 'Inter'; font-weight: 900; font-size: 20px; letter-spacing: 3px; margin-top: 40px; animation: blinker 1.2s linear infinite;">
                >>> MIRA LOS AVANCES DE NUESTRA WEB <<<
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Botón invisible para entrar
    st.markdown('<style>div.stButton > button { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: transparent !important; border: none !important; color: transparent !important; z-index: 999; }</style>', unsafe_allow_html=True)
    if st.button("ENTER"):
        st.session_state.estado = 'web'
        st.rerun()
    
    time.sleep(1)
    st.rerun()

elif st.session_state.estado == 'web':
    st.markdown("<style>.stApp { background-color: #f4f4f2 !important; }</style>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; padding-top: 20px;'><div style='font-family: \"Inter\"; font-size: 60px; font-weight: 800; color: #1a1a1a;'><span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span></div><div style='letter-spacing: 5px; color: #888; font-size: 12px; font-weight: 600; margin-bottom: 40px;'>NEGOCIOS INMOBILIARIOS</div></div>", unsafe_allow_html=True)
    
    st.write("### 🏠 Catálogo de Propiedades")
    st.info("Hacé clic en 'Ponte Rickoso!' arriba a la derecha para musicalizar la búsqueda.")
    
    if st.button("← VOLVER AL INICIO"):
        st.session_state.estado = 'intro'
        st.rerun()