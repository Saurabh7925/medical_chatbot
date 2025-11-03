from langchain_openai import ChatOpenAI
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


token = os.getenv("OPENAI_API_KEY")
client=OpenAI(api_key=token)
def chat_openai():
    llm = ChatOpenAI(
        model=os.getenv("MODEL"),  # or gpt-4o, gpt-3.5-turbo
        temperature=0
    )
    return llm


def execute_llm(sysprompt, userprompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "system",
            "content": f"""{sysprompt}"""},

            {
                "role": "user",
                "content": f"""{userprompt}"""
            }

        ],
        max_tokens=100
    )

    return response.choices[0].message.content


