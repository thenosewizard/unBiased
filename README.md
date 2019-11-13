# Running this project

In order to run this application here we need to do a few steps

## Installing the required modules

Navigate to the repository you have just cloned and type the following commands

`` pip install requirements.txt ``

## Running the program
Just type **``python app.py``** in your cmd and you should be good to go!

# File structure
````
├───reviews                        # Application
│   ├───AI                         # Machine learning and scripts to get data
│   ├───Data
│   │   └───models.py              # Database models 
│   ├───evaluation     
│   │   ├───templates              # Html files for evaluation
│   │   └───controllers.py         # Contains logic for reviews section/News and admin page
│   ├───main
│   │   ├───templates              # Html files for main
│   │   └───controllers.py         # Contains logic for login, main page, about us and etc
│   ├───static                     # main css for all pages
````

# Database structure
![Image](https://github.com/thenosewizard/unBiased/blob/master/Website/media/db.jfif)

# Creating the database in your local
1. Make sure your current working directory is where you can see the reviews, app.py etc..
2. Type python in your command line
3. Now type `from reviews.Data.models import db`
4. Type `db.create_all()`
5. You should see an __unbiased.db__ file in your __Data__ folder
6. [Click here to learn - Flask-alchemy documentation](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
