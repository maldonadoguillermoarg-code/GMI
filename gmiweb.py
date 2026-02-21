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

    /* Estilos Tasaciones Especiales */
    .tasacion-titulo {{
        color: #C41E3A;
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        font-size: 60px;
        text-align: left;
        margin-bottom: 10px;
        letter-spacing: -1px;
    }}

    .tasacion-descripcion {{
        font-family: 'Nunito Sans', sans-serif;
        font-size: 16px;
        color: #555;
        line-height: 1.6;
        margin-bottom: 40px;
        max-width: 400px;
    }}

    .tasacion-label {{
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        font-weight: 800;
        color: #000000 !important;
        margin-bottom: 8px;
        margin-top: 15px;
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
    .footer-title {{ color: #ffffff; font-weight: 900; font-size: 24px; letter-spacing: 2px; margin-bottom: 20px; }}
    .footer-subtitle {{ color: #C41E3A; font-weight: 800; font-size: 12px; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 20px; }}
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
    .btn-float:hover {{ transform: scale(1.1) rotate(15deg); }}

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
        color: transparent !important;
        overflow: hidden;
    }}

    .forma-negra {{ background-color: #1a1a1a !important; }}
    .forma-roja {{ background-color: #C41E3A !important; }}

    .container-relativo:active .forma-boton {{
        background-color: #FF0000 !important;
    }}

    .container-relativo div.stButton {{
        position: relative !important;
        z-index: 2 !important;
        width: 100% !important;
    }}

    .container-relativo div.stButton > button {{
        width: 100% !important;
        height: 50px !important;
        background: transparent !important;
        border: none !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 900 !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        margin: 0 !important;
        padding: 0 !important;
        
        background: linear-gradient(90deg, #000 0%, #000 40%, #888 50%, #000 60%, #000 100%) !important;
        background-size: 200% auto !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        animation: scan 3s linear infinite !important;
    }}

    /* Estilos Redes Sociales Contacto */
    .social-icon-box {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 30px;
        background: white;
        border-radius: 12px;
        border: 1px solid #eee;
        transition: 0.3s ease;
        cursor: pointer;
        text-decoration: none;
    }}
    .social-icon-box:hover {{
        background: #fcfcfc;
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        border-color: #C41E3A;
    }}
    .social-icon-label {{
        margin-top: 15px;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 12px;
        color: #1a1a1a;
        letter-spacing: 1px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- DATOS ---
propiedades = [
    {"id": 1, "tipo": "DEPARTAMENTOS", "operacion": "Venta", "titulo": "Penthouse Alvear", "precio": "USD 850.000", "barrio": "Recoleta", "amb": "4", "m2": "120", "img": "Deptos.jpeg"},
    {"id": 2, "tipo": "DEPARTAMENTOS", "operacion": "Venta", "titulo": "Piso Estrada", "precio": "USD 240.000", "barrio": "Nueva Córdoba", "amb": "3", "m2": "95", "img": "Deptos.jpeg"},
    {"id": 3, "tipo": "DEPARTAMENTOS", "operacion": "Alquiler", "titulo": "Torre Duomo", "precio": "$ 450.000", "barrio": "Nueva Córdoba", "amb": "2", "m2": "65", "img": "Deptos.jpeg"},
    {"id": 4, "tipo": "CASAS", "operacion": "Venta", "titulo": "Residencia Los Olivos", "precio": "USD 1.200.000", "barrio": "Norte", "amb": "6", "m2": "450", "img": "Casas.jpeg"},
    {"id": 5, "tipo": "CASAS", "operacion": "Alquiler", "titulo": "Casona del Cerro", "precio": "$ 980.000", "barrio": "Cerro de las Rosas", "amb": "5", "m2": "320", "img": "Casas.jpeg"},
    {"id": 6, "tipo": "CASAS", "operacion": "Venta", "titulo": "Moderna Manantiales", "precio": "USD 280.000", "barrio": "Manantiales", "amb": "4", "m2": "210", "img": "Casas.jpeg"},
    {"id": 7, "tipo": "TERRENOS", "operacion": "Venta", "titulo": "Lote Premium Golf", "precio": "USD 340.000", "barrio": "Country Club", "amb": "-", "m2": "1200", "img": "Terreno.jpeg"},
    {"id": 8, "tipo": "TERRENOS", "operacion": "Venta", "titulo": "Lote Valle Escondido", "precio": "USD 125.000", "barrio": "Valle Escondido", "amb": "-", "m2": "600", "img": "Terreno.jpeg"},
    {"id": 9, "tipo": "TERRENOS", "operacion": "Venta", "titulo": "Lote Tejas 3", "precio": "USD 55.000", "barrio": "Ruta 20", "amb": "-", "m2": "350", "img": "Terreno.jpeg"},
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
                if pag == "En Venta":
                    st.session_state.operacion_filtro = "Venta"
                elif pag == "Alquiler":
                    st.session_state.operacion_filtro = "Alquiler"
                else:
                    st.session_state.operacion_filtro = None
                st.rerun()

    st.markdown("<hr style='margin: 15px 0; border: 0.5px solid #d1d1d1; opacity: 0.3;'>", unsafe_allow_html=True)

    if st.session_state.pagina_actual == "Principal":
        m = folium.Map(location=[-31.4167, -64.1833], zoom_start=12, tiles='CartoDB positron', zoom_control=False)
        st_folium(m, height=350, use_container_width=True, key="mapa_principal")
        
        st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
        f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns([1, 1, 1, 1, 1])
        with f_col1:
            st.markdown("<p class='filter-label'>UBICACIÓN</p>", unsafe_allow_html=True)
            st.selectbox("u", ["Argentina, Córdoba", "Argentina, Buenos Aires"], label_visibility="collapsed", key="u1")
        with f_col2:
            st.markdown("<p class='filter-label'>TIPO DE PROPIEDAD</p>", unsafe_allow_html=True)
            st.selectbox("t", ["Departamentos", "Casas", "Terrenos"], label_visibility="collapsed", key="t1")
        with f_col3:
            st.markdown("<p class='filter-label'>PRESUPUESTO (USD)</p>", unsafe_allow_html=True)
            st.selectbox("rango", ["Seleccionar Rango", "0 a 50.000", "50.000 a 100.000", "100.000 a 350.000", "350.000 a 500.000", "+500.000"], label_visibility="collapsed", key="rango_p")
        with f_col4:
            st.markdown("<p class='filter-label'>OPERACIÓN</p>", unsafe_allow_html=True)
            st.selectbox("o", ["En Venta", "En Alquiler"], label_visibility="collapsed", key="o1")
        with f_col5:
            if st.button("BUSCAR", key="btn_search", use_container_width=True, type="primary"):
                st.toast("Filtrando resultados...")
        
        with f_col1:
            st.markdown("<p class='filter-label' style='margin-top:15px;'>BUSCADOR</p>", unsafe_allow_html=True)
            st.text_input("b", placeholder="Barrio, calle o ciudad...", label_visibility="collapsed", key="b1")
        with f_col2:
            st.markdown("<p class='filter-label' style='margin-top:15px;'>DORMITORIOS</p>", unsafe_allow_html=True)
            st.selectbox("d", ["Todos", "1+", "2+", "3+"], label_visibility="collapsed", key="d1")
        with f_col3:
            st.markdown("<p class='filter-label' style='margin-top:15px; border-bottom: 1px solid #ddd; display: inline-block;'>TELÉFONO</p>", unsafe_allow_html=True)
            st.markdown("<div class='btn-filtro-contacto'>", unsafe_allow_html=True)
            if st.button("CONSULTAR POR TELÉFONO", key="btn_tel_filter", use_container_width=True):
                st.toast("Llamando al +54 351 000 0000")
            st.markdown("</div>", unsafe_allow_html=True)
        with f_col4:
            st.markdown("<p class='filter-label' style='margin-top:15px; border-bottom: 1px solid #ddd; display: inline-block;'>WHATSAPP</p>", unsafe_allow_html=True)
            st.markdown("<div class='btn-filtro-contacto'>", unsafe_allow_html=True)
            if st.button("ENVIAR WHATSAPP", key="btn_ws_filter", use_container_width=True):
                st.toast("Abriendo WhatsApp...")
            st.markdown("</div>", unsafe_allow_html=True)
        with f_col5:
            pass
            
        st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.categoria_actual is None:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("<div style='text-align: center; font-family: Inter; font-weight: 800; letter-spacing: 12px; color: #1a1a1a; margin-bottom: 20px;'>TODAS LAS PROPIEDADES</div>", unsafe_allow_html=True)
            banner_b64 = get_image_base64("Córdoba_banner2.jpg")
            st.markdown(f"<div class='banner-cordoba'><img src='data:image/jpeg;base64,{banner_b64}' style='width: 100%; height: 350px; object-fit: cover; border-radius: 8px;'></div>", unsafe_allow_html=True)
            st.markdown("<div class='container-relativo'><div class='forma-boton forma-negra'></div>", unsafe_allow_html=True)
            if st.button("VER OPORTUNIDADES", key="btn_all_props"):
                st.session_state.categoria_actual = "TODAS"; st.session_state.operacion_filtro = None; st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br><br><br>", unsafe_allow_html=True)

        if st.session_state.categoria_actual is None:
            st.markdown("<div style='text-align: center; font-family: Inter; font-weight: 800; letter-spacing: 12px; color: #1a1a1a; margin-bottom: 40px;'>EXPLORAR</div>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            categorias = [("DEPARTAMENTOS", "Deptos.jpeg"), ("CASAS", "Casas.jpeg"), ("TERRENOS", "Terreno.jpeg")]
            for i, (nombre, img) in enumerate(categorias):
                with [col1, col2, col3][i]:
                    img_b64 = get_image_base64(img)
                    st.markdown(f"<div class='img-container-listing'><img src='data:image/jpeg;base64,{img_b64}'></div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='container-relativo'><div class='forma-boton'></div>", unsafe_allow_html=True)
                    if st.button(nombre, key=f"cat_{nombre}"):
                        st.session_state.categoria_actual = nombre; st.session_state.operacion_filtro = None; st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<br><br><br><div style='text-align: center; font-family: Inter; font-weight: 800; letter-spacing: 4px; color: #1a1a1a; margin-bottom: 30px;'>PROPIEDADES DESTACADAS</div>", unsafe_allow_html=True)
            d_col1, d_col2, d_col3 = st.columns(3)
            for i, p in enumerate([propiedades[0], propiedades[3], propiedades[6]]):
                with [d_col1, d_col2, d_col3][i]:
                    img_b64 = get_image_base64(p["img"])
                    st.markdown(f"<div class='listing-card'><div style='height: 240px; overflow: hidden; border-radius: 6px;'><img src='data:image/jpeg;base64,{img_b64}' style='width: 100%; height: 100%; object-fit: cover;'></div><div style='padding: 20px 5px;'><p class='prop-precio'>{p['precio']}</p><p class='prop-ubicacion'>{p['titulo']} | {p['barrio']}</p><p class='prop-detalles'>{p['amb']} AMBIENTES • {p['m2']} M²</p></div></div>", unsafe_allow_html=True)
                    st.markdown("<div class='container-relativo'><div class='forma-boton forma-negra'></div>", unsafe_allow_html=True)
                    if st.button("VER FICHA COMPLETA", key=f"btn_dest_{i}"): st.toast(f"Cargando ficha de {p['titulo']}...")
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            cat = st.session_state.categoria_actual
            sub_col1, sub_col2, sub_col3, sub_col4 = st.columns([1,1,1,1])
            labels_sub = ["TODAS", "DEPARTAMENTOS", "CASAS", "TERRENOS"]
            for i, (col, label) in enumerate(zip([sub_col1, sub_col2, sub_col3, sub_col4], labels_sub)):
                with col:
                    st.markdown(f"<div class='container-relativo' style='height:45px;'><div class='forma-boton' style='height:4px;'></div>", unsafe_allow_html=True)
                    if st.button(label, key=f"subnav_{label}"):
                        st.session_state.categoria_actual = label; st.session_state.operacion_filtro = None; st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

            st.markdown(f"<div style='text-align: center; font-family: Inter; font-weight: 800; letter-spacing: 5px; color: #C41E3A; margin: 30px 0;'>{cat}</div>", unsafe_allow_html=True)
            
            if cat in ["DEPARTAMENTOS", "CASAS", "TODAS"]:
                btn_v, btn_a = st.columns(2)
                with btn_v:
                    color_v = "forma-roja" if st.session_state.operacion_filtro == "Venta" else ""
                    st.markdown(f"<div class='container-relativo'><div class='forma-boton {color_v}'></div>", unsafe_allow_html=True)
                    if st.button("EN VENTA", key="btn_venta_cat"): st.session_state.operacion_filtro = "Venta"; st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                with btn_a:
                    color_a = "forma-roja" if st.session_state.operacion_filtro == "Alquiler" else ""
                    st.markdown(f"<div class='container-relativo'><div class='forma-boton {color_a}'></div>", unsafe_allow_html=True)
                    if st.button("EN ALQUILER", key="btn_alq_cat"): st.session_state.operacion_filtro = "Alquiler"; st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

            propiedades_filtradas = propiedades if cat == "TODAS" else [p for p in propiedades if p["tipo"] == cat]
            if st.session_state.operacion_filtro: propiedades_filtradas = [p for p in propiedades_filtradas if p["operacion"] == st.session_state.operacion_filtro]
                
            _, col_list, _ = st.columns([1, 2, 1])
            for i, p in enumerate(propiedades_filtradas):
                with col_list:
                    img_b64 = get_image_base64(p["img"])
                    st.markdown(f"<div class='listing-card'><div class='img-container-listing'><img src='data:image/jpeg;base64,{img_b64}'></div><div style='padding: 20px 0;'><p class='prop-precio'>{p['precio']}</p><p class='prop-ubicacion'>{p['titulo']} | {p['barrio']} ({p['operacion'].upper()})</p><p class='prop-detalles'>{p['amb']} AMBIENTES • {p['m2']} M²</p></div></div>", unsafe_allow_html=True)
                    st.markdown("<div class='container-relativo'><div class='forma-boton forma-negra'></div>", unsafe_allow_html=True)
                    if st.button("VER DETALLES", key=f"ficha_{cat}_{i}"): st.toast("Cargando detalles...")
                    st.markdown("</div><br>", unsafe_allow_html=True)

            st.markdown("<div class='container-relativo'><div class='forma-boton'></div>", unsafe_allow_html=True)
            if st.button("VOLVER", key="btn_volver_main"): st.session_state.categoria_actual = None; st.session_state.operacion_filtro = None; st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # --- PÁGINA: EN VENTA ---
    elif st.session_state.pagina_actual == "En Venta":
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; font-family: Inter; font-weight: 800; letter-spacing: 12px; color: #1a1a1a; margin-bottom: 40px;'>PROPIEDADES EN VENTA</div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        categorias_v = [("DEPARTAMENTOS", "Deptos.jpeg"), ("CASAS", "Casas.jpeg"), ("TERRENOS", "Terreno.jpeg")]
        
        for i, (nombre, img) in enumerate(categorias_v):
            with [col1, col2, col3][i]:
                img_b64 = get_image_base64(img)
                st.markdown(f"<div class='img-container-listing'><img src='data:image/jpeg;base64,{img_b64}'></div>", unsafe_allow_html=True)
                color_sel = "forma-roja" if st.session_state.categoria_actual == nombre else ""
                st.markdown(f"<div class='container-relativo'><div class='forma-boton {color_sel}'></div>", unsafe_allow_html=True)
                if st.button(nombre, key=f"venta_cat_{nombre}"):
                    st.session_state.categoria_actual = nombre; st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.categoria_actual == "TERRENOS":
            st.markdown("<br>", unsafe_allow_html=True)
            _, b_col_plans, _ = st.columns([1, 1, 1])
            with b_col_plans:
                st.markdown("<div class='container-relativo'><div class='forma-boton forma-roja'></div>", unsafe_allow_html=True)
                if st.button("CONSULTAR PLANES DE CONSTRUCCIÓN", key="btn_planes_const"): st.toast("Cargando planes...")
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br><hr style='border: 0.1px solid #d1d1d1; opacity: 0.3;'><br>", unsafe_allow_html=True)

        cat = st.session_state.categoria_actual
        operacion = "Venta"
        prop_venta = [p for p in propiedades if p["operacion"] == operacion]
        if cat: prop_venta = [p for p in prop_venta if p["tipo"] == cat]
        
        label_seccion = f"RESULTADOS: {cat} EN VENTA" if cat else "TODAS LAS PROPIEDADES EN VENTA"
        st.markdown(f"<div style='text-align: center; font-family: Inter; font-weight: 800; letter-spacing: 5px; color: #C41E3A; margin-bottom: 40px;'>{label_seccion}</div>", unsafe_allow_html=True)

        _, col_list_v, _ = st.columns([1, 2, 1])
        if prop_venta:
            for i, p in enumerate(prop_venta):
                with col_list_v:
                    img_b64 = get_image_base64(p["img"])
                    st.markdown(f"<div class='listing-card'><div class='img-container-listing'><img src='data:image/jpeg;base64,{img_b64}'></div><div style='padding: 20px 0;'><p class='prop-precio'>{p['precio']}</p><p class='prop-ubicacion'>{p['titulo']} | {p['barrio']}</p><p class='prop-detalles'>{p['amb']} AMBIENTES • {p['m2']} M²</p></div></div>", unsafe_allow_html=True)
                    st.markdown("<div class='container-relativo'><div class='forma-boton forma-negra'></div>", unsafe_allow_html=True)
                    if st.button("VER DETALLES", key=f"ficha_venta_{i}"): st.toast(f"Cargando {p['titulo']}...")
                    st.markdown("</div><br>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='text-align:center; color:#666;'>No se encontraron propiedades.</p>", unsafe_allow_html=True)

    # --- PÁGINA: ALQUILER ---
    elif st.session_state.pagina_actual == "Alquiler":
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; font-family: Inter; font-weight: 800; letter-spacing: 12px; color: #1a1a1a; margin-bottom: 40px;'>PROPIEDADES EN ALQUILER</div>", unsafe_allow_html=True)
        
        _, col1, col2, _ = st.columns([0.5, 1, 1, 0.5])
        categorias_a = [("DEPARTAMENTOS", "Deptos.jpeg"), ("CASAS", "Casas.jpeg")]
        
        for i, (nombre, img) in enumerate(categorias_a):
            with [col1, col2][i]:
                img_b64 = get_image_base64(img)
                st.markdown(f"<div class='img-container-listing'><img src='data:image/jpeg;base64,{img_b64}'></div>", unsafe_allow_html=True)
                color_sel = "forma-roja" if st.session_state.categoria_actual == nombre else ""
                st.markdown(f"<div class='container-relativo'><div class='forma-boton {color_sel}'></div>", unsafe_allow_html=True)
                if st.button(nombre, key=f"alq_cat_{nombre}"):
                    st.session_state.categoria_actual = nombre; st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br><hr style='border: 0.1px solid #d1d1d1; opacity: 0.3;'><br>", unsafe_allow_html=True)

        cat = st.session_state.categoria_actual
        operacion = "Alquiler"
        prop_alq = [p for p in propiedades if p["operacion"] == operacion]
        if cat: prop_alq = [p for p in prop_alq if p["tipo"] == cat]
        
        label_seccion = f"RESULTADOS: {cat} EN ALQUILER" if cat else "TODAS LAS PROPIEDADES EN ALQUILER"
        st.markdown(f"<div style='text-align: center; font-family: Inter; font-weight: 800; letter-spacing: 5px; color: #C41E3A; margin-bottom: 40px;'>{label_seccion}</div>", unsafe_allow_html=True)

        _, col_list_a, _ = st.columns([1, 2, 1])
        if prop_alq:
            for i, p in enumerate(prop_alq):
                with col_list_a:
                    img_b64 = get_image_base64(p["img"])
                    st.markdown(f"<div class='listing-card'><div class='img-container-listing'><img src='data:image/jpeg;base64,{img_b64}'></div><div style='padding: 20px 0;'><p class='prop-precio'>{p['precio']}</p><p class='prop-ubicacion'>{p['titulo']} | {p['barrio']}</p><p class='prop-detalles'>{p['amb']} AMBIENTES • {p['m2']} M²</p></div></div>", unsafe_allow_html=True)
                    st.markdown("<div class='container-relativo'><div class='forma-boton forma-negra'></div>", unsafe_allow_html=True)
                    if st.button("VER DETALLES", key=f"ficha_alq_{i}"): st.toast(f"Cargando {p['titulo']}...")
                    st.markdown("</div><br>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='text-align:center; color:#666;'>No se encontraron propiedades en alquiler disponibles en esta categoría.</p>", unsafe_allow_html=True)

    # --- PÁGINA: TASACIONES ---
    elif st.session_state.pagina_actual == "Tasaciones":
        st.markdown("<div style='padding: 20px 40px;'>", unsafe_allow_html=True)
        
        t_col_left, t_col_main = st.columns([1, 2])
        
        with t_col_left:
            st.markdown("<div class='tasacion-titulo'>TASACIONES</div>", unsafe_allow_html=True)
            st.markdown("""
                <div class='tasacion-descripcion'>
                    Obtenga un valor real de mercado para su propiedad. 
                    Nuestro equipo técnico analiza variables de ubicación, 
                    entorno y tendencias actuales para brindar un informe preciso.
                </div>
            """, unsafe_allow_html=True)
        
        with t_col_main:
            # Fila 1
            st.markdown("<p class='tasacion-label'>TIPO DE PROPIEDAD</p>", unsafe_allow_html=True)
            tipo_t = st.text_input("t1", placeholder="ej: Casa, Departamento, Oficina...", label_visibility="collapsed")
            
            # Fila 2
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("<p class='tasacion-label'>LOCALIDAD</p>", unsafe_allow_html=True)
                loc_t = st.text_input("t2", placeholder="ej: Córdoba Capital", label_visibility="collapsed")
            with c2:
                st.markdown("<p class='tasacion-label'>BARRIO</p>", unsafe_allow_html=True)
                bar_t = st.text_input("t3", placeholder="ej: Nueva Córdoba", label_visibility="collapsed")
            
            # Fila 3
            c3, c4 = st.columns(2)
            with c3:
                st.markdown("<p class='tasacion-label'>SUPERFICIE CUBIERTA</p>", unsafe_allow_html=True)
                m_cub_t = st.text_input("t4", placeholder="Cantidad de m2 cubiertos", label_visibility="collapsed")
            with c4:
                st.markdown("<p class='tasacion-label'>SUPERFICIE TOTAL</p>", unsafe_allow_html=True)
                m_tot_t = st.text_input("t5", placeholder="Cantidad de m2 totales", label_visibility="collapsed")
            
            # Fila 4
            st.markdown("<p class='tasacion-label'>DESCRIPCIÓN DE LA PROPIEDAD</p>", unsafe_allow_html=True)
            desc_t = st.text_area("t6", placeholder="Detalle ambientes, estado, antiguedad, etc...", height=100, label_visibility="collapsed")
            
            st.markdown("<hr style='margin: 40px 0; border: 0.5px solid #ccc; opacity: 0.3;'>", unsafe_allow_html=True)
            
            # Fila 5: Contacto
            c5, c6, c7 = st.columns(3)
            with c5:
                st.markdown("<p class='tasacion-label'>NOMBRE</p>", unsafe_allow_html=True)
                nom_t = st.text_input("t7", placeholder="Su nombre", label_visibility="collapsed")
            with c6:
                st.markdown("<p class='tasacion-label'>TELÉFONO</p>", unsafe_allow_html=True)
                tel_t = st.text_input("t8", placeholder="Su teléfono", label_visibility="collapsed")
            with c7:
                st.markdown("<p class='tasacion-label'>EMAIL</p>", unsafe_allow_html=True)
                mail_t = st.text_input("t9", placeholder="Su email", label_visibility="collapsed")
            
            if st.button("ENVIAR SOLICITUD DE TASACIÓN", key="btn_send_tasa", type="primary"):
                st.success("Solicitud enviada con éxito. Nos contactaremos a la brevedad.")

        st.markdown("</div>", unsafe_allow_html=True)

    # --- PÁGINA: ADMINISTRACIÓN ---
    elif st.session_state.pagina_actual == "Administracion":
        st.markdown("<div style='padding: 20px 40px;'>", unsafe_allow_html=True)
        
        adm_col_left, adm_col_main = st.columns([1, 2])
        
        with adm_col_left:
            st.markdown("<div class='tasacion-titulo'>ADMINISTRACIÓN</div>", unsafe_allow_html=True)
            st.markdown("""
                <div class='tasacion-descripcion'>
                    Gestión integral de propiedades. Administramos consorcios, 
                    alquileres anuales y alquileres temporales con la mayor 
                    eficiencia y transparencia del mercado.
                </div>
            """, unsafe_allow_html=True)
        
        with adm_col_main:
            # Fila 1
            st.markdown("<p class='tasacion-label'>TIPO DE PROPIEDAD O CONSORCIO</p>", unsafe_allow_html=True)
            tipo_adm = st.text_input("adm1", placeholder="ej: Edificio, Casa, Departamento, Complejo...", label_visibility="collapsed")
            
            # Fila 2
            c1_adm, c2_adm = st.columns(2)
            with c1_adm:
                st.markdown("<p class='tasacion-label'>LOCALIDAD</p>", unsafe_allow_html=True)
                loc_adm = st.text_input("adm2", placeholder="ej: Córdoba Capital", label_visibility="collapsed")
            with c2_adm:
                st.markdown("<p class='tasacion-label'>BARRIO</p>", unsafe_allow_html=True)
                bar_adm = st.text_input("adm3", placeholder="ej: Nueva Córdoba", label_visibility="collapsed")
            
            # Fila 3
            c3_adm, c4_adm = st.columns(2)
            with c3_adm:
                st.markdown("<p class='tasacion-label'>SUPERFICIE CUBIERTA</p>", unsafe_allow_html=True)
                m_cub_adm = st.text_input("adm4", placeholder="Cantidad de m2 cubiertos", label_visibility="collapsed")
            with c4_adm:
                st.markdown("<p class='tasacion-label'>SUPERFICIE TOTAL</p>", unsafe_allow_html=True)
                m_tot_adm = st.text_input("adm5", placeholder="Cantidad de m2 totales", label_visibility="collapsed")
            
            # Fila 4
            st.markdown("<p class='tasacion-label'>DETALLES PARA ADMINISTRACIÓN</p>", unsafe_allow_html=True)
            desc_adm = st.text_area("adm6", placeholder="Indique si es consorcio, alquiler anual o temporal y detalles adicionales...", height=100, label_visibility="collapsed")
            
            st.markdown("<hr style='margin: 40px 0; border: 0.5px solid #ccc; opacity: 0.3;'>", unsafe_allow_html=True)
            
            # Fila 5: Contacto
            c5_adm, c6_adm, c7_adm = st.columns(3)
            with c5_adm:
                st.markdown("<p class='tasacion-label'>NOMBRE</p>", unsafe_allow_html=True)
                nom_adm = st.text_input("adm7", placeholder="Su nombre", label_visibility="collapsed")
            with c6_adm:
                st.markdown("<p class='tasacion-label'>TELÉFONO</p>", unsafe_allow_html=True)
                tel_adm = st.text_input("adm8", placeholder="Su teléfono", label_visibility="collapsed")
            with c7_adm:
                st.markdown("<p class='tasacion-label'>EMAIL</p>", unsafe_allow_html=True)
                mail_adm = st.text_input("adm9", placeholder="Su email", label_visibility="collapsed")
            
            if st.button("ENVIAR SOLICITUD DE ADMINISTRACIÓN", key="btn_send_adm", type="primary"):
                st.success("Solicitud enviada con éxito. Nuestro departamento de administración se contactará con usted.")

        st.markdown("</div>", unsafe_allow_html=True)

    # --- PÁGINA: CONTACTO ---
    elif st.session_state.pagina_actual == "Contacto":
        st.markdown("<div style='padding: 20px 40px;'>", unsafe_allow_html=True)
        
        cont_col_left, cont_col_main = st.columns([1, 2])
        
        with cont_col_left:
            st.markdown("<div class='tasacion-titulo'>CONTACTO</div>", unsafe_allow_html=True)
            st.markdown("""
                <div class='tasacion-descripcion'>
                    Muchas gracias por visitar nuestro sitio. No dudes en contactarnos, 
                    estamos encantados de ayudarte a encontrar tu próximo hogar o inversión.
                </div>
            """, unsafe_allow_html=True)
        
        with cont_col_main:
            st.markdown("<br>", unsafe_allow_html=True)
            # Grilla de Redes Sociales
            r1, r2, r3 = st.columns(3)
            r4, r5, r6 = st.columns(3)
            
            redes = [
                {"n": "INSTAGRAM", "i": "📸", "l": "https://instagram.com", "col": r1},
                {"n": "TIKTOK", "i": "🎵", "l": "https://tiktok.com", "col": r2},
                {"n": "FACEBOOK", "i": "👤", "l": "https://facebook.com", "col": r3},
                {"n": "LINKEDIN", "i": "💼", "l": "https://linkedin.com", "col": r4},
                {"n": "WHATSAPP", "i": "💬", "l": "https://wa.me/543510000000", "col": r5},
                {"n": "GMAIL", "i": "✉️", "l": "mailto:info@gminmobiliaria.com.ar", "col": r6}
            ]
            
            for red in redes:
                with red["col"]:
                    st.markdown(f"""
                        <a href="{red['l']}" target="_blank" style="text-decoration: none;">
                            <div class="social-icon-box">
                                <span style="font-size: 30px;">{red['i']}</span>
                                <span class="social-icon-label">{red['n']}</span>
                            </div>
                        </a>
                        <br>
                    """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # --- FOOTER ---
    st.markdown(f"""
        <div class='footer-container'>
            <div style='max-width: 1200px; margin: 0 auto;'>
                <div class="row" style="display: flex; flex-wrap: wrap; justify-content: space-between;">
                    <div style="flex: 1; min-width: 300px; margin-bottom: 40px;">
                        <div class="footer-title">GMI</div>
                        <div class="footer-subtitle">Negocios Inmobiliarios</div>
                        <p style="color: #666; font-size: 13px; line-height: 1.8; max-width: 250px;">
                            Expertos en el mercado inmobiliario de Córdoba. 
                            Compromiso, transparencia y resultados.
                        </p>
                    </div>
                    <div style="flex: 1; min-width: 200px; margin-bottom: 40px;">
                        <div style="font-size: 14px; font-weight: 800; margin-bottom: 25px; letter-spacing: 2px;">NAVEGACIÓN</div>
                        <div style="display: flex; flex-direction: column;">
                            <a href="#" class="footer-link">Propiedades en Venta</a>
                            <a href="#" class="footer-link">Propiedades en Alquiler</a>
                            <a href="#" class="footer-link">Tasaciones Profesionales</a>
                            <a href="#" class="footer-link">Administración de Consorcios</a>
                        </div>
                    </div>
                    <div style="flex: 1; min-width: 200px; margin-bottom: 40px;">
                        <div style="font-size: 14px; font-weight: 800; margin-bottom: 25px; letter-spacing: 2px;">CONTACTO</div>
                        <p style="color: #888; font-size: 13px; line-height: 2;">
                            📍 25 de Mayo 496, Córdoba<br>
                            📞 +54 3515 126791 <br>
                            ✉️ info@gminmobiliaria.com.ar
                        </p>
                    </div>
                </div>
                <div style="margin-top: 60px; padding-top: 30px; border-top: 1px solid #222; text-align: center; color: #444; font-size: 11px; letter-spacing: 1px;">
                    © {datetime.datetime.now().year} GMI NEGOCIOS INMOBILIARIOS. TODOS LOS DERECHOS RESERVADOS.
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)