import json
import requests 


#getting the reviews from the steam api
def get_reviews_2(appid, num_iterations = 0, filename =""):

    cursor = ""
    i = 0
    output = []
    while i < num_iterations:
        response = requests.get("https://store.steampowered.com/appreviews/"+str(appid)+"?json=1&num_per_page=100&cursor="+str(cursor))

        #checking if request is sucessful
        if response.status_code == 200:
            response = response.json()
            cursor = response["cursor"]
            output.append(response["reviews"])
            print(cursor + " Request no: " + str(i))
            i+=1
        else:
            continue
    with open(filename+'.json', 'a+') as outfile:
        json.dump(output, outfile, sort_keys=True, indent=4)


#read reviews from the json files 
def read_reviews(filename):
    with open(filename,encoding='utf-8', errors='ignore') as json_data:
        data = json.loads(json_data.read())
    print(data)
    return data



#get_reviews_2(779340, 200, "totalWar")
get_reviews_2(730, 2000, "csgo")


#read_reviews("csgo.json")