from langgraph.graph import StateGraph, END
from graph_builder.nodes import intent_node,IntentState





def build_graph():
    graph = StateGraph(IntentState)
    graph.add_node("Intent classifier",intent_node )
    graph.set_entry_point("Intent classifier")
    graph.add_edge("Intent classifier", END)
    return graph.compile()