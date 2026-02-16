import streamlit as st
import datetime
import time

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
            letter-spacing: 2px;
        }
        .labels {
            color: #444;
            text-align: center;
            letter-spacing: clamp(5px, 2vw, 15px);
            font-size: 10px;
            margin-bottom: 30px;
            text-transform: uppercase;
        }
        .stButton { display: flex; justify-content: center; padding-top: 20px; }
        div.stButton > button {
            width: auto !important;
            min-width: 200px;
            background-color: transparent !important;
            color: white !important;
            border: 1px solid #444 !important;
            padding: 12px 25px !important;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-size: 14px;
            border-radius: 4px;
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
            <h1 style='font-size: clamp(50px, 10vw, 80px); margin-bottom: 0px;'>
                <span style='color: #003366;'>G</span><span style='color: #FFFFFF;'>M</span><span style='color: #C41E3A;'>I</span>
            </h1>
            <p style='letter-spacing: 5px; color: #333; font-size: 12px;'>SISTEMA DE GESTIÓN</p>
        </div>
        """, unsafe_allow_html=True)

    fecha_limite = datetime.datetime(2026, 10, 31, 0, 0)
    dif = fecha_limite - datetime.datetime.now()
    dias, horas, resto = dif.days, divmod(dif.seconds, 3600)[0], divmod(dif.seconds % 3600, 60)
    st.markdown(f'<div class="digital-clock">{dias:02d}:{horas:02d}:{resto[0]:02d}:{resto[1]:02d}</div>', unsafe_allow_html=True)
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
        /* Logo GMI para fondo blanco */
        .logo-text { font-size: 60px; font-weight: bold; text-align: center; margin-bottom: 0px; }
        .sub-logo { letter-spacing: 8px; color: #808080; font-size: 14px; text-align: center; margin-top: -10px; margin-bottom: 20px; }
        
        div.stButton > button {
            background-color: #1a1a1a !important;
            color: white !important;
            width: 100% !important;
            border-radius: 0px;
            border: none;
            padding: 10px;
        }
        h3 { color: #1a1a1a; font-size: 18px; margin-top: 10px; text-align: center; }
        </style>
        """, unsafe_allow_html=True)

    # Cabecera con Logo Original
    st.markdown("""
        <div class='logo-text'>
            <span style='color: #003366;'>G</span><span style='color: #1a1a1a;'>M</span><span style='color: #C41E3A;'>I</span>
        </div>
        <div class='sub-logo'>CATEGORÍAS</div>
        <hr style='border: 0.5px solid #eeeeee;'>
        """, unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        # Nueva Córdoba Aérea
        st.image("https://images.unsplash.com/photo-1590424600949-161b96d92663?w=800", caption="Vista Aérea")
        st.markdown("### DEPARTAMENTOS")
        st.button("VER LISTADO", key="cat_depto")
        
    with col_b:
        # Casa moderna realista "tranqui"
        st.image("https://images.unsplash.com/photo-1583608205776-bfd35f0d9f83?w=800")
        st.markdown("### CASAS")
        st.button("VER LISTADO", key="cat_casas")
        
    with col_c:
        # Terrenos
        st.image("https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=800")
        st.markdown("### TERRENOS")
        st.button("VER LISTADO", key="cat_terrenos")

    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("← VOLVER AL INICIO", key="back"):
        st.session_state.estado = 'intro'
        st.rerun()