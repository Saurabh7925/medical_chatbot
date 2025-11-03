# 🩺 Ayurvedic RAG Chatbot — Hybrid Retrieval System

This project implements a **Retrieval-Augmented Generation (RAG)** chatbot that combines:
- **Vector Database (Qdrant)** for contextual text retrieval, and  
- **Knowledge Graph (Neo4j)** for structured Ayurvedic relationships.

It supports intelligent query classification and **hybrid knowledge retrieval** for both **traditional Ayurvedic** and **modern scientific** insights.

---

## 🏗️ **Architecture**

The system implements a **multi-agent hybrid retrieval architecture** combining **Vector Search (RAG)** and **Knowledge Graph (CQL)** to answer Ayurvedic and scientific queries intelligently.

### **Workspaces**

- **Knowledge Graph Workspace:**  
  Handles structured Ayurvedic relationships such as *doshas, herbs, diseases, and treatments* using **Neo4j** and **CQL queries**.

- **Vector Retrieval Workspace:**  
  Manages semantic search over unstructured text (research papers, PDF content) using **Qdrant** and **BAAI/bge-large-en embeddings**.

- **Hybrid Workspace:**  
  Integrates both Knowledge Graph and Vector Retrieval outputs to provide holistic answers that blend **traditional Ayurvedic** and **modern scientific** perspectives.

---

### **Agent Pipeline**

- **Intent Agent:**  
  Classifies the user query and routes it to the appropriate workspace (Knowledge Graph, Vector DB, or Hybrid).

- **Vector Retrieval Agent:**  
  Fetches relevant contextual chunks from **Qdrant** using dense vector embeddings.

- **Knowledge Graph Agent:**  
  Generates **CQL queries** to extract structured Ayurvedic relationships (e.g., herb–disease–dosha links).

- **Hybrid Retrieval Agent:**  
  Merges results from both the Vector DB and Knowledge Graph to synthesize comprehensive answers.

- **Response Generation Agent:**  
  Uses the **LLM (OpenAI/Groq)** with a domain-specific **system prompt** to generate the final, grounded Ayurvedic response.

---

### **Components**

- **LangChain Agent Orchestration:**  
  Manages multi-agent workflows, tool execution, and reasoning across the hybrid pipeline.

- **Qdrant (Local Mode):**  
  Vector database storing embeddings for all uploaded documents (PDFs, text data).

- **Neo4j Database:**  
  Graph database storing structured Ayurvedic knowledge and entity relationships.

- **SentenceTransformer (BAAI/bge-large-en):**  
  Generates high-dimensional embeddings for document chunks and queries.

- **FastAPI:**  
  Provides REST API endpoints for document upload, retrieval, and query execution.

- **Python Backend:**  
  Orchestrates text extraction, chunking, embedding, and agent execution.

---

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.11+
- Neo4j Community Edition
- Qdrant (Local Storage Mode)
- OpenAI or Groq API Key

---

### **1️⃣ Clone and Setup**
```bash
git clone <repository-url>
cd medical_chatbot
```

### **2️⃣ Environment Configuration

```bash
# 🔑 LLM / API Keys
OPENAI_API_KEY=your_api_key_here

# 🧬 Neo4j Database
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password

# 💾 SQL / Metadata Database
DB_DRIVER=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_SCHEMA=medical_db
DB_USERNAME=your_username
DB_PASSWORD=your_password
```





