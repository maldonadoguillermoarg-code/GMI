import streamlit as st
import datetime
import time
import base64
import json
import folium
from streamlit_folium import st_folium

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="GMI | Negocios Inmobiliarios", initial_sidebar_state="collapsed")

# --- 2. CARGA DE DATOS REALES (NUEVA SECCIÓN) ---
@st.cache_data
def cargar_datos_geograficos():
    # 1. Cargar Provincias
    try:
        with open('argentina_states.json', 'r', encoding='utf-8') as f:
            provincias_data = json.load(f)
        # Adaptar según si es lista de strings o diccionarios
        provincias = sorted([p['nombre'] if isinstance(p, dict) else p for p in provincias_data])
    except:
        provincias = ["Córdoba", "Buenos Aires", "Santa Fe"]

    # 2. Cargar Localidades
    try:
        with open('argentina_localities.json', 'r', encoding='utf-8') as f:
            localidades_data = json.load(f)
        # Crear diccionario jerárquico { Provincia: [Localidades] }
        loc_dict = {}
        for item in localidades_data:
            p = item.get('provincia')
            n = item.get('nombre')
            if p and n:
                if p not in loc_dict: loc_dict[p] = []
                loc_dict[p].append(n)
        for p in loc_dict: loc_dict[p] = sorted(loc_dict[p])
    except:
        loc_dict = {"Córdoba": ["Córdoba Capital", "Villa Carlos Paz"]}

    # 3. Cargar Barrios desde cordoba.geojson
    try:
        with open('cordoba.geojson', 'r', encoding='utf-8') as f:
            geo_data = json.load(f)
        barrios_cba = sorted(list(set([feat['properties']['Nombre'] for feat in geo_data['features'] if feat['properties'].get('Nombre')])))
    except:
        barrios_cba = ["Nueva Córdoba", "Centro", "General Paz"]

    return provincias, loc_dict, barrios_cba

PROVINCIAS, LOCALIDADES_DICT, BARRIOS_CBA = cargar_datos_geograficos()

# --- 3. CONTROL DE ESTADO ---
if 'estado' not in st.session_state:
    st.session_state.estado = 'intro'
if 'categoria_actual' not in st.session_state:
    st.session_state.categoria_actual = None

