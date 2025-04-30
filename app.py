import gradio as gr
import data
from openai import OpenAI

# Configure the URL and the API key (if necessary, for lmstudio you just need a placeholder)
client = OpenAI(api_key="lmstudio", base_url="http://localhost:1234/v1/")

history = [
    {"role": "assistant", "content": data.start_prompt},
]

def respond(msg, chat_history, lore, character, plot, template, temperature_in):
    sys_prompt = template
    sys_prompt = sys_prompt.replace("___lore___", lore)
    sys_prompt = sys_prompt.replace("___character___", character)
    sys_prompt = sys_prompt.replace("___plot___", plot)
    messages = [{"role": "system", "content": sys_prompt},
                {"role": "user", "content": "Let's start!"}]
    
    for val in chat_history:
        messages.append(val)

    messages.append({"role": "user", "content": msg})
    # print(messages)

    response = client.chat.completions.create(
        # model="gemma-3-1b-it-qat",
        model = "gemma-3-4b-it-qat", # adapt to the model you want to use, gemma-3-1b-it-qat would run on CPU quite well for instance
        messages = messages,
        temperature = temperature_in,
    ).choices[0].message.content
    chat_history.append({"role": "user", "content": msg})
    chat_history.append({"role": "assistant", "content": response})
    return chat_history

with gr.Blocks() as demo:
    gr.Markdown("# Interactive Story Dialog Generator")
    with gr.Tab("Setting the Story"):
        with gr.Accordion("Engineering the Prompt", open = False):
            with gr.Row():
                text_lore = gr.Textbox(
                    label="Lore",
                    value = data.lore,
                    lines = 4,
                    info="Describing the world ...",)
                text_character = gr.Textbox(
                    label="Character",
                    value = data.character,
                    lines = 4,
                    info="Describing the characters who are interacting ...",)
            with gr.Row():
                text_plot = gr.Textbox(
                        label="Plot",
                        value = data.plot,
                        lines = 4,
                        info="The plot that is actually going on ...",)
                text_template = gr.Textbox(
                    label="Prompt Template",
                    value = data.prompt_template,
                    lines = 7,
                    info="The overall system prompt template for driving the conversation",)
    with gr.Tab("Settings"):
        context_size = gr.Slider(2048, 20480, value=4096, label="Context Size", info="The higher the better.", interactive=True)
        temperature = gr.Slider(0.0, 1.0, value=0.7, label="Temperature", info="The higher the more more creative.", interactive=True)
    
    chat = gr.Chatbot(history, type="messages")
    with gr.Row(equal_height=True):
        msg = gr.Textbox(label = "You are saying ...", scale = 3, value="OMG! What happened?")
        msg.submit(fn=respond, inputs=[msg, chat, text_lore, text_character, text_plot, text_template, temperature], outputs=chat)
        msg_button = gr.Button("Go", scale = 1)
    msg_button.click(fn=respond, inputs=[msg, chat, text_lore, text_character, text_plot, text_template, temperature], outputs=chat)

demo.launch()