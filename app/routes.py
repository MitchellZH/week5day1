from flask import request, render_template, flash, redirect, url_for
import requests
from app import app
from .forms import SearchForm, LoginForm, SignupForm
from flask_login import login_user, logout_user, current_user, login_required
from .models import User, db
from werkzeug.security import check_password_hash

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

# fake database
REGISTERED_USERS = {
   'test@thieves.com': {
      'name': 'test',
      'password': 'test'
   }
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
           login_user(queried_user)
           flash(f'Hello, {queried_user.first_name}', 'info')
           return redirect(url_for('home'))
        else:
           flash('Invalid email or password', 'danger')
           return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():

        # Grabbing our sign up form data
        first_name = form.first_name.data.title() 
        last_name = form.last_name.data.title()
        email = form.email.data.lower()
        password = form.password.data
        
        # Creating an instance of the User Model
        new_user = User(first_name, last_name, email, password)

        # Adding new user to our database
        db.session.add(new_user)
        db.session.commit()

        flash(f'Thank you for signing up {new_user.first_name}!', 'info')
        return redirect(url_for('login'))
    else:
        return render_template('signup.html', form=form)
    
@app.route('/logout')
def logout():
   logout_user()
   return redirect(url_for('home'))

@app.route('/pokemon/info', methods=['GET', 'POST'])
@login_required
def get_pokemon_info():
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
      pokemon_name = request.form.get('pokemon_name')
      url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
      response = requests.get(url)
      if response.ok and len(pokemon_name) > 0:
        data = response.json()
        pokemon = {
            'name': data['name'],
            'abilities': {
              'ability1': data['abilities'][0]['ability']['name'],
              'ability2': data['abilities'][1]['ability']['name']
            },
            'base_experience': data['base_experience'],
            'sprites': data['sprites']['front_shiny'],
            'stats': {
                'hp': data['stats'][0]['base_stat'],
                'attack': data['stats'][1]['base_stat'],
                'defense': data['stats'][2]['base_stat']
            }
        }
        return render_template('pokemon.html', pokemon=pokemon, form=form)
      return render_template('pokemon.html', form=form)
    else:
      return render_template('pokemon.html', form=form)