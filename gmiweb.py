import streamlit as st
import datetime
import time
import base64
import json
import folium
from streamlit_folium import st_folium

# 1. Configuración de página
st.set_page_config(layout="wide", page_title="GMI | Negocios Inmobiliarios")

# --- CARGA DE DATOS (NUEVO) ---
@st.cache_data
def cargar_datos_geo():
    # Cargar Provincias
    try:
        with open('argentina_states.json', 'r', encoding='utf-8') as f:
            provincias_data = json.load(f)
        provincias = sorted([p['nombre'] if isinstance(p, dict) else p for p in provincias_data])
    except:
        provincias = ["Córdoba", "Buenos Aires"]

    # Cargar Localidades vinculadas a Provincias
    loc_dict = {}
    try:
        with open('argentina_localities.json', 'r', encoding='utf-8') as f:
            localidades_data = json.load(f)
        for item in localidades_data:
            p = item.get('provincia')
            n = item.get('nombre')
            if p and n:
                if p not in loc_dict: loc_dict[p] = []
                loc_dict[p].append(n)
        for p in loc_dict: loc_dict[p] = sorted(list(set(loc_dict[p])))
    except:
        loc_dict = {"Córdoba": ["Córdoba Capital", "Villa Carlos Paz"]}

    # Cargar Barrios de Córdoba desde tu archivo geojson
    try:
        with open('cordoba.geojson', 'r', encoding='utf-8') as f:
            geo_data = json.load(f)
        barrios_cba = sorted(list(set([feat['properties']['Nombre'] for feat in geo_data['features'] if feat['properties'].get('Nombre')])))
    except:
        barrios_cba = ["Centro", "Nueva Córdoba"]

    return provincias, loc_dict, barrios_cba

PROVINCIAS, LOCALIDADES_DICT, BARRIOS_CBA = cargar_datos_geo()

# 2. Control de estado
if 'estado' not in st.session_state:
    st.session_state.estado = 'intro'
if 'categoria_actual' not in st.session_state:
    st.session_state.categoria_actual = None

