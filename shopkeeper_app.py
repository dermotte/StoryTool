"""
Shopkeeper-Player Negotiation Demo

This Gradio app simulates a negotiation between a grumpy shopkeeper and a desperate player in a fantasy setting. Users can edit the prompts and starting lines for both characters, select the model, and set the number of turns for the negotiation. The negotiation is run using a local OpenAI-compatible API.

Main Components:
- MODEL_OPTIONS: List of available model names for selection.
- shopkeeper_prompt / player_prompt: Default prompt templates for each character, editable by the user.
- shopkeeper_start / player_start: Default starting lines for each character, editable by the user.
- get_client(): Returns an OpenAI client configured for a local API endpoint.
- answer(): Sends a chat history to the model and returns the model's response.
- run_negotiation(): Runs the negotiation for a given number of turns, alternating between shopkeeper and player, using the provided prompts and starting lines.
- gradio_run(): Formats the negotiation log for display in the Gradio chatbot.
- Gradio UI: Allows users to edit prompts, select model, set turns, and run/reset the negotiation. The chatbot displays the conversation.

Usage:
- Edit the prompts and starting lines in the accordion to customize the negotiation.
- Select a model and number of turns.
- Click "Run Negotiation" to start a new negotiation with the current settings.
- Use the trash can button to reset the chat history.
"""

import gradio as gr
from openai import OpenAI

# Define available models
MODEL_OPTIONS = [
    "gemma-3-4b-it-qat",
    "granite-3.3-8b-instruct",
    "qwen2.5-7b-instruct",
    "qwen3-4b"
]

shopkeeper_prompt = """You are a grumpy shopkeeper in a bustling fantasy village. You are known for your short, unfriendly demeanor and only grudgingly part with your wares. You start with a price of 5 coins for one health potion, but with persistent haggling from the customer, you can be persuaded to reduce the price to as low as 1 coin. Your responses should be brief and curt, reflecting your character's displeasure at having to deal with customers. Speak only the text that you would say to the adventurer.

Possible arguments not to lower the price:
I have children, and a bad hair day?
This is not a charity.
Do I look like I support the idea of a clearance sale?

RULES OF ENGAGEMENT:
Never offer less than one and a quarter coin.
If the player agrees on a price, then close the deal.
Speak ONLY as your character. Your entire output must be dialogue.
Strictly limit responses to a maximum of two sentences.
ABSOLUTELY NO out-of-character text. Do not include narration, actions, emotions, descriptions, explanations, or stage directions.
React directly to the last input while keeping your character's motivations and focus in mind.
Do not break character under any circumstances.
"""

player_prompt = """You are an adventurer in a fantasy game, visiting a shopkeeper in a bustling fantasy village to buy a health potion. You are in dire need of a health potion, as your last battle left you severely wounded. You have only two coins left in your possession. If the shopkeeper offers a price higher than two coins, you must haggle to get the best deal possible. Your responses should be short and demanding, reflecting your character's urgency and desperation. Speak only the text that you would say to the shopkeeper.

Possible arguments to lower the price:
I'm injured, don't you see?
You potion looks weak to me, it's not worth the price.
Yesterday the price was much lower!
Isn't a health potion meant to be green and without the skull on the label?
I have only two coins, and I need a health potion to survive.

RULES OF ENGAGEMENT:
Start with offering half a coin.
Never offer more than two coins.
If the shopkeeper agrees on a price, don't offer a higher one.
Speak ONLY as your character. Your entire output must be dialogue.
Strictly limit responses to a maximum of two sentences.
ABSOLUTELY NO out-of-character text. Do not include narration, actions, emotions, descriptions, explanations, or stage directions.
React directly to the last input while keeping your character's motivations and focus in mind.
Do not break character under any circumstances.
"""

shopkeeper_start = "What do you want?"
player_start = "I need a health potion!"

def get_client(): # Use LM Studio or llama.cpp to run a local model. 
    return OpenAI(api_key="lmstudio", base_url="http://localhost:1234/v1/")

def answer(client, chat, model):
    output = client.chat.completions.create(
        model=model,
        messages=chat
    ).choices[0].message.content
    return output

def run_negotiation(model, turns, shopkeeper_prompt, player_prompt, shopkeeper_start, player_start):
    client = get_client()
    history_keeper = [
        {"role": "system", "content": shopkeeper_prompt},
        {"role": "user", "content": player_start},
    ]
    history_player = [
        {"role": "system", "content": player_prompt},
        {"role": "user", "content": shopkeeper_start},
        {"role": "assistant", "content": player_start},
    ]
    chat_log = [("Shopkeeper", shopkeeper_start), ("Player", player_start)]
    for _ in range(turns-1):
        keeper_answer = answer(client, history_keeper, model)
        history_player.append({"role": "user", "content": keeper_answer})
        history_keeper.append({"role": "assistant", "content": keeper_answer})
        chat_log.append(("Shopkeeper", keeper_answer))
        player_answer = answer(client, history_player, model)
        history_player.append({"role": "assistant", "content": player_answer})
        history_keeper.append({"role": "user", "content": player_answer})
        chat_log.append(("Player", player_answer))
    return chat_log

def gradio_run(model, turns, shopkeeper_prompt, player_prompt, shopkeeper_start, player_start):
    chat_log = run_negotiation(model, turns, shopkeeper_prompt, player_prompt, shopkeeper_start, player_start)
    # Format for gr.Chatbot: list of [user, bot] pairs
    messages = []
    for i in range(0, len(chat_log), 2):
        user = chat_log[i][1]
        bot = chat_log[i+1][1] if i+1 < len(chat_log) else ""
        messages.append([user, bot])
    return messages

with gr.Blocks() as demo:
    gr.Markdown("# Shopkeeper-Player Negotiation Demo")
    with gr.Row():
        model = gr.Dropdown(MODEL_OPTIONS, value=MODEL_OPTIONS[0], label="Model")
        turns = gr.Slider(2, 10, value=5, step=1, label="Number of Turns (each turn = both speak once)")
    with gr.Accordion("Edit Prompts and Starting Lines", open=False):
        shopkeeper_prompt_box = gr.Textbox(value=shopkeeper_prompt, label="Shopkeeper Prompt", lines=6)
        player_prompt_box = gr.Textbox(value=player_prompt, label="Player Prompt", lines=6)
        shopkeeper_start_box = gr.Textbox(value=shopkeeper_start, label="Shopkeeper Start", lines=1)
        player_start_box = gr.Textbox(value=player_start, label="Player Start", lines=1)
    chatbot = gr.Chatbot(label="Negotiation Chat")
    
    run_btn = gr.Button("Run Negotiation")

    def reset_and_run(*args):
        # Always start fresh, ignore previous chat
        return gradio_run(*args)

    run_btn.click(
        fn=reset_and_run,
        inputs=[model, turns, shopkeeper_prompt_box, player_prompt_box, shopkeeper_start_box, player_start_box],
        outputs=chatbot,
        queue=False
    )
    chatbot.clear(fn=lambda: [], outputs=chatbot)

demo.launch()
