from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from med_agents.tools import intent_tools
from call_llm.call_llm import chat_openai
import json
def intent_detection_agent(query,tool):
    prompt="""You are an intelligent assistant that classifies user queries into specific intents.   
    You have access to the following tools:
    {tools}
    Use this format:
    Final Answer (in JSON):
       {
          "tool_used": "<tool_name>",
          "detected_intent": "<intent_name>",
          "action_input": "<user_query>",
          "observation": "<tool_output>",
          "reasoning": [
            "<thought_1>",
            "<thought_2>"
          ]
        }

    Question: {input}
    {agent_scratchpad}"""

    llm=chat_openai()
    agent = create_agent(llm, tool, system_prompt=prompt)

    response = agent.invoke({
        "input": query
    })

    message=response["messages"][-1].content
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
