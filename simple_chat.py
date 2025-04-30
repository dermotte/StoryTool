import gradio as gr

gr.load_chat("http://localhost:1234/v1/", model="gemma-3-1b-it-qat", token="***").launch()