# Running this project

In order to run this application here we need to do a few steps

# Installing the required modules

Navigate to the repository you have just cloned and type the following commands


- **Firstly** we need to set up the virtual environment 
>- py -3 -m venv venv
- Now activate the virtual environment 
>- .\venv\Scripts\activate
- Now run this command 
>- Pip install requirements.txt 
- If you don't have pip installed, run this command
>- python get-pip.py

## Running the program

Just type **python run.py** in your cmd and you should be good to go!


# File structure
__the templates folder in each of these files contain their respective html pages__
- AI
> Contains the code for machine learning and scripts to get data

- evaluation
> Contains logic for reviews section/News and admin page

- main
> Contains logic for login, main page, about us and etc

- static
> main css for all pages
# Database structure

- to be added (Oscar add plz)

# Creating the database in your local
1. Make sure your current working directory is where you can see the reviews, app.py etc..
2. Type python in your command line
3. Now type `from reviews.Data.models import db`
4. Type `db.create_all()`
5. You should see an __unbiased.db__ file in your __Data__ folder
6. [Click here to learn - Flask-alchemy documentation](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)



