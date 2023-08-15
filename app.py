from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route('/pokemon/info', methods=['GET', 'POST'])
def get_pokemon_info():
    if request.method == 'POST':
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
        return render_template('pokemon.html', pokemon=pokemon)
      return render_template('pokemon.html')
    else:
      return render_template('pokemon.html')