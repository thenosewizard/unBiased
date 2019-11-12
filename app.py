from flask import Flask, render_template
from reviews import app 
from reviews.Data.models import db

if __name__ == "__main__":
   app.run(debug=True)
