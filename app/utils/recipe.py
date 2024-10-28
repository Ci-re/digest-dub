from datetime import datetime
import uuid
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
import numpy as np
from app.database.connect import dbconnect
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)  # Use a named logger

logging.basicConfig(level=logging.INFO)
RECIPE = "../../app/data/processed/recipe_cleaned.json"
INGREDIENTS = "../../app/data/processed/ingredients_AI.json"
MEAL = "../../app/data/processed/meal_cleaned.json"

CONN = dbconnect()
Session = sessionmaker(bind=CONN)
session = Session()

# Reflect existing tables
metadata = MetaData()
metadata.reflect(bind=CONN)

recipes_table = metadata.tables['Recipe']

def insert_data(data: List[Dict]):
    logger.info("DATABASE CONNECTION TRIGGERED")
    try:
        with CONN.connect() as conn:
            conn.execute(
                recipes_table.insert(),
                data
            )
            conn.commit()
            session.close()
            logger.info("PUSHED TO THE DATABASE")
    except Exception as e:
        logger.info(e)

def push_recipes_to_db():
    def prepare_json(path: str, columns: List[str]) -> List[Dict]:
        data = pd.read_json(path)
        data['created_at'] = datetime.now()
        data['updated_at'] = datetime.now()
        data['serial'] = np.arange(len(data))
        data.rename(columns={'cook time': 'cooking_time', 'servings': 'serving', 'recipe_id': 'id'}, inplace=True)
        data['serving'] = data['serving'].replace('', 0)
        data = data[columns]
        data_dict: List[Dict] = data.to_dict(orient='records')  # type: ignore
        return data_dict

    logger.info("PREPARING DATA")
    data = prepare_json(RECIPE, ["id", "serving", "cooking_time", "created_at", "updated_at", "serial"])
    # insert_data(data)

def push_meals_to_db():
    logger.info("PREPARING DATA")
    def prepare_json(path: str, columns: List[str]) -> List[Dict]:
           data = pd.read_json(path)
           data['created_at'] = datetime.now()
           data['updated_at'] = datetime.now()
           data['serial'] = np.arange(len(data))
           data['video_url'] = "NOT AVAILABLE"
           data.rename(columns={'meal_id': 'id'}, inplace=True)
           data = data[columns]
           data_dict: List[Dict] = data.to_dict(orient='records')  # type: ignore
           return data_dict

    data = prepare_json(MEAL, ["id", "name", "description", "serial", "status", "created_at", "updated_at", "video_url"])
    # insert_data(data)

def push_ingredients_to_db() -> None:
    logger.info("PREPARING DATA")
    data: pd.DataFrame = pd.read_json(INGREDIENTS)
    data = data.replace({np.nan: None, '': None, ' ': None})
    # Main Ingredients

    unique_ingredients = data[["main_ingredient"]].drop_duplicates()
    unique_ingredients["ingredientId"] = range(12, len(unique_ingredients) + 12)
    recipe_to_ingredients = data.merge(unique_ingredients, on="main_ingredient", how="left")

    # Alternative Ingredients
    alt_ingredient = data[["alternative_ingredient"]].drop_duplicates()
    alt_ingredient["alternative_ingredient"] = alt_ingredient[alt_ingredient["alternative_ingredient"] != None]
    alt_ingredient["alternativeOfId"] = range(1, len(alt_ingredient)+1)
    recipe_to_ingredients = recipe_to_ingredients.merge(alt_ingredient, on="alternative_ingredient", how="left")
    print(recipe_to_ingredients)

    # Measurements
    measurements = data[["measurement"]].drop_duplicates().reset_index(drop=True)
    measurements["measurementId"] = range(6, len(unique_ingredients) + 1)
    recipe_to_ingredients = data.merge(measurements, on="measurement", how="left")
    recipe_to_ingredients.drop(columns=['main_ingredient', "measurement", "alternative_ingredient"], inplace=True)
    print(recipe_to_ingredients)
    data_dict: List[Dict] = unique_ingredients.to_dict(orient='records')  # type: ignore


    # print(data)
    # insert_data(data)

if __name__ == "__main__":
    push_ingredients_to_db()
