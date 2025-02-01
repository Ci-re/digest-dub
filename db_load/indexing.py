from dotenv import load_dotenv
from neo4j import AsyncGraphDatabase
import os
from queries import queries_to_add_nodes, queries_to_add_relationships, index_queries
from typing import List
import time
import sys
from neo4j.debug import watch
import asyncio

# Loggings
watch("neo4j", out=sys.stdout)

# Get environment variables
load_dotenv(dotenv_path=".env.dev")
DB_USER = os.environ["DB__USER"]
DB_PASSWORD = os.environ["DB__PASSWORD"]
DB_HOST = os.environ["DB__HOST"]
DB_PORT = os.environ["DB__PORT"]
DB_NAME = os.environ["DB__NAME"]
url = os.environ["NEO4J__URL"]
AUTH = (os.environ["NEO4J__USERNAME"], os.environ["NEO4J__PASSWORD"])
JDBC_URL = f"jdbc:postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

driver = AsyncGraphDatabase.driver(uri=url, auth=AUTH)


async def create_data(q):
    async def create_node_and_relationships(tx, queries: List[str], params: dict):    
        for query in queries:
            await tx.run(query, **params)

    async with AsyncGraphDatabase.driver(uri=url, auth=AUTH) as driver:
        async with driver.session() as session:
            params ={
                "jdbc_url":JDBC_URL
            }
            await session.execute_write(create_node_and_relationships, q, params)

async def index_data():
    

if __name__ == "__main__":
    asyncio.run(create_data(q=queries_to_add_nodes))
    time.sleep(3)
    asyncio.run(create_data(q=queries_to_add_relationships))