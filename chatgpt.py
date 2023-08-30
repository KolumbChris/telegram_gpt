
import openai
from key import ekey

ekey

# openai.api_key = 'Your OpenAi token'


def request_chat_gpt(user_message):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return completion.choices[0].message['content']
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""  # Return an empty string or handle the error appropriately
