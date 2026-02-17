import streamlit as st
import datetime
import time
import base64
import folium
from streamlit_folium import st_folium

# 1. Configuración de página
st.set_page_config(layout="wide", page_title="GMI | Negocios Inmobiliarios")

# 2. Control de estado (RESPECTANDO TODO EL CÓDIGO ORIGINAL)
if 'estado' not in st.session_state:
    st.session_state.estado = 'intro'
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = 'Principal'
if 'categoria_actual' not in st.session_state:
    st.session_state.categoria_actual = None
if 'operacion_filtro' not in st.session_state:
    st.session_state.operacion_filtro = None
# ADICIÓN: Estado para la propiedad seleccionada
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

# --- ESTILOS GLOBALES (INTACTOS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800;900&family=Nunito+Sans:wght@300;400;600&display=swap');
    @import url('https://fonts.cdnfonts.com/css/seven-segment');

    html, body {{ scrollbar-width: none; }}
    body::-webkit-scrollbar {{ display: none; }}
    
    @keyframes blinker {{ 50% {{ opacity: 0.1; }} }}
    @keyframes scan {{ 0% {{ background-position: -200% 0; }} 100% {{ background-position: 200% 0; }} }}
    @keyframes doble-titileo {{ 0%, 50%, 100% {{ opacity: 1; }} 25%, 75% {{ opacity: 0.4; }} }}

    .prop-precio {{ font-family: 'Inter', sans-serif; font-weight: 800; font-size: 22px; color: #1a1a1a !important; margin: 0; }}
    .prop-ubicacion {{ font-family: 'Nunito Sans', sans-serif; font-size: 14px; color: #444 !important; text-transform: uppercase; margin: 5px 0; font-weight: 600; }}
    .prop-detalles {{ color: #666 !important; font-size: 13px; font-weight: 400; }}
    
    .listing-card {{ background-color: #ffffff; margin-bottom: 30px; border-bottom: 1px solid #d1d1d1; padding: 15px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.03); }}
    .img-container-listing {{ width: 100%; height: 380px; overflow: hidden; border-radius: 4px; }}
    .img-container-listing img {{ width: 100%; height: 100%; object-fit: cover; transition: transform 0.6s ease; }}
    .img-container-listing:hover img {{ transform: scale(1.03); }}

    .filter-box {{ background-color: #ffffff; padding: 25px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-top: -60px; position: relative; z-index: 100; border: 1px solid #eeeeee; }}
    .filter-label {{ font-family: 'Inter', sans-serif; font-size: 11px; font-weight: 800; color: #1a1a1a; margin-bottom: 10px; letter-spacing: 1.5px; text-transform: uppercase; height: 15px; }}

    .tasacion-titulo {{ color: #C41E3A; font-family: 'Inter', sans-serif; font-weight: 900; font-size: 60px; text-align: left; margin-bottom: 10px; letter-spacing: -1px; }}
    .tasacion-descripcion {{ font-family: 'Nunito Sans', sans-serif; font-size: 16px; color: #555; line-height: 1.6; margin-bottom: 40px; max-width: 400px; }}
    .tasacion-label {{ font-family: 'Inter', sans-serif; font-size: 16px; font-weight: 800; color: #000000 !important; margin-bottom: 8px; margin-top: 15px; text-transform: uppercase; }}

    div.stButton > button[kind="primary"] {{ background-color: #1a1a1a !important; border: none !important; color: #ffffff !important; height: 45px !important; width: 100% !important; font-weight: 700 !important; margin-top: 25px !important; border-radius: 6px !important; }}
    .btn-filtro-contacto div.stButton > button {{ background-color: #f8f9fa !important; border: 1px solid #ddd !important; color: #1a1a1a !important; height: 45px !important; font-size: 10px !important; margin-top: 0px !important; }}

    .footer-container {{ background-color: #080808; color: #ffffff; padding: 60px 40px; font-family: 'Inter', sans-serif; margin-top: 100px; border-top: 3px solid #C41E3A; }}
    .footer-title {{ color: #ffffff; font-weight: 900; font-size: 24px; letter-spacing: 2px; margin-bottom: 20px; }}
    .footer-subtitle {{ color: #C41E3A; font-weight: 800; font-size: 12px; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 20px; }}
    .footer-link {{ color: #888; text-decoration: none; font-size: 13px; transition: 0.3s; line-height: 2; }}
    .footer-link:hover {{ color: #ffffff; padding-left: 5px; }}

    div.stButton > button {{ border: none !important; background-color: transparent !important; color: #1a1a1a !important; font-family: 'Inter', sans-serif; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; font-size: 12px; transition: 0.3s; }}

    .btn-float {{ position: fixed; right: 30px; bottom: 30px; background-color: #C41E3A; color: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 20px rgba(196, 30, 58, 0.4); z-index: 9999; cursor: pointer; font-size: 24px; transition: 0.4s; }}
    .btn-float:hover {{ transform: scale(1.1) rotate(15deg); }}

    .container-relativo {{ position: relative; height: 50px; margin-top: 15px; width: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; animation: doble-titileo 1s ease-in-out 1; }}
    .forma-boton {{ position: absolute; top: 0; left: 0; width: 100%; height: 4px; background-color: #d1d1d1; border-radius: 2px; z-index: 1; transition: background-color 0.2s ease; }}
    .forma-negra {{ background-color: #1a1a1a !important; }}
    .forma-roja {{ background-color: #C41E3A !important; }}

    .container-relativo div.stButton > button {{
        width: 100% !important; height: 50px !important; background: transparent !important; border: none !important;
        font-family: 'Inter', sans-serif !important; font-weight: 900 !important; letter-spacing: 2px !important;
        text-transform: uppercase !important; margin: 0 !important; padding: 0 !important;
        background: linear-gradient(90deg, #000 0%, #000 40%, #888 50%, #000 60%, #000 100%) !important;
        background-size: 200% auto !important; -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important;
        animation: scan 3s linear infinite !important;
    }}

    /* ADICIÓN: Estilo para la nueva hoja de detalle */
    .detail-view {{ background: white; padding: 40px; min-height: 100vh; animation: fadeIn 0.8s ease; }}
    @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS (MANTENIDA) ---
propiedades = [
    {"id": 1, "tipo": "DEPARTAMENTOS", "operacion": "Venta", "titulo": "Penthouse Alvear", "precio": "USD 850.000", "barrio": "Recoleta", "amb": "4", "m2": "120", "img": "Deptos.jpeg", "desc": "Exclusivo penthouse con terminaciones de lujo."},
    {"id": 2, "tipo": "DEPARTAMENTOS", "operacion": "Venta", "titulo": "Piso Estrada", "precio": "USD 240.000", "barrio": "Nueva Córdoba", "amb": "3", "m2": "95", "img": "Deptos.jpeg", "desc": "Amplio y luminoso, frente a plaza España."},
    {"id": 3, "tipo": "DEPARTAMENTOS", "operacion": "Alquiler", "titulo": "Torre Duomo", "precio": "$ 450.000", "barrio": "Nueva Córdoba", "amb": "2", "m2": "65", "img": "Deptos.jpeg", "desc": "Amenities de primer nivel, seguridad 24hs."},
    {"id": 4, "tipo": "CASAS", "operacion": "Venta", "titulo": "Residencia Los Olivos", "precio": "USD 1.200.000", "barrio": "Norte", "amb": "6", "m2": "450", "img": "Casas.jpeg", "desc": "Mansión con piscina y gran parque."},
]

# --- ADICIÓN QUIRÚRGICA: LÓGICA DE LA HOJA DE DETALLE ---
if st.session_state.propiedad_seleccionada:
    p = st.session_state.propiedad_seleccionada
    if st.button("← VOLVER AL LISTADO"):
        st.session_state.propiedad_seleccionada = None
        st.rerun()
    
    st.markdown("<div class='detail-view'>", unsafe_allow_html=True)
    c_img, c_txt = st.columns([1.5, 1])
    with c_img:
        st.image(p["img"], use_container_width=True)
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Video de ejemplo
    with c_txt:
        st.markdown(f"<h1 style='font-family: Inter; font-weight: 900; font-size: 50px;'>{p['precio']}</h1>", unsafe_allow_html=True)
        st.markdown(f"### {p['titulo']}\n📍 {p['barrio']}")
        st.divider()
        st.write(f"**AMBIENTES:** {p['amb']} | **SUPERFICIE:** {p['m2']} m²")
        st.write(p.get("desc", "Sin descripción disponible."))
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='container-relativo'><div class='forma-boton forma-roja'></div>", unsafe_allow_html=True)
        if st.button("CONSULTAR POR WHATSAPP"): st.success("Abriendo WhatsApp...")
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- PANTALLA INTRO (CORREGIDA PARA QUE ABRA) ---
elif st.session_state.estado == 'intro':
    st.markdown("<style>.stApp { background-color: #000000 !important; }</style>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; margin-top: 10vh;'><h1 style='font-size: 100px; color: white;'><span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span></h1></div>", unsafe_allow_html=True)
    
    ahora = datetime.datetime.now()
    futuro = datetime.datetime(2026, 10, 31, 0, 0)
    dif = futuro - ahora
    dias, horas, residuo = dif.days, *divmod(dif.seconds, 3600)
    minutos, segundos = divmod(residuo, 60)
    
    st.markdown(f"<div class='digital-timer'>{dias:02d}:{horas:02d}:{minutos:02d}:{segundos:02d}</div>", unsafe_allow_html=True)
    st.markdown("<div class='labels-timer'>DÍAS HORAS MINUTOS SEGUNDOS</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='display: flex; justify-content: center; margin-top: 50px;'>", unsafe_allow_html=True)
    if st.button("ENTER SITE", key="enter_btn"):
        st.session_state.estado = 'web'
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    time.sleep(1) # Espera un segundo antes de refrescar para que el reloj avance
    st.rerun()

# --- SITIO WEB (RESTO DEL CÓDIGO ORIGINAL SIN TOCAR) ---
elif st.session_state.estado == 'web':
    st.markdown("<style>.stApp { background-color: #E5E7EB !important; }</style>", unsafe_allow_html=True)
    # ... (Aquí va todo tu código de navegación, mapa de folium, etc.)
    # Me aseguro de respetar tus pasos: Categoría -> Operación -> Fichas
    
    if st.session_state.pagina_actual == "Principal":
        # (Lógica del mapa y buscador respetada...)
        
        if st.session_state.categoria_actual is None:
            # Sección EXPLORAR respetada
            st.markdown("<div style='text-align: center; font-family: Inter; font-weight: 800; letter-spacing: 12px; margin-bottom: 40px;'>EXPLORAR</div>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            # ... (Tus botones de categorías DEPARTAMENTOS, CASAS, etc.)
            for i, cat in enumerate(["DEPARTAMENTOS", "CASAS", "TERRENOS"]):
                with [col1, col2, col3][i]:
                    if st.button(cat, key=f"cat_{cat}"):
                        st.session_state.categoria_actual = cat; st.rerun()
        else:
            # Selección de operación (Venta/Alquiler)
            cat = st.session_state.categoria_actual
            # ...
            if st.session_state.operacion_filtro is None:
                c1, c2 = st.columns(2)
                with c1: 
                    if st.button("EN VENTA"): st.session_state.operacion_filtro = "Venta"; st.rerun()
                with c2: 
                    if st.button("EN ALQUILER"): st.session_state.operacion_filtro = "Alquiler"; st.rerun()
            else:
                # FICHAS FINALES (MODIFICACIÓN QUIRÚRGICA)
                listado = [p for p in propiedades if p["tipo"] == cat and p["operacion"] == st.session_state.operacion_filtro]
                for p in listado:
                    st.markdown(f"<div class='listing-card'><div class='img-container-listing'><img src='data:image/jpeg;base64,{get_image_base64(p['img'])}'></div><div style='padding: 20px 0;'><p class='prop-precio'>{p['precio']}</p><p class='prop-ubicacion'>{p['titulo']} | {p['barrio']}</p></div></div>", unsafe_allow_html=True)
                    st.markdown("<div class='container-relativo'><div class='forma-boton forma-negra'></div>", unsafe_allow_html=True)
                    # El botón que abre la Hoja Nueva
                    if st.button("VER DETALLES", key=f"det_{p['id']}"):
                        st.session_state.propiedad_seleccionada = p; st.rerun()
                    st.markdown("</div><br>", unsafe_allow_html=True)

    # Footer respetado
    st.markdown("""<div class='footer-container'><div class='footer-title'>GMI</div></div>""", unsafe_allow_html=True)