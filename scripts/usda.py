from dataclasses import dataclass
import json
import pprint
import requests
import typing as t
import urllib.parse

API_KEY = "Hzaq8biGeexPpBqrSgyUF9VkEyahGgJWfeje5v9f"
BASE_URL = "https://api.nal.usda.gov"
SEARCH_PATH = "/fdc/v1/search"
FOOD_DETAIL_PATH = "/fdc/v1/{}"

FOOD_NUTRIENTS = {
    1003: 'protein',
    1005: 'carbs',
    1004: 'fat',
    1008: 'calories',
    1018: 'alcohol',
    1079: 'fiber',
    2000: 'sugar',
}

@dataclass
class Food():
    name: str=''
    calories: float=0.0
    fat: float=0.0
    carbs: float=0.0
    protein: float=0.0
    fiber: float=0.0
    sugar: float=0.0
    alcohol: float=0.0

def search(food_name: str):
    data = {'generalSearchInput': food_name}
    endpoint = BASE_URL + SEARCH_PATH
    params = {"api_key": API_KEY}
    r = requests.post(endpoint, json=data, params=params)
    r.raise_for_status()
    results = []
    for food in r.json()["foods"]:
        if food["dataType"] == "Survey (FNDDS)":
            results.append(food)
    return results

def get_food(fdc_id: int):
    endpoint = BASE_URL + FOOD_DETAIL_PATH.format(fdc_id)
    params = {"api_key": API_KEY}
    r = requests.get(endpoint, params=params)
    r.raise_for_status()
    return _parse_food(r.json())

def _select_result(results: t.List):
    print('Search results:')
    choices = {}
    choice_num = 1
    for r in results:
        choices[choice_num] = r
        print(f'{choice_num}. {r["description"]}')
        choice_num += 1
    choice = int(input('\nPlease select your choice: '))
    return choices[choice]["fdcId"]

def _parse_food(usda_food: t.Dict):
    food = Food()
    food.name = usda_food["description"]
    for nutrient in usda_food["foodNutrients"]:
        nutrient_id = nutrient["nutrient"]["id"]
        if nutrient_id in FOOD_NUTRIENTS:
            food.__setattr__(FOOD_NUTRIENTS[nutrient_id], nutrient["amount"])
    return food
    
def main():
    results = search("Egg raw")
    if len(results) > 1:
        result = _select_result(results[:10])
    else:
        result = results[0]["fdcId"]
    print(get_food(result))

if __name__ == '__main__':
    main()
