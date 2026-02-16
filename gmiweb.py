import streamlit as st
import datetime

# 1. Configuración de página
st.set_page_config(layout="wide", page_title="GMI | Acceso Restringido")

# 2. Control de acceso
if 'acceso_concedido' not in st.session_state:
    st.session_state.acceso_concedido = False

# 3. CSS FUTURISTA (Capa traslúcida total)
st.markdown("""
    <style>
    /* Estilo de la web de fondo */
    .main-content {
        filter: blur(8px);
        pointer-events: none;
    }

    /* Pantalla total traslúcida */
    .overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(20, 20, 20, 0.85); /* Gris oscuro traslúcido */
        backdrop-filter: blur(15px); /* Desenfoque de lo que hay atrás */
        z-index: 9999;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: white;
        text-align: center;
    }

    /* Reloj Digital Futurista */
    .digital-clock {
        font-family: 'Courier New', Courier, monospace;
        color: #FF0000;
        font-size: 80px;
        font-weight: bold;
        text-shadow: 0 0 20px rgba(255, 0, 0, 0.9), 0 0 40px rgba(255, 0, 0, 0.4);
        margin: 20px 0;
        letter-spacing: 10px;
    }

    .scanner-line {
        width: 100%;
        height: 2px;
        background: rgba(255, 0, 0, 0.5);
        position: absolute;
        top: 0;
        box-shadow: 0 0 15px #FF0000;
        animation: scan 4s linear infinite;
    }

    @keyframes scan {
        0% { top: 0%; }
        100% { top: 100%; }
    }

    /* Botón estilo Interfaz de Nave */
    div.stButton > button {
        background-color: transparent;
        color: #FF0000;
        border: 2px solid #FF0000;
        border-radius: 5px;
        padding: 15px 40px;
        text-transform: uppercase;
        letter-spacing: 5px;
        font-weight: bold;
        box-shadow: 0 0 10px rgba(255, 0, 0, 0.3);
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #FF0000;
        color: black;
        box-shadow: 0 0 30px rgba(255, 0, 0, 0.8);
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE INTERFAZ ---

if not st.session_state.acceso_concedido:
    # --- PANTALLA FUTURISTA (OVERLAY) ---
    st.markdown('<div class="scanner-line"></div>', unsafe_allow_html=True)
    
    # Logo GMI Flotante
    st.markdown("""
        <div style='position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 10000; text-align: center; width: 100%;'>
            <h1 style='font-size: 100px; margin-bottom: 0px;'>
                <span style='color: #003366; text-shadow: 0 0 10px rgba(0,51,102,0.8);'>G</span><span style='color: #FFFFFF;'>M</span><span style='color: #C41E3A; text-shadow: 0 0 10px rgba(196,30,58,0.8);'>I</span>
            </h1>
            <p style='color: white; letter-spacing: 15px; font-size: 14px; margin-bottom: 40px;'>PROTOCOLOS DE GESTIÓN ACTIVADOS</p>
    """, unsafe_allow_html=True)

    # Contador
    fecha_limite = datetime.datetime(2026, 10, 31, 0, 0)
    dif = fecha_limite - datetime.datetime.now()
    dias, horas, minutos = dif.days, divmod(dif.seconds, 3600)[0], divmod(dif.seconds % 3600, 60)[0]
    
    st.markdown(f'<div class="digital-clock">{dias:02d}:{horas:02d}:{minutos:02d}</div>', unsafe_allow_html=True)
    st.markdown("<p style='color: #666; letter-spacing: 5px;'>SISTEMA EN DESARROLLO - 31.OCT.26</p><br>", unsafe_allow_html=True)

    # Botón de entrada
    col_b1, col_b2, col_b3 = st.columns([1,2,1])
    with col_b2:
        if st.button("DESBLOQUEAR AVANCES"):
            st.session_state.acceso_concedido = True
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- CONTENIDO DE LA WEB (LO QUE SE VE ATRÁS) ---
st.markdown("<div class='main-content'>", unsafe_allow_html=True)

# Logo GMI principal (ya en la web)
st.markdown("""
    <div style='text-align: center; margin-top: 30px;'>
        <h1 style='font-size: 60px; margin-bottom: 0px;'>
            <span style='color: #003366;'>G</span><span style='color: #1a1a1a;'>M</span><span style='color: #C41E3A;'>I</span>
        </h1>
        <p style='letter-spacing: 8px; color: #808080; font-size: 12px;'>GESTIÓN INMOBILIARIA</p>
    </div>
    <hr style='opacity: 0.1;'>
    """, unsafe_allow_html=True)

# Grilla de propiedades
c1, c2, c3 = st.columns(3)
with c1:
    st.image("https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80")
    st.markdown("**EXCLUSIVO PUERTO MADERO**")
with c2:
    st.image("https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80")
    st.markdown("**PISO RECOLETA**")
with c3:
    st.image("https://images.unsplash.com/photo-1600607687940-4e5a9942d4b3?auto=format&fit=crop&w=800&q=80")
    st.markdown("**CASA NORDELTA**")

st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.acceso_concedido:
    if st.button("VOLVER AL PROTOCOLO"):
        st.session_state.acceso_concedido = False
        st.rerun()