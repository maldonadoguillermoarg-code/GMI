import streamlit as st
import datetime
import time

# 1. Configuración de página
st.set_page_config(layout="wide", page_title="GMI | Acceso")

# 2. Control de estado: ¿Está en la intro o en la web?
if 'pagina_activa' not in st.session_state:
    st.session_state.pagina_activa = 'intro'

# 3. CSS Profesional: Fondo Negro Total y Reloj Rojo
st.markdown("""
    <style>
    /* Fondo negro para la intro */
    .stApp {
        background-color: #000000;
    }
    
    /* Contenedor de la Intro */
    .intro-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 80vh;
        text-align: center;
    }

    /* Reloj Digital con Segundos */
    .digital-clock {
        font-family: 'Courier New', Courier, monospace;
        color: #FF0000;
        font-size: 80px;
        font-weight: bold;
        text-shadow: 0 0 20px rgba(255, 0, 0, 0.9);
        letter-spacing: 5px;
        margin: 30px 0;
    }

    /* Etiquetas de tiempo */
    .time-labels {
        color: #555;
        font-size: 12px;
        letter-spacing: 12px;
        text-transform: uppercase;
        margin-top: -20px;
        margin-bottom: 40px;
    }

    /* Botón Futurista */
    div.stButton > button {
        background-color: transparent;
        color: white;
        border: 1px solid #444;
        padding: 15px 40px;
        text-transform: uppercase;
        letter-spacing: 4px;
        font-size: 14px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        border: 1px solid #FF0000;
        color: #FF0000;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE NAVEGACIÓN ---

if st.session_state.pagina_activa == 'intro':
    # --- PASO 1: LA PANTALLA NEGRA CON RELOJ ---
    
    # Logo GMI en la oscuridad
    st.markdown("""
        <div style='text-align: center; margin-top: 100px;'>
            <h1 style='font-size: 80px;'>
                <span style='color: #003366;'>G</span><span style='color: #FFFFFF;'>M</span><span style='color: #C41E3A;'>I</span>
            </h1>
            <p style='color: #444; letter-spacing: 10px;'>SISTEMA DE GESTIÓN ACTIVO</p>
        </div>
    """, unsafe_allow_html=True)

    # Cálculo de tiempo (31 de Octubre)
    fecha_limite = datetime.datetime(2026, 10, 31, 0, 0)
    ahora = datetime.datetime.now()
    dif = fecha_limite - ahora
    
    dias = dif.days
    horas, resto = divmod(dif.seconds, 3600)
    minutos, segundos = divmod(resto, 60)

    # El Reloj con Segundos
    st.markdown(f"""
        <div style='text-align: center;'>
            <div class="digital-clock">
                {dias:02d}:{horas:02d}:{minutos:02d}:{segundos:02d}
            </div>
            <div class="time-labels">
                DÍAS HORAS MIN SEG
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Botón para pasar a la segunda parte
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("MIRA EL AVANCE DE NUESTRA WEB"):
            st.session_state.pagina_activa = 'web'
            st.rerun()

    # Pequeño truco: Auto-refrescar cada 1 segundo para ver el reloj correr
    time.sleep(1)
    st.rerun()

else:
    # --- PASO 2: LA PÁGINA TERMINADA (DOUGLAS ELLIMAN STYLE) ---
    # Cambiamos el fondo a blanco para la web
    st.markdown("<style>.stApp { background-color: white; }</style>", unsafe_allow_html=True)

    # Encabezado GMI Luxury
    st.markdown("""
        <div style='text-align: center; margin-top: 30px;'>
            <h1 style='font-size: 60px; margin-bottom: 0px;'>
                <span style='color: #003366;'>G</span><span style='color: #1a1a1a;'>M</span><span style='color: #C41E3A;'>I</span>
            </h1>
            <p style='letter-spacing: 8px; color: #808080; font-size: 12px;'>GESTIÓN INMOBILIARIA</p>
        </div>
        <hr style='opacity: 0.1;'>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; letter-spacing: 4px; font-weight: 300;'>EXCLUSIVOS DISPONIBLES</h3>", unsafe_allow_html=True)
    
    # Grid de Propiedades
    c1, c2, c3 = st.columns(3)
    propiedades = [
        {"zona": "PUERTO MADERO", "precio": "850.000", "img": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800"},
        {"zona": "RECOLETA", "precio": "1.200.000", "img": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800"},
        {"zona": "NORDELTA", "precio": "540.000", "img": "https://images.unsplash.com/photo-1600607687940-4e5a9942d4b3?w=800"}
    ]
    
    cols = [c1, c2, c3]
    for i, p in enumerate(propiedades):
        with cols[i]:
            st.image(p["img"])
            st.markdown(f"**{p['zona']}**")
            st.markdown(f"USD {p['precio']}")
            st.button("VER DETALLES", key=f"prop_{i}")

    # Botón para volver al modo incógnito (opcional)
    if st.button("← VOLVER AL CONTADOR"):
        st.session_state.pagina_activa = 'intro'
        st.rerun()
        