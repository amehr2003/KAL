from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
import secrets

app = Flask(__name__)

# Set a secret key for CSRF protection
app.secret_key = secrets.token_hex(16)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///makeup_advice.db'
db = SQLAlchemy(app)  # Initialize SQLAlchemy

# Flask-Login initialization
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Define User model for authentication
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Create Registration and Login Forms
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=80)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=128)])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=80)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=128)])

# Modify the calculate_makeup_advice function to handle makeup recommendations
def calculate_makeup_advice(eye_color, hair_color, skin_tone):
    # Define makeup recommendations based on user selections
    makeup_recommendations = {
        ('blue', 'brown', 'fair'): "For your Blue eyes, Brown hair, and Fair skin, consider using warm earthy tones for eyeshadow, and a nude lipstick.",
        ('blue', 'black', 'medium'): "For your Blue eyes, Black hair, and Medium skin, try cool purples or blues for eyeshadow and a deep red lipstick.",
        # Add more recommendations based on different color combinations
    }

    # Check if there's a recommendation for the user's selections
    if (eye_color, hair_color, skin_tone) in makeup_recommendations:
        return makeup_recommendations[(eye_color, hair_color, skin_tone)]
    else:
        return "Sorry, we don't have specific recommendations for your selections. Experiment with different colors to find what works best for you."

# Implement the get_user_data function to fetch user-specific data
def get_user_data(user_id):
    # Replace this with your logic to fetch user-specific data
    # For example, you can fetch makeup advice from the database
    user_data = "User-specific data or makeup advice goes here"
    return user_data

# Routes
# User profile route
@app.route('/profile')
@login_required
def profile():
    user_data = get_user_data(current_user.id)  
    return render_template('profile.html', user=current_user, user_data=user_data)

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('makeup_form.html')

@app.route('/advice', methods=['POST'])
def get_makeup_advice():
    eye_color = request.form['eye_color']
    hair_color = request.form['hair_color']
    skin_tone = request.form['skin_tone']
    advice = calculate_makeup_advice(eye_color, hair_color, skin_tone)
    return render_template('makeup_advice.html', advice=advice)

# Route for the products page
@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data)
        new_user.password = form.password.data  # In a real application, you should hash the password
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. You can now log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if form.password.data == user.password:  # In a real application, you should verify the hashed password
                login_user(user)
                return redirect(url_for('profile'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
