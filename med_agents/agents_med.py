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



response = {
    "messages": [
        HumanMessage(
            content="Human: You are an intelligent assistant that classifies user queries into specific intents.\n    You have access to the tool\n\n    Question: What herbs help with diabetes?",
            additional_kwargs={},
            response_metadata={},
            id="a7a4f799-4210-4223-8051-b8b30aa9ea76",
        ),
        "AIMessage"(
            content="",
            additional_kwargs={"refusal": None},
            response_metadata={
                "token_usage": {
                    "completion_tokens": 608,
                    "prompt_tokens": 406,
                    "total_tokens": 1014,
                    "completion_tokens_details": {
                        "accepted_prediction_tokens": 0,
                        "audio_tokens": 0,
                        "reasoning_tokens": 576,
                        "rejected_prediction_tokens": 0,
                    },
                    "prompt_tokens_details": {"audio_tokens": 0, "cached_tokens": 0},
                },
                "model_provider": "openai",
                "model_name": "gpt-5-2025-08-07",
                "system_fingerprint": None,
                "id": "chatcmpl-CYW9iJeFX1heV4Bcx8PAI92a19yVD",
                "service_tier": "default",
                "finish_reason": "tool_calls",
                "logprobs": None,
            },
            id="lc_run--bf193981-f1b0-44c7-b067-679371a74281-0",
            tool_calls=[
                {
                    "name": "query_knowladge_graph_tool",
                    "args": {"query": "What herbs help with diabetes?"},
                    "id": "call_BSLYV2ch3cKLlxq02MY5FrRD",
                    "type": "tool_call",
                }
            ],
            usage_metadata={
                "input_tokens": 406,
                "output_tokens": 608,
                "total_tokens": 1014,
                "input_token_details": {"audio": 0, "cache_read": 0},
                "output_token_details": {"audio": 0, "reasoning": 576},
            },
        ),
        "ToolMessage"(
            content='{\n  "tool": "query_knowladge_graph_tool",\n  "input": "What herbs help with diabetes?",\n  "output": {\n    "cql_query": "MATCH (d:Disease {name: \'Diabetes\'})-[:TREATED_WITH]->(h:Herb) RETURN DISTINCT h.name AS herb_name",\n    "explanation": "Fetches the disease node for Diabetes and collects names of herbs connected by TREATED_WITH."\n  },\n  "result": {\n    "status": "error",\n    "message": "Couldn\'t connect to localhost:7687 (resolved to (\'127.0.0.1:7687\',)):\\nFailed to establish connection to ResolvedIPv4Address((\'127.0.0.1\', 7687)) (reason [Errno 111] Connection refused)"\n  }\n}',
            name="query_knowladge_graph_tool",
            id="00dbe637-166a-4a0e-a7e6-8f145a396120",
            tool_call_id="call_BSLYV2ch3cKLlxq02MY5FrRD",
        ),
        "AIMessage"(
            content="knowledge_graph",
            additional_kwargs={"refusal": None},
            response_metadata={
                "token_usage": {
                    "completion_tokens": 651,
                    "prompt_tokens": 620,
                    "total_tokens": 1271,
                    "completion_tokens_details": {
                        "accepted_prediction_tokens": 0,
                        "audio_tokens": 0,
                        "reasoning_tokens": 640,
                        "rejected_prediction_tokens": 0,
                    },
                    "prompt_tokens_details": {"audio_tokens": 0, "cached_tokens": 0},
                },
                "model_provider": "openai",
                "model_name": "gpt-5-2025-08-07",
                "system_fingerprint": None,
                "id": "chatcmpl-CYW9xR1hQQSLqbPWIfoW8EiH3bxhw",
                "service_tier": "default",
                "finish_reason": "stop",
                "logprobs": None,
            },
            id="lc_run--3e639a57-8864-4a07-9303-fcc3e8b1f8b2-0",
            usage_metadata={
                "input_tokens": 620,
                "output_tokens": 651,
                "total_tokens": 1271,
                "input_token_details": {"audio": 0, "cache_read": 0},
                "output_token_details": {"audio": 0, "reasoning": 640},
            },
        ),
    ]
}
