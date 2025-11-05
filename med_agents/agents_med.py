from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain.messages import HumanMessage, AIMessage, ToolMessage

from med_agents.tools import intent_tools
from call_llm.call_llm import chat_openai
import json


def intent_detection_agent(query, tool):
    prompt = ChatPromptTemplate.from_template(
    """You are an intelligent assistant that classifies user queries into specific intents.
    You have access to the tool

    Question: {input}""")

    llm = chat_openai()

    prompt = prompt.format(input=query)
    agent = create_agent(llm, tool)
    response = agent.invoke({"messages": prompt})
    print( f"{response  =}")

    message = response["messages"][-1].content
    print("Query 1 response:eeeeeeeee", message)
    if "Final Answer" in message:
        message = message.split("Final Answer (in JSON):")[-1].strip()
    try:
        result = json.loads(message)

        return result["observation"]
    except json.JSONDecodeError:
        print("⚠️ Could not parse JSON content.")
        print("Raw message:", message)


if __name__ == "__main__":
    query1 = "What herbs help with diabetes?"
    result = intent_detection_agent(query1, intent_tools)

