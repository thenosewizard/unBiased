import json
import requests 


def get_reviews(appid, num_iterations = 0):

    cursor = ""
    i = 0
    while i < num_iterations:
        response = requests.get("https://store.steampowered.com/appreviews/"+str(appid)+"?json=1&num_per_page=100&cursor="+str(cursor))
        response = response.json()
        cursor = response["cursor"]
        print(cursor)
        i+=1



get_reviews(779340, 400)