from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
import pandas as pd
import unittest
from pymongo import MongoClient
import pymongo

class BeautyForm(FlaskForm):
    eye_color = StringField('Eye Color')
    hair_color = StringField('Hair Color')
    skin_tone = StringField('Skin Tone')
    season = SelectField('Season', choices=[('spring', 'Spring'), ('summer', 'Summer'), ('fall', 'Fall'), ('winter', 'Winter')])
    submit = SubmitField('Get Makeup Advice')

app = Flask(__name__)

# Load makeup advice data from a CSV file
makeup_data = pd.read_csv('makeup_data.csv')

@app.route('/')
def hello_world():
    form = BeautyForm()  
    return render_template('index.html', form=form)  

@app.route('/makeup-advice', methods=['GET', 'POST'])
def makeup_advice():
    form = BeautyForm()  

    if form.validate_on_submit():
        # Process user input and provide makeup advice
        eye_color = form.eye_color.data
        hair_color = form.hair_color.data
        skin_tone = form.skin_tone.data
        season = form.season.data

        # Filter the makeup data based on user input
        filtered_data = makeup_data[
            (makeup_data['EyeColor'] == eye_color) &
            (makeup_data['HairColor'] == hair_color) &
            (makeup_data['SkinTone'] == skin_tone) &
            (makeup_data['Season'] == season)
        ]

        # Get makeup advice based on the filtered data
        if not filtered_data.empty:
            makeup_advice_result = filtered_data.iloc[0]['MakeupAdvice']
        else:
            makeup_advice_result = "No makeup advice available for this combination."

        dataframe_html = filtered_data.to_html(classes='table table-striped', escape=False, index=False)

        return render_template('makeup_advice.html', form=form, makeup_advice=makeup_advice_result)

    return render_template('makeup_advice.html', form=form)

class TestMyApp(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        self.app.testing = True
        
    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Beauty Adhancer web app!', response.data)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["user_login_db"]
collection = db["user_collection"]

def create_user(username, password):

    # Create a user document
    user = {
        "username": username,
        "password": password
    }

    # this stores the login information inside of mongo
    collection.insert_one(user)


def authenticate_user(username, password):

    user = collection.find_one({"username": username, "password": password})

    if user:
        print("Login successful!")
    else:
        print("Invalid username or password.")


# THIS IS THE EXAMPLE SO THAT WE CAN USE IT
create_user("user1", "password123")

# EXAMPLE FOR AUTHENTICATION
authenticate_user("user1", "password123")


if __name__ == '__main__':
    app.run(debug=True)
    unittest.main()