# --- 4. FUNCIONES DE UTILIDAD ---
def get_image_base64(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

# --- 5. DATOS DE PROPIEDADES ---
propiedades = [
    {"tipo": "DEPARTAMENTOS", "titulo": "Penthouse Alvear", "precio": "USD 850.000", "barrio": "Recoleta", "amb": "4", "m2": "120", "img": "Deptos.jpeg"},
    {"tipo": "CASAS", "titulo": "Residencia Los Olivos", "precio": "USD 1.200.000", "barrio": "Norte", "amb": "6", "m2": "450", "img": "Casas.jpeg"},
    {"tipo": "TERRENOS", "titulo": "Lote Premium Golf", "precio": "USD 340.000", "barrio": "Country Club", "amb": "-", "m2": "1200", "img": "Terreno.jpeg"},
    {"tipo": "DEPARTAMENTOS", "titulo": "Modern Loft", "precio": "USD 210.000", "barrio": "Nueva Córdoba", "amb": "2", "m2": "65", "img": "Deptos.jpeg"},
    {"tipo": "CASAS", "titulo": "Chalet del Bosque", "precio": "USD 540.000", "barrio": "Villa Belgrano", "amb": "5", "m2": "320", "img": "Casas.jpeg"},
    {"tipo": "TERRENOS", "titulo": "Macrolote Industrial", "precio": "USD 980.000", "barrio": "Circunvalación", "amb": "-", "m2": "5000", "img": "Terreno.jpeg"},
]

# --- 6. ESTILOS CSS GENERALES Y HOUZEZ ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Nunito+Sans:wght@300;400;600&display=swap');
    @import url('https://fonts.cdnfonts.com/css/seven-segment');

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .houzez-card {
        background: white;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 30px;
        transition: 0.3s;
        border: 1px solid #eee;
        position: relative;
    }
    .houzez-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    .img-container-listing {
        width: 100%;
        height: 240px;
        overflow: hidden;
    }
    .img-container-listing img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: 0.6s;
    }
    .houzez-card:hover img { transform: scale(1.1); }
    
    .houzez-badge {
        position: absolute;
        top: 15px;
        left: 15px;
        background: #003366;
        color: white;
        padding: 5px 12px;
        font-size: 11px;
        font-weight: 700;
        border-radius: 3px;
        z-index: 10;
    }
    .houzez-price { color: #C41E3A; font-family: 'Inter'; font-weight: 800; font-size: 22px; padding: 0 20px; }
    .houzez-title { font-family: 'Inter'; font-weight: 700; font-size: 18px; color: #1a1a1a; padding: 15px 20px 5px 20px; }
    .houzez-meta {
        display: flex;
        justify-content: space-between;
        padding: 15px 20px;
        border-top: 1px solid #f0f0f0;
        color: #666;
        font-size: 13px;
    }
    
    .search-container {
        background: white;
        padding: 25px;
        border-radius: 10px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-top: -80px;
        position: relative;
        z-index: 99;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE PANTALLAS ---

if st.session_state.estado == 'intro':
    st.markdown("""
        <style>
        .stApp { background-color: #000000 !important; }
        .digital-timer {
            font-family: 'Seven Segment', sans-serif; color: #FF0000;
            font-size: clamp(45px, 10vw, 90px); text-shadow: 0 0 15px rgba(255, 0, 0, 0.7);
            text-align: center; letter-spacing: 5px; line-height: 1; margin-top: 20px;
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
        @keyframes blinker { 50% { opacity: 0.1; } }
        div.stButton > button {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: transparent !important; border: none !important; color: transparent !important; z-index: 999;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("<div style='text-align: center; margin-top: 10vh;'><h1 style='font-size: 100px; margin-bottom: 0px; color: white;'><span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span></h1><p style='letter-spacing: 8px; color: #444; font-size: 14px; font-weight: 800; margin-bottom: 50px;'>NEGOCIOS INMOBILIARIOS</p></div>", unsafe_allow_html=True)

    futuro = datetime.datetime(2026, 10, 31, 0, 0)
    ahora = datetime.datetime.now()
    dif = futuro - ahora
    dias, horas, residuo = dif.days, *divmod(dif.seconds, 3600)
    minutos, segundos = divmod(residuo, 60)
    
    st.markdown(f"<div class='digital-timer'>{dias:02d}:{horas:02d}:{minutos:02d}:{segundos:02d}</div><div class='labels-timer'>DÍAS HORAS MINUTOS SEGUNDOS</div><div class='text-link-titileo'>>>> CLICK PARA ENTRAR A LA WEB <<<</div>", unsafe_allow_html=True)

    if st.button("ENTER"):
        st.session_state.estado = 'web'
        st.rerun()
    
    time.sleep(1)
    st.rerun()

elif st.session_state.estado == 'web':
    st.markdown("<style>.stApp { background-color: #f8f9fa !important; }</style>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='text-align: center; padding: 30px 0;'>
            <div style='font-family: "Inter"; font-size: 50px; font-weight: 800; color: #1a1a1a;'>
                <span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span>
            </div>
            <div style='letter-spacing: 6px; color: #999; font-size: 11px; font-weight: 700; text-transform: uppercase;'>Negocios Inmobiliarios Premium</div>
        </div>
        """, unsafe_allow_html=True)

    m = folium.Map(location=[-31.4167, -64.1833], zoom_start=13, tiles='CartoDB positron')
    st_folium(m, height=450, use_container_width=True, key="mapa_houzez")
    
    # --- BUSCADOR EVOLUCIONADO (ESTILO CLASIFICADOS LA VOZ) ---
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    # Fila 1: Ubicación Dinámica
    col_u1, col_u2, col_u3 = st.columns(3)
    with col_u1:
        prov_sel = st.selectbox("Provincia", options=["Seleccionar..."] + PROVINCIAS)
    
    with col_u2:
        if prov_sel != "Seleccionar..." and prov_sel in LOCALIDADES_DICT:
            loc_sel = st.selectbox("Localidad", options=["Todas las localidades"] + LOCALIDADES_DICT[prov_sel])
        else:
            loc_sel = st.selectbox("Localidad", options=["-"], disabled=True)
            
    with col_u3:
        # Solo habilitamos barrios si es Córdoba Capital y cargamos los del GeoJSON
        if prov_sel == "Córdoba" and loc_sel == "Córdoba Capital":
            barrio_sel = st.selectbox("Barrio", options=["Todos los barrios"] + BARRIOS_CBA)
        else:
            barrio_sel = st.selectbox("Barrio", options=["-"], disabled=True)

    st.markdown("<hr style='margin: 15px 0; border: 0.5px solid #eee;'>", unsafe_allow_html=True)

    # Fila 2: Tipo y Precios
    col_t1, col_t2, col_t3, col_t4 = st.columns([1.5, 1, 1, 1])
    with col_t1:
        st.multiselect("Tipo de Propiedad", options=["Casa", "Departamento", "Terreno", "PH", "Oficina"], placeholder="Cualquiera")
    with col_t2:
        st.number_input("Min USD", value=0, step=5000)
    with col_t3:
        st.number_input("Max USD", value=500000, step=5000)
    with col_t4:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("BUSCAR AHORA", use_container_width=True, type="primary")
        
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Título de Sección
    st.markdown("""
        <div style='text-align: center; margin-bottom: 50px;'>
            <h2 style='font-family: Inter; font-weight: 800; font-size: 35px; color: #1a1a1a;'>Propiedades Destacadas</h2>
            <div style='width: 50px; height: 3px; background: #C41E3A; margin: 10px auto;'></div>
        </div>
    """, unsafe_allow_html=True)

    # Grid de Propiedades
    col1, col2, col3 = st.columns(3)
    for i, p in enumerate(propiedades):
        with [col1, col2, col3][i % 3]:
            img_b64 = get_image_base64(p["img"])
            st.markdown(f"""
                <div class="houzez-card">
                    <div class="houzez-badge">DESTACADO</div>
                    <div class="img-container-listing">
                        <img src="data:image/jpeg;base64,{img_b64}">
                    </div>
                    <div class="houzez-title">{p['titulo']}</div>
                    <p style="padding: 0 20px; color: #888; font-size: 14px; margin-bottom: 15px;">
                        <i class="fa fa-map-marker"></i> {p['barrio']}, Córdoba
                    </p>
                    <div class="houzez-price">{p['precio']}</div>
                    <div class="houzez-meta">
                        <span><i class="fa fa-bed"></i> {p['amb']} Dorm</span>
                        <span><i class="fa fa-bath"></i> {p['amb']} Baño</span>
                        <span><i class="fa fa-arrows-alt"></i> {p['m2']} m²</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"VER FICHA COMPLETA", key=f"btn_{i}", use_container_width=True):
                st.toast(f"Cargando detalles de {p['titulo']}...", icon="🏠")

    st.markdown("<br><br><hr>", unsafe_allow_html=True)
    if st.button("← VOLVER AL RELOJ DE LANZAMIENTO"):
        st.session_state.estado = 'intro'
        st.rerun()