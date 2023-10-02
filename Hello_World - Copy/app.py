from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField

class BeautyForm(FlaskForm):
    eye_color = StringField('Eye Color')
    hair_color = StringField('Hair Color')
    skin_tone = StringField('Skin Tone')
    season = SelectField('Season', choices=[('spring', 'Spring'), ('summer', 'Summer'), ('fall', 'Fall'), ('winter', 'Winter')])
    submit = SubmitField('Get Makeup Advice')

app = Flask(__name__)

@app.route('/')
def hello_world():
    form = BeautyForm()  
    return render_template('index.html', form=form)  

@app.route('/makeup-advice', methods=['GET', 'POST'])
def makeup_advice():
    form = BeautyForm()  # Create an instance of your BeautyForm class

    if form.validate_on_submit():
        # Process user input and provide makeup advice
        eye_color = form.eye_color.data
        hair_color = form.hair_color.data
        skin_tone = form.skin_tone.data
        season = form.season.data

        # Perform your makeup advice logic here (replace with your logic)
        makeup_advice_result = get_makeup_advice(eye_color, hair_color, skin_tone, season)

        # For now, let's just print the user input and advice result
        print(f'Eye Color: {eye_color}, Hair Color: {hair_color}, Skin Tone: {skin_tone}, Season: {season}')
        print(f'Makeup Advice: {makeup_advice_result}')

    return render_template('makeup_advice.html', form=form)

def get_makeup_advice(eye_color, hair_color, skin_tone, season):
    # Replace this with your actual makeup advice logic
    # This is just a placeholder
    return "Your makeup advice goes here."

if __name__ == '__main__':
    app.run(debug=True)
