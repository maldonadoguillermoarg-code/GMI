import streamlit as st
import datetime
import time
from PIL import Image

# 1. Configuración de página
st.set_page_config(layout="wide", page_title="GMI | Gestión Inmobiliaria")

# 2. Control de estado
if 'estado' not in st.session_state:
    st.session_state.estado = 'intro'

# --- LÓGICA DE PANTALLAS ---

if st.session_state.estado == 'intro':
    # PANTALLA 1: INTRO NEGRA
    st.markdown("""
        <style>
        .stApp { background-color: #000000 !important; }
        .digital-clock {
            font-family: 'Courier New', Courier, monospace;
            color: #FF0000;
            font-size: clamp(40px, 8vw, 80px);
            font-weight: bold;
            text-shadow: 0 0 20px rgba(255, 0, 0, 0.9);
            text-align: center;
            margin-top: 20px;
        }
        .labels {
            color: #444;
            text-align: center;
            letter-spacing: 10px;
            font-size: 10px;
            margin-bottom: 30px;
            text-transform: uppercase;
        }
        div.stButton > button {
            background-color: transparent !important;
            color: white !important;
            border: 1px solid #444 !important;
            padding: 10px 20px !important;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        div.stButton > button:hover {
            border: 1px solid #FF0000 !important;
            color: #FF0000 !important;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; margin-top: 50px;'>
            <h1 style='font-size: 80px; margin-bottom: 0px;'>
                <span style='color: #003366;'>G</span><span style='color: #FFFFFF;'>M</span><span style='color: #C41E3A;'>I</span>
            </h1>
            <p style='letter-spacing: 5px; color: #333; font-size: 12px;'>SISTEMA DE GESTIÓN</p>
        </div>
        """, unsafe_allow_html=True)

    # Contador
    futuro = datetime.datetime(2026, 10, 31, 0, 0)
    ahora = datetime.datetime.now()
    dif = futuro - ahora
    dias = dif.days
    horas, resto = divmod(dif.seconds, 3600)
    minutos, segundos = divmod(resto, 60)
    
    st.markdown(f'<div class="digital-clock">{dias:02d}:{horas:02d}:{minutos:02d}:{segundos:02d}</div>', unsafe_allow_html=True)
    st.markdown('<div class="labels">DÍAS HORAS MIN SEG</div>', unsafe_allow_html=True)

    if st.button("MIRA EL AVANCE DE NUESTRA WEB"):
        st.session_state.estado = 'web'
        st.rerun()
    
    time.sleep(1)
    st.rerun()

else:
    # PANTALLA 2: WEB BLANCA - CATEGORÍAS
    st.markdown("""
        <style>
        .stApp { background-color: #FFFFFF !important; }
        .logo-main {
            font-size: 70px;
            font-weight: 800;
            text-align: center;
            margin-top: 20px;
            line-height: 1;
        }
        .section-title {
            text-align: center;
            color: #1a1a1a;
            font-size: 28px;
            font-weight: 300;
            letter-spacing: 12px;
            margin-top: 40px;
            margin-bottom: 40px;
            text-transform: uppercase;
            border-top: 1px solid #eee;
            padding-top: 20px;
        }
        .cat-label {
            color: #1a1a1a;
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }
        /* Botones estilo minimalista */
        div.stButton > button {
            background-color: #1a1a1a !important;
            color: white !important;
            border-radius: 0px !important;
            width: 100% !important;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)

    # Logo GMI
    st.markdown("""
        <div class='logo-main'>
            <span style='color: #003366;'>G</span><span style='color: #1a1a1a;'>M</span><span style='color: #C41E3A;'>I</span>
        </div>
        <div class='section-title'>CATEGORÍAS</div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)

    try:
        with col1:
            st.markdown("<div class='cat-label'>DEPARTAMENTOS</div>", unsafe_allow_html=True)
            img1 = Image.open("deptos.jpg")
            st.image(img1, use_container_width=True)
            if st.button("VER MÁS", key="btn_d"):
                st.info("Sección Departamentos próximamente")

        with col2:
            st.markdown("<div class='cat-label'>CASAS</div>", unsafe_allow_html=True)
            img2 = Image.open("casas.jpg")
            st.image(img2, use_container_width=True)
            if st.button("VER MÁS", key="btn_c"):
                st.info("Sección Casas próximamente")

        with col3:
            st.markdown("<div class='cat-label'>TERRENOS</div>", unsafe_allow_html=True)
            img3 = Image.open("lote.jpg")
            st.image(img3, use_container_width=True)
            if st.button("VER MÁS", key="btn_l"):
                st.info("Sección Terrenos próximamente")
                
    except Exception as e:
        st.error("Error cargando imágenes. Verificá que estén en la misma carpeta que este archivo.")

    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("← VOLVER"):
        st.session_state.estado = 'intro'
        st.rerun()