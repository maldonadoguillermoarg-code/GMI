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
            min-width: 250px;
            background-color: transparent !important;
            color: white !important;
            border: 1px solid #444 !important;
            padding: 12px 25px !important;
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
    # PANTALLA 2: WEB BLANCA - CATEGORÍAS CON CLIC EN FOTO
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
            margin-bottom: 60px;
            text-transform: uppercase;
            border-top: 1px solid #eee;
            padding-top: 20px;
        }

        /* Contenedor de Imagen con Efecto Hover */
        .img-card {
            position: relative;
            height: 300px;
            overflow: hidden;
            border-radius: 8px;
            cursor: pointer;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            margin-bottom: 10px;
        }
        
        .img-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }

        .img-card img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .cat-label {
            color: #1a1a1a;
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            letter-spacing: 2px;
            margin-top: 10px;
        }

        /* Ocultar botones de Streamlit para usar los nuestros invisibles */
        .hidden-btn { display: none; }
        </style>
        """, unsafe_allow_html=True)

    # Cabecera
    st.markdown("""
        <div class='logo-main'>
            <span style='color: #003366;'>G</span><span style='color: #1a1a1a;'>M</span><span style='color: #C41E3A;'>I</span>
        </div>
        <div class='section-title'>CATEGORÍAS</div>
        """, unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns(3)
    
    # Nota: Para detectar clics en imágenes en Streamlit usamos botones invisibles o st.image con un link
    with col_a:
        st.markdown('<div class="cat-label">DEPARTAMENTOS</div>', unsafe_allow_html=True)
        if st.button(" 🏢 ", key="click_deptos", use_container_width=True, help="Ver Departamentos"):
            pass # Aquí irá la lógica para abrir la lista de deptos
        st.image("deptos.jpg", use_container_width=True)
        
    with col_b:
        st.markdown('<div class="cat-label">CASAS</div>', unsafe_allow_html=True)
        if st.button(" 🏠 ", key="click_casas", use_container_width=True, help="Ver Casas"):
            pass
        st.image("casas.jpg", use_container_width=True)
        
    with col_c:
        st.markdown('<div class="cat-label">TERRENOS</div>', unsafe_allow_html=True)
        if st.button(" 🌳 ", key="click_lotes", use_container_width=True, help="Ver Terrenos"):
            pass
        st.image("lote.jpg", use_container_width=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Botón de volver
    _, col_v2, _ = st.columns([1,1,1])
    with col_v2:
        if st.button("← VOLVER AL INICIO", key="back"):
            st.session_state.estado = 'intro'
            st.rerun()