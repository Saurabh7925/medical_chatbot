import os
import json
from db.qdrant_connection import client
from sentence_transformers import SentenceTransformer
from call_llm.call_llm import execute_llm
def retrieve_relevant_chunks(query,collection_name,top_k=5):

    model = SentenceTransformer("BAAI/bge-large-en", device="cpu")

    query_emb = model.encode(
        f"Represent this sentence for retrieval: {query}",
        normalize_embeddings=True
    )

    search_results = client.search(
        collection_name=collection_name,
        query_vector=query_emb,
        limit=top_k,
    )

    results = [
        {
            "score": round(result.score, 4),
            "text": result.payload.get("text", "")
        }
        for result in search_results
    ]

    print(f"🔍 Found {len(results)} relevant chunks for query: '{query}'")
    return results



def generate_response_from_llm(query,retrieved_chunks):
    system_prompt=f"""
            You are an intelligent assistant specialized in Ayurveda and holistic medicine. 
            You are given a user query and several relevant text chunks retrieved from a knowledge base. 
            Your task is to generate a clear, accurate, and concise answer using only the information present in the provided chunks. 
            If the answer cannot be fully determined from the chunks, acknowledge that and respond based on the closest relevant information, 
            without adding unsupported assumptions or external facts.
            
            Use a professional yet accessible tone suitable for explaining Ayurvedic concepts to both technical and non-technical users. 
            Cite or reference specific ideas from the chunks naturally when relevant.
            
            
            User Query: {query}
            Relevant Chunks:
            {retrieved_chunks}
         
    """

    user_prompt = f"""This is query: {query}"""

    try:
        response=execute_llm(sysprompt=system_prompt, userprompt=user_prompt)
        result=json.loads(response)
        return result
    except Exception as e:
        print("Could not generate CQL query by LLM\n" )
        return {"error": str(e)}






if __name__ == "__main__":
    query = "How can interdisciplinary research improve Ayurvedic medicine?"
    collection_name = "672bafa0-6db9-4395-854c-afa5ea23f2ea_new123456789"
    response=retrieve_relevant_chunks(query,collection_name)
    print(response)

