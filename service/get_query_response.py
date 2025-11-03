from call_llm.call_llm import chat_openai
# from Prompts.system_prompts import Prompts
import uuid
from graph_builder.graph import build_graph
# from call_llm.llm_call import chat_groq
from med_agents.tools import intent_tools


def query_response(query,session_id,user_id):
    user_prompt=f"""
    This is the query {query}
    """

    print("step inside getquery response",query,session_id)
    response=build_graph().invoke({
    "query": query,
    "tool": intent_tools,
    "user_id": user_id,
    "session_id":session_id,
    "llm": chat_openai() })

    print("eeeeeeeewewewewewewweewewew",str(response['intent_result']))
    message_sys_id = uuid.uuid4()
    result={"message":query,
            "message_sys_id":str(message_sys_id),
            "response":str(response['intent_result']),
            "role":"system",
            "session_id":session_id,
            "document_id":None}

    return result