import json
from call_llm.call_llm import execute_llm

def generate_hybrid_search(cql_response,relevent_chunk,cql_query):
    system_prompt=f"""
            You are given:
            1. A user query: {{query}}
            2. The response from a CQL (Cypher) query executed on a knowledge graph: {{cql_query_response}}
            3. Several relevant text chunks retrieved from a vector knowledge base: {{retrieved_chunks}}
            
            Your task:
            - Generate a clear, accurate, and concise answer using only the information present in the provided chunks and the CQL query response.
            - If the complete answer cannot be determined solely from these sources, acknowledge that explicitly and respond based on the closest relevant information.
            - Do not invent or assume facts that are not supported by the provided data.
            
            
            
             Output should be in JSON format Only :
                   {{
                      response:<generated combine result>,
                   }}     

            """

    user_prompt=f"""This is relevent chunks :{relevent_chunk}, cql_query_response: {cql_response}, cql_query:{cql_query}"""

    try:

        response = execute_llm(sysprompt=system_prompt, userprompt=user_prompt)
        result = json.loads(response)
        return result
    except Exception as e:
        print("Could not generate CQL query by LLM\n")
        return {"error": str(e)}