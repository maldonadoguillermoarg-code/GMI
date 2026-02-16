import streamlit as st
import datetime
import time

# 1. Configuración de página (Luxury Style)
st.set_page_config(layout="wide", page_title="GMI | Gestión Inmobiliaria")

# 2. Control de navegación: ¿Intro o Web?
if 'estado' not in st.session_state:
    st.session_state.estado = 'intro'

# --- INICIO DE LÓGICA DE PANTALLAS ---

if st.session_state.estado == 'intro':
    # --- PANTALLA 1: INTRO NEGRA (ESTILO FUTURISTA) ---
    st.markdown("""
        <style>
        /* Fondo negro total */
        .stApp {
            background-color: #000000 !important;
        }
        /* Reloj Digital Rojo */
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
        /* Etiquetas de tiempo */
        .labels {
            color: #444;
            text-align: center;
            letter-spacing: 15px;
            font-size: 12px;
            margin-bottom: 50px;
            text-transform: uppercase;
        }
        /* Botón de la intro: Centrado y Minimalista */
        div.stButton > button {
            display: block;
            margin: 0 auto;
            background-color: transparent !important;
            color: white !important;
            border: 1px solid #444 !important;
            padding: 15px 30px;
            text-transform: uppercase;
            letter-spacing: 3px;
            font-size: 14px;
            transition: 0.3s;
        }
        div.stButton > button:hover {
            border: 1px solid #FF0000 !important;
            color: #FF0000 !important;
            box-shadow: 0 0 20px rgba(255, 0, 0, 0.4);
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # Logo GMI en la Intro (G Azul, M Blanca para que se vea, I Roja)
    st.markdown("""
        <div style='text-align: center;'>
            <h1 style='font-size: 80px; margin-bottom: 0px;'>
                <span style='color: #003366;'>G</span><span style='color: #FFFFFF;'>M</span><span style='color: #C41E3A;'>I</span>
            </h1>
            <p style='letter-spacing: 10px; color: #333;'>SISTEMA DE GESTIÓN</p>
        </div>
        """, unsafe_allow_html=True)

    # Cálculo del tiempo (31 de Octubre)
    fecha_limite = datetime.datetime(2026, 10, 31, 0, 0)
    dif = fecha_limite - datetime.datetime.now()
    dias = dif.days
    horas, resto = divmod(dif.seconds, 3600)
    minutos, segundos = divmod(resto, 60)

    # Mostrar Reloj
    st.markdown(f'<div class="digital-clock">{dias:02d}:{horas:02d}:{minutos:02d}:{segundos:02d}</div>', unsafe_allow_html=True)
    st.markdown('<div class="labels">DÍAS HORAS MIN SEG</div>', unsafe_allow_html=True)

    # Botón de entrada CENTRADO MATEMÁTICAMENTE
    # Usamos columnas para forzar el centro absoluto
    izq, centro, der = st.columns([1, 2, 1])
    with centro:
        if st.button("MIRA EL AVANCE DE NUESTRA WEB"):
            st.session_state.estado = 'web'
            st.rerun()

    # Actualización automática del segundero
    time.sleep(1)
    st.rerun()

else:
    # --- PANTALLA 2: WEB TERMINADA (ESTILO BLANCO LUXURY) ---
    st.markdown("""
        <style>
        /* Volvemos al fondo blanco */
        .stApp {
            background-color: #FFFFFF !important;
        }
        h1, h2, h3 {
            font-family: 'Playfair Display', serif;
            font-weight: 300;
            color: #1a1a1a;
            letter-spacing: -1px;
        }
        /* Botones de la web (Negros sólidos) */
        .main-web-btn div.stButton > button {
            background-color: #1a1a1a !important;
            color: white !important;
            border-radius: 0px !important;
            border: none !important;
            width: 100%;
        }
        </style>
        """, unsafe_allow_html=True)

    # Encabezado con el Logo GMI (G Azul, M Negra, I Roja)
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
    
    # Grilla de Propiedades (3 columnas)
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.image("https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800")
        st.markdown("#### PUERTO MADERO")
        st.markdown("**USD 850.000**")
        st.markdown("<p style='font-size: 12px; color: gray;'>3 DORMITORIOS | 2 BAÑOS</p>", unsafe_allow_html=True)
        st.button("VER DETALLES", key="web_btn1")

    with col_b:
        st.image("https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800")
        st.markdown("#### RECOLETA")
        st.markdown("**USD 1.200.000**")
        st.markdown("<p style='font-size: 12px; color: gray;'>PISO EXCLUSIVO | TERRAZA</p>", unsafe_allow_html=True)
        st.button("VER DETALLES", key="web_btn2")

    with col_c:
        # Imagen corregida que carga perfecto
        st.image("https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800")
        st.markdown("#### NORDELTA")
        st.markdown("**USD 540.000**")
        st.markdown("<p style='font-size: 12px; color: gray;'>MODERNA | FRENTE AL LAGO</p>", unsafe_allow_html=True)
        st.button("VER DETALLES", key="web_btn3")

    # Botón para volver al contador (opcional)
    st.write("---")
    if st.button("← VOLVER AL PROTOCOLO", key="volver_btn"):
        st.session_state.estado = 'intro'
        st.rerun()