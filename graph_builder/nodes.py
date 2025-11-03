from med_agents.agents_med import intent_detection_agent
from med_agents.tools import intent_tools
from pydantic import BaseModel

class IntentState(BaseModel):
    user_id: str
    session_id: str
    query: str
    tool: list
    llm: object
    intent_result: str | None = None

def intent_node(state:IntentState):
    response=intent_detection_agent(state.query,intent_tools,state.user_id,state.session_id)
    return {"intent_result": response}


