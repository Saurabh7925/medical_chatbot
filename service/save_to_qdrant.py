from db.qdrant_connection import client
from qdrant_client.models import PointStruct, VectorParams, Distance
import uuid
import os


def save_to_qdrant(chunks, embeddings, collection_name, recreate=False ):


    if recreate and client.collection_exists(collection_name=collection_name):
        client.delete_collection(collection_name=collection_name)

    if not client.collection_exists(collection_name=collection_name):
        vector_size = len(embeddings[0])
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )
        print(f"Created collection '{collection_name}' with vector size {vector_size}.")
    else:
        print(f"Collection '{collection_name}' already exists — will upsert (append) points.")


    points = []
    for i, chunk in enumerate(chunks):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embeddings[i].tolist() if hasattr(embeddings[i], "tolist") else embeddings[i],
                payload={"text": chunk}
            )
        )


        if len(points) >= 256:
            client.upsert(collection_name=collection_name, points=points)
            points = []


    if points:
        client.upsert(collection_name=collection_name, points=points)

    print(f"✅ Stored {len(chunks)} chunks into local Qdrant collection: '{collection_name}'")
    return client


