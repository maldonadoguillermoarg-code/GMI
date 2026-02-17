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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&family=Nunito+Sans:wght@300;400;600&family=Hind:wght@400;500;600;700&display=swap');
    @import url('https://fonts.cdnfonts.com/css/seven-segment');

    html, body {{ scrollbar-width: none; }}
    body::-webkit-scrollbar {{ display: none; }}
    
    @keyframes blinker {{ 50% {{ opacity: 0.1; }} }}

    .prop-precio {{ font-family: 'Inter', sans-serif; font-weight: 800; font-size: 22px; color: #1a1a1a !important; margin: 0; }}
    .prop-ubicacion {{ font-family: 'Nunito Sans', sans-serif; font-size: 14px; color: #444 !important; text-transform: uppercase; margin: 5px 0; font-weight: 600; }}
    .prop-detalles {{ color: #666 !important; font-size: 13px; font-weight: 400; }}
    
    .listing-card {{ background-color: transparent; margin-bottom: 30px; border-bottom: 1px solid #d1d1d1; padding-bottom: 20px; }}
    .img-container-listing {{ width: 100%; height: 380px; overflow: hidden; border-radius: 4px; }}
    .img-container-listing img {{ width: 100%; height: 100%; object-fit: cover; transition: transform 0.6s ease; }}
    .img-container-listing:hover img {{ transform: scale(1.03); }}

    /* ESTILO FICHA ZONAPROP PARA HOJA DE RESULTADOS */
    .zp-card {{
        font-family: 'Hind', sans-serif;
        width: 100%;
        border: 1px solid #ededed;
        border-radius: 8px;
        display: flex;
        background: #fff;
        overflow: hidden;
        margin-bottom: 20px;
        text-align: left;
    }}
    .zp-gallery {{ width: 35%; min-height: 220px; background-size: cover; background-position: center; }}
    .zp-content {{ width: 65%; padding: 20px; display: flex; flex-direction: column; justify-content: space-between; }}
    .zp-price {{ font-size: 24px; font-weight: 700; color: #484848; }}
    .zp-location {{ font-size: 16px; color: #f50; font-weight: 500; margin: 5px 0; }}
    .zp-features {{ display: flex; gap: 15px; color: #727272; font-size: 14px; margin: 10px 0; }}

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

    /* Botón Gris GMI (Detalles/Acción) */
    div.stButton > button {{
        background-color: #f0f0f0 !important;
        border: 1px solid #d1d1d1 !important;
        color: #1a1a1a !important;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-size: 12px;
        height: 45px !important;
        border-radius: 4px !important;
        transition: 0.3s;
    }}
    div.stButton > button:hover {{
        background-color: #e0e0e0 !important;
        color: #C41E3A !important;
        border-color: #1a1a1a !important;
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

    .stButton>button:has(div.img-container-listing) {{
        padding: 0 !important;
        border: none !important;
        background: none !important;
        width: 100% !important;
    }}

    /* Estilo Banner */
    .banner-container-edificios {{
        width: 100%;
        border-radius: 8px;
        overflow: hidden;
        margin-top: 40px;
    }}
    .banner-container-edificios img {{
        width: 100%;
        height: 350px;
        object-fit: cover;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- DATOS ---
propiedades = [
    {"id": 1, "tipo": "DEPARTAMENTOS", "titulo": "Penthouse Alvear", "precio": "USD 850.000", "barrio": "Recoleta", "amb": "4", "m2": "120", "img": "Deptos.jpeg", "desc": "Exclusivo departamento con vistas panorámicas."},
    {"id": 2, "tipo": "DEPARTAMENTOS", "titulo": "Piso Estrada", "precio": "USD 240.000", "barrio": "Nueva Córdoba", "amb": "3", "m2": "95", "img": "Deptos.jpeg", "desc": "Ubicación privilegiada en el corazón estudiantil."},
    {"id": 4, "tipo": "CASAS", "titulo": "Residencia Los Olivos", "precio": "USD 1.200.000", "barrio": "Norte", "amb": "6", "m2": "450", "img": "Casas.jpeg", "desc": "Propiedad de lujo con piscina y gran parque."},
    {"id": 7, "tipo": "TERRENOS", "titulo": "Lote Premium Golf", "precio": "USD 340.000", "barrio": "Country Club", "amb": "-", "m2": "1200", "img": "Terreno.jpeg", "desc": "Terreno nivelado frente al campo de golf."}
]

# --- PANTALLA 1: RELOJ (INTRO) ---
if st.session_state.estado == 'intro':
    st.markdown("""<style>.stApp { background-color: #000000 !important; }</style>""", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; margin-top: 10vh;'><h1 style='font-size: 100px; margin-bottom: 0px; color: white;'><span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span></h1><p style='letter-spacing: 8px; color: #444; font-size: 14px; font-weight: 800; margin-bottom: 50px;'>NEGOCIOS INMOBILIARIOS</p></div>", unsafe_allow_html=True)

    futuro = datetime.datetime(2026, 10, 31, 0, 0)
    ahora = datetime.datetime.now()
    dif = futuro - ahora
    dias, horas, residuo = dif.days, *divmod(dif.seconds, 3600)
    minutos, segundos = divmod(residuo, 60)
    
    st.markdown(f"<div style='font-family: \"Seven Segment\", sans-serif; color: #FF0000; font-size: 80px; text-align: center;'>{dias:02d}:{horas:02d}:{minutos:02d}:{segundos:02d}</div><div style='color: #8B0000; text-align: center; letter-spacing: 12px; font-size: 14px; font-weight: 800; text-transform: uppercase;'>DÍAS HORAS MINUTOS SEGUNDOS</div><div style='color: #FF0000; text-align: center; margin-top: 40px; animation: blinker 1.2s linear infinite; font-weight: 900; letter-spacing: 3px;'>MIRA LOS AVANCES DE NUESTRA WEB</div>", unsafe_allow_html=True)

    if st.button("ENTER", key="btn_enter_invisible", use_container_width=True):
        st.session_state.estado = 'web'
        st.rerun()
    time.sleep(1)
    st.rerun()

# --- PANTALLA 2: SITIO WEB ---
elif st.session_state.estado == 'web':
    st.markdown("<style>.stApp { background-color: #f4f4f2 !important; }</style>", unsafe_allow_html=True)
    
    head_col1, head_col2 = st.columns([1.5, 3])
    with head_col1:
        st.markdown("<div style='text-align: left; padding-left: 30px;'><div style='font-family: \"Inter\"; font-size: 45px; font-weight: 800; line-height: 0.9; color: #1a1a1a;'><span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span></div><div style='letter-spacing: 4px; color: #666; font-size: 10px; font-weight: 700; margin-top: 5px;'>NEGOCIOS INMOBILIARIOS</div></div>", unsafe_allow_html=True)
            
    with head_col2:
        nav_cols = st.columns(6)
        paginas = ["Principal", "En Venta", "Alquiler", "Tasaciones", "Administracion", "Contacto"]
        for i, pag in enumerate(paginas):
            label = f" {pag} " if st.session_state.pagina_actual != pag else f"● {pag}"
            if nav_cols[i].button(label, key=f"nav_{pag}"):
                st.session_state.pagina_actual = pag
                st.session_state.categoria_actual = None
                st.rerun()

    st.markdown("<hr style='margin: 15px 0; border: 0.5px solid #d1d1d1; opacity: 0.3;'>", unsafe_allow_html=True)

    if st.session_state.pagina_actual == "Principal":
        # Si no estamos en una sub-hoja (carpeta), mostramos la Home
        if st.session_state.categoria_actual is None:
            m = folium.Map(location=[-31.4167, -64.1833], zoom_start=12, tiles='CartoDB positron', zoom_control=False)
            st_folium(m, height=350, use_container_width=True, key="mapa_p")
            
            # --- SUPER FILTRO ---
            st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
            f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns([1, 1, 1, 1, 1])
            with f_col1: st.markdown("<p class='filter-label'>UBICACIÓN</p>", unsafe_allow_html=True); st.selectbox("u", ["Córdoba", "Buenos Aires"], label_visibility="collapsed", key="u1")
            with f_col2: st.markdown("<p class='filter-label'>TIPO</p>", unsafe_allow_html=True); st.selectbox("t", ["Departamentos", "Casas", "Terrenos"], label_visibility="collapsed", key="t1")
            with f_col3: st.markdown("<p class='filter-label'>PRESUPUESTO</p>", unsafe_allow_html=True); st.selectbox("r", ["Cualquiera", "0-100k"], label_visibility="collapsed", key="r1")
            with f_col4: st.markdown("<p class='filter-label'>OPERACIÓN</p>", unsafe_allow_html=True); st.selectbox("o", ["Venta", "Alquiler"], label_visibility="collapsed", key="o1")
            with f_col5: st.button("BUSCAR", key="btn_search", use_container_width=True, type="primary")
            st.markdown("</div>", unsafe_allow_html=True)

            # --- CAMBIO QUIRÚRGICO: BANNER Y BOTÓN CARPETA ---
            st.markdown("<div class='banner-container-edificios'>", unsafe_allow_html=True)
            banner_b64 = get_image_base64("Córdoba_banner2.jpg")
            st.markdown(f"<img src='data:image/jpeg;base64,{banner_b64}'></div>", unsafe_allow_html=True)
            
            _, col_btn_folder, _ = st.columns([1, 1, 1])
            with col_btn_folder:
                if st.button("PROPIEDADES DISPONIBLES", use_container_width=True):
                    st.session_state.categoria_actual = "TODAS"
                    st.rerun()

            st.markdown("<br><br><br><div style='text-align: center; font-family: Inter; font-weight: 800; letter-spacing: 12px; color: #1a1a1a; margin-bottom: 40px;'>EXPLORAR</div>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            for i, (nombre, img) in enumerate([("DEPARTAMENTOS", "Deptos.jpeg"), ("CASAS", "Casas.jpeg"), ("TERRENOS", "Terreno.jpeg")]):
                with [col1, col2, col3][i]:
                    img_b64 = get_image_base64(img)
                    if st.button(f" ", key=f"img_cat_{nombre}"):
                        st.session_state.categoria_actual = nombre
                        st.rerun()
                    st.markdown(f"<div style='margin-top: -65px;' class='img-container-listing'><img src='data:image/jpeg;base64,{img_b64}'></div>", unsafe_allow_html=True)
                    st.button(nombre, key=f"cat_{nombre}", use_container_width=True)

        # --- HOJA DE PROPIEDADES (LA CARPETA) ---
        else:
            cat = st.session_state.categoria_actual
            st.markdown(f"<div style='text-align: center; font-family: Inter; font-weight: 800; letter-spacing: 5px; color: #C41E3A; margin-bottom: 40px;'>{cat}</div>", unsafe_allow_html=True)
            
            # Filtramos si es una categoría específica o mostramos todas
            pro_filt = propiedades if cat == "TODAS" else [p for p in propiedades if p["tipo"] == cat]
            
            _, col_list, _ = st.columns([1, 3, 1])
            with col_list:
                for i, p in enumerate(pro_filt):
                    img_b64 = get_image_base64(p["img"])
                    st.markdown(f"""
                        <div class="zp-card">
                            <div class="zp-gallery" style="background-image: url('data:image/jpeg;base64,{img_b64}')"></div>
                            <div class="zp-content">
                                <div>
                                    <div class="zp-price">{p['precio']}</div>
                                    <div class="zp-location">{p['barrio']}</div>
                                    <div class="zp-features">
                                        <span><b>{p['m2']}</b> m²</span> • <span><b>{p['amb']}</b> amb.</span> • <span><b>{p['tipo']}</b></span>
                                    </div>
                                    <div style="font-size: 14px; color: #666;">{p['desc']}</div>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.button(f"VER DETALLES DE {p['titulo'].upper()}", key=f"det_{i}", use_container_width=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("← VOLVER AL INICIO", use_container_width=True):
                    st.session_state.categoria_actual = None
                    st.rerun()

    # Footer
    st.markdown(f"""<div class="footer-container"><p style="text-align: center; font-size: 10px; color: #444;">© 2026 GMI NEGOCIOS INMOBILIARIOS. TODOS LOS DERECHOS RESERVADOS.</p></div>""", unsafe_allow_html=True)