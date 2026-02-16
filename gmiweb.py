import streamlit as st
import datetime
import time
from streamlit_extras.stylable_container import stylable_container
import streamlit_antd_components as sac

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
        .stApp {
            background-color: #000000 !important;
        }
        .digital-clock {
            font-family: 'Courier New', Courier, monospace;
            color: #FF0000;
            font-size: clamp(45px, 10vw, 85px);
            font-weight: bold;
            text-shadow: 0 0 20px rgba(255, 0, 0, 0.9);
            text-align: center;
            margin-top: 50px;
            letter-spacing: 5px;
        }
        .labels {
            color: #333;
            text-align: center;
            letter-spacing: clamp(5px, 2vw, 15px);
            font-size: 10px;
            margin-bottom: 50px;
            text-transform: uppercase;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Logo GMI
    st.markdown("""
        <div style='text-align: center;'>
            <h1 style='font-size: clamp(60px, 12vw, 90px); margin-bottom: 0px;'>
                <span style='color: #003366;'>G</span><span style='color: #FFFFFF;'>M</span><span style='color: #C41E3A;'>I</span>
            </h1>
            <p style='letter-spacing: 10px; color: #444; font-size: 12px;'>SISTEMA DE GESTIÓN</p>
        </div>
        """, unsafe_allow_html=True)

    # Tiempo
    fecha_limite = datetime.datetime(2026, 10, 31, 0, 0)
    dif = fecha_limite - datetime.datetime.now()
    dias, horas, resto = dif.days, divmod(dif.seconds, 3600)[0], divmod(dif.seconds % 3600, 60)
    
    st.markdown(f'<div class="digital-clock">{dias:02d}:{horas:02d}:{resto[0]:02d}:{resto[1]:02d}</div>', unsafe_allow_html=True)
    st.markdown('<div class="labels">DÍAS HORAS MIN SEG</div>', unsafe_allow_html=True)

    # BOTÓN CENTRADO (Usando la librería extras)
    with stylable_container(
        key="boton_principal",
        css_styles="""
            button {
                background-color: transparent !important;
                color: white !important;
                border: 1px solid #444 !important;
                padding: 15px 40px !important;
                text-transform: uppercase;
                letter-spacing: 3px;
                display: block;
                margin: 0 auto !important;
                transition: 0.5s;
            }
            button:hover {
                border: 1px solid #FF0000 !important;
                color: #FF0000 !important;
                box-shadow: 0 0 20px rgba(255, 0, 0, 0.4);
            }
        """,
    ):
        if st.button("MIRA EL AVANCE DE NUESTRA WEB"):
            st.session_state.estado = 'web'
            st.rerun()

    time.sleep(1)
    st.rerun()

else:
    # PANTALLA 2: WEB BLANCA
    st.markdown("<style>.stApp { background-color: white !important; }</style>", unsafe_allow_html=True)
    
    # Menú de pasos moderno (antd)
    sac.steps(
        items=[
            sac.StepsItem(title='Inicio', icon='house'),
            sac.StepsItem(title='Propiedades', icon='building'),
            sac.StepsItem(title='Contacto', icon='envelope', disabled=True),
        ], format_value='dot', index=1, color='dark'
    )

    st.markdown("<h1 style='color: black; text-align: center; margin-top: 20px;'>CATÁLOGO EXCLUSIVO</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.image("https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800")
        st.button("PUERTO MADERO", key="p1")
    with col_b:
        st.image("https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800")
        st.button("RECOLETA", key="p2")
    with col_c:
        st.image("https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800")
        st.button("NORDELTA", key="p3")

    if st.button("← VOLVER"):
        st.session_state.estado = 'intro'
        st.rerun()
        