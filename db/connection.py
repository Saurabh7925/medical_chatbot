import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()




class Neo4jConnector:
    def __init__(self):
        uri = os.getenv("NEO4J_URI")
        username = os.getenv("NEO4J_USERNAME")
        password = os.getenv("NEO4J_PASSWORD")

        self.driver = GraphDatabase.driver(uri, auth=(username, password))
    def close(self):
        self.driver.close()

    def run_cql_query(self, cql_query: str):
        """
        Executes a CQL (Cypher) query and returns the results.
        """
        try:
            with self.driver.session() as session:
                result = session.run(cql_query)
                records = [record.data() for record in result]
                return {
                    "status": "success",
                    "records": records,
                    "count": len(records)
                }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

def get_connector():
    """ database connection creds """
    connect_url = sqlalchemy.engine.URL.create(drivername='postgresql+psycopg2',
                                               username=os.getenv("DB_USERNAME"),
                                               password=os.getenv("DB_PASSWORD"),
                                               host=os.getenv("DB_HOST"),
                                               port=os.getenv("DB_PORT"),
                                               database=os.getenv("DB_SCHEMA")
                                               )
    return connect_url


engine = sqlalchemy.create_engine(
    get_connector(),
    pool_size=10,
    max_overflow=2,
    pool_recycle=300,
    pool_pre_ping=True,
    pool_use_lifo=True,
    future=True,
    echo=False
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



