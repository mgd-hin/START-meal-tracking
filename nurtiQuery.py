import requests

def fetch_data_from_api():
    # Define the URL of the API endpoint
    search_url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    """headers = {
        "User-Agent": "My Custom User Agent",  # Example header
        "Authorization": "Bearer qODbFNgUV6tkyuCkDhOxeL1aU74FjazhfbIOTCbh",  # Example authorization header
        "Content-Type": "application/json"  # Example content type header
        # Add any other headers as needed
    }"""

    test_query = "Cheddar%20Cheese"
    query = test_query

    try:
        response = requests.get(search_url + "?api_key=qODbFNgUV6tkyuCkDhOxeL1aU74FjazhfbIOTCbh&query=" + query)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json().get("foods")
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
data = fetch_data_from_api()
#print(requests.get("https://api.nal.usda.gov/fdc/v1/foods/search?api_key=qODbFNgUV6tkyuCkDhOxeL1aU74FjazhfbIOTCbh&query=tomato").json().get('foods')[0]["foodNutrients"])
