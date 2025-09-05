import streamlit as st

# --- Configuración de la página ---
# Esto establece el título que se ve en la pestaña del navegador, el ícono y el layout.
st.set_page_config(
    page_title="Calculadora de Balance de Masa",
    page_icon="🍓",
    layout="wide",
)

# --- Título Principal y Descripción ---
st.title("⚙️ Calculadora de Balance de Masa")
st.markdown("### Estandarización de °Brix en Pulpa de Fruta")
st.write(
    """
    Esta aplicación web resuelve un problema común en la industria de alimentos:
    ajustar la concentración de azúcar (°Brix) de un producto.
    Ingresa los datos de tu proceso para calcular la cantidad de azúcar necesaria.
    """
)
st.write("---") # Dibuja una línea horizontal para separar secciones

# --- Layout en dos columnas para una mejor organización ---
col1, col2 = st.columns([2, 3]) # La columna 2 será 1.5 veces más ancha que la 1

# --- Columna 1: Entradas de datos y Resultados ---
with col1:
    st.header("Parámetros del Proceso")

    # --- Formularios de entrada para el usuario ---
    # Usamos st.number_input para campos numéricos, con valores por defecto del problema
    masa_pulpa_inicial = st.number_input(
        "Masa inicial de la pulpa (kg)", min_value=0.1, value=50.0, step=1.0
    )
    brix_inicial = st.number_input(
        "°Brix iniciales de la pulpa (%)", min_value=0.0, max_value=100.0, value=7.0, step=0.1
    )
    brix_final_deseado = st.number_input(
        "°Brix finales deseados (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.1
    )

    # --- Botón para ejecutar el cálculo ---
    if st.button("Calcular Cantidad de Azúcar", type="primary"):
        # --- Lógica y validación del cálculo ---
        if brix_final_deseado <= brix_inicial:
            st.error(
                "Error: Los °Brix deseados deben ser mayores que los iniciales para necesitar agregar azúcar."
            )
        else:
            # --- Balance de Masa ---
            # Sólidos iniciales = Masa total * (% de sólidos)
            solidos_iniciales = masa_pulpa_inicial * (brix_inicial / 100)

            # Azúcar a agregar (X) es 100% sólidos.
            # Ecuación de balance de sólidos:
            # (Masa_inicial + X) * (%Brix_final) = Solidos_iniciales + X * (100% solidos)
            # Despejando X (azucar_a_agregar):
            numerador = solidos_iniciales - (masa_pulpa_inicial * (brix_final_deseado / 100))
            denominador = (brix_final_deseado / 100) - 1
            azucar_a_agregar = numerador / denominador

            masa_final_pulpa = masa_pulpa_inicial + azucar_a_agregar

            # --- Mostrar Resultados ---
            st.success("¡Cálculo completado!")
            st.metric(
                label="Azúcar que se debe agregar",
                value=f"{azucar_a_agregar:.2f} kg",
                help="Esta es la masa de azúcar (100% sólidos) que se necesita añadir."
            )
            st.metric(
                label="Masa final de la pulpa ajustada",
                value=f"{masa_final_pulpa:.2f} kg",
                help="Esta es la masa total del producto después de añadir el azúcar."
            )

# --- Columna 2: Explicación del problema y Diagrama ---
with col2:
    st.header("Contexto del Problema")
    st.info(
        """
        **Problema:** Se parte de **50 kg de pulpa de fruta** con una concentración de **7 °Brix**.
        El objetivo es estandarizar el producto para que alcance una concentración final de **10 °Brix**.
        
        **Pregunta:** ¿Cuánta azúcar (considerada 100% sólidos) se debe agregar para lograrlo?
        """
    )
    st.image(
        "https://i.imgur.com/8aIs5jG.png",
        caption="Diagrama del proceso de balance de masa para estandarizar °Brix.",
    )

st.write("---")
st.markdown("Creado con 🐍 Python y Streamlit.")
