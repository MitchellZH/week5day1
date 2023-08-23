from . import main
from flask import request, render_template
import requests
from .forms import SearchForm
from flask_login import login_required

@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html')

@main.route('/info', methods=['GET', 'POST'])
@login_required
def get_pokemon_info():
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
      pokemon_name = request.form.get('pokemon_name').lower()
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