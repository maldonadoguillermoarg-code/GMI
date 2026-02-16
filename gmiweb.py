import streamlit as st
import datetime
import time
from PIL import Image
from streamlit_card import card

# 1. Configuración de página
st.set_page_config(layout="wide", page_title="GMI | Negocios Inmobiliarios")

# 2. Control de estado
if 'estado' not in st.session_state:
    st.session_state.estado = 'intro'

# --- ESTILOS GLOBALES (Respetando tus fuentes originales) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@700;800&family=Nunito+Sans:wght@400;600&display=swap');
    @import url('https://fonts.cdnfonts.com/css/seven-segment');

    h1, h2, h3, .section-title { font-family: 'Inter', sans-serif !important; letter-spacing: -0.02em !important; }
    p, div, span, label { font-family: 'Nunito Sans', sans-serif !important; }
    
    @keyframes blinker { 50% { opacity: 0.3; } }
    </style>
    """, unsafe_allow_html=True)

if st.session_state.estado == 'intro':
    # PANTALLA 1: INTRO NEGRA (Tu diseño original con el botón invisible)
    st.markdown("""
        <style>
        .stApp { background-color: #000000 !important; cursor: pointer; }
        .clock-container { text-align: center; width: 100%; margin-top: 30px; }
        .digital-timer {
            font-family: 'Seven Segment', sans-serif;
            color: #FF0000;
            font-size: clamp(45px, 10vw, 90px);
            text-shadow: 0 0 15px rgba(255, 0, 0, 0.7);
            letter-spacing: 5px;
            line-height: 1;
        }
        .labels-timer {
            color: #8B0000;
            letter-spacing: 12px;
            font-size: 14px;
            margin-top: 15px;
            font-weight: 800;
            text-transform: uppercase;
            margin-bottom: 80px; 
        }
        .click-instruction {
            color: #FF0000 !important;
            font-size: 22px !important;
            font-weight: 900 !important;
            letter-spacing: 4px;
            text-transform: uppercase;
            animation: blinker 1.5s linear infinite;
            text-shadow: -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000;
        }
        div.stButton { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 999; }
        div.stButton > button {
            width: 100% !important; height: 100% !important;
            background: transparent !important; border: none !important;
            color: transparent !important; cursor: pointer !important;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div style='text-align: center;'>
            <h1 style='font-size: 100px; margin-bottom: 0px; color: white;'>
                <span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span>
            </h1>
            <p style='letter-spacing: 8px; color: #333; font-size: 14px; font-weight: 800; margin-bottom: 30px;'>NEGOCIOS INMOBILIARIOS</p>
        </div>
        """, unsafe_allow_html=True)

    futuro = datetime.datetime(2026, 10, 31, 0, 0)
    ahora = datetime.datetime.now()
    dif = futuro - ahora
    dias, horas, resto = dif.days, divmod(dif.seconds, 3600)
    minutos, segundos = divmod(resto[1], 60)
    
    st.markdown(f"""
        <div class='clock-container'>
            <div class='digital-timer'>{dias:02d}:{resto[0]:02d}:{minutos:02d}:{segundos:02d}</div>
            <div class='labels-timer'>DÍAS HORAS MINUTOS SEGUNDOS</div>
            <p class='click-instruction'>HACÉ CLICK Y MIRÁ LOS AVANCES</p>
        </div>
        """, unsafe_allow_html=True)

    if st.button("Click Overlay"):
        st.session_state.estado = 'web'
        st.rerun()
    
    time.sleep(1)
    st.rerun()

else:
    # PANTALLA 2: WEB BLANCA (Con tus tipografías y tus imágenes locales)
    st.markdown("""
        <style>
        .stApp { background-color: #FFFFFF !important; }
        .logo-main { font-family: 'Inter', sans-serif; font-size: 80px; font-weight: 800; text-align: center; margin-top: 20px; color: #1a1a1a; }
        .subtitle-main { text-align: center; letter-spacing: 4px; color: #888; font-size: 14px; font-weight: 600; margin-bottom: 40px; }
        .section-title { text-align: center; color: #1a1a1a; font-size: 26px; font-weight: 800; letter-spacing: 10px; border-top: 1px solid #eee; padding-top: 30px; margin-bottom: 50px; }
        
        /* Ajuste para que el botón de volver use tu estilo original */
        .btn-volver > div.stButton > button {
            background-color: #1a1a1a !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 10px 25px !important;
            font-family: 'Nunito Sans', sans-serif !important;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div class='logo-main'><span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span></div>
        <div class='subtitle-main'>NEGOCIOS INMOBILIARIOS</div>
        <div class='section-title'>CATEGORÍAS</div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)

    # Función para renderizar tarjetas con tus imágenes locales
    def render_card(titulo, imagen_path, clave):
        try:
            # Intentamos cargar la imagen local para verificar que existe
            Image.open(imagen_path)
            card(
                title=titulo,
                text="Haz clic para ver más",
                image=imagen_path,
                styles={
                    "card": {
                        "width": "100%",
                        "height": "350px",
                        "border-radius": "12px",
                        "box-shadow": "0 0 10px rgba(0,0,0,0.1)",
                        "font-family": "Inter"
                    },
                    "title": {"font-family": "Inter", "font-weight": "800"},
                    "text": {"font-family": "Nunito Sans"}
                },
                key=clave
            )
        except:
            st.error(f"Falta {imagen_path}")

    with col1: render_card("DEPARTAMENTOS", "Deptos.jpeg", "c1")
    with col2: render_card("CASAS", "Casas.jpeg", "c2")
    with col3: render_card("TERRENOS", "Terreno.jpeg", "c3")

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("<div class='btn-volver'>", unsafe_allow_html=True)
    if st.button("← VOLVER AL INICIO"):
        st.session_state.estado = 'intro'
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)