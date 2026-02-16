import streamlit as st
import datetime
import time
import base64

# 1. Configuración de página
st.set_page_config(layout="wide", page_title="GMI | Negocios Inmobiliarios")

# 2. Control de estado
if 'estado' not in st.session_state:
    st.session_state.estado = 'intro'
if 'categoria_actual' not in st.session_state:
    st.session_state.categoria_actual = None

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

# --- ESTILOS GLOBALES Y ANIMACIONES ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&family=Nunito+Sans:wght@300;400;600&display=swap');
    @import url('https://fonts.cdnfonts.com/css/seven-segment');

    /* Reset Scrollbar oculto */
    html, body {{ scrollbar-width: none; }}
    body::-webkit-scrollbar {{ display: none; }}
    
    @keyframes blinker {{ 50% {{ opacity: 0.1; }} }}

    /* Animación Protector de Pantalla DVD (Pepinillo) */
    @keyframes dvdBounce {{
        0%   {{ top: 0%; left: 0%; transform: rotate(0deg); }}
        25%  {{ top: 80%; left: 20%; transform: rotate(90deg); }}
        50%  {{ top: 10%; left: 80%; transform: rotate(180deg); }}
        75%  {{ top: 70%; left: 40%; transform: rotate(270deg); }}
        100% {{ top: 0%; left: 0%; transform: rotate(360deg); }}
    }}

    /* Estilo para Pepinillo (DVD) */
    .pepinillo-dvd {{
        position: fixed;
        width: 150px;
        z-index: 10000;
        animation: dvdBounce 15s linear infinite;
        pointer-events: none;
    }}

    /* Estilo para Ricoso (Fijo abajo a la derecha) */
    .ricoso-fijo {{
        position: fixed;
        bottom: 10px;
        right: 10px;
        width: 180px;
        z-index: 10001;
        pointer-events: none;
    }}

    /* TARJETA ESTILO ELLIMAN */
    .listing-card {{ background-color: transparent; margin-bottom: 20px; transition: 0.3s; }}
    .img-container-listing {{ width: 100%; height: 350px; overflow: hidden; border-radius: 2px; }}
    .img-container-listing img {{ width: 100%; height: 100%; object-fit: cover; transition: transform 0.6s ease; }}
    .img-container-listing:hover img {{ transform: scale(1.05); }}
    .info-container {{ padding: 15px 0; border-bottom: 1px solid #d1d1d1; }}
    .prop-precio {{ font-family: 'Inter', sans-serif; font-weight: 800; font-size: 20px; color: #1a1a1a; margin: 0; }}
    .prop-ubicacion {{ font-family: 'Nunito Sans', sans-serif; font-size: 14px; color: #666; text-transform: uppercase; margin: 5px 0; }}
    </style>

    <div class="pepinillo-dvd"><img src="data:image/gif;base64,{pepinillo_b64}" width="100%"></div>
    <div class="ricoso-fijo"><img src="data:image/gif;base64,{ricoso_b64}" width="100%"></div>
    """, unsafe_allow_html=True)

# --- DATOS DE ZOHO ---
propiedades = [
    {"tipo": "DEPARTAMENTOS", "titulo": "Penthouse Alvear", "precio": "USD 850.000", "barrio": "Recoleta", "amb": "4", "m2": "120", "img": "Deptos.jpeg"},
    {"tipo": "CASAS", "titulo": "Residencia Los Olivos", "precio": "USD 1.200.000", "barrio": "Norte", "amb": "6", "m2": "450", "img": "Casas.jpeg"},
    {"tipo": "TERRENOS", "titulo": "Lote Premium Golf", "precio": "USD 340.000", "barrio": "Country Club", "amb": "-", "m2": "1200", "img": "Terreno.jpeg"},
]

if st.session_state.estado == 'intro':
    # PANTALLA 1: INTRO NEGRA
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

    st.markdown("<div style='text-align: center; margin-top: 5vh;'><h1 style='font-size: 100px; margin-bottom: 0px; color: white;'><span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span></h1><p style='letter-spacing: 8px; color: #333; font-size: 14px; font-weight: 800; margin-bottom: 50px;'>NEGOCIOS INMOBILIARIOS</p></div>", unsafe_allow_html=True)

    futuro = datetime.datetime(2026, 10, 31, 0, 0)
    ahora = datetime.datetime.now()
    dif = futuro - ahora
    dias, horas, residuo = dif.days, *divmod(dif.seconds, 3600)
    minutos, segundos = divmod(residuo, 60)
    
    st.markdown(f"<div class='digital-timer'>{dias:02d}:{horas:02d}:{minutos:02d}:{segundos:02d}</div><div class='labels-timer'>DÍAS HORAS MINUTOS SEGUNDOS</div><div class='text-link-titileo'>>>> MIRA LOS AVANCES DE NUESTRA WEB <<<</div>", unsafe_allow_html=True)

    if st.button("ENTER"):
        st.session_state.estado = 'web'
        st.rerun()
    time.sleep(1)
    st.rerun()

elif st.session_state.estado == 'web':
    # PANTALLA 2: WEB BLANCA / HUESO
    st.markdown("<style>.stApp { background-color: #f4f4f2 !important; }</style>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='text-align: center; padding-top: 20px;'>
            <div style='font-family: "Inter"; font-size: 60px; font-weight: 800; color: #1a1a1a;'>
                <span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span>
            </div>
            <div style='letter-spacing: 5px; color: #888; font-size: 12px; font-weight: 600; margin-bottom: 40px;'>NEGOCIOS INMOBILIARIOS</div>
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
        # VISTA DE LISTADO FILTRADO
        cat = st.session_state.categoria_actual
        st.markdown(f"<div style='text-align: center; font-family: Inter; font-weight: 800; letter-spacing: 5px; margin-bottom: 40px;'>{cat}</div>", unsafe_allow_html=True)
        
        propiedades_filtradas = [p for p in propiedades if p["tipo"] == cat]
        col_list, col_spacer = st.columns([1, 2])
        
        for i, p in enumerate(propiedades_filtradas):
            with col_list:
                img_b64 = get_image_base64(p["img"])
                st.markdown(f"""
                    <div class="listing-card">
                        <div class="img-container-listing"><img src="data:image/jpeg;base64,{img_b64}"></div>
                        <div class="info-container">
                            <p class="prop-precio">{p['precio']}</p>
                            <p class="prop-ubicacion">{p['titulo']} | {p['barrio']}</p>
                            <p style='color: #888; font-size: 13px;'>{p['amb']} AMB  •  {p['m2']} M²</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                st.button("VER FICHA COMPLETA", key=f"ficha_{i}")

        if st.button("← VOLVER A CATEGORÍAS"):
            st.session_state.categoria_actual = None
            st.rerun()

    if st.button("← VOLVER AL INICIO"):
        st.session_state.estado = 'intro'
        st.session_state.categoria_actual = None
        st.rerun()