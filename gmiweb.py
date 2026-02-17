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
if 'operacion_filtro' not in st.session_state:
    st.session_state.operacion_filtro = None

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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800;900&family=Nunito+Sans:wght@300;400;600&display=swap');
    @import url('https://fonts.cdnfonts.com/css/seven-segment');

    html, body {{ scrollbar-width: none; }}
    body::-webkit-scrollbar {{ display: none; }}
    
    @keyframes blinker {{ 50% {{ opacity: 0.1; }} }}
    @keyframes scan {{
        0% {{ background-position: -200% 0; }}
        100% {{ background-position: 200% 0; }}
    }}

    /* Optimización Estilo Compass para GMI */
    .prop-precio {{ 
        font-family: 'Inter', sans-serif; 
        font-weight: 700; 
        font-size: 20px; 
        color: #0b0e0f !important;
        margin-bottom: 4px;
    }}
    .prop-ubicacion {{ 
        font-family: 'Inter', sans-serif; 
        font-size: 14px; 
        color: #5b564e !important; 
        margin: 0; 
        font-weight: 400; 
    }}
    .prop-detalles {{ 
        color: #5b564e !important; 
        font-size: 13px; 
        font-weight: 400;
        display: flex;
        gap: 8px;
        align-items: center;
    }}
    
    .listing-card {{ 
        background-color: #ffffff; 
        margin-bottom: 24px; 
        border: 1px solid #e2e8f0; 
        padding: 0px; 
        border-radius: 4px; 
        overflow: hidden;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .listing-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.1);
    }}

    .img-container-listing {{ 
        width: 100%; 
        height: 250px; 
        overflow: hidden;
        position: relative;
    }}
    .img-container-listing img {{ 
        width: 100%; 
        height: 100%; 
        object-fit: cover; 
    }}

    /* Badges inspirados en Compass */
    .badge-gmi {{
        position: absolute;
        top: 12px;
        left: 12px;
        background-color: #0b0e0f;
        color: white;
        padding: 4px 8px;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    .filter-box {{
        background-color: #ffffff;
        padding: 30px;
        border-radius: 2px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-top: -50px;
        position: relative;
        z-index: 100;
        border: 1px solid #eeeeee;
        max-width: 1200px;
        margin-left: auto;
        margin-right: auto;
    }}
    
    .filter-label {{
        font-family: 'Inter', sans-serif;
        font-size: 10px;
        font-weight: 700;
        color: #848fa1;
        margin-bottom: 8px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }}

    .footer-container {{
        background-color: #0b0e0f;
        color: #ffffff;
        padding: 80px 60px;
        font-family: 'Inter', sans-serif;
        margin-top: 100px;
    }}
    
    .btn-compass-gmi div.stButton > button {{
        background-color: #0076df !important;
        color: white !important;
        border-radius: 2px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        border: none !important;
    }}

    .nav-button div.stButton > button {{
        border: none !important;
        background-color: transparent !important;
        color: #0b0e0f !important;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        letter-spacing: 0.5px;
        text-transform: none;
        font-size: 14px;
        transition: 0.2s;
    }}
    .nav-button div.stButton > button:hover {{
        color: #0076df !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- DATOS ---
propiedades = [
    {"id": 1, "tipo": "DEPARTAMENTOS", "operacion": "Venta", "titulo": "Penthouse Alvear", "precio": "USD 850.000", "barrio": "Recoleta", "amb": "4", "m2": "120", "img": "Deptos.jpeg", "badge": "Exclusivo"},
    {"id": 2, "tipo": "DEPARTAMENTOS", "operacion": "Venta", "titulo": "Piso Estrada", "precio": "USD 240.000", "barrio": "Nueva Córdoba", "amb": "3", "m2": "95", "img": "Deptos.jpeg", "badge": "Nuevo"},
    {"id": 3, "tipo": "DEPARTAMENTOS", "operacion": "Alquiler", "titulo": "Torre Duomo", "precio": "$ 450.000", "barrio": "Nueva Córdoba", "amb": "2", "m2": "65", "img": "Deptos.jpeg", "badge": "Alquilado"},
    {"id": 4, "tipo": "CASAS", "operacion": "Venta", "titulo": "Residencia Los Olivos", "precio": "USD 1.200.000", "barrio": "Norte", "amb": "6", "m2": "450", "img": "Casas.jpeg", "badge": "Destacado"},
    {"id": 5, "tipo": "CASAS", "operacion": "Alquiler", "titulo": "Casona del Cerro", "precio": "$ 980.000", "barrio": "Cerro de las Rosas", "amb": "5", "m2": "320", "img": "Casas.jpeg", "badge": "Oportunidad"},
    {"id": 6, "tipo": "CASAS", "operacion": "Venta", "titulo": "Moderna Manantiales", "precio": "USD 280.000", "barrio": "Manantiales", "amb": "4", "m2": "210", "img": "Casas.jpeg", "badge": "Vendido"},
    {"id": 7, "tipo": "TERRENOS", "operacion": "Venta", "titulo": "Lote Premium Golf", "precio": "USD 340.000", "barrio": "Country Club", "amb": "-", "m2": "1200", "img": "Terreno.jpeg", "badge": "Lote"},
    {"id": 8, "tipo": "TERRENOS", "operacion": "Venta", "titulo": "Lote Valle Escondido", "precio": "USD 125.000", "barrio": "Valle Escondido", "amb": "-", "m2": "600", "img": "Terreno.jpeg", "badge": "Urgent"},
    {"id": 9, "tipo": "TERRENOS", "operacion": "Venta", "titulo": "Lote Tejas 3", "precio": "USD 55.000", "barrio": "Ruta 20", "amb": "-", "m2": "350", "img": "Terreno.jpeg", "badge": "Oferta"},
]

# --- PANTALLA 1: RELOJ (INTRO) ---
if st.session_state.estado == 'intro':
    st.markdown("""
        <style>
        .stApp { background-color: #000000 !important; }
        .digital-timer {
            font-family: 'Seven Segment', sans-serif;
            color: #FF0000;
            font-size: clamp(45px, 10vw, 90px); text-shadow: 0 0 15px rgba(255, 0, 0, 0.7);
            text-align: center; letter-spacing: 5px; line-height: 1;
        }
        .labels-timer {
            color: #8B0000;
            text-align: center; letter-spacing: 12px; font-size: 14px;
            font-weight: 800; text-transform: uppercase; margin-top: 15px;
        }
        .text-link-titileo {
            color: #FF0000 !important;
            font-family: 'Inter', sans-serif; font-weight: 900;
            font-size: 20px; text-align: center; letter-spacing: 3px; margin-top: 40px;
            animation: blinker 1.2s linear infinite; text-transform: uppercase;
        }
        div.stButton > button {
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: transparent !important; border: none !important; color: transparent !important; z-index: 999;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("<div style='text-align: center; margin-top: 10vh;'><h1 style='font-size: 100px; margin-bottom: 0px; color: white;'><span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span></h1><p style='letter-spacing: 8px; color: #444; font-size: 14px; font-weight: 800; margin-bottom: 50px;'>NEGOCIOS INMOBILIARIOS</p></div>", unsafe_allow_html=True)

    ahora = datetime.datetime.now()
    futuro = datetime.datetime(2026, 10, 31, 0, 0)
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

# --- PANTALLA 2: SITIO WEB (OPTIMIZADA ESTILO COMPASS) ---
elif st.session_state.estado == 'web':
    st.markdown("<style>.stApp { background-color: #ffffff !important; }</style>", unsafe_allow_html=True)
    
    # Header minimalista
    head_col1, head_col2 = st.columns([1, 2])
    with head_col1:
        st.markdown(f"""
            <div style='text-align: left; padding-left: 40px; padding-top: 20px;'>
                <div style='font-family: "Inter"; font-size: 24px; font-weight: 800; letter-spacing: 2px; color: #0b0e0f;'>
                    GMI<span style='color: #C41E3A;'>.</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with head_col2:
        st.markdown("<div style='padding-top: 15px;'>", unsafe_allow_html=True)
        nav_cols = st.columns(6)
        paginas = ["Principal", "En Venta", "Alquiler", "Tasaciones", "Servicios", "Contacto"]
        for i, pag in enumerate(paginas):
            with nav_cols[i]:
                st.markdown("<div class='nav-button'>", unsafe_allow_html=True)
                if st.button(pag.upper(), key=f"nav_{pag}"):
                    st.session_state.pagina_actual = pag
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr style='margin: 0; border: 0.5px solid #eee;'>", unsafe_allow_html=True)

    if st.session_state.pagina_actual == "Principal":
        # Hero con Mapa (Inspiración Compass)
        m = folium.Map(location=[-31.4167, -64.1833], zoom_start=13, tiles='CartoDB positron', zoom_control=False)
        st_folium(m, height=450, use_container_width=True, key="mapa_principal")

        # Filtros Estilo Compass
        st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
        f_col1, f_col2, f_col3, f_col4 = st.columns([1.5, 1, 1, 0.8])
        with f_col1:
            st.markdown("<p class='filter-label'>UBICACIÓN</p>", unsafe_allow_html=True)
            st.selectbox("u", ["Córdoba Capital", "Valle de Calamuchita", "Villa Carlos Paz"], label_visibility="collapsed", key="u1")
        with f_col2:
            st.markdown("<p class='filter-label'>TIPO</p>", unsafe_allow_html=True)
            st.selectbox("t", ["Departamentos", "Casas", "Terrenos"], label_visibility="collapsed", key="t1")
        with f_col3:
            st.markdown("<p class='filter-label'>PRECIO MÁX (USD)</p>", unsafe_allow_html=True)
            st.selectbox("rango", ["Cualquier precio", "100k", "250k", "500k+"], label_visibility="collapsed", key="r1")
        with f_col4:
            st.markdown("<div class='btn-compass-gmi' style='margin-top: 20px;'>", unsafe_allow_html=True)
            st.button("BUSCAR")
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Grilla de Propiedades (Optimización Estructural)
        st.markdown("<div style='padding: 60px 40px;'>", unsafe_allow_html=True)
        st.markdown("<h2 style='font-family: Inter; font-weight: 700; color: #0b0e0f; margin-bottom: 30px;'>Propiedades Destacadas en Córdoba</h2>", unsafe_allow_html=True)
        
        cols = st.columns(3)
        for idx, prop in enumerate(propiedades[:6]):
            with cols[idx % 3]:
                st.markdown(f"""
                    <div class='listing-card'>
                        <div class='img-container-listing'>
                            <div class='badge-gmi'>{prop['badge']}</div>
                            <img src='https://images.unsplash.com/photo-1568605114967-8130f3a36994?auto=format&fit=crop&q=80&w=800'>
                        </div>
                        <div style='padding: 20px;'>
                            <div class='prop-precio'>{prop['precio']}</div>
                            <div class='prop-ubicacion'>{prop['titulo']} | {prop['barrio']}</div>
                            <div class='prop-detalles' style='margin-top: 12px;'>
                                <span>{prop['amb']} Dorms</span> 
                                <span style='color: #ddd;'>|</span> 
                                <span>{prop['m2']} m² cubiertos</span>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Footer Institucional
    st.markdown(f"""
        <div class='footer-container'>
            <div style='display: flex; justify-content: space-between; flex-wrap: wrap; max-width: 1200px; margin: 0 auto;'>
                <div style='flex: 1; min-width: 300px; margin-bottom: 40px;'>
                    <div style='font-size: 24px; font-weight: 800; margin-bottom: 20px; letter-spacing: 2px;'>GMI<span style='color: #C41E3A;'>.</span></div>
                    <p style='color: #848fa1; font-size: 14px; line-height: 1.8; max-width: 300px;'>
                        Líderes en el mercado inmobiliario de Córdoba, brindando soluciones integrales y tasaciones profesionales con el respaldo de años de experiencia.
                    </p>
                </div>
                <div style='flex: 0.5; min-width: 200px; margin-bottom: 40px;'>
                    <div style='font-size: 12px; font-weight: 700; color: #848fa1; margin-bottom: 25px; letter-spacing: 1.5px; text-transform: uppercase;'>Navegación</div>
                    <div style='display: flex; flex-direction: column; gap: 12px;'>
                        <a href='#' style='color: white; text-decoration: none; font-size: 14px;'>Propiedades</a>
                        <a href='#' style='color: white; text-decoration: none; font-size: 14px;'>Tasaciones</a>
                        <a href='#' style='color: white; text-decoration: none; font-size: 14px;'>Administración</a>
                    </div>
                </div>
                <div style='flex: 0.5; min-width: 200px; margin-bottom: 40px;'>
                    <div style='font-size: 12px; font-weight: 700; color: #848fa1; margin-bottom: 25px; letter-spacing: 1.5px; text-transform: uppercase;'>Contacto</div>
                    <p style='color: #848fa1; font-size: 14px; line-height: 2;'>
                        📍 Av. Rafael Nuñez 4500, Córdoba<br>
                        📞 +54 351 000 0000<br>
                        ✉️ info@gminmobiliaria.com.ar
                    </p>
                </div>
            </div>
            <div style='margin-top: 60px; padding-top: 30px; border-top: 1px solid #1a1a1a; text-align: left; color: #444; font-size: 11px;'>
                © 2026 GMI Negocios Inmobiliarios. Todos los derechos reservados. | Córdoba, Argentina.
            </div>
        </div>
    """, unsafe_allow_html=True)