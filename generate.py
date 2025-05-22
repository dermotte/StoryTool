import random
from openai import OpenAI
import json
import pprint

# Define available models
MODEL_OPTIONS = [
    "gemma-3-1b-it-qat",
    "gemma-3-4b-it-qat",
    "llama-3.2-3b-instruct",
    "granite-3.3-8b-instruct",
    "qwen2.5-7b-instruct",
    "qwen3-4b",
    "deepseek-r1-distill-qwen-1.5b",
]

model_id = 0

client = OpenAI(api_key="lmstudio", base_url="http://localhost:1234/v1/")

prompt_shopkeeper = """You are a grumpy shopkeeper in a bustling fantasy village. You are known for your short, unfriendly demeanor and only grudgingly part with your wares. You start with a price of 5 coins for one health potion, but with persistent haggling from the customer, you can be persuaded to reduce the price to as low as one coin. Your responses should be brief and curt, reflecting your character's displeasure at having to deal with customers. Speak only the text that you would say to the adventurer.

Possible arguments not to lower the price:
You need to pay a fair price for a quality potion.
This is not a charity.
Do I look like I support the idea of a clearance sale?

RULES OF ENGAGEMENT:
Never offer less than one and a half coins.
If the player agrees on a price, then close the deal.
Speak ONLY as your character. Your entire output must be dialogue.
Strictly limit responses to a maximum of two sentences.
ABSOLUTELY NO out-of-character text. Do not include narration, actions, emotions, descriptions, explanations, or stage directions.
React directly to the last input while keeping your character's motivations and focus in mind.
Do not break character under any circumstances.
"""

prompt_player = """You are an adventurer in a fantasy game, visiting a shopkeeper in a bustling fantasy village to buy a health potion. You are in desperate need of a health potion, as your last battle left you severely wounded. You have only two coins left in your possession. If the shopkeeper offers a price higher than two coins, you must haggle to get the best deal possible. you can also offer half and quarter coins. Your responses should be short and demanding, reflecting your character's urgency and desperation. Speak only the text that you would say to the shopkeeper.

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

def reset_history(prompt_shopkeeper, prompt_player, shopkeeper_start, player_start):
    history_keeper = [ # assistant is the shopkeeper
        {"role": "system", "content": prompt_shopkeeper},
        {"role": "user", "content": player_start},
    ]

    history_player = [ # assistant is the player
        {"role": "system", "content": prompt_player},
        {"role": "user", "content": shopkeeper_start},
        {"role": "assistant", "content": player_start},
    ]
    return history_keeper,history_player


def answer(chat, model):
    output = client.chat.completions.create(
        model=model, # Change this to the desired model
        temperature=0.7,
        # max_tokens=100,
        presence_penalty=1,
        messages= chat
    ).choices[0].message.content
    if "</think>" in output:
        output = output.split("</think>", 1)[-1]
    return output.strip()

for m in range(len(MODEL_OPTIONS)):
    history_keeper, history_player = reset_history(prompt_shopkeeper, prompt_player, shopkeeper_start, player_start)

    print("\n## LLM model: ", MODEL_OPTIONS[m])
    print("*Shopkeeper*: ", shopkeeper_start)
    print("*Player*: ", player_start)

    for i in range(4):
        keeper_answer = answer(history_keeper, MODEL_OPTIONS[m])
        history_player.append({"role": "user", "content": keeper_answer})
        history_keeper.append({"role": "assistant", "content": keeper_answer})
        print("*Shopkeeper*: ", keeper_answer)
        player_answer = answer(history_player, MODEL_OPTIONS[m])
        history_player.append({"role": "assistant", "content": player_answer})
        history_keeper.append({"role": "user", "content": player_answer})
        print("*Player*: ", player_answer)
