import streamlit as st
import datetime
import time
from PIL import Image

# 1. Configuración de página
st.set_page_config(layout="wide", page_title="GMI | Negocios Inmobiliarios")

# 2. Control de estado
if 'estado' not in st.session_state:
    st.session_state.estado = 'intro'

# --- ESTILOS GLOBALES (Tipografías y Botones Pro) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@700;800&family=Nunito+Sans:wght@400;600&display=swap');
    @import url('https://fonts.cdnfonts.com/css/seven-segment');

    /* Títulos Impactantes (Inter) */
    h1, h2, h3, .section-title {
        font-family: 'Inter', sans-serif !important;
        letter-spacing: -0.02em !important;
    }
    
    /* Cuerpo y Lectura (Nunito Sans) */
    p, div, span, label {
        font-family: 'Nunito Sans', sans-serif !important;
    }

    /* BOTONES MODERNOS (8px radius + Padding Proporcional) */
    div.stButton > button {
        font-family: 'Nunito Sans', sans-serif !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 16px 32px !important;
        border: none !important;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE PANTALLAS ---

if st.session_state.estado == 'intro':
    # PANTALLA 1: INTRO NEGRA (La confirmación de Morty - Estilo Red Stopwatch)
    st.markdown("""
        <style>
        .stApp { background-color: #000000 !important; }
        
        .clock-container {
            text-align: center;
            margin-top: 50px;
        }

        /* EL RELOJ DIGITAL (7 Segmentos + Resplandor del video) */
        .digital-timer {
            font-family: 'Seven Segment', sans-serif;
            color: #FF0000;
            font-size: clamp(60px, 15vw, 120px);
            text-shadow: 
                0 0 10px rgba(255, 0, 0, 0.9), 
                0 0 20px rgba(255, 0, 0, 0.6),
                0 0 40px rgba(255, 0, 0, 0.3);
            letter-spacing: 5px;
            line-height: 1;
        }

        .labels-timer {
            color: #222;
            text-align: center;
            letter-spacing: 12px;
            font-size: 11px;
            margin-top: 20px;
            font-weight: 800;
            text-transform: uppercase;
        }

        /* FUERZA EL CENTRADO TOTAL DEL BOTÓN */
        .stButton {
            display: flex;
            justify-content: center;
            margin-top: 50px;
        }

        /* Estilo Ghost para el botón de Intro */
        .stButton > button {
            background-color: transparent !important;
            color: #444 !important;
            border: 1px solid #222 !important;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        .stButton > button:hover {
            color: #FF0000 !important;
            border: 1px solid #FF0000 !important;
            box-shadow: 0 0 20px rgba(255, 0, 0, 0.2) !important;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center;'>
            <h1 style='font-size: 100px; margin-bottom: 0px; color: white;'>
                <span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span>
            </h1>
            <p style='letter-spacing: 8px; color: #333; font-size: 14px; font-weight: 800;'>NEGOCIOS INMOBILIARIOS</p>
        </div>
        """, unsafe_allow_html=True)

    # Lógica de tiempo
    futuro = datetime.datetime(2026, 10, 31, 0, 0)
    ahora = datetime.datetime.now()
    dif = futuro - ahora
    dias = dif.days
    horas, resto = divmod(dif.seconds, 3600)
    minutos, segundos = divmod(resto, 60)
    
    st.markdown(f"""
        <div class='clock-container'>
            <div class='digital-timer'>{dias:02d}:{horas:02d}:{minutos:02d}:{segundos:02d}</div>
            <div class='labels-timer'>DÍAS HORAS MINUTOS SEGUNDOS</div>
        </div>
        """, unsafe_allow_html=True)

    # Botón centrado automáticamente por el CSS de arriba
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
            font-size: 80px;
            font-weight: 800;
            text-align: center;
            margin-top: 20px;
            line-height: 1;
            color: #1a1a1a;
        }
        
        .subtitle-main {
            text-align: center;
            letter-spacing: 4px;
            color: #888;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 40px;
        }

        .section-title {
            text-align: center;
            color: #1a1a1a;
            font-size: 26px;
            font-weight: 800;
            letter-spacing: 10px;
            margin-top: 40px;
            margin-bottom: 50px;
            text-transform: uppercase;
            border-top: 1px solid #eee;
            padding-top: 30px;
        }

        /* Imágenes consistentes (Alineación Terrenos) */
        [data-testid="stImage"] img {
            height: 350px !important;
            object-fit: cover !important;
            border-radius: 12px !important;
        }

        /* Botones de Categoría (Negros) */
        div.stButton > button {
            background-color: #1a1a1a !important;
            color: white !important;
            width: 100% !important;
            text-transform: uppercase;
        }
        div.stButton > button:hover {
            background-color: #C41E3A !important;
            transform: scale(1.02);
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
            st.markdown(f"<div style='text-align:center; font-weight:800; margin-bottom:15px; font-family:Inter;'>{titulo}</div>", unsafe_allow_html=True)
            try:
                img = Image.open(archivo)
                st.image(img, use_container_width=True)
                st.button(f"VER {titulo}", key=clave)
            except FileNotFoundError:
                st.error(f"Falta archivo: {archivo}")

    mostrar_categoria(col1, "DEPARTAMENTOS", "Deptos.jpeg", "cat_d")
    mostrar_categoria(col2, "CASAS", "Casas.jpeg", "cat_c")
    mostrar_categoria(col3, "TERRENOS", "Terreno.jpeg", "cat_t")

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Botón Volver centrado
    if st.button("← VOLVER AL INICIO", key="back_home"):
        st.session_state.estado = 'intro'
        st.rerun()