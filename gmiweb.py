import streamlit as st

# 1. Configuración de página ancha (Estilo Luxury)
st.set_page_config(layout="wide", page_title="GMI | Gestión Inmobiliaria")

# 2. El "Truco" de Estilo (CSS) para colores y tipografía
st.markdown("""
    <style>
    /* Fondo blanco puro */
    .stApp {
        background-color: #FFFFFF;
    }
    /* Estilo para los títulos */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        font-weight: 300;
        color: #1a1a1a;
        letter-spacing: -1px;
    }
    /* Botones negros y rectos (Estilo Elliman) */
    div.stButton > button {
        background-color: #1a1a1a;
        color: white;
        border-radius: 0px;
        border: none;
        padding: 10px 25px;
        text-transform: uppercase;
        font-size: 12px;
        letter-spacing: 2px;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #4a4a4a;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Encabezado con el Logo GMI (G Azul, M Negra, I Roja)
st.markdown("""
    <div style='text-align: center; margin-top: 30px;'>
        <h1 style='font-size: 80px; margin-bottom: 0px;'>
            <span style='color: #003366;'>G</span><span style='color: #1a1a1a;'>M</span><span style='color: #C41E3A;'>I</span>
        </h1>
        <p style='letter-spacing: 8px; color: #808080; font-size: 14px; margin-top: -10px;'>
            GESTIÓN INMOBILIARIA
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border: 0.5px solid #eeeeee;'>", unsafe_allow_html=True)

# 4. Sección de Propiedades Destacadas
st.markdown("<h3 style='text-align: center; letter-spacing: 3px;'>EXCLUSIVOS</h3>", unsafe_allow_html=True)
st.write("") # Espacio

col1, col2, col3 = st.columns(3)

with col1:
    st.image("https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80")
    st.markdown("#### PUERTO MADERO")
    st.markdown("**USD 850.000**")
    st.markdown("<p style='font-size: 12px; color: gray;'>3 DORMITORIOS | 2 BAÑOS</p>", unsafe_allow_html=True)
    st.button("VER DETALLES", key="btn1")

with col2:
    st.image("https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80")
    st.markdown("#### RECOLETA")
    st.markdown("**USD 1.200.000**")
    st.markdown("<p style='font-size: 12px; color: gray;'>PISO EXCLUSIVO | TERRAZA</p>", unsafe_allow_html=True)
    st.button("VER DETALLES", key="btn2")

with col3:
    st.image("https://images.unsplash.com/photo-1600607687940-4e5a9942d4b3?auto=format&fit=crop&w=800&q=80")
    st.markdown("#### NORDELTA")
    st.markdown("**USD 540.000**")
    st.markdown("<p style='font-size: 12px; color: gray;'>MODERNA | FRENTE AL LAGO</p>", unsafe_allow_html=True)
    st.button("VER DETALLES", key="btn3")