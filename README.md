# Grocerly

This Python script fetches data from the Open Food Facts API to retrieve information about food products. It extracts nutrient data from the API response, constructs JSON objects, and provides recommendations for healthy food choices based on the Nova group value.

## Requirements

- Python 3.x
- `openfoodfacts` library
- `json` library
- `pandas` library

## Example usage:
The food you are eating / have scanned is recognized as a cookie:
fetch_data_from_api("cookie")

## Function Documentation

fetch_data_from_api(query)
Fetches data from the Open Food Facts API based on the provided query.

Parameters:
query (str): The search query to find relevant products.
Returns:
JSON data of nutrients.
extract_nutrient_data(api_obj)
Extracts nutrient data from the API response and constructs a JSON object.

Parameters:
api_obj (dict): The API response containing product data.
Returns:
dict: A JSON object containing extracted nutrient data.
recommend_healthy_suggestions(json_data, nova_group, num_suggestions)
Recommends healthy food suggestions based on nutrient data.

Parameters:
json_data (dict): JSON object containing nutrient data.
nova_group (int): Nova group value for the product.
num_suggestions (int): Number of healthy suggestions to recommend.
