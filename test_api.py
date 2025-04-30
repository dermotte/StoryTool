from openai import OpenAI

client = OpenAI(api_key="lmstudio", base_url="http://localhost:1234/v1/")

history = []
output = client.chat.completions.create(
    model="gemma-3-1b-it-qat",
    messages=[
        {"role": "system", "content": "You are a helpful AI assistant"},
        {"role": "user", "content": "What is the biggest town in Austria?"},
    ],  # type: ignore
).choices[0].message.content

print(output)
