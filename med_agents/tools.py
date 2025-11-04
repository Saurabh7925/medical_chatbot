from langchain.tools import tool
from db.qdrant_connection import client
from service.generate_cql_query.cql_generator import retrieval_data_from_kg,fetch_from_neo4j
from service.vector_db_search.vector_search import retrieve_relevant_chunks, generate_response_from_llm
from service.hybrid_search.kg_vector_search import generate_hybrid_search

import json



@tool(
    name_or_callable="query_knowladge_graph_tool",
    description=""" Generates a Cypher Query Language (CQL) query to retrieve structured information 
    from the Neo4j Knowledge Graph. 
    Use this tool when the user's query involves **specific Ayurvedic relationships or entities**, 
    such as herbs, diseases, doshas, treatments, or symptoms. 
    This includes questions where the user asks for *what, which, or how* type facts 
    directly related to Ayurvedic knowledge connections."""
)
def query_knowladge_graph_tool(query: str) -> str:

    cql_query = retrieval_data_from_kg(query)
    response=fetch_from_neo4j(cql_query['cql_query'])
    result = {
        "tool": "query_knowladge_graph_tool",
        "input": query,
        "output": cql_query,
        "result": response
    }
    return json.dumps(result, indent=2)

@tool(
    name_or_callable="query_vector_db_tool",
    description= """Retrieves relevant contextual information from the **user’s stored knowledge base or uploaded documents** 
    using semantic vector search (Qdrant). 
    Use this tool when the query asks about **conceptual explanations, theories, or textual insights** 
    that come from documents such as PDFs, Excel files, or notes — not from structured graph relationships. """

)
def query_vector_db_tool(query: str) -> str:
    """Detect document type mentioned in a user's query."""
    try:
        collection_name = "1234" + "_" + "abcde345"
        collections_response = client.get_collections()
        all_collection_names = [c.name for c in collections_response.collections]
        if collection_name not in all_collection_names:
            return "collection name not found"
        relevent_chunks=retrieve_relevant_chunks(query,collection_name)
        response=generate_response_from_llm(query,relevent_chunks)
        result = {
            "tool": "query_vector_db_tool",
            "input": query,
            "output": response
        }
        return json.dumps(result, indent=2)
    except Exception as e:
        return str(e)



@tool(
    name_or_callable="hybrid_retrival_tool",
    description="""Combines **Knowledge Graph reasoning** and **Vector-based retrieval** to generate 
    comprehensive answers that integrate both **traditional Ayurvedic knowledge** 
    and **modern scientific context**.
    Use this tool when the query requires **both structured relationships (from KG)** 
    and **textual explanations or scientific references (from Vector DB)**."""
)
def hybrid_retrival_tool(query: str)->str:
    try:
        collection_name = "1234" + "_" + "abcde345"
        collections_response = client.get_collections()
        all_collection_names = [c.name for c in collections_response.collections]
        if collection_name not in all_collection_names:
            return "collection name not found"
        cql_query = retrieval_data_from_kg(query)
        relevent_chunks = retrieve_relevant_chunks(query, collection_name)
        cql_query_result=fetch_from_neo4j(cql_query)
        hybrid_result=generate_hybrid_search(cql_query_result,relevent_chunks,cql_query_result)
        result={
            "tool": "query_vector_db_tool",
            "input": query,
            "cql_query_result":cql_query_result,
            "output": hybrid_result
        }

        return json.dumps(result, indent=2)
    except Exception as e:
        return str(e)

#
# @tool(
#     name_or_callable="general_purpose_tool",
#     description=""
# )
# def general_purpose_tool(query:str)->str:
#     """General reasoning using LLM without retrieval."""
#     return llm.invoke(query)


intent_tools=[query_knowladge_graph_tool,query_vector_db_tool,hybrid_retrival_tool]
