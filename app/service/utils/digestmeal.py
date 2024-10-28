from typing import Dict
import pandas as pd
import os

def datasource() -> Dict[str, str]:
    data_path = "app/data/processed"
    meal_data = {}
    for filename in os.listdir(data_path):
        if filename.endswith('.json'):
            name = os.path.splitext(filename)[0]
            file_path = os.path.join(data_path, filename)
            meal_data[name] = file_path
    return meal_data

def combine_meal() -> pd.DataFrame:
    all_data = datasource()
    meal = pd.read_json(all_data["meal_cleaned"])
    ingredients = pd.read_json(all_data["ingredients"])
    recipe = pd.read_json(all_data["recipe_cleaned"])
    meal_recipe = pd.read_json(all_data["mealtorecipe"])
    merged = pd.merge(ingredients, recipe, on="recipe_id")
    grouped_df = merged.groupby(
        ['recipe_id', 'course', 'cuisine', 'servings', 'calories', 'prep time', 'cook time', 'total time']
    ).agg({
        'ingredient': lambda x: ', '.join(x)
    }).reset_index()
    grouped_df = pd.merge(grouped_df, meal_recipe, on="recipe_id")
    final_df = pd.merge(grouped_df, meal)
    return final_df
