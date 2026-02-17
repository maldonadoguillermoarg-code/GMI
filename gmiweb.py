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
        transition: box-shadow 0.3s ease;
    }}
    .listing-card-horizontal:hover {{ box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
    .img-side {{ width: 350px; height: 230px; overflow: hidden; cursor: pointer; }}
    .img-side img {{ width: 100%; height: 100%; object-fit: cover; }}
    .info-side {{ padding: 20px; flex: 1; display: flex; flex-direction: column; justify-content: space-between; }}

    /* Ficha del Inmueble */
    .ficha-container {{ background: white; padding: 30px; border-radius: 12px; border: 1px solid #eee; }}
    .sidebar-contacto {{ 
        background: #f9f9f9; 
        padding: 25px; 
        border-radius: 8px; 
        border: 1px solid #ddd;
        position: sticky;
        top: 20px;
    }}

    /* Super Filtro */
    .filter-box {{
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-top: -60px;
        position: relative;
        z-index: 100;
        border: 1px solid #eeeeee;
    }}
    
    .filter-label {{
        font-family: 'Inter', sans-serif;
        font-size: 11px;
        font-weight: 800;
        color: #1a1a1a;
        margin-bottom: 10px;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        height: 15px;
    }}

    /* Botones invisibles para fotos clicables */
    .stButton>button.img-click-btn {{
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        width: 100% !important;
        height: auto !important;
    }}

    /* Botón Buscar Estilo Morty */
    div.stButton > button[kind="primary"] {{
        background-color: #1a1a1a !important;
        border: none !important;
        color: #ffffff !important;
        height: 45px !important;
        width: 100% !important;
        font-weight: 700 !important;
        margin-top: 25px !important;
        border-radius: 6px !important;
    }}

    .footer-container {{
        background-color: #1a1a1a;
        color: #ffffff;
        padding: 80px 60px;
        font-family: 'Inter', sans-serif;
        margin-top: 80px;
    }}

    div.stButton > button {{
        border: none !important;
        background-color: transparent !important;
        color: #1a1a1a !important;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-size: 12px;
        transition: 0.3s;
    }}
    div.stButton > button:hover {{
        color: #C41E3A !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- DATOS AMPLIADOS (3 POR CATEGORÍA - CÓRDOBA) ---
propiedades = [
    # DEPARTAMENTOS
    {"id": 1, "tipo": "DEPARTAMENTOS", "titulo": "Piso Exclusivo", "precio": "USD 240.000", "barrio": "Nueva Córdoba", "dire": "Estrada 150", "amb": "3", "dorm": "2", "baños": "2", "m2": "95", "img": "Deptos.jpeg", "desc": "Departamento premium frente a Plaza España. Balcón terraza, cocina equipada y seguridad."},
    {"id": 2, "tipo": "DEPARTAMENTOS", "titulo": "Loft General Paz", "precio": "USD 115.000", "barrio": "General Paz", "dire": "25 de Mayo 1100", "amb": "2", "dorm": "1", "baños": "1", "m2": "55", "img": "Deptos.jpeg", "desc": "Ideal inversión. Loft de diseño en zona gastronómica. Amenities con piscina y SUM."},
    {"id": 3, "tipo": "DEPARTAMENTOS", "titulo": "Cardinales Alto Panorama", "precio": "USD 135.000", "barrio": "Colón", "dire": "Av. Colón 3400", "amb": "3", "dorm": "2", "baños": "1", "m2": "72", "img": "Deptos.jpeg", "desc": "Vista panorámica a la ciudad. Seguridad integral, cochera y pileta de uso común."},
    # CASAS
    {"id": 4, "tipo": "CASAS", "titulo": "Casona del Cerro", "precio": "USD 450.000", "barrio": "Cerro de las Rosas", "dire": "Fader 3800", "amb": "6", "dorm": "4", "baños": "3", "m2": "320", "img": "Casas.jpeg", "desc": "Clásica residencia del Cerro. Gran parque, quincho cerrado y excelentes materiales de construcción."},
    {"id": 5, "tipo": "CASAS", "titulo": "Modern House Manantiales", "precio": "USD 280.000", "barrio": "Manantiales", "dire": "La Cascada S/N", "amb": "5", "dorm": "3", "baños": "3", "m2": "210", "img": "Casas.jpeg", "desc": "Diseño contemporáneo minimalista. Doble altura, galería con asador y patio parquizado."},
    {"id": 6, "tipo": "CASAS", "titulo": "Residencia La Carolina", "precio": "USD 520.000", "barrio": "Country La Carolina", "dire": "Av. Recta Martinolli", "amb": "7", "dorm": "5", "baños": "4", "m2": "480", "img": "Casas.jpeg", "desc": "Máximo confort en barrio cerrado. Suite principal con vestidor, dependencia y gran piscina."},
    # TERRENOS
    {"id": 7, "tipo": "TERRENOS", "titulo": "Lote Valle Escondido", "precio": "USD 125.000", "barrio": "Los Sueños", "dire": "Valle Escondido", "amb": "-", "dorm": "-", "baños": "-", "m2": "600", "img": "Terreno.jpeg", "desc": "Lote plano ideal para vivienda familiar. Cercano a la guardia de ingreso."},
    {"id": 8, "tipo": "TERRENOS", "titulo": "Macrolote Las Cañitas", "precio": "USD 85.000", "barrio": "Las Cañitas", "dire": "Camino a Falda del Carmen", "amb": "-", "dorm": "-", "baños": "-", "m2": "450", "img": "Terreno.jpeg", "desc": "Excelente oportunidad de inversión. Barrio en constante crecimiento con seguridad."},
    {"id": 9, "tipo": "TERRENOS", "titulo": "Terreno Country Golf", "precio": "USD 210.000", "barrio": "Las Delicias", "dire": "Av. Ejército Argentino", "amb": "-", "dorm": "-", "baños": "-", "m2": "1500", "img": "Terreno.jpeg", "desc": "Lote exclusivo sobre campo de golf. Entorno natural único y privacidad absoluta."},
]

# --- PANTALLA 1: RELOJ ---
if st.session_state.estado == 'intro':
    # (Código de intro omitido por brevedad para centrarse en el cambio quirúrgico solicitado, se asume el ya existente)
    st.markdown("""<style>.stApp { background-color: #000; }</style>""", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; margin-top: 10vh;'><h1 style='font-size: 100px; color: white;'><span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span></h1></div>", unsafe_allow_html=True)
    if st.button("ENTER"):
        st.session_state.estado = 'web'
        st.rerun()
    time.sleep(1)
    st.rerun()

# --- PANTALLA 2: SITIO WEB ---
elif st.session_state.estado == 'web':
    st.markdown("<style>.stApp { background-color: #f4f4f2 !important; }</style>", unsafe_allow_html=True)
    
    # Header
    head_col1, head_col2 = st.columns([1.5, 3])
    with head_col1:
        st.markdown("<div style='text-align: left; padding-left: 30px;'><div style='font-family: \"Inter\"; font-size: 45px; font-weight: 800; color: #1a1a1a;'><span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span></div><div style='letter-spacing: 4px; color: #666; font-size: 10px; font-weight: 700;'>NEGOCIOS INMOBILIARIOS</div></div>", unsafe_allow_html=True)
    with head_col2:
        nav_cols = st.columns(6)
        paginas = ["Principal", "En Venta", "Alquiler", "Tasaciones", "Administracion", "Contacto"]
        for i, pag in enumerate(paginas):
            if nav_cols[i].button(f"● {pag}" if st.session_state.pagina_actual == pag else pag, key=f"nav_{pag}"):
                st.session_state.pagina_actual, st.session_state.categoria_actual, st.session_state.propiedad_seleccionada = pag, None, None
                st.rerun()

    st.markdown("<hr style='margin: 15px 0; opacity: 0.3;'>", unsafe_allow_html=True)

    if st.session_state.propiedad_seleccionada:
        # --- VISTA: FICHA ---
        p = st.session_state.propiedad_seleccionada
        if st.button("← VOLVER"):
            st.session_state.propiedad_seleccionada = None
            st.rerun()
        
        img_b64 = get_image_base64(p["img"])
        st.markdown(f"<div style='display: grid; grid-template-columns: 2fr 1fr; gap: 10px; height: 450px; margin-bottom: 20px;'><div style='overflow: hidden; border-radius: 8px;'><img src='data:image/jpeg;base64,{img_b64}' style='width: 100%; height: 100%; object-fit: cover;'></div><div style='background: #eee; border-radius: 8px;'></div></div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown(f"<div class='ficha-container'><h1 style='margin-bottom:0;'>{p['titulo']}</h1><p style='color: #666;'>{p['dire']}, {p['barrio']}, CBA</p><hr><p>{p['desc']}</p></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='sidebar-contacto'><h2>{p['precio']}</h2><p>Venta exclusiva GMI</p></div>", unsafe_allow_html=True)
            st.button("CONSULTAR", type="primary", use_container_width=True)

    elif st.session_state.pagina_actual == "Principal":
        if st.session_state.categoria_actual is None:
            # --- HOME: MAPA + FILTRO ---
            m = folium.Map(location=[-31.4167, -64.1833], zoom_start=12, tiles='CartoDB positron', zoom_control=False)
            st_folium(m, height=350, use_container_width=True, key="mapa_main")
            
            st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
            f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns([1, 1, 1, 1, 1])
            with f_col1: st.selectbox("UBICACIÓN", ["Córdoba, Arg"], label_visibility="visible", key="u1")
            with f_col2: st.selectbox("TIPO", ["Departamentos", "Casas", "Terrenos"], key="t1")
            with f_col3: st.selectbox("PRESUPUESTO", ["Cualquier rango", "50k-100k", "100k-300k", "300k+"], key="r1")
            with f_col4: st.selectbox("OPERACIÓN", ["Venta", "Alquiler"], key="o1")
            with f_col5: st.button("BUSCAR", type="primary", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # EXPLORAR CATEGORÍAS
            st.markdown("<br><div style='text-align: center; font-weight: 800; letter-spacing: 8px;'>EXPLORAR</div><br>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            for i, (nombre, img) in enumerate([("DEPARTAMENTOS", "Deptos.jpeg"), ("CASAS", "Casas.jpeg"), ("TERRENOS", "Terreno.jpeg")]):
                with [col1, col2, col3][i]:
                    img_b64 = get_image_base64(img)
                    if st.button("", key=f"img_cat_{nombre}", help=f"Ver {nombre}"): # Hack para foto clicable
                        st.session_state.categoria_actual = nombre
                        st.rerun()
                    st.markdown(f"<div style='margin-top:-60px;'><div class='img-container-listing' style='height:280px;'><img src='data:image/jpeg;base64,{img_b64}'></div></div>", unsafe_allow_html=True)
                    if st.button(nombre, key=f"btn_cat_{nombre}", use_container_width=True):
                        st.session_state.categoria_actual = nombre
                        st.rerun()

            # PROPIEDADES DESTACADAS (RESTAURADO)
            st.markdown("<br><div style='text-align: center; font-weight: 800; letter-spacing: 3px;'>PROPIEDADES DESTACADAS</div><br>", unsafe_allow_html=True)
            d_col1, d_col2, d_col3 = st.columns(3)
            destacadas = [propiedades[0], propiedades[4], propiedades[8]] # 1 de cada una
            for i, p in enumerate(destacadas):
                with [d_col1, d_col2, d_col3][i]:
                    img_b64 = get_image_base64(p["img"])
                    # Foto clicable
                    if st.button(" ", key=f"img_dest_{p['id']}", help="Ver propiedad"):
                        st.session_state.propiedad_seleccionada = p
                        st.rerun()
                    st.markdown(f"""
                        <div style='margin-top:-60px; background: white; border: 1px solid #eee; padding: 15px; border-radius: 8px;'>
                            <img src='data:image/jpeg;base64,{img_b64}' style='width: 100%; height: 200px; object-fit: cover; border-radius: 4px;'>
                            <p class='prop-precio'>{p['precio']}</p>
                            <p class='prop-ubicacion'>{p['barrio']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"VER FICHA", key=f"btn_dest_{p['id']}", use_container_width=True):
                        st.session_state.propiedad_seleccionada = p
                        st.rerun()
        else:
            # --- LISTADO POR CATEGORÍA ---
            cat = st.session_state.categoria_actual
            st.markdown(f"<h2 style='text-align: center;'>{cat} EN CÓRDOBA</h2>", unsafe_allow_html=True)
            _, col_list, _ = st.columns([1, 4, 1])
            with col_list:
                for p in [pr for pr in propiedades if pr["tipo"] == cat]:
                    img_b64 = get_image_base64(p["img"])
                    # Card con foto clicable
                    st.markdown(f"<div class='listing-card-horizontal'><div class='img-side'><img src='data:image/jpeg;base64,{img_b64}'></div><div class='info-side'><div><p class='prop-precio'>{p['precio']}</p><p class='prop-ubicacion'>{p['titulo']} | {p['barrio']}</p><p class='prop-detalles'>{p['m2']} m² • {p['dorm']} dorm.</p></div></div></div>", unsafe_allow_html=True)
                    if st.button(f"VER DETALLES DE {p['titulo']}", key=f"list_btn_{p['id']}", use_container_width=True):
                        st.session_state.propiedad_seleccionada = p
                        st.rerun()
                if st.button("← VOLVER A CATEGORÍAS"):
                    st.session_state.categoria_actual = None
                    st.rerun()

    # Footer (omitido contenido para brevedad)
    st.markdown("<div class='footer-container'><p style='text-align:center;'>© 2026 GMI NEGOCIOS INMOBILIARIOS</p></div>", unsafe_allow_html=True)