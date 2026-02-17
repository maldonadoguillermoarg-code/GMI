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
    
    /* Estilo Zonaprop para Listado */
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
    .img-side {{ width: 350px; height: 230px; overflow: hidden; }}
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

    div[data-testid="stCheckbox"] label p {{
        color: #1a1a1a !important;
        font-weight: 600;
        margin-top: 5px;
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

    /* Footer */
    .footer-container {{
        background-color: #1a1a1a;
        color: #ffffff;
        padding: 80px 60px;
        font-family: 'Inter', sans-serif;
        margin-top: 80px;
    }}

    /* Navbar Custom */
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

# --- DATOS AMPLIADOS PARA FICHA ---
propiedades = [
    {"id": 1, "tipo": "DEPARTAMENTOS", "titulo": "Penthouse Alvear", "precio": "USD 850.000", "barrio": "Recoleta", "amb": "4", "dorm": "3", "baños": "2", "m2": "120", "img": "Deptos.jpeg", "desc": "Exclusivo penthouse con vista al río. Terminaciones de lujo, seguridad 24hs y cochera doble."},
    {"id": 2, "tipo": "CASAS", "titulo": "Residencia Los Olivos", "precio": "USD 1.200.000", "barrio": "Norte", "amb": "6", "dorm": "4", "baños": "3", "m2": "450", "img": "Casas.jpeg", "desc": "Casa de estilo moderno desarrollada en dos plantas. Gran jardín con pileta, quincho y dependencia."},
    {"id": 3, "tipo": "TERRENOS", "titulo": "Lote Premium Golf", "precio": "USD 340.000", "barrio": "Country Club", "amb": "-", "dorm": "-", "baños": "-", "m2": "1200", "img": "Terreno.jpeg", "desc": "Excelente lote central con fondo al golf. Nivelado y listo para construir."},
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

    st.markdown("<div style='text-align: center; margin-top: 10vh;'><h1 style='font-size: 100px; margin-bottom: 0px; color: white;'><span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span></h1><p style='letter-spacing: 8px; color: #444; font-size: 14px; font-weight: 800; margin-bottom: 50px;'>NEGOCIOS INMOBILIARIOS</p></div>", unsafe_allow_html=True)

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
    
    st.markdown("<br>", unsafe_allow_html=True)
    head_col1, head_col2 = st.columns([1.5, 3])
    
    with head_col1:
        st.markdown(f"""
            <div style='text-align: left; padding-left: 30px;'>
                <div style='font-family: "Inter"; font-size: 45px; font-weight: 800; line-height: 0.9; color: #1a1a1a;'>
                    <span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span>
                </div>
                <div style='letter-spacing: 4px; color: #666; font-size: 10px; font-weight: 700; margin-top: 5px; line-height: 1.2;'>
                    NEGOCIOS<br>INMOBILIARIOS
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    with head_col2:
        nav_cols = st.columns(6)
        paginas = ["Principal", "En Venta", "Alquiler", "Tasaciones", "Administracion", "Contacto"]
        for i, pag in enumerate(paginas):
            label = f" {pag} " if st.session_state.pagina_actual != pag else f"● {pag}"
            if nav_cols[i].button(label, key=f"nav_{pag}"):
                st.session_state.pagina_actual = pag
                st.session_state.categoria_actual = None
                st.session_state.propiedad_seleccionada = None
                st.rerun()

    st.markdown("<hr style='margin: 15px 0; border: 0.5px solid #d1d1d1; opacity: 0.3;'>", unsafe_allow_html=True)

    # --- LÓGICA DE NAVEGACIÓN ---
    if st.session_state.propiedad_seleccionada:
        # --- VISTA: FICHA DEL INMUEBLE (TIPO ZONAPROP) ---
        p = st.session_state.propiedad_seleccionada
        if st.button("← VOLVER AL LISTADO"):
            st.session_state.propiedad_seleccionada = None
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        img_b64 = get_image_base64(p["img"])
        
        # Grid de Imágenes superior
        st.markdown(f"""
            <div style='display: grid; grid-template-columns: 2fr 1fr; gap: 10px; height: 500px; margin-bottom: 30px;'>
                <div style='overflow: hidden; border-radius: 8px 0 0 8px;'>
                    <img src='data:image/jpeg;base64,{img_b64}' style='width: 100%; height: 100%; object-fit: cover;'>
                </div>
                <div style='display: grid; grid-template-rows: 1fr 1fr; gap: 10px;'>
                    <div style='background: #ddd; border-radius: 0 8px 0 0;'></div>
                    <div style='background: #ccc; border-radius: 0 0 8px 0;'></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        col_main, col_side = st.columns([2, 1])
        
        with col_main:
            st.markdown(f"""
                <div class='ficha-container'>
                    <h1 style='font-family: Inter; font-weight: 800; font-size: 32px; margin-bottom: 5px;'>{p['titulo']}</h1>
                    <p style='color: #666; font-size: 18px; margin-bottom: 20px;'>{p['barrio']}, Córdoba</p>
                    <hr>
                    <div style='display: flex; gap: 40px; margin: 25px 0;'>
                        <div><p style='font-size: 12px; color: #888; margin: 0;'>SUP. TOTAL</p><b>{p['m2']} m²</b></div>
                        <div><p style='font-size: 12px; color: #888; margin: 0;'>DORMITORIOS</p><b>{p['dorm']}</b></div>
                        <div><p style='font-size: 12px; color: #888; margin: 0;'>BAÑOS</p><b>{p['baños']}</b></div>
                        <div><p style='font-size: 12px; color: #888; margin: 0;'>AMBIENTES</p><b>{p['amb']}</b></div>
                    </div>
                    <hr>
                    <h3 style='margin-top: 30px;'>Descripción</h3>
                    <p style='color: #444; line-height: 1.8;'>{p['desc']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br><h3>Ubicación</h3>", unsafe_allow_html=True)
            m = folium.Map(location=[-31.4167, -64.1833], zoom_start=15, tiles='CartoDB positron')
            folium.Marker([-31.4167, -64.1833]).add_to(m)
            st_folium(m, height=300, use_container_width=True, key="mapa_ficha")

        with col_side:
            st.markdown(f"""
                <div class='sidebar-contacto'>
                    <h2 style='font-family: Inter; font-weight: 800; color: #1a1a1a;'>{p['precio']}</h2>
                    <p style='color: #666; font-size: 13px;'>Expensas: Consultar</p>
                    <br>
                    <input type='text' placeholder='Nombre' style='width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ddd; border-radius: 4px;'>
                    <input type='text' placeholder='Email' style='width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ddd; border-radius: 4px;'>
                    <textarea placeholder='Me interesa esta propiedad...' style='width: 100%; padding: 10px; height: 100px; border: 1px solid #ddd; border-radius: 4px;'></textarea>
                </div>
            """, unsafe_allow_html=True)
            st.button("CONTACTAR", type="primary", use_container_width=True)
            st.button("WhatsApp", use_container_width=True)

    elif st.session_state.pagina_actual == "Principal":
        # --- VISTA: HOME ---
        if st.session_state.categoria_actual is None:
            m = folium.Map(location=[-31.4167, -64.1833], zoom_start=12, tiles='CartoDB positron', zoom_control=False)
            st_folium(m, height=350, use_container_width=True, key="mapa_principal")
            
            # --- SUPER FILTRO ---
            st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
            f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns([1, 1, 1, 1, 1])
            with f_col1:
                st.markdown("<p class='filter-label'>UBICACIÓN</p>", unsafe_allow_html=True)
                st.selectbox("u", ["Argentina, Córdoba"], label_visibility="collapsed", key="u1")
            with f_col2:
                st.markdown("<p class='filter-label'>TIPO</p>", unsafe_allow_html=True)
                st.selectbox("t", ["Departamentos", "Casas", "Terrenos"], label_visibility="collapsed", key="t1")
            with f_col3:
                st.markdown("<p class='filter-label'>PRESUPUESTO (USD)</p>", unsafe_allow_html=True)
                st.selectbox("rango", ["Seleccionar Rango", "0-50k", "50-100k", "100k+"], label_visibility="collapsed", key="rango_p")
            with f_col4:
                st.markdown("<p class='filter-label'>OPERACIÓN</p>", unsafe_allow_html=True)
                st.selectbox("o", ["En Venta", "En Alquiler"], label_visibility="collapsed", key="o1")
            with f_col5:
                st.button("BUSCAR", key="btn_search", use_container_width=True, type="primary")
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<br><br><br>", unsafe_allow_html=True)

            st.markdown("<div style='text-align: center; font-family: Inter; font-weight: 800; letter-spacing: 12px; color: #1a1a1a; margin-bottom: 40px;'>EXPLORAR</div>", unsafe_allow_html=True)
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
            # --- VISTA: LISTADO (TIPO ZONAPROP) ---
            cat = st.session_state.categoria_actual
            st.markdown(f"<h2 style='font-family: Inter; font-weight: 800; text-align: center;'>{cat} DISPONIBLES</h2>", unsafe_allow_html=True)
            
            propiedades_filtradas = [p for p in propiedades if p["tipo"] == cat]
            
            _, col_list, _ = st.columns([1, 4, 1])
            with col_list:
                for p in propiedades_filtradas:
                    img_b64 = get_image_base64(p["img"])
                    st.markdown(f"""
                        <div class='listing-card-horizontal'>
                            <div class='img-side'><img src='data:image/jpeg;base64,{img_b64}'></div>
                            <div class='info-side'>
                                <div>
                                    <p class='prop-precio'>{p['precio']}</p>
                                    <p class='prop-ubicacion'>{p['titulo']} | {p['barrio']}</p>
                                    <p class='prop-detalles'>{p['m2']} m² • {p['amb']} amb. • {p['dorm']} dorm.</p>
                                    <p style='font-size: 13px; color: #777; margin-top: 10px;'>{p['desc'][:100]}...</p>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"VER DETALLES: {p['titulo']}", key=f"det_{p['id']}", use_container_width=True):
                        st.session_state.propiedad_seleccionada = p
                        st.rerun()

                if st.button("← VOLVER A CATEGORÍAS", use_container_width=True):
                    st.session_state.categoria_actual = None
                    st.rerun()

    # --- PIE DE PÁGINA ---
    st.markdown("""
        <div class="footer-container">
            <div style="display: flex; justify-content: space-between; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 250px; margin-bottom: 30px;">
                    <h2 style="color: white; margin: 0;"><span style="color: #003366;">G</span>M<span style="color: #C41E3A;">I</span></h2>
                    <p style="font-size: 11px; letter-spacing: 3px; color: #666; font-weight: 800; margin-top: 5px;">NEGOCIOS INMOBILIARIOS</p>
                </div>
            </div>
            <hr style="border: 0.1px solid #333; margin: 40px 0;">
            <p style="text-align: center; font-size: 10px; color: #444;">© 2026 GMI NEGOCIOS INMOBILIARIOS.</p>
        </div>
    """, unsafe_allow_html=True)