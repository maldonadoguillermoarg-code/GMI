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

# --- ESTILOS GLOBALES (La confiramcion de Morty) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&family=Nunito+Sans:wght@300;400;600&display=swap');
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

# --- DATOS ---
propiedades = [
    {"tipo": "DEPARTAMENTOS", "titulo": "Penthouse Alvear", "precio": "USD 850.000", "barrio": "Recoleta", "amb": "4", "m2": "120", "img": "Deptos.jpeg"},
    {"tipo": "CASAS", "titulo": "Residencia Los Olivos", "precio": "USD 1.200.000", "barrio": "Norte", "amb": "6", "m2": "450", "img": "Casas.jpeg"},
    {"tipo": "TERRENOS", "titulo": "Lote Premium Golf", "precio": "USD 340.000", "barrio": "Country Club", "amb": "-", "m2": "1200", "img": "Terreno.jpeg"},
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
        
        # --- SUPER FILTRO CON CAMBIO QUIRÚRGICO: SOLO RANGO ---
        st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
        
        f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns([1, 1, 1, 1, 1])
        
        # FILA 1
        with f_col1:
            st.markdown("<p class='filter-label'>UBICACIÓN</p>", unsafe_allow_html=True)
            st.selectbox("u", ["Argentina, Córdoba", "Argentina, Buenos Aires"], label_visibility="collapsed", key="u1")
        with f_col2:
            st.markdown("<p class='filter-label'>TIPO DE PROPIEDAD</p>", unsafe_allow_html=True)
            st.selectbox("t", ["Departamentos", "Casas", "Terrenos"], label_visibility="collapsed", key="t1")
        with f_col3:
            # CAMBIO QUIRÚRGICO: Solo Rango de Presupuesto
            st.markdown("<p class='filter-label'>PRESUPUESTO (USD)</p>", unsafe_allow_html=True)
            st.selectbox("rango", ["Seleccionar Rango", "0 a 50.000", "50.000 a 100.000", "100.000 a 350.000", "350.000 a 500.000", "+500.000"], label_visibility="collapsed", key="rango_p")
        with f_col4:
            st.markdown("<p class='filter-label'>OPERACIÓN</p>", unsafe_allow_html=True)
            st.selectbox("o", ["En Venta", "En Alquiler"], label_visibility="collapsed", key="o1")
        with f_col5:
            if st.button("BUSCAR", key="btn_search", use_container_width=True, type="primary"):
                st.toast("Filtrando resultados...")

        # FILA 2 (Para mantener la alineación de los otros campos)
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
        st.markdown("<br><br><br>", unsafe_allow_html=True)

        if st.session_state.categoria_actual is None:
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

            st.markdown("<br><br><br><div style='text-align: center; font-family: Inter; font-weight: 800; letter-spacing: 4px; color: #1a1a1a; margin-bottom: 30px;'>PROPIEDADES DESTACADAS</div>", unsafe_allow_html=True)
            d_col1, d_col2, d_col3 = st.columns(3)
            
            for i, p in enumerate(propiedades):
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
                    st.button(f"VER FICHA COMPLETA", key=f"btn_dest_{i}", use_container_width=True)

        else:
            cat = st.session_state.categoria_actual
            st.markdown(f"<div style='text-align: center; font-family: Inter; font-weight: 800; letter-spacing: 5px; color: #C41E3A; margin-bottom: 40px;'>{cat}</div>", unsafe_allow_html=True)
            propiedades_filtradas = [p for p in propiedades if p["tipo"] == cat]
            _, col_list, _ = st.columns([1, 2, 1])
            for i, p in enumerate(propiedades_filtradas):
                with col_list:
                    img_b64 = get_image_base64(p["img"])
                    st.markdown(f"""
                        <div class='listing-card'>
                            <div class='img-container-listing'><img src='data:image/jpeg;base64,{img_b64}'></div>
                            <div style='padding: 20px 0;'>
                                <p class='prop-precio'>{p['precio']}</p>
                                <p class='prop-ubicacion'>{p['titulo']} | {p['barrio']}</p>
                                <p class='prop-detalles'>{p['amb']} AMBIENTES  •  {p['m2']} M²</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.button(f"VER DETALLES", key=f"ficha_{i}", use_container_width=True)

            if st.button("← VOLVER A CATEGORÍAS", use_container_width=True):
                st.session_state.categoria_actual = None
                st.rerun()

    else:
        st.markdown(f"<div style='text-align: center; padding: 120px;'><h2 style='font-family: Inter; color: #1a1a1a; letter-spacing: 5px;'>{st.session_state.pagina_actual.upper()}</h2><p style='color: #666;'>Contenido en proceso de carga para GMI Negocios Inmobiliarios.</p></div>", unsafe_allow_html=True)

    # --- PIE DE PÁGINA (FOOTER) ---
    st.markdown("""
        <div class="footer-container">
            <div style="display: flex; justify-content: space-between; flex-wrap: wrap;">
                <div style="flex: 1; min-width: 250px; margin-bottom: 30px;">
                    <h2 style="color: white; margin: 0;"><span style="color: #003366;">G</span>M<span style="color: #C41E3A;">I</span></h2>
                    <p style="font-size: 11px; letter-spacing: 3px; color: #666; font-weight: 800; margin-top: 5px;">NEGOCIOS INMOBILIARIOS</p>
                    <p style="margin-top: 25px; font-size: 14px; color: #888; line-height: 1.6; max-width: 250px;">
                        Excelencia y transparencia en servicios inmobiliarios. Tu próxima inversión comienza aquí.
                    </p>
                </div>
                <div style="flex: 1; min-width: 200px; margin-bottom: 30px;">
                    <h4 style="color: white; font-size: 14px; letter-spacing: 2px; margin-bottom: 25px;">SERVICIOS</h4>
                    <p style="font-size: 13px; color: #888; margin-bottom: 12px;">Venta de Propiedades</p>
                    <p style="font-size: 13px; color: #888; margin-bottom: 12px;">Alquileres Anuales</p>
                    <p style="font-size: 13px; color: #888; margin-bottom: 12px;">Tasaciones Profesionales</p>
                    <p style="font-size: 13px; color: #888; margin-bottom: 12px;">Administración de Consorcios</p>
                </div>
                <div style="flex: 1; min-width: 200px; margin-bottom: 30px;">
                    <h4 style="color: white; font-size: 14px; letter-spacing: 2px; margin-bottom: 25px;">CONTACTO</h4>
                    <p style="font-size: 13px; color: #888; margin-bottom: 12px;">Bv. Chacabuco 1234, Córdoba</p>
                    <p style="font-size: 13px; color: #888; margin-bottom: 12px;">+54 351 123 4567</p>
                    <p style="font-size: 13px; color: #888; margin-bottom: 12px;">info@gminegocios.com.ar</p>
                </div>
                <div style="flex: 1; min-width: 200px;">
                    <h4 style="color: white; font-size: 14px; letter-spacing: 2px; margin-bottom: 25px;">SÍGUENOS</h4>
                    <div style="display: flex; gap: 20px;">
                        <span style="color: #888; font-size: 13px;">Instagram</span>
                        <span style="color: #888; font-size: 13px;">Facebook</span>
                        <span style="color: #888; font-size: 13px;">LinkedIn</span>
                    </div>
                </div>
            </div>
            <hr style="border: 0.1px solid #333; margin: 60px 0 40px 0;">
            <p style="text-align: center; font-size: 10px; color: #444; letter-spacing: 1px;">
                © 2026 GMI NEGOCIOS INMOBILIARIOS. TODOS LOS DERECHOS RESERVADOS.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    _, fcol, _ = st.columns([2, 1, 2])
    if fcol.button("VOLVER AL INICIO / CERRAR", use_container_width=True):
        st.session_state.estado = 'intro'
        st.session_state.pagina_actual = 'Principal'
        st.session_state.categoria_actual = None
        st.rerun()