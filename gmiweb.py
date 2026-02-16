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
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@700;800&family=Nunito+Sans:wght@400;600&display=swap');
    /* Importamos una fuente digital real */
    @import url('https://fonts.cdnfonts.com/css/seven-segment');

    h1, h2, h3, .section-title {
        font-family: 'Inter', sans-serif !important;
        letter-spacing: -0.02em !important;
    }

    p, div, span, label {
        font-family: 'Nunito Sans', sans-serif !important;
    }

    /* BOTONES MODERNOS 8px */
    div.stButton > button {
        font-family: 'Nunito Sans', sans-serif !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 16px 32px !important;
        border: none !important;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s ease;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

if st.session_state.estado == 'intro':
    # PANTALLA 1: INTRO NEGRA
    st.markdown("""
        <style>
        .stApp { background-color: #000000 !important; }
        
        /* CONTENEDOR DEL RELOJ */
        .clock-wrapper {
            position: relative;
            display: inline-block;
            background: #050505;
            padding: 30px;
            border-radius: 15px;
            border: 2px solid #111;
            box-shadow: inset 0 0 20px #000;
        }

        /* CAPA DE FONDO (Segmentos apagados) */
        .clock-bg {
            font-family: 'Seven Segment', sans-serif;
            color: rgba(255, 0, 0, 0.05); /* El "8" fantasma */
            font-size: clamp(50px, 12vw, 100px);
            position: absolute;
            z-index: 1;
        }

        /* CAPA ACTIVA (Números encendidos) */
        .clock-active {
            font-family: 'Seven Segment', sans-serif;
            color: #FF0000;
            font-size: clamp(50px, 12vw, 100px);
            position: relative;
            z-index: 2;
            text-shadow: 0 0 15px rgba(255, 0, 0, 0.9), 0 0 30px rgba(255, 0, 0, 0.4);
        }
        
        .clock-container { text-align: center; width: 100%; margin-top: 30px; }

        .labels {
            color: #333;
            text-align: center;
            letter-spacing: 15px;
            font-size: 12px;
            margin-top: 15px;
            text-transform: uppercase;
            font-weight: 800;
        }

        div.stButton > button {
            background-color: transparent !important;
            color: white !important;
            border: 1px solid #333 !important;
            margin-top: 50px;
        }
        div.stButton > button:hover {
            border: 1px solid #FF0000 !important;
            color: #FF0000 !important;
            box-shadow: 0px 0px 20px rgba(255, 0, 0, 0.2) !important;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center;'>
            <h1 style='font-size: 100px; margin-bottom: 0px; color: white;'>
                <span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span>
            </h1>
            <p style='letter-spacing: 8px; color: #444; font-size: 16px; font-weight: 800;'>NEGOCIOS INMOBILIARIOS</p>
        </div>
        """, unsafe_allow_html=True)

    # Lógica del tiempo
    futuro = datetime.datetime(2026, 10, 31, 0, 0)
    ahora = datetime.datetime.now()
    dif = futuro - ahora
    dias, horas, resto = dif.days, divmod(dif.seconds, 3600)[0], divmod(dif.seconds % 3600, 60)
    
    # Renderizado del reloj con capas
    st.markdown(f"""
        <div class='clock-container'>
            <div class='clock-wrapper'>
                <div class='clock-bg'>88:88:88:88</div>
                <div class='clock-active'>{dias:02d}:{horas:02d}:{resto[0]:02d}:{resto[1]:02d}</div>
            </div>
            <div class='labels'>DÍAS HORAS MIN SEG</div>
        </div>
        """, unsafe_allow_html=True)

    col_btn = st.columns([1, 2, 1])
    with col_btn[1]:
        if st.button("MIRA EL AVANCE DE NUESTRA WEB"):
            st.session_state.estado = 'web'
            st.rerun()
    
    time.sleep(1)
    st.rerun()

else:
    # PANTALLA 2: WEB BLANCA - CATEGORÍAS (Mantenemos el Pro Mix de fuentes)
    st.markdown("""
        <style>
        .stApp { background-color: #FFFFFF !important; }
        .logo-main { font-family: 'Inter', sans-serif; font-size: 80px; font-weight: 800; text-align: center; margin-top: 20px; color: #1a1a1a; }
        .subtitle-main { font-family: 'Nunito Sans', sans-serif; text-align: center; letter-spacing: 5px; color: #999; font-size: 15px; font-weight: 600; margin-bottom: 40px; }
        .section-title { text-align: center; color: #1a1a1a; font-size: 26px; font-weight: 800; letter-spacing: 10px; border-top: 1px solid #eee; padding-top: 30px; margin-bottom: 50px; }
        .cat-label { font-family: 'Inter', sans-serif; color: #1a1a1a; font-size: 18px; font-weight: 800; text-align: center; margin-bottom: 15px; }
        
        /* Imágenes consistentes */
        [data-testid="stImage"] img { height: 350px !important; object-fit: cover !important; border-radius: 12px !important; }
        
        div.stButton > button { background-color: #1a1a1a !important; color: white !important; width: 100% !important; }
        div.stButton > button:hover { background-color: #C41E3A !important; transform: scale(1.02); }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div class='logo-main'><span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span></div>
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
            except:
                st.error(f"Falta: {archivo}")

    mostrar_categoria(col1, "DEPARTAMENTOS", "Deptos.jpeg", "btn_d")
    mostrar_categoria(col2, "CASAS", "Casas.jpeg", "btn_c")
    mostrar_categoria(col3, "TERRENOS", "Terreno.jpeg", "btn_l")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← VOLVER"):
        st.session_state.estado = 'intro'
        st.rerun()