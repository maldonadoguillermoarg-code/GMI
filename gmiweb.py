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
if 'categoria_actual' not in st.session_state:
    st.session_state.categoria_actual = None
if 'mostrar_mapa' not in st.session_state:
    st.session_state.mostrar_mapa = False

# Función para convertir imagen local a Base64
def get_image_base64(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

# Cargamos los GIFs (Asegurate de que los archivos estén en la misma carpeta)
ricoso_b64 = get_image_base64("ricoso.gif")
pepinillo_b64 = get_image_base64("pepinillo.gif")

# --- ESTILOS GLOBALES Y ANIMACIONES (TODO CONSERVADO) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&family=Nunito+Sans:wght@300;400;600&display=swap');
    @import url('https://fonts.cdnfonts.com/css/seven-segment');

    html, body {{ scrollbar-width: none; }}
    body::-webkit-scrollbar {{ display: none; }}
    
    @keyframes blinker {{ 50% {{ opacity: 0.1; }} }}

    @keyframes dvdBounce {{
        0%   {{ top: 0%; left: 0%; transform: rotate(0deg); }}
        25%  {{ top: 80%; left: 20%; transform: rotate(90deg); }}
        50%  {{ top: 10%; left: 80%; transform: rotate(180deg); }}
        75%  {{ top: 70%; left: 40%; transform: rotate(270deg); }}
        100% {{ top: 0%; left: 0%; transform: rotate(360deg); }}
    }}

    .pepinillo-dvd {{
        position: fixed; width: 150px; z-index: 10000;
        animation: dvdBounce 15s linear infinite; pointer-events: none;
    }}

    .ricoso-fijo {{
        position: fixed; bottom: 10px; right: 10px; width: 180px;
        z-index: 10001; pointer-events: none;
    }}

    /* ESTILO LA CONFIRMACIÓN DE MORTY (TABLA NEGRA) */
    .morty-card {{
        background-color: #000000;
        color: #ffffff;
        padding: 30px;
        border-radius: 0px;
        font-family: 'Inter', sans-serif;
        border-left: 5px solid #C41E3A;
    }}
    .morty-precio {{ font-size: 32px; font-weight: 800; margin-bottom: 5px; }}
    .morty-detalle {{ color: #888; text-transform: uppercase; letter-spacing: 2px; font-size: 12px; }}

    .listing-card {{ background-color: transparent; margin-bottom: 20px; transition: 0.3s; }}
    .img-container-listing {{ width: 100%; height: 350px; overflow: hidden; border-radius: 2px; }}
    .img-container-listing img {{ width: 100%; height: 100%; object-fit: cover; transition: transform 0.6s ease; }}
    .img-container-listing:hover img {{ transform: scale(1.05); }}
    </style>

    <div class="pepinillo-dvd"><img src="data:image/gif;base64,{pepinillo_b64}" width="100%"></div>
    <div class="ricoso-fijo"><img src="data:image/gif;base64,{ricoso_b64}" width="100%"></div>
    """, unsafe_allow_html=True)

# --- DATOS ---
propiedades = [
    {"tipo": "DEPARTAMENTOS", "titulo": "Penthouse Alvear", "precio": "USD 850.000", "barrio": "Recoleta", "amb": "4", "m2": "120", "img": "Deptos.jpeg", "coords": [-31.4167, -64.1833]},
    {"tipo": "CASAS", "titulo": "Residencia Los Olivos", "precio": "USD 1.200.000", "barrio": "Norte", "amb": "6", "m2": "450", "img": "Casas.jpeg", "coords": [-31.3900, -64.2200]},
    {"tipo": "TERRENOS", "titulo": "Lote Premium Golf", "precio": "USD 340.000", "barrio": "Country Club", "amb": "-", "m2": "1200", "img": "Terreno.jpeg", "coords": [-31.4500, -64.1500]},
]

if st.session_state.estado == 'intro':
    # PANTALLA 1: INTRO NEGRA (CONSERVADA)
    st.markdown("""
        <style>.stApp { background-color: #000000 !important; }</style>
        """, unsafe_allow_html=True)

    st.markdown("<div style='text-align: center; margin-top: 5vh;'><h1 style='font-size: 100px; margin-bottom: 0px; color: white;'><span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span></h1><p style='letter-spacing: 8px; color: #333; font-size: 14px; font-weight: 800; margin-bottom: 50px;'>NEGOCIOS INMOBILIARIOS</p></div>", unsafe_allow_html=True)

    futuro = datetime.datetime(2026, 10, 31, 0, 0)
    ahora = datetime.datetime.now()
    dif = futuro - ahora
    dias, horas, residuo = dif.days, *divmod(dif.seconds, 3600)
    minutos, segundos = divmod(residuo, 60)
    
    st.markdown(f"<div class='digital-timer' style='font-family:\"Seven Segment\"; color:#FF0000; font-size:90px; text-align:center;'>{dias:02d}:{horas:02d}:{minutos:02d}:{segundos:02d}</div><div style='color:#8B0000; text-align:center; letter-spacing:12px;'>DÍAS HORAS MINUTOS SEGUNDOS</div><div class='text-link-titileo' style='color:#FF0000; text-align:center; animation: blinker 1.2s infinite; margin-top:40px;'>>>> MIRA LOS AVANCES DE NUESTRA WEB <<<</div>", unsafe_allow_html=True)

    if st.button("ENTER", key="btn_enter"):
        st.session_state.estado = 'web'
        st.rerun()
    time.sleep(1)
    st.rerun()

elif st.session_state.estado == 'web':
    # PANTALLA 2: WEB BLANCA
    st.markdown("<style>.stApp { background-color: #f4f4f2 !important; }</style>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='text-align: center; padding-top: 20px;'>
            <div style='font-family: "Inter"; font-size: 60px; font-weight: 800; color: #1a1a1a;'>
                <span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span>
            </div>
            <div style='letter-spacing: 5px; color: #888; font-size: 12px; font-weight: 600; margin-bottom: 40px;'>NEGOCIOS INMOBILIARIOS | CÓRDOBA</div>
        </div>
        """, unsafe_allow_html=True)

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
        # VISTA FILTRADA + LA CONFIRMACIÓN DE MORTY
        cat = st.session_state.categoria_actual
        st.markdown(f"<div style='text-align: center; font-family: Inter; font-weight: 800; letter-spacing: 5px; margin-bottom: 40px;'>{cat}</div>", unsafe_allow_html=True)
        
        propiedades_filtradas = [p for p in propiedades if p["tipo"] == cat]
        
        for i, p in enumerate(propiedades_filtradas):
            col_img, col_info = st.columns([1, 1])
            with col_img:
                img_b64 = get_image_base64(p["img"])
                st.markdown(f"<div class='img-container-listing'><img src='data:image/jpeg;base64,{img_b64}'></div>", unsafe_allow_html=True)
            with col_info:
                # LA CONFIRMACIÓN DE MORTY (TABLA NEGRA)
                st.markdown(f"""
                    <div class="morty-card">
                        <div class="morty-detalle">Propiedad Seleccionada</div>
                        <div class="morty-precio">{p['precio']}</div>
                        <hr style="border-color: #333;">
                        <p style="margin: 5px 0;"><b>UBICACIÓN:</b> {p['barrio']}, Córdoba</p>
                        <p style="margin: 5px 0;"><b>MEDIDAS:</b> {p['m2']} M² Totales</p>
                        <p style="margin: 5px 0;"><b>AMBIENTES:</b> {p['amb']} Dormitorios</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"VER UBICACIÓN EN MAPA", key=f"map_btn_{i}"):
                    st.session_state.mostrar_mapa = not st.session_state.mostrar_mapa

            # MAPA DE CÓRDOBA
            if st.session_state.mostrar_mapa:
                st.markdown("<br>", unsafe_allow_html=True)
                m = folium.Map(location=p['coords'], zoom_start=14, tiles="CartoDB positron")
                folium.Marker(p['coords'], popup=p['titulo'], icon=folium.Icon(color='red')).addTo(m)
                st_folium(m, width="100%", height=400)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← VOLVER A CATEGORÍAS"):
            st.session_state.categoria_actual = None
            st.session_state.mostrar_mapa = False
            st.rerun()

    if st.button("← VOLVER AL INICIO"):
        st.session_state.estado = 'intro'
        st.session_state.categoria_actual = None
        st.rerun()