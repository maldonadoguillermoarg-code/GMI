import streamlit as st
import datetime
import time
from PIL import Image
from streamlit_card import card  # Nueva librería para tarjetas estéticas

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
    
    @keyframes blinker { 50% { opacity: 0.3; } }
    
    /* Mejoras en el contenedor de las tarjetas */
    .st-emotion-cache-12w0qpk { gap: 2rem; }
    </style>
    """, unsafe_allow_html=True)

if st.session_state.estado == 'intro':
    # PANTALLA 1: INTRO NEGRA INTERACTIVA
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
            margin-bottom: 60px; 
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

        /* Overlay invisible para el clic */
        div.stButton > button {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: transparent !important; border: none !important;
            color: transparent !important; z-index: 999; cursor: pointer !important;
        }
        </style>
        """, unsafe_allow_html=True)

    # Logo GMI
    st.markdown("""
        <div style='text-align: center;'>
            <h1 style='font-size: 100px; margin-bottom: 0px; color: white;'>
                <span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span>
            </h1>
            <p style='letter-spacing: 8px; color: #333; font-size: 14px; font-weight: 800; margin-bottom: 30px;'>NEGOCIOS INMOBILIARIOS</p>
        </div>
        """, unsafe_allow_html=True)

    # Lógica del Reloj
    futuro = datetime.datetime(2026, 10, 31, 0, 0)
    ahora = datetime.datetime.now()
    dif = futuro - ahora
    dias, horas, minutos, segundos = dif.days, dif.seconds//3600, (dif.seconds//60)%60, dif.seconds%60
    
    st.markdown(f"""
        <div class='clock-container'>
            <div class='digital-timer'>{dias:02d}:{horas:02d}:{minutos:02d}:{segundos:02d}</div>
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
    # PANTALLA 2: WEB BLANCA CON TARJETAS PREMIUM
    st.markdown("""
        <style>
        .stApp { background-color: #FFFFFF !important; }
        .logo-main { font-family: 'Inter', sans-serif; font-size: 80px; font-weight: 800; text-align: center; margin-top: 20px; color: #1a1a1a; }
        .subtitle-main { text-align: center; letter-spacing: 4px; color: #888; font-size: 14px; font-weight: 600; margin-bottom: 40px; }
        .section-title { text-align: center; color: #1a1a1a; font-size: 26px; font-weight: 800; letter-spacing: 10px; border-top: 1px solid #eee; padding-top: 30px; margin-bottom: 50px; }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div class='logo-main'><span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span></div>
        <div class='subtitle-main'>NEGOCIOS INMOBILIARIOS</div>
        <div class='section-title'>EXPLORAR PROPIEDADES</div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)

    # Implementación de streamlit-card para un look moderno
    with col1:
        card(
            title="DEPARTAMENTOS",
            text="Ver unidades disponibles",
            image="https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&q=80&w=400", # Reemplazar por tu Deptos.jpeg local
            on_click=lambda: print("Click Deptos")
        )

    with col2:
        card(
            title="CASAS",
            text="Hogares a tu medida",
            image="https://images.unsplash.com/photo-1518780664697-55e3ad937233?auto=format&fit=crop&q=80&w=400", # Reemplazar por tu Casas.jpeg local
            on_click=lambda: print("Click Casas")
        )

    with col3:
        card(
            title="TERRENOS",
            text="Tu inversión a futuro",
            image="https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&q=80&w=400", # Reemplazar por tu Terreno.jpeg local
            on_click=lambda: print("Click Terrenos")
        )

    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("← VOLVER AL INICIO"):
        st.session_state.estado = 'intro'
        st.rerun()