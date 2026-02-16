import streamlit as st
import requests # Esta es la que instalamos para traer datos de internet

st.set_page_config(page_title="GMI - Panel Profesional", page_icon="🏠")

# --- FUNCIÓN PARA TRAER EL DÓLAR ---
def obtener_dolar():
    try:
        # Usamos la API de dolarapi.com para traer el valor real
        url = "https://dolarapi.com/v1/dolares/blue"
        respuesta = requests.get(url)
        datos = respuesta.json()
        return datos['venta']
    except:
        return "No disponible"

valor_dolar = obtener_dolar()

# --- DISEÑO ---
st.title("🏠 GMI - Gestión Inmobiliaria")

# Mostramos el dólar en un "Métrico" (se ve muy pro)
st.metric(label="Cotización Dólar Blue (Venta)", value=f"${valor_dolar}")

st.markdown("---")
st.write("### Estado del Sistema")
st.success("Conexión con Python: OK")
st.info("Próximo paso: Conectar la base de datos de propiedades.")

# Sidebar
st.sidebar.header("Menú de Gestión")
if st.sidebar.button("Actualizar Datos"):
    st.rerun()
    
