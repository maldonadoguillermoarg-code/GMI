import streamlit as st
import datetime

# 1. Configuración de página
st.set_page_config(layout="wide", page_title="GMI | Próximamente")

# 2. Control de navegación (para pasar del contador a la web)
if 'entrar' not in st.session_state:
    st.session_state.entrar = False

# 3. CSS: Estilo Douglas Elliman + Reloj Digital Rojo
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    
    /* Contenedor traslúcido estilo moderno */
    .countdown-container {
        background-color: rgba(40, 40, 40, 0.9);
        padding: 50px;
        border-radius: 20px;
        text-align: center;
        margin: 40px auto;
        max-width: 700px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    /* Fuente de reloj digital */
    .digital-clock {
        font-family: 'Courier New', Courier, monospace;
        color: #FF0000;
        font-size: 75px;
        font-weight: bold;
        text-shadow: 0 0 15px rgba(255, 0, 0, 0.8), 0 0 5px rgba(255, 0, 0, 1);
        letter-spacing: 4px;
        margin: 20px 0;
    }
    
    .label-clock {
        color: #aaaaaa;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 4px;
    }

    /* Botón Negro Minimalista */
    div.stButton > button {
        background-color: #000000;
        color: white;
        border-radius: 0px;
        border: 1px solid #444;
        padding: 15px 30px;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-size: 14px;
        transition: 0.4s;
    }
    div.stButton > button:hover {
        background-color: #333333;
        border: 1px solid white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE PANTALLA ---

if not st.session_state.entrar:
    # --- PANTALLA 1: LANZAMIENTO (COUNTDOWN) ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Logo GMI
    st.markdown("""
        <div style='text-align: center;'>
            <h1 style='font-size: 70px; margin-bottom: 0px;'>
                <span style='color: #003366;'>G</span><span style='color: #1a1a1a;'>M</span><span style='color: #C41E3A;'>I</span>
            </h1>
            <p style='letter-spacing: 10px; color: gray; font-size: 14px;'>GESTIÓN INMOBILIARIA</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Cálculo del tiempo hasta el 31 de Octubre
    fecha_limite = datetime.datetime(2026, 10, 31, 0, 0)
    ahora = datetime.datetime.now()
    dif = fecha_limite - ahora
    
    dias = dif.days
    horas, resto = divmod(dif.seconds, 3600)
    minutos, _ = divmod(resto, 60)

    # Mostrar la caja del contador
    st.markdown(f"""
        <div class="countdown-container">
            <p style='color: white; letter-spacing: 5px; font-size: 16px; margin-bottom: 10px;'>GRAND OPENING</p>
            <div class="digital-clock">
                {dias:02d}:{horas:02d}:{minutos:02d}
            </div>
            <div class="label-clock">
                DÍAS &nbsp;&nbsp;&nbsp; HORAS &nbsp;&nbsp;&nbsp; MINUTOS
            </div>
            <p style='color: #666; font-size: 12px; margin-top: 30px;'>31 . OCTUBRE . 2026</p>
        </div>
        """, unsafe_allow_html=True)

    # Botón de entrada
    col_b1, col_b2, col_b3 = st.columns([1,2,1])
    with col_b2:
        if st.button("MIRA LOS AVANCES DE NUESTRA WEB"):
            st.session_state.entrar = True
            st.rerun()

else:
    # --- PANTALLA 2: LA WEB PROVISIONAL (GMI LUXURY) ---
    st.markdown("""
        <div style='text-align: center; margin-top: 30px;'>
            <h1 style='font-size: 60px; margin-bottom: 0px;'>
                <span style='color: #003366;'>G</span><span style='color: #1a1a1a;'>M</span><span style='color: #C41E3A;'>I</span>
            </h1>
            <p style='letter-spacing: 8px; color: #808080; font-size: 12px;'>GESTIÓN INMOBILIARIA</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr style='opacity: 0.2;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; letter-spacing: 4px; font-weight: 300;'>EXCLUSIVOS EN OBRA</h3>", unsafe_allow_html=True)
    st.write("")

    # Cuadrícula de propiedades (como ya las teníamos)
    c1, c2, c3 = st.columns(3)
    
    propiedades = [
        {"zona": "PUERTO MADERO", "precio": "850.000", "img": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80"},
        {"zona": "RECOLETA", "precio": "1.200.000", "img": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80"},
        {"zona": "NORDELTA", "precio": "540.000", "img": "https://images.unsplash.com/photo-1600607687940-4e5a9942d4b3?auto=format&fit=crop&w=800&q=80"}
    ]

    cols = [c1, c2, c3]
    for i, p in enumerate(propiedades):
        with cols[i]:
            st.image(p["img"])
            st.markdown(f"**{p['zona']}**")
            st.markdown(f"USD {p['precio']}")
            st.button("MÁS INFO", key=f"p{i}")

    st.write("")
    if st.button("← VOLVER AL CONTADOR"):
        st.session_state.entrar = False
        st.rerun()