import streamlit as st

# 1. Configuración de página ancha (estilo Douglas Elliman)
st.set_page_config(layout="wide", page_title="GMI | Luxury Real Estate")

# 2. El "Truco" de Estilo (CSS) para que se vea Pro
st.markdown("""
    <style>
    /* Cambiar el fondo a blanco puro */
    .stApp {
        background-color: #FFFFFF;
    }
    /* Estilo para los títulos (Tipografía elegante y fina) */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        font-weight: 300;
        color: #1a1a1a;
        letter-spacing: -1px;
    }
    /* Botones estilo Douglas Elliman (Negros, rectos, elegantes) */
    div.stButton > button {
        background-color: #1a1a1a;
        color: white;
        border-radius: 0px;
        border: none;
        padding: 10px 25px;
        text-transform: uppercase;
        font-size: 12px;
        letter-spacing: 2px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #4a4a4a;
        color: white;
    }
    /* Quitar bordes de las imágenes */
    img {
        border-radius: 0px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Encabezado Minimalista con Colores Personalizados
st.markdown("""
    <h1 style='text-align: center; margin-top: 50px; font-size: 60px;'>
        <span style='color: #003366;'>G</span><span style='color: #1a1a1a;'>M</span><span style='color: #C41E3A;'>I</span>
    </h1>
    """, unsafe_allow_html=True)
st.markdown("<p style='text-align: center; letter-spacing: 5px; color: grey;'>GESTIÓN INMOBILIARIA</p>", unsafe_allow_html=True)
st.markdown("---")

# 4. Sección de Propiedades Destacadas
st.markdown("### EXCLUSIVOS")

# Creamos 3 columnas para las tarjetas de propiedades
col1, col2, col3 = st.columns(3)

# Simulación de propiedades con el look de Elliman
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