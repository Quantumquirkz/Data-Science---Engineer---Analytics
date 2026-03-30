import gradio as gr

# Función del chatbot
def chatbot(mensaje, historial):
    if historial is None:
        historial = []

    # Respuesta simple (puedes cambiar esto por IA real)
    respuesta = f"Echo: {mensaje}"

    historial.append((mensaje, respuesta))
    return "", historial

# Interfaz
with gr.Blocks() as demo:
    gr.Markdown("## 🤖 Chatbot sencillo con Gradio")

    chatbot_ui = gr.Chatbot()
    msg = gr.Textbox(placeholder="Escribe tu mensaje aquí...")

    estado = gr.State([])

    msg.submit(chatbot, [msg, estado], [msg, chatbot_ui])

# Ejecutar
demo.launch()