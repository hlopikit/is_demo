import openai

openai.api_key = "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"
model = "gpt-3.5-turbo"

text = "Tell me about best lib for machine learning in Python"
messages = []

while True:
    content = input()
    messages.append({"role": "user", "content": content})
    completion = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    response_content = completion.choices[0].message.content
    print(f'ChatGPT: {response_content}')
    messages.append({"role": "assistant", "content": response_content})
