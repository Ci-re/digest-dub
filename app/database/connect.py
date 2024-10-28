from sqlalchemy import create_engine
from psycopg2 import DatabaseError
from sqlalchemy.engine.base import Engine
from app.database.config import load_config
# import logging


def dbconnect() -> Engine:
    """Connect to postgres server"""
    # logger = logging.getLogger(__name__)
    try:
        config = load_config()
        print("🔃 Connecting")
        conn = create_engine(url=f"postgresql+psycopg2://{config["user"]}:{config["password"]}@{config["host"]}/{config["database"]}")
        print("✅ Connected to pg server")
        return conn
    except (DatabaseError, Exception) as e:
        raise RuntimeError("❌ Failed to connect to the database") from e


# if __name__ == "__main__":
#     dbconnect(load_config())
