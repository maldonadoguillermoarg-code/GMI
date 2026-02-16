import streamlit as st
import datetime
import time
import base64

# 1. Configuración de página
st.set_page_config(layout="wide", page_title="GMI | Negocios Inmobiliarios")

# 2. Control de estado
if 'estado' not in st.session_state:
    st.session_state.estado = 'intro'

# Función para convertir imagen local a Base64
def get_image_base64(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

# --- DATOS DE PRUEBA (Lo que vendrá de Zoho) ---
propiedades_ejemplo = [
    {"titulo": "Penthouse Av. Alvear", "precio": "USD 850.000", "barrio": "Recoleta", "amb": "4", "m2": "120", "img": "Deptos.jpeg"},
    {"titulo": "Residencia Los Olivos", "precio": "USD 1.200.000", "barrio": "Norte", "amb": "6", "m2": "450", "img": "Casas.jpeg"},
    {"titulo": "Lote Premium Golf", "precio": "USD 340.000", "barrio": "Country Club", "amb": "-", "m2": "1200", "img": "Terreno.jpeg"},
    {"titulo": "Departamento Studio", "precio": "USD 120.000", "barrio": "Centro", "amb": "1", "m2": "35", "img": "Deptos.jpeg"},
]

# --- ESTILOS GLOBALES ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&family=Nunito+Sans:wght@300;400;600&display=swap');
    @import url('https://fonts.cdnfonts.com/css/seven-segment');

    /* Reset Estilo Elliman */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #f4f4f2 !important;
        scrollbar-width: none;
    }
    
    h1, h2, h3 { font-family: 'Inter', sans-serif !important; }
    
    /* Animación de titileo */
    @keyframes blinker { 50% { opacity: 0.1; } }

    /* TARJETA DE PROPIEDAD ESTILO ELLIMAN */
    .listing-card {
        background-color: transparent;
        margin-bottom: 40px;
        transition: 0.3s;
        cursor: pointer;
    }

    .img-container-listing {
        width: 100%;
        height: 300px;
        overflow: hidden;
        position: relative;
        border-radius: 2px;
    }

    .img-container-listing img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.6s ease;
    }

    .img-container-listing:hover img {
        transform: scale(1.05);
    }

    .info-container {
        padding: 15px 0;
        border-bottom: 1px solid #d1d1d1;
    }

    .prop-precio {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 20px;
        color: #1a1a1a;
        margin: 0;
    }

    .prop-ubicacion {
        font-family: 'Nunito Sans', sans-serif;
        font-size: 14px;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 5px 0;
    }

    .prop-detalles {
        font-family: 'Nunito Sans', sans-serif;
        font-size: 13px;
        color: #888;
        font-weight: 400;
    }
    </style>
    """, unsafe_allow_html=True)

if st.session_state.estado == 'intro':
    # PANTALLA 1: INTRO NEGRA
    st.markdown("""
        <style>
        .stApp { background-color: #000000 !important; }
        .digital-timer {
            font-family: 'Seven Segment', sans-serif; color: #FF0000;
            font-size: clamp(45px, 10vw, 90px); text-shadow: 0 0 15px rgba(255, 0, 0, 0.7);
            text-align: center; letter-spacing: 5px;
        }
        .labels-timer {
            color: #8B0000; text-align: center; letter-spacing: 12px; font-size: 14px;
            font-weight: 800; text-transform: uppercase; margin-top: 10px;
        }
        .text-link-titileo {
            color: #FF0000 !important; font-family: 'Inter', sans-serif; font-weight: 900;
            font-size: 20px; text-align: center; letter-spacing: 3px; margin-top: 40px;
            animation: blinker 1.2s linear infinite; text-transform: uppercase;
        }
        div.stButton > button {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: transparent !important; border: none !important; color: transparent !important; z-index: 999;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("<div style='text-align: center;'><h1 style='font-size: 100px; margin-bottom: 0px; color: white;'><span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span></h1><p style='letter-spacing: 8px; color: #333; font-size: 14px; font-weight: 800; margin-bottom: 50px;'>NEGOCIOS INMOBILIARIOS</p></div>", unsafe_allow_html=True)

    futuro = datetime.datetime(2026, 10, 31, 0, 0)
    ahora = datetime.datetime.now()
    dif = futuro - ahora
    dias, horas, residuo = dif.days, *divmod(dif.seconds, 3600)
    minutos, segundos = divmod(residuo, 60)
    
    st.markdown(f"<div class='digital-timer'>{dias:02d}:{horas:02d}:{minutos:02d}:{segundos:02d}</div><div class='labels-timer'>DÍAS HORAS MINUTOS SEGUNDOS</div><div class='text-link-titileo'>>>> MIRA LOS AVANCES DE NUESTRA WEB <<<</div>", unsafe_allow_html=True)

    if st.button("ENTER"):
        st.session_state.estado = 'web'
        st.rerun()
    time.sleep(1)
    st.rerun()

else:
    # PANTALLA 2: LISTADO DE PROPIEDADES (Estilo Elliman)
    st.markdown(f"""
        <div style='text-align: center; padding-top: 20px;'>
            <div style='font-family: "Inter"; font-size: 60px; font-weight: 800; color: #1a1a1a;'>
                <span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span>
            </div>
            <div style='letter-spacing: 5px; color: #888; font-size: 12px; font-weight: 600; margin-bottom: 40px;'>LISTADO DE PROPIEDADES</div>
        </div>
        """, unsafe_allow_html=True)

    # Grilla de Propiedades (3 columnas)
    cols = st.columns(3)
    
    for i, prop in enumerate(propiedades_ejemplo):
        img_b64 = get_image_base64(prop["img"])
        with cols[i % 3]:
            st.markdown(f"""
                <div class="listing-card">
                    <div class="img-container-listing">
                        <img src="data:image/jpeg;base64,{img_b64}">
                    </div>
                    <div class="info-container">
                        <p class="prop-precio">{prop['precio']}</p>
                        <p class="prop-ubicacion">{prop['titulo']} | {prop['barrio']}</p>
                        <p class="prop-detalles">{prop['amb']} AMB  •  {prop['m2']} M² TOT.</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            if st.button(f"VER DETALLE", key=f"btn_{i}", use_container_width=True):
                st.write(f"Conectando con Zoho para la propiedad: {prop['titulo']}...")

    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("← VOLVER AL INICIO"):
        st.session_state.estado = 'intro'
        st.rerun()