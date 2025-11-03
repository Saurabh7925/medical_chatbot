from neo4j import GraphDatabase

from py2neo import Graph, Node, Relationship
import pandas as pd
graph = Graph("bolt://<server-ip>:7687", auth=("USERNAME", "<YOUR PASSWORD>"))
print(graph.run("RETURN 1").to_table())


graph.delete_all()


# --- Load your dataset ---
df = pd.read_csv("AyurGenixAI_Dataset.csv")


# --- Helper function to create nodes and relationships ---
def create_relationship(start_label, start_name, rel_type, end_label, end_name):
    start_node = Node(start_label, name=start_name)
    end_node = Node(end_label, name=end_name)
    rel = Relationship(start_node, rel_type, end_node)
    graph.merge(start_node, start_label, "name")
    graph.merge(end_node, end_label, "name")
    graph.merge(rel)


# --- Loop through dataset rows ---
for _, row in df.iterrows():
    disease = row['Disease']

    # Symptoms
    if pd.notna(row['Symptoms']):
        for symptom in str(row['Symptoms']).split(','):
            create_relationship("Disease", disease.strip(),
                                "HAS_SYMPTOM", "Symptom", symptom.strip())

    # Herbs
    if pd.notna(row['Ayurvedic Herbs']):
        for herb in str(row['Ayurvedic Herbs']).split(','):
            create_relationship("Disease", disease.strip(),
                                "TREATED_WITH", "Herb", herb.strip())

    # Formulation
    if pd.notna(row['Formulation']):
        for form in str(row['Formulation']).split(','):
            create_relationship("Disease", disease.strip(),
                                "USES_FORMULATION", "Formulation", form.strip())

    # Dosha
    if pd.notna(row['Doshas']):
        for dosha in str(row['Doshas']).split(','):
            create_relationship("Disease", disease.strip(),
                                "RELATED_DOSHA", "Dosha", dosha.strip())

    # Lifestyle
    if pd.notna(row['Occupation and Lifestyle']):
        for life in str(row['Occupation and Lifestyle']).split(','):
            create_relationship("Disease", disease.strip(),
                                "HAS_LIFESTYLE", "Lifestyle", life.strip())

    # Risk Factors
    if pd.notna(row['Risk Factors']):
        for risk in str(row['Risk Factors']).split(','):
            create_relationship("Disease", disease.strip(),
                                "HAS_RISK_FACTOR", "RiskFactor", risk.strip())

    # Recommendations
    if pd.notna(row['Diet and Lifestyle Recommendations']):
        for rec in str(row['Diet and Lifestyle Recommendations']).split(','):
            create_relationship("Disease", disease.strip(),
                                "HAS_RECOMMENDATION", "Recommendation", rec.strip())
