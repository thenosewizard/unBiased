import json
import requests
import os

################
filename = "abi"
appid = "730"
################

filename = os.getcwd() + "/reviews/AI/" + filename + '.json'

#getting the reviews from the steam api


def get_reviews_2(appid, num_iterations=0, filename=""):
    f = open(filename, 'w+')
    cursor = ""
    i = 0
    output = []
    while i < num_iterations:
        # Num per page roughly 78
        response = requests.get("https://store.steampowered.com/appreviews/" +
                                str(appid)+"?json=1&num_per_page=100&cursor="+str(cursor))

        #checking if request is sucessful
        if response.status_code == 200:
            response = response.json()
            cursor = response["cursor"]
            output.append(response["reviews"])
            print(cursor + " Request no: " + str(i))
            i += 1
        else:
            continue
    with open(filename, 'a+') as outfile:
        json.dump(output, outfile, sort_keys=True, indent=4)


#read reviews from the json files
def read_reviews(filename):
    with open(filename, encoding='utf-8', errors='ignore') as json_data:
        data = json.loads(json_data.read())
    print(data)
    return data


def clean_reviews(filename):
    with open(filename, 'r') as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('\n', ' ')

    # Write the file out again
    with open('edited.json', 'w') as file:
        file.write(filedata)

# get_reviews_2(appid, 1, filename)
# read_reviews(filename)
clean_reviews(filename)
