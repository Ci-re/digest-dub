from dotenv import load_dotenv
import json
import google.generativeai as genai
import pandas as pd
import os
import typing_extensions as typing
import time
from app.utils.stomach import save_json

load_dotenv()
genai.configure(api_key=os.environ["API_KEY"])

class Category(typing.TypedDict):
    meal_type: str
    alternative_meal_type: str
    course_type: str
    category: str

data = pd.read_json("../../app/data/processed/recipe_cleaned.json")
recipes = data["course"]
recipes_id = data["recipe_id"]

prompt = '''
You are a nutritionist or a food expert, your goal is to extract some details from a text about a particular recipe and
put in a proper JSON format. Don't worry, this is not a difficult task, However, you must put in mind that the text you are given
must output only a single dictionary or single JSON object like this  {meal_type : "breakfast/lunch/dinner",
"alternative_meal_type" : "lunch/dinner/breakfast" , "course_type": "main course/side dish", "category": "seafood/..."}
and in situations where you can't find a specific property or feature, return an empty string for that attribute.
'''

def structure_recipe() -> None:
    for recipe, recipe_id in zip(recipes, recipes_id):
        model = genai.GenerativeModel("gemini-1.5-flash")
        rec_data = []
        try:
            result = model.generate_content(
                f"{prompt} \n {recipe}",
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json", response_schema=list[Category]
                ),
            )
            response = json.loads(result.text)[0]
            response["recipe_id"] = recipe_id
            rec_data.append(response)
            save_json(data = rec_data, file="recipes_AI")
        except Exception as e:
            if isinstance(e, AttributeError):
                pass
            else:
                raise e
        time.sleep(4)

# if __name__ == "__main__":
#     structure_recipe()
