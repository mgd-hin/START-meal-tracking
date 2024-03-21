import requests
import openfoodfacts
import json

# User-Agent is mandatory
api = openfoodfacts.API(user_agent="Grocerly/Prototype")

def fetch_data_from_api(query):
    data = api.product.text_search(query).get("products")
    allergens = data[0].get("allergens")
    nutrients = data[0].get("nutriments")
    print(data[0]) #TODO Get the type of the food on order to recommend a better food of the same type with better nova score
    #print(nutrients)
    #print(allergens)
    #print(nutrients["nova-group"])

    data = {
        "nutrients": {
            "nova-group": nutrients["nova-group"],
            "nutrition-score-fr_100g": nutrients["nutrition-score-fr_100g"],
            "proteins_100g":  nutrients["proteins_100g"],
            "salt_100g": nutrients["salt_100g"],
            "sugars_100g": nutrients["sugars_100g"],
            "saturated-fat_100g":  nutrients["saturated-fat_100g"],
            "ph_100g": nutrients["ph_100g"],
            "fat_100g": nutrients["fat_100g"],
            "energy_100g": nutrients["energy_100g"],
            "carbohydrates_100g": nutrients["carbohydrates_100g"]
        },
        "allergens": allergens
    }

    json_data = json.dumps(data)

    print(json_data)

fetch_data_from_api("water")




# Deprecated:
"""
def fetch_data_from_api(query):

    search_url = "https://api.nal.usda.gov/fdc/v1/foods/search"

    try:
        response = requests.get(search_url + "?api_key=qODbFNgUV6tkyuCkDhOxeL1aU74FjazhfbIOTCbh&query=" + query)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json().get("foods")
            print(data)
            nutrients = {}
            num_foods = len(data)

            # Initialize the nutrients dictionary with zero values
            for nutrient in data[0]["foodNutrients"]:
                nutrients[nutrient.get("nutrientName")] = 0

            # Sum up the nutrient values
            for food in data:
                for nutrient in food["foodNutrients"]:
                    nutrient_name = nutrient.get("nutrientName")
                    if nutrient_name in nutrients.keys():
                        nutrients[nutrient_name] += nutrient.get("value")

            # Calculate the average nutrient values
            for nutrient_name, total_value in nutrients.items():
                if nutrient_name in nutrients.keys():
                    nutrients[nutrient_name] = total_value / num_foods

            print(nutrients)

            return data
        else:
            # Print an error message if the request was not successful
            print(f"Error: Unable to fetch data from API (status code {response.status_code})")
            return None

    except requests.RequestException as e:
        # Print an error message if there was a problem with the request
        print(f"Error: {e}")
        return None

# Example usage:
#data = fetch_data_from_api("Cheddar Cheese")
#print(requests.get("https://api.nal.usda.gov/fdc/v1/foods/search?api_key=qODbFNgUV6tkyuCkDhOxeL1aU74FjazhfbIOTCbh&query=tomato").json().get('foods')[0]["foodNutrients"])
"""
