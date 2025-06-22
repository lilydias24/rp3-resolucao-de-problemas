import os

from groq import Groq
from dotenv import load_dotenv
load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
def LLM(content):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        model="llama-3.3-70b-versatile",
        stream=False,
    )
    print(chat_completion.choices[0].message.content)




