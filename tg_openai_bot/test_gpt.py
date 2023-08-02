import openai

openai.api_key = "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"
model = "gpt-3.5-turbo"

messages = []

while True:
    content = input('Текст: ')
    messages.append({"role": "user", "content": content})
    completion = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    response_content = completion.choices[0].message.content
    print(f'ChatGPT: {response_content}')
    messages.append({"role": "assistant", "content": response_content})
