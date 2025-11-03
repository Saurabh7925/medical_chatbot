import json
from call_llm.call_llm import execute_llm
from db.connection import Neo4jConnector

def retrieval_data_from_kg(user_query):


    system_prompt=f"""
            You are a specialized Cypher generator for an Ayurveda knowledge graph stored in Neo4j.
            Given a user natural-language query, produce a safe, parameterized Cypher query that retrieves the requested structured information.
            
            REQUIREMENTS (must follow exactly):
            2. Always use parameterized queries (e.g., WHERE d.name = $disease_name). Do not insert raw user text into the query.
            3. Limit results when appropriate (use `LIMIT $limit`), and include ORDER BY when returning ranked results.
            4. Return nodes and relationships (e.g., `RETURN d, r, h`) or projection fields (e.g., `RETURN d.name AS disease, collect(h.name) AS herbs`), depending on the query.
            5. If the user asks to "count" or "aggregate", produce the correct aggregation Cypher (COUNT, collect, etc.).
            6. If the query is ambiguous (multiple possible intents), produce two candidate Cypher queries labelled as "cypher_candidates" (array of objects) with short explanations; otherwise produce a single cypher in the "cypher" field.
            7. If a step needs additional clarification that would change the Cypher (e.g., which entity to use), do not ask the user; instead produce reasonable defaults and note the assumption in the "explanation".
            8. Protect against injection: map potentially multi-valued inputs by splitting in application code; here use parameters only.
            
            INPUT:
            {user_query}
            
            FEW-SHOT EXAMPLES:
            # Example 1
            NL: "Find all herbs that are used to treat Diabetes."
            JSON:
            {{
              "cql_query": "MATCH (d:Disease {{name: $disease_name}})-[:TREATED_WITH]->(h:Herb) RETURN d.name AS disease, collect(h.name) AS herbs LIMIT $limit",
              "explanation": "Fetches the disease node for Diabetes and collects names of herbs connected by TREATED_WITH."
            }}
            
            NL: "List diseases associated with Kapha dosha."
            JSON:
            {{
              "cql_query": "MATCH (d:Disease)-[:RELATED_DOSHA]->(dosha:Dosha {{name: $dosha_name}}) RETURN collect(d.name) AS diseases LIMIT $limit",
              "explanation": "Finds diseases linked to the specified Dosha node (Kapha) and returns their names."
            }}
                        
            # Example 3
            NL: "Show symptoms and their severity for Arthritis."
            JSON:
            {{
              "cql_query": "MATCH (d:Disease {{name: $disease_name}})-[:HAS_SYMPTOM]->(s:Symptom) RETURN s.name AS symptom, s.severity AS severity ORDER BY s.severity DESC LIMIT $limit",
              "explanation": "Fetches symptoms linked to Arthritis and returns symptom names and their severity, ordered by severity."
            }}
            
            
            Output should be in JSON format Only :
                   {{
                      cql_query:<generated cql query>,
                      explanation:<query explanation> 
                   }}     
            """
    user_prompt=f"""This is query: {user_query}"""

    try:

        response=execute_llm(sysprompt=system_prompt, userprompt=user_prompt)
        result=json.loads(response)
        return result
    except Exception as e:
        print("Could not generate CQL query by LLM\n" )
        return {"error": str(e)}


def fetch_from_neo4j(cql_query):
    conn=Neo4jConnector()
    response=conn.run_cql_query(cql_query)
    return response


if __name__ == "__main__":
    query="Which dosha is imbalanced in insomnia?"
    response=retrieval_data_from_kg(query)
    print(response)


