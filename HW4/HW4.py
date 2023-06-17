import openai

openai.api_key = 'YOUR_API_KEY'

def chat_with_openai(message):
    response = openai.Completion.create(
        engine='davinci',
        prompt=message,
        max_tokens=100,
        temperature=0.6,
        n=1,
        stop=None,
        timeout=5
    )

    reply = response.choices[0].text.strip()
    return reply

def main():
    print("歡迎使用聊天機器人！請輸入您的訊息（輸入'結束'以退出）。")
    user_message = input("> ")

    while user_message.lower() != '結束':
        reply = chat_with_openai(user_message)
        print("機器人回覆：", reply)
        user_message = input("> ")

    print("感謝您使用聊天機器人！")

if __name__ == '__main__':
    main()
