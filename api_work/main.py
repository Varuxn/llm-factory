import openai
import sys

api_key = "EMPTY"

with open("URL.txt", "r", encoding="utf-8") as file:
    api_base = file.read()
openai.api_base = api_base + "/v1"


def chat_with_gpt3_5(messages):
    response = openai.ChatCompletion.create(
        model="xxx",
        messages=messages,
        api_key=api_key,
        stream=True  # 启用流式输出
    )

    full_response = ""
    for chunk in response:
        if 'choices' in chunk and len(chunk['choices']) > 0:
            content = chunk['choices'][0].get('delta', {}).get('content', '')
            if content:
                print(content, end='', flush=True)
                full_response += content
    print() 
    return full_response

conversation = [
    {"role": "system", "content": "你是一个聪明的AI"}
]

while True:

    user_input = input("You: ")

    if user_input.lower() == '退出':
        print("Assistant: 再见！")
        break

    conversation.append({"role": "user", "content": user_input})

    print("Assistant: ", end='', flush=True)
    assistant_message = chat_with_gpt3_5(conversation)

    conversation.append({"role": "assistant", "content": assistant_message})


