import streamlit as st
import datetime
import time
import base64
import json
import folium
from streamlit_folium import st_folium

# --- 1. CONFIGURACIÓN DE PÁGINA (ESTÁNDAR BOUTIQUE) ---
st.set_page_config(layout="wide", page_title="GMI | Negocios Inmobiliarios", initial_sidebar_state="collapsed")

# --- 2. CONTROL DE ESTADO ---
if 'estado' not in st.session_state:
    st.session_state.estado = 'intro'
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'home'
if 'propiedad_id' not in st.session_state:
    st.session_state.propiedad_id = None

# --- 3. CARGA DE DATOS REALISTAS (CÓRDOBA) ---
@st.cache_data
def cargar_propiedades():
    return [
        {
            "id": 1, "tipo": "TERRENO", "titulo": "Lote Premium Manantiales II", "precio": "USD 45.000", 
            "zona": "Manantiales", "m2": "300", "m2_cub": "0", "amb": "0", "banos": "0", "coch": "0",
            "desc": "Terreno nivelado en etapa avanzada. Seguridad 24hs y todos los servicios subterráneos.",
            "lat": -31.4650, "lon": -64.2480, "video": "https://youtube.com/watch?v=ejemplo1"
        },
        {
            "id": 2, "tipo": "TERRENO", "titulo": "Macrolote en Docta Etapa 1", "precio": "USD 38.000", 
            "zona": "Docta", "m2": "250", "m2_cub": "0", "amb": "0", "banos": "0", "coch": "0",
            "desc": "Excelente ubicación cerca del ingreso principal. Posesión inmediata.",
            "lat": -31.4320, "lon": -64.2950, "video": "https://youtube.com/watch?v=ejemplo2"
        },
        {
            "id": 3, "tipo": "DEPTO", "titulo": "Semipiso Categoría Nueva Córdoba", "precio": "USD 125.000", 
            "zona": "Nueva Córdoba", "m2": "85", "m2_cub": "80", "amb": "3", "banos": "2", "coch": "1",
            "desc": "Frente al Palacio Ferreyra. Terminaciones en yeso, aberturas DVH y balcón terraza.",
            "lat": -31.4280, "lon": -64.1870, "video": "https://youtube.com/watch?v=ejemplo3"
        },
        {
            "id": 4, "tipo": "CASA", "titulo": "Casa Estilo Colonial Cofico", "precio": "USD 180.000", 
            "zona": "Cofico", "m2": "400", "m2_cub": "220", "amb": "5", "banos": "3", "coch": "2",
            "desc": "Propiedad reciclada a nuevo. Amplio patio con asador y techos altos originales.",
            "lat": -31.4020, "lon": -64.1850, "video": "https://youtube.com/watch?v=ejemplo4"
        }
    ]

PROPIEDADES = cargar_propiedades()

