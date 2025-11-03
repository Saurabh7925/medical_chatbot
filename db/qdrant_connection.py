import os
from qdrant_client import QdrantClient



base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
storage_path = os.path.join(base_dir, "qdrant_storage")

# Ensure the directory exists
os.makedirs(storage_path, exist_ok=True)
client = QdrantClient(path=storage_path)