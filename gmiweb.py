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

# --- ESTILOS GLOBALES ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800;900&family=Nunito+Sans:wght@300;400;600&display=swap');
    @import url('https://fonts.cdnfonts.com/css/seven-segment');

    html, body {{ scrollbar-width: none; }}
    body::-webkit-scrollbar {{ display: none; }}
    
    @keyframes blinker {{ 50% {{ opacity: 0.1; }} }}

    @keyframes scan {{
        0% {{ background-position: -200% 0; }}
        100% {{ background-position: 200% 0; }}
    }}

    @keyframes doble-titileo {{
        0%, 50%, 100% {{ opacity: 1; }}
        25%, 75% {{ opacity: 0.4; }}
    }}

    .prop-precio {{ font-family: 'Inter', sans-serif; font-weight: 800; font-size: 22px; color: #1a1a1a !important; margin: 0; }}
    .prop-ubicacion {{ font-family: 'Nunito Sans', sans-serif; font-size: 14px; color: #444 !important; text-transform: uppercase; margin: 5px 0; font-weight: 600; }}
    .prop-detalles {{ color: #666 !important; font-size: 13px; font-weight: 400; }}
    
    .listing-card {{ background-color: #ffffff; margin-bottom: 30px; border-bottom: 1px solid #d1d1d1; padding: 15px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.03); }}
    .img-container-listing {{ width: 100%; height: 380px; overflow: hidden; border-radius: 4px; }}
    .img-container-listing img {{ width: 100%; height: 100%; object-fit: cover; transition: transform 0.6s ease; }}
    .img-container-listing:hover img {{ transform: scale(1.03); }}

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

    /* Estilos Ficha de Propiedad (Inspiración Compass) */
    .ficha-header {{
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        font-size: 40px;
        color: #1a1a1a;
        letter-spacing: -1px;
        line-height: 1;
    }}
    .ficha-precio {{
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        font-size: 28px;
        color: #C41E3A;
        margin: 10px 0;
    }}
    .ficha-tag {{
        display: inline-block;
        background: #f0f0f0;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        margin-right: 10px;
        text-transform: uppercase;
    }}

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

    .btn-filtro-contacto div.stButton > button {{
        background-color: #f8f9fa !important;
        border: 1px solid #ddd !important;
        color: #1a1a1a !important;
        height: 45px !important;
        font-size: 10px !important;
        margin-top: 0px !important;
    }}

    .footer-container {{
        background-color: #080808;
        color: #ffffff;
        padding: 60px 40px;
        font-family: 'Inter', sans-serif;
        margin-top: 100px;
        border-top: 3px solid #C41E3A;
    }}
    .footer-link {{ color: #888; text-decoration: none; font-size: 13px; transition: 0.3s; line-height: 2; }}
    .footer-link:hover {{ color: #ffffff; padding-left: 5px; }}

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

    .btn-float {{
        position: fixed;
        right: 30px;
        bottom: 30px;
        background-color: #C41E3A;
        color: white;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 20px rgba(196, 30, 58, 0.4);
        z-index: 9999;
        cursor: pointer;
        font-size: 24px;
        transition: 0.4s;
    }}

    .container-relativo {{
        position: relative;
        height: 50px;
        margin-top: 15px;
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        animation: doble-titileo 1s ease-in-out 1;
    }}

    .forma-boton {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px; 
        background-color: #d1d1d1;
        border-radius: 2px;
        z-index: 1;
        transition: background-color 0.2s ease;
    }}
    .forma-negra {{ background-color: #1a1a1a !important; }}
    .forma-roja {{ background-color: #C41E3A !important; }}

    .container-relativo div.stButton > button {{
        width: 100% !important;
        height: 50px !important;
        background: transparent !important;
        border: none !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 900 !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        background: linear-gradient(90deg, #000 0%, #000 40%, #888 50%, #000 60%, #000 100%) !important;
        background-size: 200% auto !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        animation: scan 3s linear infinite !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- DATOS ---
propiedades = [
    {"id": 1, "tipo": "DEPARTAMENTOS", "operacion": "Venta", "titulo": "Penthouse Alvear", "precio": "USD 850.000", "barrio": "Recoleta", "amb": "4", "m2": "120", "img": "Deptos.jpeg", "desc": "Exclusivo penthouse con vista panorámica a la ciudad. Terminaciones de lujo y amplios ventanales."},
    {"id": 2, "tipo": "DEPARTAMENTOS", "operacion": "Venta", "titulo": "Piso Estrada", "precio": "USD 240.000", "barrio": "Nueva Córdoba", "amb": "3", "m2": "95", "img": "Deptos.jpeg", "desc": "Ubicación privilegiada en el corazón de Nueva Córdoba. Piso alto, muy luminoso."},
    {"id": 3, "tipo": "DEPARTAMENTOS", "operacion": "Alquiler", "titulo": "Torre Duomo", "precio": "$ 450.000", "barrio": "Nueva Córdoba", "amb": "2", "m2": "65", "img": "Deptos.jpeg", "desc": "Amenities de primer nivel: pileta, gimnasio y seguridad 24hs."},
    {"id": 4, "tipo": "CASAS", "operacion": "Venta", "titulo": "Residencia Los Olivos", "precio": "USD 1.200.000", "barrio": "Norte", "amb": "6", "m2": "450", "img": "Casas.jpeg", "desc": "Espectacular casona estilo clásico con jardín parquizado y piscina propia."},
    {"id": 5, "tipo": "CASAS", "operacion": "Alquiler", "titulo": "Casona del Cerro", "precio": "$ 980.000", "barrio": "Cerro de las Rosas", "amb": "5", "m2": "320", "img": "Casas.jpeg", "desc": "Ideal para familias. Amplios espacios sociales y excelente entorno."},
    {"id": 6, "tipo": "CASAS", "operacion": "Venta", "titulo": "Moderna Manantiales", "precio": "USD 280.000", "barrio": "Manantiales", "amb": "4", "m2": "210", "img": "Casas.jpeg", "desc": "Casa a estrenar con diseño vanguardista en barrio con seguridad."},
    {"id": 7, "tipo": "TERRENOS", "operacion": "Venta", "titulo": "Lote Premium Golf", "precio": "USD 340.000", "barrio": "Country Club", "amb": "-", "m2": "1200", "img": "Terreno.jpeg", "desc": "Lote plano con frente al golf. El mejor entorno de la ciudad."},
    {"id": 8, "tipo": "TERRENOS", "operacion": "Venta", "titulo": "Lote Valle Escondido", "precio": "USD 125.000", "barrio": "Valle Escondido", "amb": "-", "m2": "600", "img": "Terreno.jpeg", "desc": "Lote en barrio consolidado con todos los servicios subterráneos."},
    {"id": 9, "tipo": "TERRENOS", "operacion": "Venta", "titulo": "Lote Tejas 3", "precio": "USD 55.000", "barrio": "Ruta 20", "amb": "-", "m2": "350", "img": "Terreno.jpeg", "desc": "Oportunidad de inversión en zona de gran crecimiento."},
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

# --- PANTALLA 2: SITIO WEB ---
elif st.session_state.estado == 'web':
    st.markdown("<style>.stApp { background-color: #E5E7EB !important; }</style>", unsafe_allow_html=True)
    
    st.markdown("""<a href='#' class='btn-float'>📩</a>""", unsafe_allow_html=True)

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
                if pag == "En Venta": st.session_state.operacion_filtro = "Venta"
                elif pag == "Alquiler": st.session_state.operacion_filtro = "Alquiler"
                else: st.session_state.operacion_filtro = None
                st.rerun()

    st.markdown("<hr style='margin: 15px 0; border: 0.5px solid #d1d1d1; opacity: 0.3;'>", unsafe_allow_html=True)

    # --- LÓGICA DE FICHA DETALLADA (MODO COMPASS) ---
    if st.session_state.propiedad_seleccionada:
        p = st.session_state.propiedad_seleccionada
        st.markdown("<br>", unsafe_allow_html=True)
        col_f1, col_f2 = st.columns([2, 1])
        
        with col_f1:
            img_b64 = get_image_base64(p["img"])
            st.markdown(f"""
                <div style='border-radius: 12px; overflow: hidden; height: 500px;'>
                    <img src='data:image/jpeg;base64,{img_b64}' style='width: 100%; height: 100%; object-fit: cover;'>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-family: Inter; color: #555; line-height: 1.8;'>{p['desc']}</p>", unsafe_allow_html=True)
            
        with col_f2:
            st.markdown(f"""
                <div class='ficha-header'>{p['titulo']}</div>
                <div class='ficha-precio'>{p['precio']}</div>
                <div style='margin: 20px 0;'>
                    <span class='ficha-tag'>{p['barrio']}</span>
                    <span class='ficha-tag'>{p['tipo']}</span>
                    <span class='ficha-tag'>{p['operacion']}</span>
                </div>
                <hr style='opacity: 0.1;'>
                <div style='font-family: Inter; font-size: 14px; color: #666; display: flex; flex-direction: column; gap: 10px;'>
                    <div><b>Superficie:</b> {p['m2']} m²</div>
                    <div><b>Ambientes:</b> {p['amb']}</div>
                    <div><b>Estado:</b> Excelente</div>
                </div>
                <br>
            """, unsafe_allow_html=True)
            
            st.markdown("<div class='btn-filtro-contacto'>", unsafe_allow_html=True)
            if st.button("CONSULTAR POR WHATSAPP", use_container_width=True): st.toast("Redirigiendo...")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='container-relativo'><div class='forma-boton forma-negra'></div>", unsafe_allow_html=True)
            if st.button("VOLVER AL LISTADO"):
                st.session_state.propiedad_seleccionada = None
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # --- CONTENIDO PRINCIPAL ---
    elif st.session_state.pagina_actual == "Principal":
        m = folium.Map(location=[-31.4167, -64.1833], zoom_start=12, tiles='CartoDB positron', zoom_control=False)
        st_folium(m, height=350, use_container_width=True, key="mapa_principal")
        
        st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
        f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns([1, 1, 1, 1, 1])
        with f_col1:
            st.markdown("<p class='filter-label'>UBICACIÓN</p>", unsafe_allow_html=True)
            st.selectbox("u", ["Córdoba, Argentina", "Buenos Aires, Argentina"], label_visibility="collapsed", key="u1")
        with f_col2:
            st.markdown("<p class='filter-label'>TIPO</p>", unsafe_allow_html=True)
            st.selectbox("t", ["Departamentos", "Casas", "Terrenos"], label_visibility="collapsed", key="t1")
        with f_col3:
            st.markdown("<p class='filter-label'>PRESUPUESTO (USD)</p>", unsafe_allow_html=True)
            st.selectbox("rango", ["Seleccionar Rango", "0 a 50k", "50k a 150k", "+150k"], label_visibility="collapsed", key="r1")
        with f_col4:
            st.markdown("<p class='filter-label'>OPERACIÓN</p>", unsafe_allow_html=True)
            st.selectbox("o", ["En Venta", "En Alquiler"], label_visibility="collapsed", key="o1")
        with f_col5:
            if st.button("BUSCAR", key="btn_search", use_container_width=True, type="primary"): st.toast("Buscando...")
        st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.categoria_actual is None:
            st.markdown("<br><br><br><div style='text-align: center; font-family: Inter; font-weight: 800; letter-spacing: 4px; color: #1a1a1a; margin-bottom: 30px;'>PROPIEDADES DESTACADAS</div>", unsafe_allow_html=True)
            d_col1, d_col2, d_col3 = st.columns(3)
            for i, p in enumerate([propiedades[0], propiedades[3], propiedades[6]]):
                with [d_col1, d_col2, d_col3][i]:
                    img_b64 = get_image_base64(p["img"])
                    st.markdown(f"<div class='listing-card'><div style='height: 240px; overflow: hidden; border-radius: 6px;'><img src='data:image/jpeg;base64,{img_b64}' style='width: 100%; height: 100%; object-fit: cover;'></div><div style='padding: 20px 5px;'><p class='prop-precio'>{p['precio']}</p><p class='prop-ubicacion'>{p['titulo']} | {p['barrio']}</p><p class='prop-detalles'>{p['amb']} AMBIENTES • {p['m2']} M²</p></div></div>", unsafe_allow_html=True)
                    st.markdown("<div class='container-relativo'><div class='forma-boton forma-negra'></div>", unsafe_allow_html=True)
                    if st.button("VER FICHA COMPLETA", key=f"btn_dest_{i}"):
                        st.session_state.propiedad_seleccionada = p
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            # Lista de propiedades filtrada (Estilo Compass)
            cat = st.session_state.categoria_actual
            propiedades_filtradas = propiedades if cat == "TODAS" else [p for p in propiedades if p["tipo"] == cat]
            
            st.markdown(f"<div style='text-align: center; font-family: Inter; font-weight: 800; letter-spacing: 5px; color: #C41E3A; margin: 30px 0;'>LISTADO {cat}</div>", unsafe_allow_html=True)
            
            _, col_list, _ = st.columns([1, 2, 1])
            for i, p in enumerate(propiedades_filtradas):
                with col_list:
                    img_b64 = get_image_base64(p["img"])
                    st.markdown(f"<div class='listing-card'><div class='img-container-listing'><img src='data:image/jpeg;base64,{img_b64}'></div><div style='padding: 20px 0;'><p class='prop-precio'>{p['precio']}</p><p class='prop-ubicacion'>{p['titulo']} | {p['barrio']} ({p['operacion'].upper()})</p><p class='prop-detalles'>{p['amb']} AMBIENTES • {p['m2']} M²</p></div></div>", unsafe_allow_html=True)
                    st.markdown("<div class='container-relativo'><div class='forma-boton forma-negra'></div>", unsafe_allow_html=True)
                    if st.button("VER DETALLES", key=f"ficha_{cat}_{i}"):
                        st.session_state.propiedad_seleccionada = p
                        st.rerun()
                    st.markdown("</div><br>", unsafe_allow_html=True)

    # Footer Institucional (Sin cambios)
    st.markdown(f"""
        <div class='footer-container'>
            <div style='display: flex; justify-content: space-between; flex-wrap: wrap; max-width: 1200px; margin: 0 auto;'>
                <div style='flex: 1; min-width: 300px; margin-bottom: 40px;'>
                    <div style='font-size: 24px; font-weight: 900; margin-bottom: 20px;'>GMI<span style='color: #C41E3A;'>.</span></div>
                    <p style='color: #888; font-size: 13px; line-height: 1.8; max-width: 300px;'>Líderes en el mercado de Córdoba.</p>
                </div>
                <div style='flex: 1; min-width: 200px; margin-bottom: 40px;'>
                    <div style='font-size: 14px; font-weight: 800; margin-bottom: 25px;'>NAVEGACIÓN</div>
                    <div style='display: flex; flex-direction: column;'>
                        <a href='#' class='footer-link'>Propiedades</a>
                        <a href='#' class='footer-link'>Tasaciones</a>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)