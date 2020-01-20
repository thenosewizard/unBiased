
import flask
import firebase_admin
from firebase_admin import db

firebase_admin.initialize_app(options={
    'databaseURL': 'https://unbiased-ded52.firebaseio.com'
})

firedb = db.reference('user')
testdata = {
    "username":"john.bb",
    "email":"abi@email.com",
    "password":"123456780",
    "role":"Member"
    }
print(firedb.push(testdata).key)
print(firedb.get())