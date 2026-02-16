import streamlit as st
import datetime
import time

# 1. Configuración de página
st.set_page_config(layout="wide", page_title="GMI | Próximamente")

# 2. Control de estado: Empezamos en la 'intro'
if 'estado' not in st.session_state:
    st.session_state.estado = 'intro'

# --- LÓGICA DE PANTALLAS ---

if st.session_state.estado == 'intro':
    # PANTALLA 1: NEGRO TOTAL CON RELOJ
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
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='text-align: center;'>
            <h1 style='font-size: 80px; margin-bottom: 0px;'>
                <span style='color: #003366;'>G</span><span style='color: #FFFFFF;'>M</span><span style='color: #C41E3A;'>I</span>
            </h1>
            <p style='letter-spacing: 10px; color: #333;'>SISTEMA DE GESTIÓN</p>
        </div>
        """, unsafe_allow_html=True)

    fecha_limite = datetime.datetime(2026, 10, 31, 0, 0)
    dif = fecha_limite - datetime.datetime.now()
    dias = dif.days
    horas, resto = divmod(dif.seconds, 3600)
    minutos, segundos = divmod(resto, 60)

    st.markdown(f'<div class="digital-clock">{dias:02d}:{horas:02d}:{minutos:02d}:{segundos:02d}</div>', unsafe_allow_html=True)
    st.markdown('<div class="labels">DÍAS HORAS MIN SEG</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("MIRA EL AVANCE DE NUESTRA WEB"):
            st.session_state.estado = 'web'
            st.rerun()

    time.sleep(1)
    st.rerun()

else:
    # PANTALLA 2: TU PÁGINA (ESTILO BLANCO DOUGLAS ELLIMAN)
    st.markdown("""
        <style>
        .stApp {
            background-color: #FFFFFF !important;
        }
        h1, h2, h3 {
            font-family: 'Playfair Display', serif;
            font-weight: 300;
            color: #1a1a1a;
            letter-spacing: -1px;
        }
        div.stButton > button {
            background-color: #1a1a1a;
            color: white;
            border-radius: 0px;
            border: none;
            padding: 10px 25px;
            text-transform: uppercase;
            font-size: 12px;
            letter-spacing: 2px;
            width: 100%;
        }
        div.stButton > button:hover {
            background-color: #4a4a4a;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div style='text-align: center; margin-top: 30px;'>
            <h1 style='font-size: 80px; margin-bottom: 0px;'>
                <span style='color: #003366;'>G</span><span style='color: #1a1a1a;'>M</span><span style='color: #C41E3A;'>I</span>
            </h1>
            <p style='letter-spacing: 8px; color: #808080; font-size: 14px; margin-top: -10px;'>
                GESTIÓN INMOBILIARIA
            </p>
        </div>
        <hr style='border: 0.5px solid #eeeeee;'>
        """, unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; letter-spacing: 3px;'>EXCLUSIVOS</h3>", unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.image("https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80")
        st.markdown("#### PUERTO MADERO")
        st.markdown("**USD 850.000**")
        st.markdown("<p style='font-size: 12px; color: gray;'>3 DORMITORIOS | 2 BAÑOS</p>", unsafe_allow_html=True)
        st.button("VER DETALLES", key="btn1")

    with col_b:
        st.image("https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80")
        st.markdown("#### RECOLETA")
        st.markdown("**USD 1.200.000**")
        st.markdown("<p style='font-size: 12px; color: gray;'>PISO EXCLUSIVO | TERRAZA</p>", unsafe_allow_html=True)
        st.button("VER DETALLES", key="btn2")

    with col_c:
        # Aquí corregí la sangría y el link
        st.image("https://images.unsplash.com/photo-1600607687940-4e5a9942d4b3?auto=format&fit=crop&w=800&q=80")
        st.markdown("#### NORDELTA")
        st.markdown("**USD 540.000**")
        st.markdown("<p style='font-size: 12px; color: gray;'>MODERNA | FRENTE AL LAGO</p>", unsafe_allow_html=True)
        st.button("VER DETALLES", key="btn3")

    if st.button("← CERRAR SISTEMA"):
        st.session_state.estado = 'intro'
        st.rerun()
        