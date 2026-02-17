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
if 'propiedad_seleccionada' not in st.session_state:
    st.session_state.propiedad_seleccionada = None

# Función para imágenes
def get_image_base64(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

# --- ESTILOS GLOBALES (La confiramcion de Morty) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&family=Nunito+Sans:wght@300;400;600&display=swap');
    @import url('https://fonts.cdnfonts.com/css/seven-segment');

    html, body {{ scrollbar-width: none; }}
    body::-webkit-scrollbar {{ display: none; }}
    
    @keyframes blinker {{ 50% {{ opacity: 0.1; }} }}

    .prop-precio {{ font-family: 'Inter', sans-serif; font-weight: 800; font-size: 24px; color: #1a1a1a !important; margin: 0; }}
    .prop-ubicacion {{ font-family: 'Nunito Sans', sans-serif; font-size: 14px; color: #444 !important; text-transform: uppercase; margin: 5px 0; font-weight: 600; }}
    .prop-detalles {{ color: #666 !important; font-size: 13px; font-weight: 400; }}
    
    .listing-card-horizontal {{ 
        display: flex; 
        background: white; 
        border-radius: 8px; 
        overflow: hidden; 
        margin-bottom: 20px; 
        border: 1px solid #e0e0e0;
    }}
    .img-side-h {{ width: 350px; height: 230px; overflow: hidden; }}
    .img-side-h img {{ width: 100%; height: 100%; object-fit: cover; }}
    
    .img-container-listing {{ width: 100%; height: 280px; overflow: hidden; border-radius: 4px; cursor: pointer; }}
    .img-container-listing img {{ width: 100%; height: 100%; object-fit: cover; transition: 0.3s; }}
    .img-container-listing:hover img {{ transform: scale(1.05); }}

    /* Ficha del Inmueble */
    .ficha-container {{ background: white; padding: 30px; border-radius: 12px; border: 1px solid #eee; }}
    .sidebar-contacto {{ background: #f9f9f9; padding: 25px; border-radius: 8px; border: 1px solid #ddd; }}

    /* Super Filtro */
    .filter-box {{
        background-color: #ffffff; padding: 25px; border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-top: -60px;
        position: relative; z-index: 100; border: 1px solid #eeeeee;
    }}
    
    .filter-label {{ font-family: 'Inter', sans-serif; font-size: 11px; font-weight: 800; color: #1a1a1a; letter-spacing: 1.5px; text-transform: uppercase; }}

    /* Botón Buscar Estilo Morty */
    div.stButton > button[kind="primary"] {{
        background-color: #1a1a1a !important; border: none !important; color: #ffffff !important;
        height: 45px !important; width: 100% !important; font-weight: 700 !important; border-radius: 6px !important;
    }}

    /* Botón Invisible para Fotos */
    .stButton>button:has(div.img-wrap) {{
        padding: 0 !important;
        border: none !important;
        background: none !important;
    }}

    .footer-container {{ background-color: #1a1a1a; color: #ffffff; padding: 60px; font-family: 'Inter', sans-serif; margin-top: 80px; }}
    </style>
    """, unsafe_allow_html=True)

# --- DATOS (3 POR CATEGORÍA - CÓRDOBA) ---
propiedades = [
    {"id": 1, "tipo": "DEPARTAMENTOS", "titulo": "Piso Estrada", "precio": "USD 240.000", "barrio": "Nueva Córdoba", "dire": "Estrada 150", "amb": "3", "dorm": "2", "baños": "2", "m2": "95", "img": "Deptos.jpeg", "desc": "Piso exclusivo frente a Plaza España."},
    {"id": 2, "tipo": "DEPARTAMENTOS", "titulo": "Loft General Paz", "precio": "USD 115.000", "barrio": "General Paz", "dire": "25 de Mayo 1100", "amb": "2", "dorm": "1", "baños": "1", "m2": "55", "img": "Deptos.jpeg", "desc": "Diseño industrial en el corazón de Gral Paz."},
    {"id": 3, "tipo": "DEPARTAMENTOS", "titulo": "Torre Duomo", "precio": "USD 160.000", "barrio": "Nueva Córdoba", "dire": "Tránsito Cáceres 450", "amb": "3", "dorm": "2", "baños": "2", "m2": "85", "img": "Deptos.jpeg", "desc": "Piso alto con vistas a la Terminal y el Parque."},
    {"id": 4, "tipo": "CASAS", "titulo": "Casona del Cerro", "precio": "USD 450.000", "barrio": "Cerro de las Rosas", "dire": "Fader 3800", "amb": "6", "dorm": "4", "baños": "3", "m2": "320", "img": "Casas.jpeg", "desc": "Clásica residencia con gran parque."},
    {"id": 5, "tipo": "CASAS", "titulo": "Moderna Manantiales", "precio": "USD 280.000", "barrio": "Manantiales", "dire": "La Cascada S/N", "amb": "5", "dorm": "3", "baños": "3", "m2": "210", "img": "Casas.jpeg", "desc": "A estrenar, diseño contemporáneo."},
    {"id": 6, "tipo": "CASAS", "titulo": "Residencia Urca", "precio": "USD 320.000", "barrio": "Urca", "dire": "Lamarca 3200", "amb": "6", "dorm": "3", "baños": "2", "m2": "280", "img": "Casas.jpeg", "desc": "Excelente ubicación, reciclada a nuevo."},
    {"id": 7, "tipo": "TERRENOS", "titulo": "Lote Valle Escondido", "precio": "USD 125.000", "barrio": "Valle Escondido", "dire": "Los Sueños", "amb": "-", "dorm": "-", "baños": "-", "m2": "600", "img": "Terreno.jpeg", "desc": "Lote plano central."},
    {"id": 8, "tipo": "TERRENOS", "titulo": "Terreno Cañitas", "precio": "USD 85.000", "barrio": "Las Cañitas", "dire": "Camino Falda del Carmen", "amb": "-", "dorm": "-", "baños": "-", "m2": "450", "img": "Terreno.jpeg", "desc": "Oportunidad de inversión."},
    {"id": 9, "tipo": "TERRENOS", "titulo": "Lote Tejas 3", "precio": "USD 55.000", "barrio": "Tejas 3", "dire": "Ruta 20", "amb": "-", "dorm": "-", "baños": "-", "m2": "350", "img": "Terreno.jpeg", "desc": "Lote con posesión inmediata, apto dúplex."},
]

# --- PANTALLA 1: RELOJ ---
if st.session_state.estado == 'intro':
    st.markdown("<h1 style='text-align:center; color:white; margin-top:20vh;'>GMI</h1>", unsafe_allow_html=True)
    if st.button("ENTER"):
        st.session_state.estado = 'web'
        st.rerun()
    time.sleep(1)
    st.rerun()

# --- PANTALLA 2: SITIO WEB ---
elif st.session_state.estado == 'web':
    # Navbar
    c_nav1, c_nav2 = st.columns([1, 2])
    with c_nav1:
        st.markdown("<div style='font-family:Inter; font-size:35px; font-weight:800;'><span style='color:#003366;'>G</span>M<span style='color:#C41E3A;'>I</span></div>", unsafe_allow_html=True)
    with c_nav2:
        cols = st.columns(6)
        for i, p in enumerate(["Principal", "En Venta", "Alquiler", "Tasaciones", "Administracion", "Contacto"]):
            if cols[i].button(p, key=f"n_{p}"):
                st.session_state.pagina_actual, st.session_state.categoria_actual, st.session_state.propiedad_seleccionada = p, None, None
                st.rerun()

    if st.session_state.propiedad_seleccionada:
        # --- FICHA ---
        p = st.session_state.propiedad_seleccionada
        if st.button("← VOLVER AL LISTADO"):
            st.session_state.propiedad_seleccionada = None
            st.rerun()
        
        st.markdown(f"<h1>{p['titulo']}</h1><p>{p['dire']}, {p['barrio']}</p>", unsafe_allow_html=True)
        col_f1, col_f2 = st.columns([2,1])
        with col_f1:
            st.image(p['img'], use_container_width=True)
            st.markdown(f"<div class='ficha-container'><h3>Descripción</h3><p>{p['desc']}</p></div>", unsafe_allow_html=True)
        with col_f2:
            st.markdown(f"<div class='sidebar-contacto'><h2>{p['precio']}</h2><hr><p>Vende GMI Negocios</p></div>", unsafe_allow_html=True)
            st.button("CONSULTAR AHORA", type="primary", use_container_width=True)

    elif st.session_state.pagina_actual == "Principal":
        if st.session_state.categoria_actual is None:
            # --- HOME ---
            m = folium.Map(location=[-31.4167, -64.1833], zoom_start=12)
            st_folium(m, height=300, use_container_width=True)
            
            # Filtro
            st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
            f1, f2, f3, f4, f5 = st.columns(5)
            f1.selectbox("UBICACIÓN", ["Córdoba"])
            f2.selectbox("TIPO", ["Casas", "Deptos", "Lotes"])
            f3.selectbox("PRECIO", ["Todos"])
            f4.selectbox("OPERACIÓN", ["Venta"])
            f5.button("BUSCAR", type="primary", key="main_search")
            st.markdown("</div>", unsafe_allow_html=True)

            # Categorías
            st.markdown("<br><h3 style='text-align:center;'>EXPLORAR CATEGORÍAS</h3>", unsafe_allow_html=True)
            cc1, cc2, cc3 = st.columns(3)
            cats = [("DEPARTAMENTOS", "Deptos.jpeg"), ("CASAS", "Casas.jpeg"), ("TERRENOS", "Terreno.jpeg")]
            for i, (n, img) in enumerate(cats):
                with [cc1, cc2, cc3][i]:
                    if st.button("", key=f"img_cat_{n}"):
                        st.session_state.categoria_actual = n
                        st.rerun()
                    st.markdown(f"<div style='margin-top:-60px;'><img src='data:image/jpeg;base64,{get_image_base64(img)}' style='width:100%; border-radius:4px;'></div>", unsafe_allow_html=True)
                    if st.button(n, key=f"btn_c_{n}", use_container_width=True):
                        st.session_state.categoria_actual = n
                        st.rerun()

            # DESTACADAS
            st.markdown("<br><h3 style='text-align:center;'>PROPIEDADES DESTACADAS</h3>", unsafe_allow_html=True)
            d1, d2, d3 = st.columns(3)
            # Mostramos las IDs 1, 4 y 7 (una de cada tipo)
            for i, p in enumerate([propiedades[0], propiedades[3], propiedades[6]]):
                with [d1, d2, d3][i]:
                    if st.button("", key=f"img_dest_{p['id']}"):
                        st.session_state.propiedad_seleccionada = p
                        st.rerun()
                    st.markdown(f"<div style='margin-top:-60px;'><img src='data:image/jpeg;base64,{get_image_base64(p['img'])}' style='width:100%; border-radius:4px;'></div>", unsafe_allow_html=True)
                    st.markdown(f"<b>{p['precio']}</b><br>{p['barrio']}", unsafe_allow_html=True)
                    if st.button("VER FICHA", key=f"dest_b_{p['id']}", use_container_width=True):
                        st.session_state.propiedad_seleccionada = p
                        st.rerun()
        else:
            # --- LISTADO ---
            cat = st.session_state.categoria_actual
            if st.button("← VOLVER A CATEGORÍAS"):
                st.session_state.categoria_actual = None
                st.rerun()
            st.title(f"{cat} en Córdoba")
            for p in [pr for pr in propiedades if pr["tipo"] == cat]:
                with st.container():
                    col_l1, col_l2 = st.columns([1, 2])
                    with col_l1:
                        if st.button("", key=f"img_list_{p['id']}"):
                            st.session_state.propiedad_seleccionada = p
                            st.rerun()
                        st.markdown(f"<div style='margin-top:-60px;'><img src='data:image/jpeg;base64,{get_image_base64(p['img'])}' style='width:100%; border-radius:4px;'></div>", unsafe_allow_html=True)
                    with col_l2:
                        st.markdown(f"<h3>{p['precio']}</h3><h4>{p['titulo']}</h4><p>{p['barrio']}</p>", unsafe_allow_html=True)
                        if st.button("VER DETALLES", key=f"lp_{p['id']}", use_container_width=True):
                            st.session_state.propiedad_seleccionada = p
                            st.rerun()
                    st.markdown("<hr>", unsafe_allow_html=True)

    # Footer
    st.markdown("<div class='footer-container'><p style='text-align:center;'>© 2026 GMI NEGOCIOS INMOBILIARIOS</p></div>", unsafe_allow_html=True)
    