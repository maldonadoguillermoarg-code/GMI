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
    # PANTALLA 1: INTRO NEGRA (La confirmación de Morty)
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
            <h1 style='font-size: 80px; margin-bottom: 0px;'>
                <span style='color: #003366;'>G</span><span style='color: #FFFFFF;'>M</span><span style='color: #C41E3A;'>I</span>
            </h1>
            <p style='letter-spacing: 5px; color: #333; font-size: 12px;'>SISTEMA DE GESTIÓN</p>
        </div>
        """, unsafe_allow_html=True)

    # Contador para "La confirmación de Morty"
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
        div.stButton > button {
            background-color: #1a1a1a !important;
            color: white !important;
            border-radius: 2px !important;
            width: 100% !important;
            font-weight: bold;
            border: none;
        }
        div.stButton > button:hover {
            background-color: #C41E3A !important;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div class='logo-main'>
            <span style='color: #003366;'>G</span><span style='color: #1a1a1a;'>M</span><span style='color: #C41E3A;'>I</span>
        </div>
        <div class='section-title'>CATEGORÍAS</div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)

    # Función de carga con nombres corregidos
    def mostrar_categoria(columna, titulo, archivo, clave):
        with columna:
            st.markdown(f"<div class='cat-label'>{titulo}</div>", unsafe_allow_html=True)
            try:
                img = Image.open(archivo)
                st.image(img, use_container_width=True)
                if st.button(f"VER {titulo}", key=clave):
                    st.toast(f"Cargando catálogo de {titulo.lower()}...")
                    st.info(f"Muy pronto podrás ver todos nuestros {titulo.lower()} aquí.")
            except FileNotFoundError:
                st.error(f"No se encontró: {archivo}")

    # Uso de los nombres exactos que pasaste
    mostrar_categoria(col1, "DEPARTAMENTOS", "Deptos.jpg", "btn_deptos")
    mostrar_categoria(col2, "CASAS", "Casas.jpg", "btn_casas")
    mostrar_categoria(col3, "TERRENOS", "lote.jpg", "btn_lotes")

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    if st.button("← VOLVER AL INICIO", key="back_btn"):
        st.session_state.estado = 'intro'
        st.rerun()