# Función para imágenes de propiedades
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
    
    /* Estilo para el contenedor del buscador a la derecha */
    .search-sidebar {{
        background-color: white;
        padding: 20px;
        border-radius: 5px;
        border: 1px solid #d1d1d1;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- DATOS ---
propiedades = [
    {"tipo": "DEPARTAMENTOS", "titulo": "Penthouse Alvear", "precio": "USD 850.000", "barrio": "Recoleta", "amb": "4", "m2": "120", "img": "Deptos.jpeg"},
    {"tipo": "CASAS", "titulo": "Residencia Los Olivos", "precio": "USD 1.200.000", "barrio": "Norte", "amb": "6", "m2": "450", "img": "Casas.jpeg"},
    {"tipo": "TERRENOS", "titulo": "Lote Premium Golf", "precio": "USD 340.000", "barrio": "Country Club", "amb": "-", "m2": "1200", "img": "Terreno.jpeg"},
]

if st.session_state.estado == 'intro':
    # --- PANTALLA INTRO (SIN MODIFICAR) ---
    st.markdown("""<style>.stApp { background-color: #000000 !important; }</style>""", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; margin-top: 5vh;'><h1 style='font-size: 100px; margin-bottom: 0px; color: white;'><span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span></h1><p style='letter-spacing: 8px; color: #333; font-size: 14px; font-weight: 800; margin-bottom: 50px;'>NEGOCIOS INMOBILIARIOS</p></div>", unsafe_allow_html=True)
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

elif st.session_state.estado == 'web':
    st.markdown("<style>.stApp { background-color: #f4f4f2 !important; }</style>", unsafe_allow_html=True)
    
    # Header
    st.markdown(f"""
        <div style='text-align: center; padding-top: 20px;'>
            <div style='font-family: "Inter"; font-size: 60px; font-weight: 800; color: #1a1a1a;'>
                <span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span>
            </div>
            <div style='letter-spacing: 5px; color: #888; font-size: 12px; font-weight: 600; margin-bottom: 10px;'>NEGOCIOS INMOBILIARIOS</div>
        </div>
        """, unsafe_allow_html=True)

    # --- DISEÑO DIVIDIDO: MAPA (IZQ) Y BUSCADOR (DER) ---
    col_mapa, col_busc = st.columns([1, 1])

    with col_mapa:
        m = folium.Map(location=[-31.4167, -64.1833], zoom_start=12, tiles='CartoDB positron')
        st_folium(m, height=400, use_container_width=True, key="mapa_principal")
    
    with col_busc:
        st.markdown('<div class="search-sidebar">', unsafe_allow_html=True)
        st.markdown("<p style='font-family: Inter; font-weight: 800; margin-bottom: 10px;'>BUSCADOR AVANZADO</p>", unsafe_allow_html=True)
        
        # 1. Selector de Provincia
        prov_sel = st.selectbox("Provincia", options=["Seleccionar Provincia..."] + PROVINCIAS)
        
        # 2. Selector de Localidad (Se activa solo si hay provincia)
        opciones_loc = ["Todas las localidades"]
        if prov_sel != "Seleccionar Provincia..." and prov_sel in LOCALIDADES_DICT:
            opciones_loc = ["Todas las localidades"] + LOCALIDADES_DICT[prov_sel]
        
        loc_sel = st.selectbox("Localidad", options=opciones_loc, disabled=(prov_sel == "Seleccionar Provincia..."))
        
        # 3. Selector de Barrio (Se activa solo si es Córdoba Capital)
        es_cba_cap = (prov_sel == "Córdoba" and loc_sel == "Córdoba Capital")
        barrio_sel = st.selectbox("Barrio", 
                                  options=["Todos los barrios"] + BARRIOS_CBA if es_cba_cap else ["Selecciona Localidad primero"], 
                                  disabled=not es_cba_cap)
        
        # Filtros adicionales
        c1, c2 = st.columns(2)
        with c1: st.selectbox("Operación", ["Venta", "Alquiler"])
        with c2: st.multiselect("Tipo", ["Casa", "Depto", "Lote"])
        
        st.button("BUSCAR AHORA", use_container_width=True, type="primary")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- CATEGORÍAS Y LISTADO (MANTENIENDO TU LÓGICA) ---
    if st.session_state.categoria_actual is None:
        st.markdown("<div style='text-align: center; font-family: Inter; font-weight: 800; letter-spacing: 10px; border-top: 1px solid #d1d1d1; padding-top: 20px; margin-bottom: 40px;'>EXPLORAR</div>", unsafe_allow_html=True)
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
        cat = st.session_state.categoria_actual
        st.markdown(f"<div style='text-align: center; font-family: Inter; font-weight: 800; letter-spacing: 5px; margin-bottom: 40px;'>{cat}</div>", unsafe_allow_html=True)
        propiedades_filtradas = [p for p in propiedades if p["tipo"] == cat]
        col_list, col_spacer = st.columns([1, 2])
        for i, p in enumerate(propiedades_filtradas):
            with col_list:
                img_b64 = get_image_base64(p["img"])
                st.markdown(f"""
                    <div class="listing-card">
                        <div class="img-container-listing"><img src="data:image/jpeg;base64,{img_b64}"></div>
                        <div class="info-container">
                            <p class="prop-precio">{p['precio']}</p>
                            <p class="prop-ubicacion">{p['titulo']} | {p['barrio']}</p>
                            <p style='color: #888; font-size: 13px;'>{p['amb']} AMB  •  {p['m2']} M²</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                st.button("VER FICHA COMPLETA", key=f"ficha_{i}")
        if st.button("← VOLVER A CATEGORÍAS"):
            st.session_state.categoria_actual = None
            st.rerun()

    if st.button("← VOLVER AL INICIO"):
        st.session_state.estado = 'intro'
        st.session_state.categoria_actual = None
        st.rerun()