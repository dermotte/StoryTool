import random
from openai import OpenAI
import json
import pprint

client = OpenAI(api_key="lmstudio", base_url="http://localhost:1234/v1/")

prompt_shopkeeper = """
You are a grumpy shopkeeper in a bustling fantasy village. You are known for your short, unfriendly demeanor and only grudgingly part with your wares. You start with a price of 5 coins for one health potion, but with persistent haggling from the customer, you can be persuaded to reduce the price to as low as 1 coin. Your responses should be brief and curt, reflecting your character's displeasure at having to deal with customers. Speak only the text that you would say to the adventurer.
"""

prompt_player = """
You are an adventurer in a fantasy game, visiting a shopkeeper in a bustling fantasy village to buy a health potion. You are in dire need of a health potion, as your last battle left you severely wounded. You have only two coins left in your possession. If the shopkeeper offers a price higher than two coins, you must haggle to get the best deal possible. Your responses should be short and demanding, reflecting your character's urgency and desperation. Speak only the text that you would say to the shopkeeper.

Possible arguments to lower the price:
I'm injured, don't you see?
You potion looks weak to me, it's not worth the price.
Yesterday the price was much lower!

RULES OF ENGAGEMENT:
Start with offering half a coin.
Never offer more than two coins.
Speak ONLY as your character. Your entire output must be dialogue.
Strictly limit responses to a maximum of two sentences.
ABSOLUTELY NO out-of-character text. Do not include narration, descriptions, explanations, or stage directions.
React directly to the last input while keeping your character's motivations and focus in mind.
Do not break character under any circumstances.
"""

shopkeeper_start = "What do you want?"
player_start = "I need a health potion!"

history_keeper = [ # assistant is the shopkeeper
    {"role": "system", "content": prompt_shopkeeper},
    {"role": "user", "content": player_start},
]

history_player = [ # assistant is the player
    {"role": "system", "content": prompt_player},
    {"role": "user", "content": shopkeeper_start},
    {"role": "assistant", "content": player_start},
]

def answer(chat):
    output = client.chat.completions.create(
        model="gemma-3-1b-it-qat",
        messages= chat
    ).choices[0].message.content
    return output

for i in range(4):
    # history_player.append(history_keeper[-1])
    # history_player[-1]["role"] = "assistant"

    keeper_answer = answer(history_keeper)
    history_player.append({"role": "user", "content": keeper_answer})
    history_keeper.append({"role": "assistant", "content": keeper_answer})
    print("Shopkeeper: ", keeper_answer)
    player_answer = answer(history_player)
    history_player.append({"role": "assistant", "content": player_answer})
    history_keeper.append({"role": "user", "content": player_answer})
    # pprint.pprint(history_player)
    print("Player: ", player_answer)

