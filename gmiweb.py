import streamlit as st
import datetime
import time
import base64
import json
import folium
from streamlit_folium import st_folium

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="GMI | Negocios Inmobiliarios", initial_sidebar_state="collapsed")

# --- 2. CARGA DE DATOS REALES ---
@st.cache_data
def cargar_datos_geograficos():
    # Cargar Provincias
    try:
        with open('argentina_states.json', 'r', encoding='utf-8') as f:
            provincias_data = json.load(f)
        # Probamos distintos formatos comunes de JSON
        if isinstance(provincias_data, list):
            provincias = sorted([p['nombre'] if isinstance(p, dict) else p for p in provincias_data])
        else:
            provincias = sorted(list(provincias_data.keys()))
    except:
        provincias = ["Córdoba", "Buenos Aires", "Santa Fe"]

    # Cargar Localidades
    loc_dict = {}
    try:
        with open('argentina_localities.json', 'r', encoding='utf-8') as f:
            localidades_data = json.load(f)
        for item in localidades_data:
            # Ajusta 'provincia' y 'nombre' según tus archivos
            p = item.get('provincia') or item.get('state')
            n = item.get('nombre') or item.get('city')
            if p and n:
                if p not in loc_dict: loc_dict[p] = []
                loc_dict[p].append(n)
        for p in loc_dict: loc_dict[p] = sorted(list(set(loc_dict[p])))
    except:
        loc_dict = {"Córdoba": ["Córdoba Capital", "Villa Carlos Paz"]}

    # Cargar Barrios desde cordoba.geojson
    try:
        with open('cordoba.geojson', 'r', encoding='utf-8') as f:
            geo_data = json.load(f)
        # Buscamos el nombre en las propiedades del GeoJSON
        barrios_cba = sorted(list(set([feat['properties'].get('Nombre') or feat['properties'].get('nombre') 
                                       for feat in geo_data['features'] if feat['properties']])))
        barrios_cba = [b for b in barrios_cba if b] # Quitar nulos
    except:
        barrios_cba = ["Nueva Córdoba", "Centro", "General Paz"]

    return provincias, loc_dict, barrios_cba

PROVINCIAS, LOCALIDADES_DICT, BARRIOS_CBA = cargar_datos_geograficos()

# --- 3. FUNCIONES DE UTILIDAD ---
def get_image_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except: return ""

if 'estado' not in st.session_state: st.session_state.estado = 'intro'

# --- 4. ESTILOS CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    @import url('https://fonts.cdnfonts.com/css/seven-segment');
    
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #f8f9fa; }
    
    /* Buscador al costado */
    .search-sidebar-style {
        background: white;
        padding: 25px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #eee;
        height: 100%;
    }
    
    .houzez-card {
        background: white; border-radius: 8px; overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px;
        transition: 0.3s; border: 1px solid #eee;
    }
    .houzez-card:hover { transform: translateY(-5px); }
    .price-style { color: #C41E3A; font-weight: 800; font-size: 20px; padding: 10px 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. LÓGICA DE PANTALLAS ---

if st.session_state.estado == 'intro':
    # (Mantengo tu intro igual para no romper nada)
    st.markdown("<style>.stApp { background-color: #000 !important; }</style>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; margin-top: 15vh; color: white;'><h1 style='font-size: 100px;'>GMI</h1></div>", unsafe_allow_html=True)
    diff = datetime.datetime(2026, 10, 31) - datetime.datetime.now()
    st.markdown(f"<div style='font-family:\"Seven Segment\"; color:red; font-size:80px; text-align:center;'>{diff.days}:{diff.seconds//3600:02d}:{(diff.seconds//60)%60:02d}</div>", unsafe_allow_html=True)
    if st.button("ENTRAR"):
        st.session_state.estado = 'web'
        st.rerun()
    time.sleep(1)
    st.rerun()

elif st.session_state.estado == 'web':
    # Header
    st.markdown("<h1 style='text-align:center; font-family:Inter; font-weight:800;'>GMI Negocios Inmobiliarios</h1>", unsafe_allow_html=True)
    
    # --- MITAD MAPA / MITAD BUSCADOR ---
    col_mapa, col_buscador = st.columns([1, 1])
    
    with col_mapa:
        m = folium.Map(location=[-31.4167, -64.1833], zoom_start=12, tiles='CartoDB positron')
        st_folium(m, height=450, use_container_width=True, key="mapa_web")

    with col_buscador:
        st.markdown('<div class="search-sidebar-style">', unsafe_allow_html=True)
        st.subheader("🔎 Encontrá tu próxima propiedad")
        
        # Lógica de selectores vinculados
        prov_sel = st.selectbox("Provincia", options=["Seleccionar..."] + PROVINCIAS)
        
        # Filtro de Localidades según Provincia
        opciones_loc = ["Todas las localidades"]
        if prov_sel != "Seleccionar..." and prov_sel in LOCALIDADES_DICT:
            opciones_loc = ["Todas las localidades"] + LOCALIDADES_DICT[prov_sel]
        
        loc_sel = st.selectbox("Localidad", options=opciones_loc, disabled=(prov_sel == "Seleccionar..."))
        
        # Filtro de Barrios (Solo si es Cba Cap)
        es_cba_cap = (prov_sel == "Córdoba" and loc_sel == "Córdoba Capital")
        barrio_sel = st.selectbox("Barrio", 
                                  options=["Todos los barrios"] + BARRIOS_CBA if es_cba_cap else ["-"], 
                                  disabled=not es_cba_cap)
        
        # Otros filtros
        c1, c2 = st.columns(2)
        with c1: st.multiselect("Tipo", ["Casa", "Depto", "Lote"])
        with c2: st.selectbox("Operación", ["Venta", "Alquiler"])
        
        st.button("APLICAR FILTROS", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- GRILLA DE PROPIEDADES ABAJO ---
    st.markdown("<br><h3 style='text-align:center;'>Propiedades Destacadas</h3>", unsafe_allow_html=True)
    
    grid = st.columns(3)
    # Datos de ejemplo (se pueden conectar a una base de datos luego)
    props = [
        {"t": "Penthouse Alvear", "p": "USD 850.000", "b": "Recoleta", "img": "Deptos.jpeg"},
        {"t": "Residencia Olivos", "p": "USD 1.2M", "b": "Norte", "img": "Casas.jpeg"},
        {"t": "Lote Premium", "p": "USD 340.000", "b": "Country", "img": "Terreno.jpeg"}
    ]
    
    for i, p in enumerate(props):
        with grid[i % 3]:
            img_b64 = get_image_base64(p["img"])
            st.markdown(f"""
                <div class="houzez-card">
                    <img src="data:image/jpeg;base64,{img_b64}" style="width:100%; height:200px; object-fit:cover;">
                    <div style="padding:15px;">
                        <h4 style="margin:0;">{p['t']}</h4>
                        <p style="color:gray;">{p['b']}</p>
                    </div>
                    <div class="price-style">{p['p']}</div>
                </div>
            """, unsafe_allow_html=True)
            st.button("Ver Detalle", key=f"v_{i}", use_container_width=True)

    if st.button("← VOLVER"):
        st.session_state.estado = 'intro'
        st.rerun()