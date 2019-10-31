import json
import requests 


def get_reviews(str(appid), num_iterations = 1):
    response = requests.get("https://store.steampowered.com/appreviews/"+appid+"?json=1&num_per_page=100")
    response = response.json()
    print(response["reviews"])




get_reviews(779340)