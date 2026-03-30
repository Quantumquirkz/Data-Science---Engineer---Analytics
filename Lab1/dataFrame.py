import gradio as gr
import pandas as pd

# Datos iniciales
def cargar_datos():
    return pd.DataFrame({
        "Nombre": ["Ana", "Luis", "Carlos"],
        "Edad": [25, 30, 22]
    })

# Procesar datos (ejemplo: calcular edad promedio)
def procesar(df):
    df['Edad'].astype(int)
    promedio = df["Edad"].mean()
    return f"Edad promedio: {promedio:.2f}"

with gr.Blocks() as demo:
    gr.Markdown("## 📊 Ejemplo con Dataframe")

    tabla = gr.Dataframe(
        value=cargar_datos,
        headers=["Nombre", "Edad"],
        datatype=["str", "number"],
        interactive=True
    )

    salida = gr.Textbox(label="Resultado")

    btn = gr.Button("Calcular promedio")

    btn.click(fn=procesar, inputs=tabla, outputs=salida)

demo.launch()