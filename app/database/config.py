
from neo4j import GraphDatabase
from dotenv import load_dotenv
from neo4j import GraphDatabase
import os

load_dotenv(os.getenv("../../.env.dev"))

username = os.environ["NEO4J__USERNAME"]
password = os.environ["NEO4J__PASSWORD"]

PATH = "../../"

URI = "http://localhost:7474/"
driver = GraphDatabase.driver(uri=URI, auth=(username, password))

def index_graph_db_from_postgres():
    with driver.session() as session:
        with open("../../queries_to_load_db.cypher", "r") as cypher_file:
            cypher_query = cypher_file.read()
            result = session.run(query=cypher_query)
            for record in result:
                print(record)
            
    

