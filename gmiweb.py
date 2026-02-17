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

    /* Animación Scanner Light */
    @keyframes scan {{
        0% {{ background-position: -200% 0; }}
        100% {{ background-position: 200% 0; }}
    }}

    .prop-precio {{ font-family: 'Inter', sans-serif; font-weight: 800; font-size: 22px; color: #1a1a1a !important; margin: 0; }}
    .prop-ubicacion {{ font-family: 'Nunito Sans', sans-serif; font-size: 14px; color: #444 !important; text-transform: uppercase; margin: 5px 0; font-weight: 600; }}
    .prop-detalles {{ color: #666 !important; font-size: 13px; font-weight: 400; }}
    
    .listing-card {{ background-color: transparent; margin-bottom: 30px; border-bottom: 1px solid #d1d1d1; padding-bottom: 20px; }}
    .img-container-listing {{ width: 100%; height: 380px; overflow: hidden; border-radius: 4px; }}
    .img-container-listing img {{ width: 100%; height: 100%; object-fit: cover; transition: transform 0.6s ease; }}
    .img-container-listing:hover img {{ transform: scale(1.03); }}

    /* Super Filtro - PROHIBIDO MODIFICAR */
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

    /* Botón Buscar Estilo */
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

    /* Footer Container */
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

    /* Banner Córdoba */
    .banner-cordoba {{
        width: 100%;
        border-radius: 8px;
        overflow: hidden;
        margin-top: 20px;
        height: 350px;
    }}
    .banner-cordoba img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }}

    /* --- ARQUITECTURA DE CAPAS ESTÉTICA (INTERVENCIÓN SOLICITADA) --- */
    .container-relativo {{
        position: relative;
        height: 50px;
        margin-top: 15px;
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }}

    /* La forma ahora es una línea fina arriba del botón */
    .forma-boton {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px; /* Altura fina */
        background-color: #e0e0e0;
        border-radius: 2px;
        z-index: 1;
        transition: background-color 0.2s ease;
        /* Ocultamos el texto original de la forma para que no ensucie */
        color: transparent !important;
        overflow: hidden;
    }}

    .forma-negra {{ background-color: #1a1a1a !important; }}
    .forma-roja {{ background-color: #C41E3A !important; }}

    /* Cuando tocan el botón, la línea se pone roja */
    .container-relativo:active .forma-boton {{
        background-color: #FF0000 !important;
    }}

    /* Ajuste del botón real de Streamlit con efecto Scanner */
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
        
        /* Efecto Scanner de Luz en el texto */
        background: linear-gradient(90deg, #000 0%, #000 40%, #888 50%, #000 60%, #000 100%) !important;
        background-size: 200% auto !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        animation: scan 3s linear infinite !important;
    }}

    .container-relativo div.stButton > button:hover {{
        background: rgba(0, 0, 0, 0.05) !important;
        -webkit-background-clip: text !important;
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
                st.rerun()

    st.markdown("<hr style='margin: 15px 0; border: 0.5px solid #d1d1d1; opacity: 0.3;'>", unsafe_allow_html=True)

    if st.session_state.pagina_actual == "Principal":
        m = folium.Map(location=[-31.4167, -64.1833], zoom_start=12, tiles='CartoDB positron', zoom_control=False)
        st_folium(m, height=350, use_container_width=True, key="mapa_principal")
        
        # --- SUPER FILTRO (ESTRUCTURA ORIGINAL) ---
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
        with f_col4:
            st.markdown("<div style='margin-top:35px;'></div>", unsafe_allow_html=True)
            st.checkbox("Apto Crédito", key="apto_check")
        st.markdown("</div>", unsafe_allow_html=True)

        # --- SECCIÓN BANNER Y BOTÓN ---
        if st.session_state.categoria_actual is None:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("<div style='text-align: center; font-family: Inter; font-weight: 800; letter-spacing: 12px; color: #1a1a1a; margin-bottom: 20px;'>TODAS LAS PROPIEDADES</div>", unsafe_allow_html=True)
            
            banner_b64 = get_image_base64("Córdoba_banner2.jpg")
            st.markdown(f"<div class='banner-cordoba'><img src='data:image/jpeg;base64,{banner_b64}'></div>", unsafe_allow_html=True)
            
            st.markdown("<div class='container-relativo'><div class='forma-boton forma-negra'>VER OPORTUNIDADES</div>", unsafe_allow_html=True)
            if st.button("VER OPORTUNIDADES", key="btn_all_props"):
                st.session_state.categoria_actual = "TODAS"
                st.session_state.operacion_filtro = None
                st.rerun()
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
                        st.session_state.categoria_actual = nombre
                        st.session_state.operacion_filtro = None
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<br><br><br><div style='text-align: center; font-family: Inter; font-weight: 800; letter-spacing: 4px; color: #1a1a1a; margin-bottom: 30px;'>PROPIEDADES DESTACADAS</div>", unsafe_allow_html=True)
            d_col1, d_col2, d_col3 = st.columns(3)
            
            for i, p in enumerate([propiedades[0], propiedades[3], propiedades[6]]):
                with [d_col1, d_col2, d_col3][i]:
                    img_b64 = get_image_base64(p["img"])
                    st.markdown(f"""
                        <div class='listing-card' style='background: white; border: 1px solid #eeeeee; padding: 15px; border-radius: 10px;'>
                            <div style='height: 240px; overflow: hidden; border-radius: 6px;'>
                                <img src='data:image/jpeg;base64,{img_b64}' style='width: 100%; height: 100%; object-fit: cover;'>
                            </div>
                            <div style='padding: 20px 5px;'>
                                <p class='prop-precio'>{p['precio']}</p>
                                <p class='prop-ubicacion'>{p['titulo']} | {p['barrio']}</p>
                                <p class='prop-detalles'>{p['amb']} AMBIENTES • {p['m2']} M²</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown("<div class='container-relativo'><div class='forma-boton forma-negra'></div>", unsafe_allow_html=True)
                    if st.button("VER FICHA COMPLETA", key=f"btn_dest_{i}"):
                         st.toast(f"Cargando ficha de {p['titulo']}...")
                    st.markdown("</div>", unsafe_allow_html=True)

        else:
            cat = st.session_state.categoria_actual
            sub_col1, sub_col2, sub_col3, sub_col4 = st.columns([1,1,1,1])
            labels_sub = ["TODAS", "DEPARTAMENTOS", "CASAS", "TERRENOS"]
            for i, (col, label) in enumerate(zip([sub_col1, sub_col2, sub_col3, sub_col4], labels_sub)):
                with col:
                    st.markdown(f"<div class='container-relativo' style='height:45px;'><div class='forma-boton' style='height:4px;'></div>", unsafe_allow_html=True)
                    if st.button(label, key=f"subnav_{label}"):
                        st.session_state.categoria_actual = label
                        st.session_state.operacion_filtro = None
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

            st.markdown(f"<div style='text-align: center; font-family: Inter; font-weight: 800; letter-spacing: 5px; color: #C41E3A; margin: 30px 0;'>{cat}</div>", unsafe_allow_html=True)
            
            if cat in ["DEPARTAMENTOS", "CASAS", "TODAS"]:
                btn_v, btn_a = st.columns(2)
                with btn_v:
                    color_v = "forma-roja" if st.session_state.operacion_filtro == "Venta" else ""
                    st.markdown(f"<div class='container-relativo'><div class='forma-boton {color_v}'></div>", unsafe_allow_html=True)
                    if st.button("EN VENTA", key="btn_venta_cat"):
                        st.session_state.operacion_filtro = "Venta"
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                with btn_a:
                    color_a = "forma-roja" if st.session_state.operacion_filtro == "Alquiler" else ""
                    st.markdown(f"<div class='container-relativo'><div class='forma-boton {color_a}'></div>", unsafe_allow_html=True)
                    if st.button("EN ALQUILER", key="btn_alq_cat"):
                        st.session_state.operacion_filtro = "Alquiler"
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
            
            elif cat == "TERRENOS":
                st.markdown("<div class='container-relativo'><div class='forma-boton forma-negra'></div>", unsafe_allow_html=True)
                if st.button("CONSULTAR PLANES", key="btn_planes_terrenos"):
                    st.session_state.pagina_actual = "Planes_Construccion"
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

            # --- LÓGICA FILTRADO ---
            if cat == "TODAS":
                propiedades_filtradas = propiedades
            else:
                propiedades_filtradas = [p for p in propiedades if p["tipo"] == cat]
                if st.session_state.operacion_filtro:
                    propiedades_filtradas = [p for p in propiedades_filtradas if p["operacion"] == st.session_state.operacion_filtro]
                
            _, col_list, _ = st.columns([1, 2, 1])
            for i, p in enumerate(propiedades_filtradas):
                with col_list:
                    img_b64 = get_image_base64(p["img"])
                    st.markdown(f"""
                        <div class='listing-card'>
                            <div class='img-container-listing'><img src='data:image/jpeg;base64,{img_b64}'></div>
                            <div style='padding: 20px 0;'>
                                <p class='prop-precio'>{p['precio']}</p>
                                <p class='prop-ubicacion'>{p['titulo']} | {p['barrio']} ({p['operacion'].upper()})</p>
                                <p class='prop-detalles'>{p['amb']} AMBIENTES  •  {p['m2']} M²</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown("<div class='container-relativo'><div class='forma-boton forma-negra'></div>", unsafe_allow_html=True)
                    if st.button("VER DETALLES", key=f"ficha_{cat}_{i}"):
                        st.toast("Cargando detalles...")
                    st.markdown("</div><br>", unsafe_allow_html=True)

            st.markdown("<div class='container-relativo'><div class='forma-boton'></div>", unsafe_allow_html=True)
            if st.button("VOLVER", key="btn_volver_main"):
                st.session_state.categoria_actual = None
                st.session_state.operacion_filtro = None
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.pagina_actual == "Planes_Construccion":
        st.markdown("<div style='text-align: center; padding: 120px;'><h2 style='font-family: Inter; color: #1a1a1a; letter-spacing: 5px;'>PLANES DE CONSTRUCCIÓN</h2></div>", unsafe_allow_html=True)
        st.markdown("<div class='container-relativo'><div class='forma-boton'></div>", unsafe_allow_html=True)
        if st.button("VOLVER", key="btn_volver_terrenos"):
            st.session_state.pagina_actual = "Principal"
            st.session_state.categoria_actual = "TERRENOS"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown(f"<div style='text-align: center; padding: 120px;'><h2 style='font-family: Inter; color: #1a1a1a; letter-spacing: 5px;'>{st.session_state.pagina_actual.upper()}</h2></div>", unsafe_allow_html=True)

    # --- PIE DE PÁGINA ---
    st.markdown("""<div class="footer-container">...</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    _, fcol, _ = st.columns([2, 1, 2])
    with fcol:
        st.markdown("<div class='container-relativo' style='height:45px;'><div class='forma-boton' style='height:4px;'></div>", unsafe_allow_html=True)
        if st.button("LOGOUT", key="btn_close"):
            st.session_state.estado = 'intro'
            st.session_state.pagina_actual = 'Principal'
            st.session_state.categoria_actual = None
            st.session_state.operacion_filtro = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)