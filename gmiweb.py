import streamlit as st
import datetime
import time
import base64
import folium
from streamlit_folium import st_folium

# 1. Configuración de página
st.set_page_config(layout="wide", page_title="GMI | Negocios Inmobiliarios")

# 2. Control de estado
if 'estado' not in st.session_state:
    st.session_state.estado = 'intro'
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = 'Principal'
if 'categoria_actual' not in st.session_state:
    st.session_state.categoria_actual = None

# Función para imágenes
def get_image_base64(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

# --- ESTILOS GLOBALES ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&family=Nunito+Sans:wght@300;400;600&display=swap');
    @import url('https://fonts.cdnfonts.com/css/seven-segment');

    html, body {{ scrollbar-width: none; }}
    body::-webkit-scrollbar {{ display: none; }}
    
    @keyframes blinker {{ 50% {{ opacity: 0.1; }} }}

    .listing-card {{ background-color: transparent; margin-bottom: 20px; transition: 0.3s; }}
    .img-container-listing {{ width: 100%; height: 350px; overflow: hidden; border-radius: 2px; }}
    .img-container-listing img {{ width: 100%; height: 100%; object-fit: cover; transition: transform 0.6s ease; }}
    .img-container-listing:hover img {{ transform: scale(1.05); }}
    .info-container {{ padding: 15px 0; border-bottom: 1px solid #d1d1d1; }}
    .prop-precio {{ font-family: 'Inter', sans-serif; font-weight: 800; font-size: 20px; color: #1a1a1a; margin: 0; }}
    .prop-ubicacion {{ font-family: 'Nunito Sans', sans-serif; font-size: 14px; color: #666; text-transform: uppercase; margin: 5px 0; }}
    
    /* Ajustes para los botones de navegación */
    div.stButton > button {{
        border: none;
        background-color: transparent;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        letter-spacing: 1px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- DATOS ---
propiedades = [
    {"tipo": "DEPARTAMENTOS", "titulo": "Penthouse Alvear", "precio": "USD 850.000", "barrio": "Recoleta", "amb": "4", "m2": "120", "img": "Deptos.jpeg"},
    {"tipo": "CASAS", "titulo": "Residencia Los Olivos", "precio": "USD 1.200.000", "barrio": "Norte", "amb": "6", "m2": "450", "img": "Casas.jpeg"},
    {"tipo": "TERRENOS", "titulo": "Lote Premium Golf", "precio": "USD 340.000", "barrio": "Country Club", "amb": "-", "m2": "1200", "img": "Terreno.jpeg"},
]

# --- PANTALLA 1: RELOJ (INTRO) ---
if st.session_state.estado == 'intro':
    st.markdown("""
        <style>
        .stApp { background-color: #000000 !important; }
        .digital-timer {
            font-family: 'Seven Segment', sans-serif; color: #FF0000;
            font-size: clamp(45px, 10vw, 90px); text-shadow: 0 0 15px rgba(255, 0, 0, 0.7);
            text-align: center; letter-spacing: 5px; line-height: 1;
        }
        .labels-timer {
            color: #8B0000; text-align: center; letter-spacing: 12px; font-size: 14px;
            font-weight: 800; text-transform: uppercase; margin-top: 15px;
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

    st.markdown("<div style='text-align: center; margin-top: 5vh;'><h1 style='font-size: 100px; margin-bottom: 0px; color: white;'><span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span></h1><p style='letter-spacing: 8px; color: #333; font-size: 14px; font-weight: 800; margin-bottom: 50px;'>NEGOCIOS INMOBILIARIOS</p></div>", unsafe_allow_html=True)

    futuro = datetime.datetime(2026, 10, 31, 0, 0)
    ahora = datetime.datetime.now()
    dif = futuro - ahora
    dias, horas, residuo = dif.days, *divmod(dif.seconds, 3600)
    minutos, segundos = divmod(residuo, 60)
    
    st.markdown(f"""
        <div class='digital-timer'>{dias:02d}:{horas:02d}:{minutos:02d}:{segundos:02d}</div>
        <div class='labels-timer'>DÍAS HORAS MINUTOS SEGUNDOS</div>
        <div class='text-link-titileo'>MIRA LOS AVANCES DE NUESTRA WEB</div>
        """, unsafe_allow_html=True)

    if st.button("ENTER"):
        st.session_state.estado = 'web'
        st.rerun()

    time.sleep(1)
    st.rerun()

# --- PANTALLA 2: SITIO WEB ---
elif st.session_state.estado == 'web':
    st.markdown("<style>.stApp { background-color: #f4f4f2 !important; }</style>", unsafe_allow_html=True)
    
    # --- HEADER Y NAVBAR ---
    # Usamos columnas para poner el logo a la izquierda y el menú a la derecha
    head_col1, head_col2 = st.columns([1, 2])
    
    with head_col1:
        st.markdown(f"""
            <div style='text-align: left; padding-left: 20px;'>
                <div style='font-family: "Inter"; font-size: 40px; font-weight: 800; line-height: 1;'>
                    <span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span>
                </div>
                <div style='letter-spacing: 2px; color: #888; font-size: 9px; font-weight: 600;'>NEGOCIOS INMOBILIARIOS</div>
            </div>
            """, unsafe_allow_html=True)
            
    with head_col2:
        # Pestañas de navegación
        nav_cols = st.columns(6)
        paginas = ["Principal", "En Venta", "Alquiler", "Tasaciones", "Administracion", "Contacto"]
        for i, pag in enumerate(paginas):
            if nav_cols[i].button(pag, key=f"nav_{pag}"):
                st.session_state.pagina_actual = pag
                st.session_state.categoria_actual = None # Resetear categorías al cambiar de pestaña
                st.rerun()

    st.markdown("<hr style='margin: 0; border: 0.5px solid #d1d1d1;'>", unsafe_allow_html=True)

    # --- LÓGICA DE CONTENIDO POR PESTAÑA ---
    
    if st.session_state.pagina_actual == "Principal":
        # Contenido original de la página principal
        m = folium.Map(location=[-31.4167, -64.1833], zoom_start=12, tiles='CartoDB positron')
        st_folium(m, height=300, use_container_width=True, key="mapa_principal")
        
        st.markdown("<br>", unsafe_allow_html=True)

        if st.session_state.categoria_actual is None:
            st.markdown("<div style='text-align: center; font-family: Inter; font-weight: 800; letter-spacing: 10px; padding-top: 20px; margin-bottom: 40px;'>EXPLORAR</div>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            
            categorias = [("DEPARTAMENTOS", "Deptos.jpeg"), ("CASAS", "Casas.jpeg"), ("TERRENOS", "Terreno.jpeg")]
            for i, (nombre, img) in enumerate(categorias):
                with [col1, col2, col3][i]:
                    img_b64 = get_image_base64(img)
                    st.markdown(f"<div class='img-container-listing'><img src='data:image/jpeg;base64,{img_b64}'></div>", unsafe_allow_html=True)
                    if st.button(nombre, key=f"cat_{nombre}", use_container_width=True):
                        st.session_state.categoria_actual = nombre
                        st.rerun()
        else:
            # Vista filtrada (reutilizada)
            cat = st.session_state.categoria_actual
            st.markdown(f"<div style='text-align: center; font-family: Inter; font-weight: 800; letter-spacing: 5px; margin-bottom: 40px;'>{cat}</div>", unsafe_allow_html=True)
            
            propiedades_filtradas = [p for p in propiedades if p["tipo"] == cat]
            col_list, _ = st.columns([1, 2])
            
            for i, p in enumerate(propiedades_filtradas):
                with col_list:
                    img_b64 = get_image_base64(p["img"])
                    st.markdown(f"<div class='listing-card'><div class='img-container-listing'><img src='data:image/jpeg;base64,{img_b64}'></div><div class='info-container'><p class='prop-precio'>{p['precio']}</p><p class='prop-ubicacion'>{p['titulo']} | {p['barrio']}</p></div></div>", unsafe_allow_html=True)
                    st.button("VER FICHA", key=f"ficha_{i}")

            if st.button("← VOLVER"):
                st.session_state.categoria_actual = None
                st.rerun()

    elif st.session_state.pagina_actual == "En Venta":
        st.title("Propiedades en Venta")
        st.write("Sección en desarrollo...")

    elif st.session_state.pagina_actual == "Alquiler":
        st.title("Alquileres")
        st.write("Sección en desarrollo...")

    elif st.session_state.pagina_actual == "Tasaciones":
        st.title("Tasaciones Profesionales")
        st.write("Sección en desarrollo...")

    elif st.session_state.pagina_actual == "Administracion":
        st.title("Administración de Propiedades")
        st.write("Sección en desarrollo...")

    elif st.session_state.pagina_actual == "Contacto":
        st.title("Contacto")
        st.write("Sección en desarrollo...")

    # Botón flotante al final para volver al reloj si se desea
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("← VOLVER AL INICIO"):
        st.session_state.estado = 'intro'
        st.session_state.pagina_actual = 'Principal'
        st.session_state.categoria_actual = None
        st.rerun()