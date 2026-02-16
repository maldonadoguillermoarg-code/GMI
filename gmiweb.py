import streamlit as st
import datetime
import time
from PIL import Image

# 1. Configuración de página
st.set_page_config(layout="wide", page_title="GMI | Negocios Inmobiliarios")

# 2. Control de estado
if 'estado' not in st.session_state:
    st.session_state.estado = 'intro'

# --- ESTILOS GLOBALES ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@700;800&family=Nunito+Sans:wght@400;600&display=swap');
    @import url('https://fonts.cdnfonts.com/css/seven-segment');

    h1, h2, h3, .section-title { font-family: 'Inter', sans-serif !important; letter-spacing: -0.02em !important; }
    p, div, span, label { font-family: 'Nunito Sans', sans-serif !important; }
    </style>
    """, unsafe_allow_html=True)

if st.session_state.estado == 'intro':
    # PANTALLA 1: INTRO NEGRA INTERACTIVA
    st.markdown("""
        <style>
        .stApp { background-color: #000000 !important; cursor: pointer; }
        
        .clock-container {
            text-align: center;
            width: 100%;
            margin-top: 30px;
        }

        .digital-timer {
            font-family: 'Seven Segment', sans-serif;
            color: #FF0000;
            /* Tamaño reducido del reloj */
            font-size: clamp(45px, 10vw, 90px);
            text-shadow: 0 0 15px rgba(255, 0, 0, 0.7);
            letter-spacing: 5px;
            line-height: 1;
        }

        .labels-timer {
            color: #222;
            letter-spacing: 12px;
            font-size: 11px;
            margin-top: 15px;
            font-weight: 800;
            text-transform: uppercase;
        }

        /* ESTILO SOLICITADO PARA EL TEXTO "HACE CLIC" */
        .click-instruction {
            color: #FF0000 !important;
            margin-top: 50px;
            font-size: 18px !important; /* Letra más grande */
            font-weight: 900 !important;
            letter-spacing: 3px;
            text-transform: uppercase;
            /* Contorno negro (Text Stroke) */
            text-shadow: 
                -2px -2px 0 #000,  
                 2px -2px 0 #000,
                -2px  2px 0 #000,
                 2px  2px 0 #000,
                 0px  0px 10px rgba(255, 0, 0, 0.5);
        }

        /* CAPA INVISIBLE SOBRE TODA LA PANTALLA */
        div.stButton {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 999;
        }

        div.stButton > button {
            width: 100% !important;
            height: 100% !important;
            background: transparent !important;
            border: none !important;
            color: transparent !important;
            cursor: pointer !important;
        }
        </style>
        """, unsafe_allow_html=True)

    # Diseño visual
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
    dias = dif.days
    horas, resto = divmod(dif.seconds, 3600)
    minutos, segundos = divmod(resto, 60)
    
    st.markdown(f"""
        <div class='clock-container'>
            <div class='digital-timer'>{dias:02d}:{horas:02d}:{minutos:02d}:{segundos:02d}</div>
            <div class='labels-timer'>DÍAS HORAS MINUTOS SEGUNDOS</div>
            <p class='click-instruction'>HACE CLIC EN CUALQUIER LUGAR PARA EXPLORAR</p>
        </div>
        """, unsafe_allow_html=True)

    # Overlay para el clic (La confirmación de Morty)
    if st.button("Click Overlay"):
        st.session_state.estado = 'web'
        st.rerun()
    
    time.sleep(1)
    st.rerun()

else:
    # PANTALLA 2: WEB BLANCA
    st.markdown("""
        <style>
        .stApp { background-color: #FFFFFF !important; }
        .logo-main { font-family: 'Inter', sans-serif; font-size: 80px; font-weight: 800; text-align: center; margin-top: 20px; color: #1a1a1a; }
        .subtitle-main { text-align: center; letter-spacing: 4px; color: #888; font-size: 14px; font-weight: 600; margin-bottom: 40px; }
        .section-title { text-align: center; color: #1a1a1a; font-size: 26px; font-weight: 800; letter-spacing: 10px; border-top: 1px solid #eee; padding-top: 30px; margin-bottom: 50px; }
        [data-testid="stImage"] img { height: 350px !important; object-fit: cover !important; border-radius: 12px !important; }
        div.stButton > button { 
            background-color: #1a1a1a !important; 
            color: white !important; 
            width: 100% !important; 
            border-radius: 8px !important;
            padding: 10px !important;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div class='logo-main'><span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span></div>
        <div class='subtitle-main'>NEGOCIOS INMOBILIARIOS</div>
        <div class='section-title'>CATEGORÍAS</div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)

    def mostrar_categoria(columna, titulo, archivo, clave):
        with columna:
            st.markdown(f"<div style='text-align:center; font-weight:800; margin-bottom:15px; font-family:Inter;'>{titulo}</div>", unsafe_allow_html=True)
            try:
                img = Image.open(archivo)
                st.image(img, use_container_width=True)
                st.button(f"VER {titulo}", key=clave)
            except: 
                st.error(f"Falta {archivo}")

    mostrar_categoria(col1, "DEPARTAMENTOS", "Deptos.jpeg", "cat_d")
    mostrar_categoria(col2, "CASAS", "Casas.jpeg", "cat_c")
    mostrar_categoria(col3, "TERRENOS", "Terreno.jpeg", "cat_t")

    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("← VOLVER AL INICIO"):
        st.session_state.estado = 'intro'
        st.rerun()