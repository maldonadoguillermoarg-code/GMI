import streamlit as st
import datetime
import time
from PIL import Image

# 1. Configuración de página
st.set_page_config(layout="wide", page_title="GMI | Negocios Inmobiliarios")

# 2. Control de estado
if 'estado' not in st.session_state:
    st.session_state.estado = 'intro'

# --- ESTILOS GLOBALES (Fuentes y Botones) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@700;800&family=Nunito+Sans:wght@400;600&family=Orbitron:wght@700&display=swap');

    /* Títulos e Impacto Visual (Inter) */
    h1, h2, h3, .section-title {
        font-family: 'Inter', sans-serif !important;
        letter-spacing: -0.02em !important;
    }

    /* Cuerpo de texto (Nunito Sans) */
    p, div, span, label {
        font-family: 'Nunito Sans', sans-serif !important;
    }

    /* BOTONES MODERNOS (8px radius + Sombra sutil) */
    div.stButton > button {
        font-family: 'Nunito Sans', sans-serif !important;
        font-weight: 600 !important;
        border-radius: 8px !important; /* Regla de los 8px */
        padding: 16px 32px !important; /* Proporción doble ancho que alto */
        border: none !important;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE PANTALLAS ---

if st.session_state.estado == 'intro':
    # PANTALLA 1: INTRO NEGRA (La confirmación de Morty)
    st.markdown("""
        <style>
        .stApp { background-color: #000000 !important; }
        
        /* RELOJ 7 SEGMENTOS */
        .digital-clock {
            font-family: 'Orbitron', sans-serif; /* Estilo digital */
            color: #FF0000;
            font-size: clamp(45px, 10vw, 90px);
            font-weight: 700;
            text-shadow: 0 0 15px rgba(255, 0, 0, 0.7), 0 0 30px rgba(255, 0, 0, 0.5);
            text-align: center;
            margin-top: 20px;
            background: #0a0a0a;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #1a1a1a;
            display: inline-block;
        }
        
        .clock-container { text-align: center; width: 100%; }

        .labels {
            color: #444;
            text-align: center;
            letter-spacing: 12px;
            font-size: 11px;
            margin-top: 10px;
            text-transform: uppercase;
            font-family: 'Inter', sans-serif;
        }

        /* Botón Intro Ghost */
        div.stButton > button {
            background-color: transparent !important;
            color: white !important;
            border: 1px solid #444 !important;
            margin-top: 40px;
        }
        div.stButton > button:hover {
            border: 1px solid #FF0000 !important;
            color: #FF0000 !important;
            box-shadow: 0px 0px 15px rgba(255, 0, 0, 0.3) !important;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; margin-top: 50px;'>
            <h1 style='font-size: 90px; margin-bottom: 0px; color: white;'>
                <span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span>
            </h1>
            <p style='letter-spacing: 6px; color: #555; font-size: 16px; font-weight: 700;'>NEGOCIOS INMOBILIARIOS</p>
        </div>
        """, unsafe_allow_html=True)

    # Lógica del tiempo
    futuro = datetime.datetime(2026, 10, 31, 0, 0)
    ahora = datetime.datetime.now()
    dif = futuro - ahora
    dias = dif.days
    horas, resto = divmod(dif.seconds, 3600)
    minutos, segundos = divmod(resto, 60)
    
    st.markdown(f"""
        <div class='clock-container'>
            <div class='digital-clock'>{dias:02d}:{horas:02d}:{minutos:02d}:{segundos:02d}</div>
            <div class='labels'>DÍAS HORAS MIN SEG</div>
        </div>
        """, unsafe_allow_html=True)

    col_btn_center = st.columns([1, 2, 1])
    with col_btn_center[1]:
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
            font-family: 'Inter', sans-serif;
            font-size: 75px;
            font-weight: 800;
            text-align: center;
            margin-top: 20px;
            line-height: 1;
            color: #1a1a1a;
        }
        
        .subtitle-main {
            font-family: 'Nunito Sans', sans-serif;
            text-align: center;
            letter-spacing: 4px;
            color: #888;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 30px;
        }

        .section-title {
            text-align: center;
            color: #1a1a1a;
            font-size: 26px;
            font-weight: 800;
            letter-spacing: 8px;
            margin-top: 40px;
            margin-bottom: 50px;
            text-transform: uppercase;
            border-top: 1px solid #f0f0f0;
            padding-top: 30px;
        }

        .cat-label {
            font-family: 'Inter', sans-serif;
            color: #1a1a1a;
            font-size: 16px;
            font-weight: 800;
            text-align: center;
            letter-spacing: 2px;
            margin-bottom: 15px;
        }

        /* AJUSTE DE IMÁGENES ALINEADAS */
        [data-testid="stImage"] img {
            height: 320px !important;
            object-fit: cover !important;
            border-radius: 12px !important; /* Un poco más de curva para las fotos */
            margin-bottom: 10px;
        }

        /* Botón de Categoría (Sólido) */
        div.stButton > button {
            background-color: #1a1a1a !important;
            color: white !important;
            width: 100% !important;
        }
        div.stButton > button:hover {
            background-color: #C41E3A !important;
            transform: translateY(-2px);
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div class='logo-main'>
            <span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span>
        </div>
        <div class='subtitle-main'>NEGOCIOS INMOBILIARIOS</div>
        <div class='section-title'>CATEGORÍAS</div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)

    def mostrar_categoria(columna, titulo, archivo, clave):
        with columna:
            st.markdown(f"<div class='cat-label'>{titulo}</div>", unsafe_allow_html=True)
            try:
                img = Image.open(archivo)
                st.image(img, use_container_width=True)
                st.button(f"EXPLORAR {titulo}", key=clave)
            except FileNotFoundError:
                st.error(f"Falta: {archivo}")

    # Nombres de archivos corregidos
    mostrar_categoria(col1, "DEPARTAMENTOS", "Deptos.jpeg", "btn_d")
    mostrar_categoria(col2, "CASAS", "Casas.jpeg", "btn_c")
    mostrar_categoria(col3, "TERRENOS", "Terreno.jpeg", "btn_l")

    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col_back, _ = st.columns([1, 0.5, 1])
    with col_back:
        if st.button("← VOLVER", key="back_btn"):
            st.session_state.estado = 'intro'
            st.rerun()