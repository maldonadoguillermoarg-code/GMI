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
        .stApp {
            background-color: #000000 !important;
        }
        .digital-clock {
            font-family: 'Courier New', Courier, monospace;
            color: #FF0000;
            font-size: 80px;
            font-weight: bold;
            text-shadow: 0 0 20px rgba(255, 0, 0, 0.9);
            text-align: center;
            margin-top: 50px;
            letter-spacing: 5px;
        }
        .labels {
            color: #444;
            text-align: center;
            letter-spacing: 15px;
            font-size: 12px;
            margin-bottom: 50px;
            text-transform: uppercase;
        }
        
        /* EL TRUCO PARA EL CENTRADO TOTAL */
        /* Buscamos el contenedor del botón de Streamlit y lo centramos con Flex */
        .stButton {
            display: flex !important;
            justify-content: center !important;
            width: 100% !important;
        }

        div.stButton > button {
            width: auto !important;
            min-width: 250px; /* Tamaño mínimo elegante */
            background-color: transparent !important;
            color: white !important;
            border: 1px solid #444 !important;
            padding: 10px 30px !important;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-size: 13px;
            transition: 0.3s;
            border-radius: 4px;
        }
        
        div.stButton > button:hover {
            border: 1px solid #FF0000 !important;
            color: #FF0000 !important;
            box-shadow: 0 0 15px rgba(255, 0, 0, 0.3);
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # Logo
    st.markdown("""
        <div style='text-align: center;'>
            <h1 style='font-size: 80px; margin-bottom: 0px;'>
                <span style='color: #003366;'>G</span><span style='color: #FFFFFF;'>M</span><span style='color: #C41E3A;'>I</span>
            </h1>
            <p style='letter-spacing: 10px; color: #333;'>SISTEMA DE GESTIÓN</p>
        </div>
        """, unsafe_allow_html=True)

    # Tiempo
    fecha_limite = datetime.datetime(2026, 10, 31, 0, 0)
    dif = fecha_limite - datetime.datetime.now()
    dias, horas, resto = dif.days, divmod(dif.seconds, 3600)[0], divmod(dif.seconds % 3600, 60)
    minutos, segundos = resto[0], resto[1]

    st.markdown(f'<div class="digital-clock">{dias:02d}:{horas:02d}:{minutos:02d}:{segundos:02d}</div>', unsafe_allow_html=True)
    st.markdown('<div class="labels">DÍAS HORAS MIN SEG</div>', unsafe_allow_html=True)

    # El botón ahora será forzado al centro por el CSS arriba
    if st.button("MIRA EL AVANCE DE NUESTRA WEB"):
        st.session_state.estado = 'web'
        st.rerun()

    time.sleep(1)
    st.rerun()

else:
    # PANTALLA 2: WEB BLANCA LUXURY
    st.markdown("""
        <style>
        .stApp { background-color: #FFFFFF !important; }
        h1, h2, h3 { font-family: 'Playfair Display', serif; font-weight: 300; color: #1a1a1a; }
        div.stButton > button {
            background-color: #1a1a1a !important;
            color: white !important;
            border-radius: 0px !important;
            width: 100% !important;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div style='text-align: center; margin-top: 30px;'>
            <h1 style='font-size: 80px; margin-bottom: 0px;'>
                <span style='color: #003366;'>G</span><span style='color: #1a1a1a;'>M</span><span style='color: #C41E3A;'>I</span>
            </h1>
            <p style='letter-spacing: 8px; color: #808080; font-size: 14px; margin-top: -10px;'>GESTIÓN INMOBILIARIA</p>
        </div>
        <hr style='border: 0.5px solid #eeeeee;'>
        """, unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.image("https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800")
        st.markdown("#### PUERTO MADERO")
        st.button("VER DETALLES", key="w1")
    with col_b:
        st.image("https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800")
        st.markdown("#### RECOLETA")
        st.button("VER DETALLES", key="w2")
    with col_c:
        st.image("https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800")
        st.markdown("#### NORDELTA")
        st.button("VER DETALLES", key="w3")

    if st.button("← VOLVER", key="back"):
        st.session_state.estado = 'intro'
        st.rerun()