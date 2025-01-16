from logging import Logger
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

class Recipe(typing.TypedDict):
    main_ingredient: str
    quantity: str
    measurement: str
    alternative_ingredient: str
    weight: str

data = pd.read_json("../../app/data/processed/ingredients.json")
ingredient_list = data["ingredient"]
ingredients_id = data["recipe_id"]

# print(ingredient_list[2416:])
# count = 0
# for ing in ingredient_list:
#     count += 1
#     print(count, ing)

prompt = '''
You are a nutritionist or a food expert, your goal is to extract some details from a text about a particular ingredient and
put in a proper JSON format. Don't worry, this is not a difficult task, However, you must put in mind that the text you are given
must output only a single dictionary or single JSON object like this  {main_ingredient : "peanut", "quantity" : "2.5", "measurement": "cups",
"alternative_ingredient": "groundnut", "weight": "5kcal"} and in situations where you can't find a specific property or feature, return an empty
string for that attribute. I also noticed you are not good at identifying floating points values in texts. Please understand the 2.4 is
different from 24, and also 1.5 is different from 15, be careful to identify the difference to avoid wrong data
'''
def structure_ingredients():
    for ingredients, ingredient_id in zip(ingredient_list, ingredients_id):
        model = genai.GenerativeModel("gemini-1.5-flash")
        ing_data = []
        try:
            result = model.generate_content(
                f"{prompt} \n {ingredients}",
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json", response_schema=list[Recipe]
                ),
            )
            response = json.loads(result.text)[0]
            response["ingredient_id"] = ingredient_id
            ing_data.append(response)
            save_json(data = ing_data, file="ingredients_AI")
        except Exception as e:
            if isinstance(e, AttributeError):
                pass
            else:
                raise e
        time.sleep(4)


# if __name__ == "__main__":
#     structure_ingredients()

class Measurements(typing.TypedDict):
    unit: str
    shortform_unit: str

prompt_measurements = '''
You are a nutritionist or a food expert, your goal is to extract plural and singular from a text about a particular measurement and
put in a proper JSON format. Don't worry, this is not a difficult task, However, you must put in mind that the text you are given
can be singular or plural and must output only a single dictionary or single JSON object like this if the unit is plural
{unit : "", "shortform_unit" : "", "unit_plural": "grams", "shortform_unit_plural": "g"} and
{unit : "gram", "shortform_unit" : "g", "unit_plural": "", "shortform_unit_plural": ""} if singular
please don't give units where it is not specified and in situations where you can't find a specific property or feature,
return an empty string for that attribute just like I did.
'''
data = pd.read_json("../../app/data/processed/ingredients_AI.json")
measurements = data["measurement"].drop_duplicates()
def structure_measurements():
    for measurement in measurements:
        model = genai.GenerativeModel("gemini-1.5-flash")
        measurement_data = []
        try:
            result = model.generate_content(
                f"{prompt} \n {measurement}",
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json", response_schema=list[Measurements]
                ),
            )
            response = json.loads(result.text)[0]
            measurement_data.append(response)
            save_json(data = measurement_data, file="measurements_AI")
        except Exception as e:
            if isinstance(e, AttributeError):
                pass
            else:
                raise e
        time.sleep(4)

# if __name__ == "__main__":
#     structure_measurements()
