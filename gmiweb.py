import streamlit as st
import datetime
import time
import requests
from streamlit_lottie import st_lottie
from streamlit_extras.stylable_container import stylable_container

# --- FUNCIÓN PARA ANIMACIÓN ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

# 1. Configuración
st.set_page_config(layout="wide", page_title="GMI | Gestión Inmobiliaria")

if 'estado' not in st.session_state:
    st.session_state.estado = 'intro'

# --- PANTALLA INTRO ---
if st.session_state.estado == 'intro':
    st.markdown("""
        <style>
        .stApp { background-color: #000000 !important; }
        .digital-clock {
            font-family: 'Courier New', Courier, monospace;
            color: #FF0000;
            font-size: clamp(40px, 10vw, 80px);
            font-weight: bold;
            text-shadow: 0 0 20px rgba(255, 0, 0, 0.9);
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    # Animación sutil superior
    lottie_code = load_lottieurl("https://lottie.host/817d23d8-21d3-463d-864b-b0b3013c7c22/Yd2g74t52v.json")
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st_lottie(lottie_code, height=120, key="radar")

    # Logo
    st.markdown("""
        <div style='text-align: center; margin-bottom: 20px;'>
            <h1 style='font-size: clamp(50px, 12vw, 90px); margin-bottom: 0px;'>
                <span style='color: #003366;'>G</span><span style='color: #FFFFFF;'>M</span><span style='color: #C41E3A;'>I</span>
            </h1>
            <p style='letter-spacing: 10px; color: #444; font-size: 12px;'>SISTEMA DE GESTIÓN</p>
        </div>
    """, unsafe_allow_html=True)

    # Reloj
    fecha_limite = datetime.datetime(2026, 10, 31, 0, 0)
    dif = fecha_limite - datetime.datetime.now()
    dias, horas, resto = dif.days, divmod(dif.seconds, 3600)[0], divmod(dif.seconds % 3600, 60)
    st.markdown(f'<div class="digital-clock">{dias:02d}:{horas:02d}:{resto[0]:02d}:{resto[1]:02d}</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#333; text-align:center; letter-spacing:10px; font-size:10px; margin-bottom:40px;">DÍAS HORAS MIN SEG</div>', unsafe_allow_html=True)

    # EL BOTÓN PROFESIONAL (Usando stylable_container)
    with stylable_container(
        key="botón_morty",
        css_styles="""
            button {
                background-color: transparent !important;
                color: white !important;
                border: 1px solid #444 !important;
                padding: 15px 40px !important;
                text-transform: uppercase;
                letter-spacing: 3px;
                display: block;
                margin: 0 auto; /* CENTRADO TOTAL */
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

# --- PANTALLA WEB ---
else:
    st.markdown("<style>.stApp { background-color: white !important; }</style>", unsafe_allow_html=True)
    
    # Usamos un componente de antd para un menú moderno arriba
    import streamlit_antd_components as sac
    sac.steps(
        items=[
            sac.StepsItem(title='Inicio', subtitle='GMI Intro'),
            sac.StepsItem(title='Propiedades', subtitle='Catálogo Activo'),
            sac.StepsItem(title='Contacto', disabled=True),
        ], format_value='dot', index=1
    )

    st.markdown("<h1 style='color: black; text-align: center;'>CATÁLOGO EXCLUSIVO</h1>", unsafe_allow_html=True)
    
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
        