# --- 4. ESTILOS CSS (REPETANDO IDENTIDAD GMI) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    @import url('https://fonts.cdnfonts.com/css/seven-segment');

    /* UI BOUTIQUE */
    .stApp { background-color: #ffffff; }
    .header-gmi { display: flex; justify-content: space-between; align-items: center; padding: 1rem 5%; border-bottom: 1px solid #eee; position: sticky; top: 0; background: white; z-index: 999; }
    .logo-text { font-family: 'Inter'; font-weight: 800; font-size: 32px; }
    .btn-tasacion-nav { border: 2px solid #C41E3A; color: #C41E3A; padding: 5px 15px; border-radius: 5px; font-weight: 700; text-decoration: none; }
    
    /* CARDS */
    .houzez-card { background: white; border-radius: 12px; overflow: hidden; border: 1px solid #eee; margin-bottom: 20px; transition: 0.3s; }
    .houzez-card:hover { box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
    .houzez-price { color: #C41E3A; font-weight: 800; font-size: 22px; padding: 0 15px; }
    .houzez-title { font-weight: 700; padding: 10px 15px 5px; }
    
    /* FICHA DETALLE */
    .infografia-box { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; background: #f9f9f9; padding: 15px; border-radius: 8px; margin: 20px 0; }
    .info-icon { text-align: center; font-size: 12px; color: #555; }
    .sticky-contact { border: 2px solid #003366; padding: 20px; border-radius: 10px; position: sticky; top: 100px; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. LÓGICA DE PANTALLAS ---

if st.session_state.estado == 'intro':
    # PANTALLA DE RELOJ (SIN CAMBIOS)
    st.markdown("""
        <style>
        .stApp { background-color: #000000 !important; }
        .digital-timer { font-family: 'Seven Segment', sans-serif; color: #FF0000; font-size: clamp(45px, 10vw, 90px); text-shadow: 0 0 15px rgba(255, 0, 0, 0.7); text-align: center; margin-top: 20px; }
        .text-link-titileo { color: #FF0000 !important; font-family: 'Inter', sans-serif; font-weight: 900; text-align: center; animation: blinker 1.2s linear infinite; margin-top: 40px; }
        @keyframes blinker { 50% { opacity: 0.1; } }
        div.stButton > button { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: transparent !important; border: none !important; color: transparent !important; z-index: 999; }
        </style>
        <div style='text-align: center; margin-top: 10vh;'><h1 style='font-size: 100px; color: white;'><span style='color: #003366;'>G</span>M<span style='color: #C41E3A;'>I</span></h1></div>
    """, unsafe_allow_html=True)
    
    futuro = datetime.datetime(2026, 10, 31, 0, 0)
    dif = futuro - datetime.datetime.now()
    dias, horas, residuo = dif.days, *divmod(dif.seconds, 3600)
    minutos, segundos = divmod(residuo, 60)
    
    st.markdown(f"<div class='digital-timer'>{dias:02d}:{horas:02d}:{minutos:02d}:{segundos:02d}</div><div class='text-link-titileo'>>>> CLICK PARA ENTRAR <<<</div>", unsafe_allow_html=True)
    if st.button("ENTER"):
        st.session_state.estado = 'web'
        st.rerun()
    time.sleep(1)
    st.rerun()

elif st.session_state.estado == 'web':
    # HEADER STICKY
    st.markdown("""
        <div class="header-gmi">
            <div class="logo-text"><span style="color:#003366">G</span>M<span style="color:#C41E3A">I</span></div>
            <div style="display:flex; gap:20px; align-items:center;">
                <small>VENTAS</small> <small>ALQUILERES</small> <a href="#" class="btn-tasacion-nav">TASACIONES</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.pagina == 'home':
        # --- HERO MAP & FILTRO MAESTRO ---
        col_map, col_filtro = st.columns([1.2, 0.8])
        
        with col_map:
            m = folium.Map(location=[-31.42, -64.20], zoom_start=12, tiles='CartoDB positron')
            for p in PROPIEDADES:
                folium.Marker(
                    [p['lat'], p['lon']], 
                    popup=f"{p['titulo']} - {p['precio']}",
                    icon=folium.Icon(color='red' if p['id']%2==0 else 'blue')
                ).add_to(m)
            st_folium(m, height=450, use_container_width=True)

        with col_der := col_filtro:
            st.markdown('<div style="padding:20px; background:#f9f9f9; border-radius:10px;">', unsafe_allow_html=True)
            st.subheader("Buscador")
            st.selectbox("Zona", ["Todas", "Manantiales", "Docta", "Nueva Córdoba", "Cofico"])
            st.multiselect("Tipo", ["Casas", "Deptos", "Terrenos"], default=["Casas"])
            if st.button("LA CONFIRMACIÓN DE MORTY", use_container_width=True, type="primary"):
                st.toast("Filtrando...")
            st.markdown('</div>', unsafe_allow_html=True)

        # GRID DE DESTACADOS
        st.markdown("<h2 style='text-align:center; margin-top:50px;'>Propiedades Destacadas</h2>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, p in enumerate(PROPIEDADES[:3]):
            with cols[i]:
                st.markdown(f"""
                    <div class="houzez-card">
                        <div style="height:200px; background:#eee;"></div>
                        <div class="houzez-title">{p['titulo']}</div>
                        <div class="houzez-price">{p['precio']}</div>
                        <p style="padding:0 15px; color:#777; font-size:13px;">{p['zona']}</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"VER FICHA COMPLETA", key=f"p_{p['id']}", use_container_width=True):
                    st.session_state.propiedad_id = p['id']
                    st.session_state.pagina = 'detalle'
                    st.rerun()

    elif st.session_state.pagina == 'detalle':
        # --- FICHA DE PROPIEDAD: LA CONFIRMACIÓN DE MORTY ---
        p = next(item for item in PROPIEDADES if item["id"] == st.session_state.propiedad_id)
        
        if st.button("← VOLVER AL LISTADO"):
            st.session_state.pagina = 'home'
            st.rerun()

        col_main, col_side = st.columns([1.5, 1])
        
        with col_main:
            st.title(p['titulo'])
            tab1, tab2, tab3 = st.tabs(["📸 Fotos", "🎥 Video", "📍 Mapa"])
            with tab1: st.image("https://via.placeholder.com/800x450?text=Imagen+Propiedad")
            with tab2: st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Placeholder
            with tab3: st.write("Mapa detallado aquí")

            st.markdown(f"""
                <div class="infografia-box">
                    <div class="info-icon">📐<br><b>{p['m2']}m²</b><br>Totales</div>
                    <div class="info-icon">🏠<br><b>{p['amb']}</b><br>Ambientes</div>
                    <div class="info-icon">🛁<br><b>{p['banos']}</b><br>Baños</div>
                    <div class="info-icon">🚗<br><b>{p['coch']}</b><br>Cochera</div>
                    <div class="info-icon">🏗️<br><b>{p['m2_cub']}m²</b><br>Cubiertos</div>
                    <div class="info-icon">🏢<br><b>{p['tipo']}</b><br>Tipo</div>
                </div>
                <h3>Descripción</h3>
                <p style='font-size:18px; line-height:1.6; color:#444;'>{p['desc']}</p>
            """, unsafe_allow_html=True)

        with col_side:
            st.markdown(f"""
                <div class="sticky-contact">
                    <h2 style="color:#C41E3A; margin-bottom:0;">{p['precio']}</h2>
                    <p style="color:#666; margin-bottom:20px;">Expensas estimadas: $35.000</p>
                    <hr>
                </div>
            """, unsafe_allow_html=True)
            
            # FORMULARIO CONECTABLE A ZOHO
            with st.form("contacto_zoho"):
                nombre = st.text_input("Nombre")
                email = st.text_input("Email")
                mensaje = st.text_area("Mensaje", value=f"Hola GMI, me interesa: {p['titulo']}")
                submit = st.form_submit_button("CONSULTAR AHORA", use_container_width=True)
                if submit:
                    st.success("Enviado a Zoho CRM (Simulado)")

            # WHATSAPP DIRECTO
            st.markdown(f"""
                <a href="https://wa.me/543512345678?text=Consulta%20por%20{p['titulo']}" 
                   style="text-decoration:none;">
                    <button style="width:100%; background:#25D366; color:white; border:none; padding:12px; border-radius:5px; font-weight:700; cursor:pointer;">
                        WHATSAPP DIRECTO
                    </button>
                </a>
            """, unsafe_allow_html=True)

    # FOOTER OBLIGATORIO
    st.markdown("""
        <hr><div style='text-align:center; padding:20px; color:#999; font-size:12px;'>
        GMI Negocios Inmobiliarios - Matrícula Profesional CPI 1234<br>
        Córdoba, Argentina. 2026
        </div>
    """, unsafe_allow_html=True)