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
        # Imagen de respaldo si falla la carga
        return ""

# --- ESTILOS GLOBALES (Mejorados con arquitectura Zonaprop) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&family=Nunito+Sans:wght@300;400;600&display=swap');
    @import url('https://fonts.cdnfonts.com/css/seven-segment');

    /* Variables de marca GMI */
    :root {{
        --gmi-blue: #003366;
        --gmi-red: #C41E3A;
        --gmi-black: #1a1a1a;
        --gmi-grey: #666666;
        --gmi-light-grey: #f4f4f2;
        --whatsapp-color: #25d366;
    }}

    html, body {{ scrollbar-width: none; background-color: var(--gmi-light-grey); }}
    body::-webkit-scrollbar {{ display: none; }}
    
    @keyframes blinker {{ 50% {{ opacity: 0.1; }} }}

    /* Estilos de Tarjetas inspirados en Zonaprop */
    .listing-card {{ 
        background-color: #ffffff; 
        margin-bottom: 30px; 
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        overflow: hidden;
        transition: transform 0.3s ease;
        border: 1px solid #e1e1e1;
    }}
    .listing-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    }}

    .img-container-listing {{ 
        width: 100%; 
        height: 280px; 
        overflow: hidden; 
        position: relative;
    }}
    .img-container-listing img {{ 
        width: 100%; 
        height: 100%; 
        object-fit: cover; 
    }}
    
    .badge-destacado {{
        position: absolute;
        top: 15px;
        left: 15px;
        background-color: var(--gmi-blue);
        color: white;
        padding: 5px 12px;
        font-family: 'Inter', sans-serif;
        font-size: 10px;
        font-weight: 800;
        text-transform: uppercase;
        border-radius: 4px;
        letter-spacing: 1px;
    }}

    .card-content {{ padding: 20px; }}
    
    .prop-precio {{ 
        font-family: 'Inter', sans-serif; 
        font-weight: 800; 
        font-size: 24px; 
        color: var(--gmi-black); 
        margin: 0; 
    }}
    .prop-expensas {{
        font-family: 'Nunito Sans', sans-serif;
        font-size: 13px;
        color: var(--gmi-grey);
        margin-bottom: 10px;
    }}
    .prop-ubicacion {{ 
        font-family: 'Nunito Sans', sans-serif; 
        font-size: 15px; 
        color: var(--gmi-black); 
        margin: 5px 0; 
        font-weight: 600; 
    }}
    
    /* Icon Features al estilo Zonaprop */
    .features-row {{
        display: flex;
        gap: 15px;
        margin-top: 15px;
        padding-top: 15px;
        border-top: 1px solid #eee;
    }}
    .feature-item {{
        display: flex;
        align-items: center;
        gap: 6px;
        color: var(--gmi-grey);
        font-size: 13px;
    }}
    .feature-icon {{
        font-weight: bold;
        color: var(--gmi-blue);
    }}

    /* Super Filtro Refinado */
    .filter-box {{
        background-color: #ffffff;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        margin-top: -50px;
        position: relative;
        z-index: 1000;
        border: 1px solid #ffffff;
    }}
    
    .filter-label {{
        font-family: 'Inter', sans-serif;
        font-size: 10px;
        font-weight: 800;
        color: var(--gmi-grey);
        margin-bottom: 8px;
        letter-spacing: 1.2px;
        text-transform: uppercase;
    }}

    /* Botones de Navegación */
    div.stButton > button {{
        border: none !important;
        background-color: transparent !important;
        color: var(--gmi-black) !important;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-size: 12px;
        transition: color 0.3s;
    }}
    div.stButton > button:hover {{
        color: var(--gmi-red) !important;
    }}

    /* Footer Estilo Corporativo */
    .footer-container {{
        background-color: var(--gmi-black);
        color: #ffffff;
        padding: 80px 10%;
        font-family: 'Inter', sans-serif;
        margin-top: 100px;
    }}

    /* Estilo para botón de WhatsApp flotante */
    .whatsapp-float {{
        position: fixed;
        bottom: 40px;
        right: 40px;
        background-color: var(--whatsapp-color);
        color: white;
        width: 60px;
        height: 60px;
        border-radius: 50px;
        text-align: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        cursor: pointer;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- DATOS AMPLIADOS ---
propiedades = [
    {"tipo": "DEPARTAMENTOS", "titulo": "Penthouse Alvear", "precio": "USD 850.000", "expensas": "+ $120.000 expensas", "barrio": "Recoleta, CABA", "amb": "4", "dorm": "3", "bano": "3", "m2": "120", "img": "Deptos.jpeg", "destacado": True},
    {"tipo": "DEPARTAMENTOS", "titulo": "Moderno Studio", "precio": "USD 120.000", "expensas": "+ $25.000 expensas", "barrio": "Nueva Córdoba, Córdoba", "amb": "1", "dorm": "0", "bano": "1", "m2": "40", "img": "Deptos.jpeg", "destacado": False},
    {"tipo": "CASAS", "titulo": "Residencia Los Olivos", "precio": "USD 1.200.000", "expensas": "Sin expensas", "barrio": "Country Norte, Córdoba", "amb": "6", "dorm": "4", "bano": "4", "m2": "450", "img": "Casas.jpeg", "destacado": True},
    {"tipo": "CASAS", "titulo": "Chalet del Sol", "precio": "USD 450.000", "expensas": "Sin expensas", "barrio": "Villa Belgrano, Córdoba", "amb": "4", "dorm": "3", "bano": "2", "m2": "280", "img": "Casas.jpeg", "destacado": False},
    {"tipo": "TERRENOS", "titulo": "Lote Premium Golf", "precio": "USD 340.000", "expensas": "+ $40.000 expensas", "barrio": "Country Club, Córdoba", "amb": "-", "dorm": "-", "bano": "-", "m2": "1200", "img": "Terreno.jpeg", "destacado": True},
]

# --- PANTALLA 1: RELOJ (INTRO) - SIN MODIFICACIONES SEGÚN PEDIDO ---
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

# --- PANTALLA 2: SITIO WEB (MEJORADA) ---
elif st.session_state.estado == 'web':
    # Navbar y Logo
    st.markdown("<br>", unsafe_allow_html=True)
    head_col1, head_col2 = st.columns([1.5, 4])
    
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
        nav_cols = st.columns(7)
        paginas = ["Principal", "Propiedades", "En Venta", "Alquiler", "Tasaciones", "Administracion", "Contacto"]
        for i, pag in enumerate(paginas):
            label = f" {pag} " if st.session_state.pagina_actual != pag else f"● {pag}"
            if nav_cols[i].button(label, key=f"nav_{pag}"):
                st.session_state.pagina_actual = pag
                if pag != "Propiedades": st.session_state.categoria_actual = None
                st.rerun()

    st.markdown("<hr style='margin: 15px 0; border: 0.5px solid #d1d1d1; opacity: 0.3;'>", unsafe_allow_html=True)

    # --- CONTENIDO DE PÁGINAS ---
    if st.session_state.pagina_actual == "Principal":
        # Mapa de fondo estilo Zonaprop
        m = folium.Map(location=[-31.4167, -64.1833], zoom_start=13, tiles='CartoDB positron', zoom_control=False)
        st_folium(m, height=450, use_container_width=True, key="mapa_principal")
        
        # --- SUPER FILTRO (MEJORADO) ---
        st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
        f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns([1.2, 1.2, 1.2, 1, 0.8])
        with f_col1:
            st.markdown("<p class='filter-label'>UBICACIÓN</p>", unsafe_allow_html=True)
            st.selectbox("u", ["Todas", "Córdoba, Capital", "CABA, Buenos Aires"], label_visibility="collapsed", key="u_home")
        with f_col2:
            st.markdown("<p class='filter-label'>TIPO DE PROPIEDAD</p>", unsafe_allow_html=True)
            tipo_h = st.selectbox("t", ["Todos", "Departamentos", "Casas", "Terrenos"], label_visibility="collapsed", key="t_home")
        with f_col3:
            st.markdown("<p class='filter-label'>PRESUPUESTO</p>", unsafe_allow_html=True)
            st.selectbox("rango", ["Cualquier precio", "USD 0 - 100k", "USD 100k - 300k", "USD +300k"], label_visibility="collapsed", key="r_home")
        with f_col4:
            st.markdown("<p class='filter-label'>OPERACIÓN</p>", unsafe_allow_html=True)
            st.selectbox("o", ["Venta", "Alquiler"], label_visibility="collapsed", key="o_home")
        with f_col5:
            if st.button("BUSCAR", key="btn_search_home", use_container_width=True, type="primary"):
                st.session_state.categoria_actual = tipo_h.upper() if tipo_h != "Todos" else None
                st.session_state.pagina_actual = "Propiedades"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br><br><br><br>", unsafe_allow_html=True)
        
        # SECCIÓN EXPLORAR
        st.markdown("<div style='text-align: center; font-family: Inter; font-weight: 800; letter-spacing: 12px; color: #1a1a1a; margin-bottom: 50px;'>CATEGORÍAS DESTACADAS</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        categorias = [("DEPARTAMENTOS", "Deptos.jpeg"), ("CASAS", "Casas.jpeg"), ("TERRENOS", "Terreno.jpeg")]
        for i, (nombre, img) in enumerate(categorias):
            with [col1, col2, col3][i]:
                img_b64 = get_image_base64(img)
                st.markdown(f"""
                    <div class='img-container-listing' style='height: 450px; border-radius: 12px;'>
                        <img src='data:image/jpeg;base64,{img_b64}'>
                        <div style='position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(transparent, rgba(0,0,0,0.8)); padding: 40px 20px;'>
                            <h3 style='color: white; font-family: Inter; font-weight: 800; letter-spacing: 3px; margin: 0;'>{nombre}</h3>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"VER {nombre}", key=f"cat_btn_{nombre}", use_container_width=True):
                    st.session_state.categoria_actual = nombre
                    st.session_state.pagina_actual = "Propiedades"
                    st.rerun()

    elif st.session_state.pagina_actual == "Propiedades":
        st.markdown("<div style='text-align: center; margin-top: 40px;'><h2 style='font-family: Inter; font-weight: 800; letter-spacing: 5px; color: #1a1a1a;'>LISTADO PROFESIONAL</h2></div>", unsafe_allow_html=True)
        
        # Filtro estático para listado
        st.markdown("<div class='filter-box' style='margin-top: 30px; margin-bottom: 50px;'>", unsafe_allow_html=True)
        pf1, pf2, pf3, pf4, pf5 = st.columns([1, 1, 1, 1, 1])
        with pf1:
            st.markdown("<p class='filter-label'>ZONA</p>", unsafe_allow_html=True)
            st.selectbox("u", ["Todas las zonas", "Córdoba", "Buenos Aires"], label_visibility="collapsed", key="u_filt")
        with pf2:
            st.markdown("<p class='filter-label'>TIPO</p>", unsafe_allow_html=True)
            opciones_tipo = ["TODAS", "DEPARTAMENTOS", "CASAS", "TERRENOS"]
            index_tipo = opciones_tipo.index(st.session_state.categoria_actual) if st.session_state.categoria_actual in opciones_tipo else 0
            tipo_sel = st.selectbox("t", opciones_tipo, index=index_tipo, label_visibility="collapsed", key="t_filt")
            st.session_state.categoria_actual = tipo_sel if tipo_sel != "TODAS" else None
        with pf3:
            st.markdown("<p class='filter-label'>DORMITORIOS</p>", unsafe_allow_html=True)
            st.selectbox("d", ["Cualquiera", "1+", "2+", "3+", "4+"], label_visibility="collapsed", key="d_filt")
        with pf4:
            st.markdown("<p class='filter-label'>ORDENAR POR</p>", unsafe_allow_html=True)
            st.selectbox("o", ["Precio: Menor a Mayor", "Precio: Mayor a Menor", "Más Recientes"], label_visibility="collapsed", key="o_filt")
        with pf5:
            st.markdown("<div style='margin-top:22px;'></div>", unsafe_allow_html=True)
            st.button("APLICAR", type="primary", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Listado de fichas mejoradas
        props_mostrar = propiedades if not st.session_state.categoria_actual else [p for p in propiedades if p["tipo"] == st.session_state.categoria_actual]

        if not props_mostrar:
            st.info("No se encontraron resultados para los filtros aplicados.")
        else:
            _, col_center, _ = st.columns([1, 2.5, 1])
            with col_center:
                for i, p in enumerate(props_mostrar):
                    img_b64 = get_image_base64(p["img"])
                    badge = "<div class='badge-destacado'>Destacado</div>" if p.get("destacado") else ""
                    
                    st.markdown(f"""
                        <div class='listing-card'>
                            <div class='img-container-listing'>
                                {badge}
                                <img src='data:image/jpeg;base64,{img_b64}'>
                            </div>
                            <div class='card-content'>
                                <p class='prop-precio'>{p['precio']}</p>
                                <p class='prop-expensas'>{p['expensas']}</p>
                                <p class='prop-ubicacion'>{p['titulo']} | <span style='color: #666;'>{p['barrio']}</span></p>
                                
                                <div class='features-row'>
                                    <div class='feature-item'><span class='feature-icon'>📏</span> {p['m2']} m² tot.</div>
                                    <div class='feature-item'><span class='feature-icon'>🛏️</span> {p['dorm']} dorm.</div>
                                    <div class='feature-item'><span class='feature-icon'>🚿</span> {p['bano']} baños</div>
                                    <div class='feature-item'><span class='feature-icon'>🚗</span> 1 coch.</div>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.button(f"VER DETALLES DE {p['titulo'].upper()}", key=f"btn_p_{i}", use_container_width=True)
                    st.markdown("<br>", unsafe_allow_html=True)

    else:
        # Páginas en construcción
        st.markdown(f"""
            <div style='text-align: center; padding: 150px 0;'>
                <h2 style='font-family: Inter; font-weight: 800; color: #1a1a1a; letter-spacing: 5px;'>{st.session_state.pagina_actual.upper()}</h2>
                <div style='width: 50px; height: 2px; background: var(--gmi-red); margin: 20px auto;'></div>
                <p style='color: #666; font-family: Nunito Sans;'>Módulo en desarrollo para la plataforma GMI.</p>
            </div>
        """, unsafe_allow_html=True)

    # --- FOOTER ---
    st.markdown("""
        <div class="footer-container">
            <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 50px;">
                <div style="flex: 2; min-width: 300px;">
                    <h2 style="color: white; margin: 0; font-family: Inter; font-weight: 800;">
                        <span style="color: #003366;">G</span>M<span style="color: #C41E3A;">I</span>
                    </h2>
                    <p style="font-size: 11px; letter-spacing: 3px; color: #666; font-weight: 800; margin-top: 5px; text-transform: uppercase;">
                        Negocios Inmobiliarios
                    </p>
                    <p style="margin-top: 30px; font-size: 15px; color: #aaa; line-height: 1.8; max-width: 400px; font-family: 'Nunito Sans';">
                        Líderes en el mercado premium de Córdoba y Buenos Aires. Nuestra misión es conectar sueños con realidades a través de una gestión transparente y eficiente.
                    </p>
                </div>
                <div style="flex: 1; min-width: 150px;">
                    <h4 style="color: white; font-size: 13px; letter-spacing: 2px; margin-bottom: 25px; font-weight: 800;">EXPLORAR</h4>
                    <p style="font-size: 14px; color: #888; margin-bottom: 15px; cursor: pointer;">Buscar Propiedades</p>
                    <p style="font-size: 14px; color: #888; margin-bottom: 15px; cursor: pointer;">Publicar mi Inmueble</p>
                    <p style="font-size: 14px; color: #888; margin-bottom: 15px; cursor: pointer;">Inversiones</p>
                </div>
                <div style="flex: 1; min-width: 200px;">
                    <h4 style="color: white; font-size: 13px; letter-spacing: 2px; margin-bottom: 25px; font-weight: 800;">CONTACTO</h4>
                    <p style="font-size: 14px; color: #888; margin-bottom: 12px;">Bv. Chacabuco 1234, Córdoba, Argentina</p>
                    <p style="font-size: 14px; color: #888; margin-bottom: 12px;">+54 351 123 4567</p>
                    <p style="font-size: 14px; color: #888; margin-bottom: 12px;">atencion@gmi.com.ar</p>
                </div>
            </div>
            <hr style="border: 0.1px solid #333; margin: 60px 0 40px 0; opacity: 0.5;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <p style="font-size: 11px; color: #555; letter-spacing: 1px;">
                    © 2026 GMI NEGOCIOS INMOBILIARIOS. TODOS LOS DERECHOS RESERVADOS.
                </p>
                <div style="display: flex; gap: 30px;">
                    <span style="color: #666; font-size: 12px; font-weight: 800;">INSTAGRAM</span>
                    <span style="color: #666; font-size: 12px; font-weight: 800;">LINKEDIN</span>
                </div>
            </div>
        </div>
        
        <a href="https://wa.me/543511234567" target="_blank" style="text-decoration: none;">
            <div class="whatsapp-float">
                <span style="font-family: Arial;">W</span>
            </div>
        </a>
    """, unsafe_allow_html=True)

    # Botón de cierre
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, fcol, _ = st.columns([2, 1, 2])
    if fcol.button("SALIR DEL SISTEMA", use_container_width=True):
        st.session_state.estado = 'intro'
        st.session_state.pagina_actual = 'Principal'
        st.session_state.categoria_actual = None
        st.rerun()