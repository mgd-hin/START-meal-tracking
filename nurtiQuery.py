import openfoodfacts
import json
import pandas as pd

# User-Agent is mandatory
api = openfoodfacts.API(user_agent="Grocerly - Python - Version 1.0 ")


def fetch_data_from_api(query):
    """
       Fetches data from the Open Food Facts API based on the provided query.

       Parameters:
       - query (str): The search query to find relevant products.

       Returns:
       - json_data of nutrients
    """
    query_data = api.product.text_search(query).get("products")
    print(query_data[0])

    json_data = extract_nutrient_data(query_data)

    if int(json_data["nutrients"]["nova-group"]) != 1:
        recommend_healthy_suggestions(json_data, int(json_data["nutrients"]["nova-group"]), 3)

    return json_data


def extract_nutrient_data(api_obj):
    """
        Extracts nutrient data from the API response and constructs a JSON object.

        Parameters:
        - api_obj (dict): The API response containing product data.

        Returns:
        dict: A JSON object containing extracted nutrient data.
    """
    allergens = api_obj[0].get("allergens")
    nutrients = api_obj[0].get("nutriments")

    json_data = {
        "name": api_obj[0].get("abbreviated_product_name"),
        "categories": [],
        "nutrients": {
            "nova-group": nutrients["nova-group"],
            "nutrition-score-fr_100g": nutrients["nutrition-score-fr_100g"],
            "proteins_100g": nutrients["proteins_100g"],
            "saturated-fat_100g": nutrients["saturated-fat_100g"],
            "fat_100g": nutrients["fat_100g"],
            "energy_100g": nutrients["energy_100g"],
            "carbohydrates_100g": nutrients["carbohydrates_100g"]
        },
        "allergens": allergens
    }

    for i in range(3):
        if i < len(api_obj[0].get("categories_hierarchy")):
            json_data["categories"].append(api_obj[0].get("categories_hierarchy")[i])

    optional_nutrients = ["salt_100g", "sugars_100g", "ph_100g"]
    for nutrient in optional_nutrients:
        if nutrient in nutrients:
            json_data["nutrients"][nutrient] = nutrients[nutrient]

    json_string = json.dumps(json_data)
    print(json_string)

    return json_data


def recommend_healthy_suggestions(json_data, nova_group, num_suggestions):
    """
        Recommends healthy food suggestions based on nutrient data.

        Parameters:
        - json_data (dict): JSON object containing nutrient data.
        - nova_group (int): Nova group value for the product.
        - num_suggestions (int): Number of healthy suggestions to recommend.

        Returns:
        None
        """
    print("RECOMMENDATIONS (based on nova-group):")

    for category in json_data["categories"]:
        category = category.strip("en:")
        query_data = api.product.text_search(category).get("products")
        df = pd.DataFrame(query_data)
        filtered_df = df[df["nutriments"].apply(lambda x: "nova-group" in x and x["nova-group"] < nova_group)]
        item = min(num_suggestions, len(filtered_df))
        for i in range(item):
            data = filtered_df.iloc[i]
            nutrients = data["nutriments"]
            recommendation = {
                "name": data["product_name"],
                "nutrients": {
                    "nova-group": nutrients["nova-group"],
                    "nutrition-score-fr_100g": nutrients["nutrition-score-fr_100g"],
                    "proteins_100g": nutrients["proteins_100g"],
                    "saturated-fat_100g": nutrients["saturated-fat_100g"],
                    "fat_100g": nutrients["fat_100g"],
                    "energy_100g": nutrients["energy_100g"],
                    "carbohydrates_100g": nutrients["carbohydrates_100g"]
                },
            }
            print(recommendation)

# Example usage
fetch_data_from_api("cookie")

"""
Deprecated:
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
