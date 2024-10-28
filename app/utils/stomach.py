import pickle
from pandas import DataFrame
import json
import os

def save_model_weights(model: DataFrame) -> None:
    if model is not None:
        try:
            with open("app/word_embeddings_01.pkl", 'wb') as file:
                pickle.dump(model, file)
        except Exception as e:
            print(e)

def get_model_weights() -> DataFrame:
    with open("app/weights/word_embeddings_01.pkl",'rb') as file:
        data = pickle.load(file)
    return data

def save_json(file, data):
    file_path = f"../../app/data/processed/{file}.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            existing_data = json.load(f)
        existing_data.extend(data)
        with open(file_path, "w") as f:
            f.write(json.dumps(existing_data, indent=2))
    else:
        try:
            with open(file_path, "w") as f:
                f.write(json.dumps(data, indent=2))
        except Exception as e:
            print(e)

def get_json(file_path: str):
    with open(file_path, "r") as f:
        existing_data = json.load(f)
    return existing_data
