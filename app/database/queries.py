import logging
from typing import Dict, List
from sqlalchemy import MetaData
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from app.database.connect import dbconnect

logger = logging.getLogger(__name__)  # Use a named logger
CONN = dbconnect()
Session = sessionmaker(bind=CONN)
session = Session()

# Reflect existing tables
metadata = MetaData()
metadata.reflect(bind=CONN)

def insert_data(data: List[Dict], schema: str) -> None:
    _table = metadata.tables[schema]
    logger.info("DATABASE CONNECTION TRIGGERED")
    try:
        with CONN.connect() as conn:
            _extracted_from_insert_data_6(conn, _table, data)
    except Exception as e:
        logger.info(e)

# TODO Rename this here and in `insert_data`
def _extracted_from_insert_data_6(conn, _table, data):
    # conn.execute(text("SET session_replication_role = 'replica';"))
    conn.execute(
        _table.insert(),
        data
    )
    # conn.execute(text("SET session_replication_role = 'origin';"))
    conn.commit()
    session.close()
    logger.info("PUSHED TO THE DATABASE")