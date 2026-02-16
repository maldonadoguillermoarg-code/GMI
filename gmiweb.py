import streamlit as st
import datetime
import time
from PIL import Image

# 1. Configuración de página
st.set_page_config(layout="wide", page_title="GMI | Negocios Inmobiliarios")

# 2. Control de estado
if 'estado' not in st.session_state:
    st.session_state.estado = 'intro'

# --- ESTILOS GLOBALES ---
# Combinamos fuentes y estilos base para evitar múltiples llamadas a st.markdown
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@700;800&family=Nunito+Sans:wght@400;600&display=swap');
    @import url('https://fonts.cdnfonts.com/css/seven-segment');

    h1, h2, h3, .section-title { font-family: 'Inter', sans-serif !important; letter-spacing: -0.02em !important; }
    p, div, span, label { font-family: 'Nunito Sans', sans-serif !important; }
    
    /* Estilo base de botones para evitar repetición */
    div.stButton > button {
        border-radius: 8px !important;
        font-family: 'Nunito Sans', sans-serif !important;
        transition: all 0.4s ease;
    }
    </style>
    """, unsafe_allow_html=True)

def vista_intro():
    st.markdown("""
        <style>
        .stApp { background-color: #000000 !important; }
        .clock-container { text-align: center; width: 100%; margin-top: 50px; }
        .digital-timer {
            font-family: 'Seven Segment', sans-serif;
            color: #FF0000;
            font-size: clamp(60px, 15vw, 120px);
            text-shadow: 0 0 15px rgba(255, 0, 0, 0.9);
            letter-spacing: 5px;
            line-height: 1;
        }
        .labels-timer {
            color: #222;
            letter-spacing: 12px;
            font-size: 11px;
            margin-top: 20px;
            font-weight: 800;
            text-transform: uppercase;
        }
        div.stButton > button {
            display: block;
            width: 80% !important;
            max-width: 900px;
            margin: 60px auto 0 auto !important;
            background-color: transparent !important;
            color: #555 !important;
            border: 1px solid #222 !important;
            font-size: 14px !important;
            letter-spacing: 3px !important;
            text-transform: uppercase;
        }
        div.stButton > button:hover {
            color: #FF0000 !important;
            border: 1px solid #FF0000 !important;
            box-shadow: 0 0 20px rgba(255, 0, 0, 0.15) !important;
            background-color: rgba(255, 0, 0, 0.02) !important;
        }
        </style>
        
        <div style='text-align: center;'>
            <h1 style='font-size: 100px; margin-bottom: 0px; color: white;'>
                <span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span>
            </h1>
            <p style='letter-spacing: 8px; color: #333; font-size: 14px; font-weight: 800; margin-bottom: 50px;'>NEGOCIOS INMOBILIARIOS</p>
        </div>
        """, unsafe_allow_html=True)

    # Cálculo de tiempo optimizado
    futuro = datetime.datetime(2026, 10, 31, 0, 0)
    ahora = datetime.datetime.now()
    dif = futuro - ahora
    
    segundos_totales = int(dif.total_seconds())
    dias, rem = divmod(segundos_totales, 86400)
    horas, rem = divmod(rem, 3600)
    minutos, segundos = divmod(rem, 60)

    st.markdown(f"""
        <div class='clock-container'>
            <div class='digital-timer'>{dias:02d}:{horas:02d}:{minutos:02d}:{segundos:02d}</div>
            <div class='labels-timer'>DÍAS HORAS MINUTOS SEGUNDOS</div>
        </div>
        """, unsafe_allow_html=True)

    if st.button("MIRA EL AVANCE DE NUESTRA WEB"):
        st.session_state.estado = 'web'
        st.rerun()
    
    time.sleep(1)
    st.rerun()

def vista_web():
    st.markdown("""
        <style>
        .stApp { background-color: #FFFFFF !important; }
        .logo-main { font-family: 'Inter', sans-serif; font-size: 80px; font-weight: 800; text-align: center; margin-top: 20px; color: #1a1a1a; }
        .subtitle-main { text-align: center; letter-spacing: 4px; color: #888; font-size: 14px; font-weight: 600; margin-bottom: 40px; }
        .section-title { text-align: center; color: #1a1a1a; font-size: 26px; font-weight: 800; letter-spacing: 10px; border-top: 1px solid #eee; padding-top: 30px; margin-bottom: 50px; }
        [data-testid="stImage"] img { height: 350px !important; object-fit: cover !important; border-radius: 12px !important; }
        div.stButton > button { 
            background-color: #1a1a1a !important; 
            color: white !important; 
            width: 100% !important; 
            font-size: 16px !important;
        }
        </style>
        
        <div class='logo-main'><span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span></div>
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
                st.error(f"Falta {archivo}")

    mostrar_categoria(col1, "DEPARTAMENTOS", "Deptos.jpeg", "cat_d")
    mostrar_categoria(col2, "CASAS", "Casas.jpeg", "cat_c")
    mostrar_categoria(col3, "TERRENOS", "Terreno.jpeg", "cat_t")

    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("← VOLVER AL INICIO"):
        st.session_state.estado = 'intro'
        st.rerun()

# Lógica principal
if st.session_state.estado == 'intro':
    vista_intro()
else:
    vista_web()