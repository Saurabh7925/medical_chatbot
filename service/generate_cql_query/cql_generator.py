import json
from call_llm.call_llm import execute_llm
from db.connection import Neo4jConnector

def retrieval_data_from_kg(user_query):


    system_prompt=f"""
        You are a specialized Cypher (CQL) query generator for an Ayurveda Knowledge Graph stored in Neo4j.
        Your task is to translate natural language questions into safe, parameterized Cypher queries that accurately retrieve structured Ayurvedic information.
        The graph schema includes the following:
        Node Labels: Disease, Symptom, Herb, Formulation, Dosha, Treatment, Recommendation, RiskFactor, Lifestyle  
        Relationship Types: HAS_SYMPTOM, TREATED_WITH, USES_FORMULATION, RELATED_DOSHA, RECOMMENDED_TREATMENT, HAS_RECOMMENDATION, 

            INPUT:
            {user_query}
            
            FEW-SHOT EXAMPLES:
            # Example 1
            NL: "What herbs help with diabetes?"
            JSON:
            {{
              "cql_query": "MATCH (d:Disease {{name: "Diabetes"}})-[:TREATED_WITH]->(h:Herb)RETURN DISTINCT h.name AS herb_name",
              "explanation": "Fetches the disease node for Diabetes and collects names of herbs connected by TREATED_WITH."
            }}
            
            NL: "List diseases associated with Kapha dosha."
            JSON:
            {{
              "cql_query": "MATCH (do:Dosha {{name: "Kapha"}})-[:RELATED_DOSHA]->(d:Disease) RETURN DISTINCT d.name AS disease_name",
              "explanation": "Finds diseases linked to the specified Dosha node (Kapha) and returns their names."
            }}
                        
            # Example 3
            NL: "Show symptoms and their severity for Arthritis."
            JSON:
            {{
              "cql_query": "MATCH (d:Disease {{name: "Arthritis"}})-[:HAS_SYMPTOM]->(s:Symptom)RETURN DISTINCT s.name AS symptom_name, s.severity AS severity
",
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
        print(result)
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
    query="""MATCH (d:Disease {name: "Insomnia"})-[:RELATED_DOSHA]->(do:Dosha) RETURN DISTINCT do.name AS dosha_name """
    res=fetch_from_neo4j(response['cql_query'])
    print(res)


