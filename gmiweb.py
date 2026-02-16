import streamlit as st
import datetime
import time
import base64
import json
import folium
from streamlit_folium import st_folium

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="GMI | Negocios Inmobiliarios", initial_sidebar_state="collapsed")

# --- 2. CONTROL DE ESTADO ---
if 'estado' not in st.session_state:
    st.session_state.estado = 'intro'
if 'categoria_actual' not in st.session_state:
    st.session_state.categoria_actual = None

# --- 3. CARGA DE DATOS PARA BUSCADOR (NUEVO) ---
@st.cache_data
def cargar_base_predictiva():
    sugerencias = []
    try:
        with open('argentina_states.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            sugerencias += [p['nombre'] for p in data] if isinstance(data[0], dict) else data
    except: pass
    try:
        with open('argentina_localities.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            sugerencias += [l['nombre'] for l in data]
    except: pass
    try:
        with open('cordoba.geojson', 'r', encoding='utf-8') as f:
            data = json.load(f)
            sugerencias += [feat['properties']['Nombre'] for feat in data['features'] if feat['properties'].get('Nombre')]
    except: pass
    return sorted(list(set(sugerencias)))

OPCIONES_BUSQUEDA = cargar_base_predictiva()

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
        background: white; border-radius: 8px; overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 30px;
        transition: 0.3s; border: 1px solid #eee; position: relative;
    }
    .houzez-card:hover { transform: translateY(-5px); box-shadow: 0 8px 25px rgba(0,0,0,0.1); }
    .img-container-listing { width: 100%; height: 240px; overflow: hidden; }
    .img-container-listing img { width: 100%; height: 100%; object-fit: cover; transition: 0.6s; }
    
    .houzez-badge {
        position: absolute; top: 15px; left: 15px; background: #003366;
        color: white; padding: 5px 12px; font-size: 11px; font-weight: 700;
        border-radius: 3px; z-index: 10;
    }
    .houzez-price { color: #C41E3A; font-family: 'Inter'; font-weight: 800; font-size: 22px; padding: 0 20px; }
    .houzez-title { font-family: 'Inter'; font-weight: 700; font-size: 18px; color: #1a1a1a; padding: 15px 20px 5px 20px; }
    .houzez-meta {
        display: flex; justify-content: space-between; padding: 15px 20px;
        border-top: 1px solid #f0f0f0; color: #666; font-size: 13px;
    }
    
    .search-container-box {
        background: white; padding: 25px; border-radius: 10px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); border: 1px solid #eee;
    }

    .map-preview-card {
        border: 2px dashed #ddd;
        border-radius: 8px;
        padding: 30px 20px;
        text-align: center;
        color: #999;
        margin-bottom: 25px;
        background: #fafafa;
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
    
    # Header
    st.markdown(f"""
        <div style='text-align: center; padding: 30px 0;'>
            <div style='font-family: "Inter"; font-size: 50px; font-weight: 800; color: #1a1a1a;'>
                <span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span>
            </div>
            <div style='letter-spacing: 6px; color: #999; font-size: 11px; font-weight: 700; text-transform: uppercase;'>Negocios Inmobiliarios Premium</div>
        </div>
        """, unsafe_allow_html=True)

    # --- DISEÑO 50/50: MAPA Y BUSCADOR ---
    col_izq, col_der = st.columns([1, 1])
    
    with col_izq:
        m = folium.Map(location=[-31.4167, -64.1833], zoom_start=13, tiles='CartoDB positron')
        st_folium(m, height=450, use_container_width=True, key="mapa_houzez")
    
    with col_der:
        st.markdown('<div class="search-container-box">', unsafe_allow_html=True)
        
        # ARRIBA: Cuadrado para vista previa de propiedad seleccionada en el mapa
        st.markdown("""
            <div class="map-preview-card">
                <p style="font-family: Inter; font-weight: 600; font-size: 14px; margin: 0; color: #555;">PROPIEDAD SELECCIONADA</p>
                <p style="font-size: 12px; margin-top: 5px;">Toca un pin en el mapa para ver los detalles aquí.</p>
            </div>
        """, unsafe_allow_html=True)

        # ABAJO: Filtros de búsqueda
        seleccion = st.selectbox(
            "Localidad o Barrio", 
            options=[""] + OPCIONES_BUSQUEDA,
            format_func=lambda x: "Escribí para buscar (Ej: Nueva Córdoba)..." if x == "" else x
        )
        
        c1, c2 = st.columns(2)
        with c1: st.selectbox("Operación", ["Venta", "Alquiler"], key="op_web")
        with c2: st.selectbox("Tipo de Propiedad", ["Departamentos", "Casas", "Terrenos"], key="tipo_web")
        
        if st.button("PONTE RICKOSO", use_container_width=True, type="primary"):
            st.toast(f"Buscando en {seleccion}...")

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
                    <div class="img-container-listing"><img src="data:image/jpeg;base64,{img_b64}"></div>
                    <div class="houzez-title">{p['titulo']}</div>
                    <p style="padding: 0 20px; color: #888; font-size: 14px; margin-bottom: 15px;">
                        {p['barrio']}, Córdoba
                    </p>
                    <div class="houzez-price">{p['precio']}</div>
                    <div class="houzez-meta">
                        <span>{p['amb']} Dorm</span>
                        <span>{p['m2']} m²</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.button(f"VER FICHA COMPLETA", key=f"btn_{i}", use_container_width=True)

    st.markdown("<br><br><hr>", unsafe_allow_html=True)
    if st.button("← VOLVER AL RELOJ DE LANZAMIENTO"):
        st.session_state.estado = 'intro'
        st.rerun()