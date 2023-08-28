from . import main
from flask import request, render_template, redirect, url_for, flash
import requests
from .forms import SearchForm
from app.models import db, Caught_Pokemon, User, team
from flask_login import login_required, current_user


@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html')

@main.route('/attack/<int:user_id>')
@login_required
def attack(user_id):
  user1 = User.query.get(current_user.id)
  user2 = User.query.get(user_id)

  user_1_team = user1.team.all()
  user_2_team = user2.team.all()

  user_1_power = 0
  user_2_power = 0
  for pokemon in user_1_team:
    user_1_power += int(pokemon.attack) + int(pokemon.defense) + int(pokemon.hp)
    
  for pokemon in user_2_team:
    user_2_power += int(pokemon.attack) + int(pokemon.defense) + int(pokemon.hp)

  if user_1_power > user_2_power:
      winner = user1.first_name
  elif user_2_power > user_1_power:
      winner = user2.first_name
  else:
      winner = "No one!"

  return render_template("attack.html", user1=user1, user2=user2, user_1_team=user_1_team, user_2_team=user_2_team, winner=winner, user_1_power=user_1_power, user_2_power=user_2_power)

@main.route('/trainers')
def trainers():
   users = User.query.all()
   
   return render_template("trainers.html", users=users)

@main.route('/view_team')
@login_required
def view_team():
  user = User.query.get(current_user.id)
  
  pokemon_list = user.team.all()
  
  return render_template("team.html", pokemon_list=pokemon_list)


@main.route('/add_to_team/<int:pokemon_id>')
@login_required
def add_to_team(pokemon_id):
  if current_user.can_add_pokemon():
    pokemon = Caught_Pokemon.query.get(pokemon_id)

    current_user.team.append(pokemon)

    db.session.commit()

    flash(f"{pokemon.name} was added to your team!", 'success')
    return redirect(url_for('main.caught_pokemon'))
  else:
    flash(f"Your team is at full capacity!", 'danger')
    return redirect(url_for('main.caught_pokemon'))
      

@main.route('/remove_from_team/<int:pokemon_id>')
@login_required
def remove_from_team(pokemon_id):
  pokemon = Caught_Pokemon.query.get(pokemon_id)

  current_user.team.remove(pokemon)

  db.session.commit()

  flash(f"{pokemon.name} was released from your team!", 'warning')
  return redirect(url_for('main.caught_pokemon'))
  
@main.route('/caught_pokemon')
def caught_pokemon():
   caught_pokemon = Caught_Pokemon.query.all()
   for pokemon in caught_pokemon:
      if pokemon in current_user.team:
         pokemon.inTeam = True
   return render_template('caught_pokemon.html', caught_pokemon=caught_pokemon)

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
            'abilities': "",
            'base_experience': data['base_experience'],
            'sprites': data['sprites']['front_shiny'],
            'stats': {
                'hp': data['stats'][0]['base_stat'],
                'attack': data['stats'][1]['base_stat'],
                'defense': data['stats'][2]['base_stat']
            }
        }
        for ability in data['abilities']:
            pokemon['abilities'] += " " + ability['ability']['name']
        return render_template('pokemon.html', pokemon=pokemon, form=form)
      return render_template('pokemon.html', form=form)
    else:
      return render_template('pokemon.html', form=form)
    
@main.route('/catch-pokemon/<string:pokemon_name>', methods=['GET', 'POST'])
@login_required
def catch_pokemon(pokemon_name):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
    response = requests.get(url)
    if response.ok and len(pokemon_name) > 0:
      data = response.json()
      
      name = data['name'].title()
      abilities = ""
      for ability in data['abilities']:
        abilities += " " + ability['ability']['name']
      base_experience = data['base_experience']
      sprites = data['sprites']['front_shiny']
      hp = data['stats'][0]['base_stat']
      attack = data['stats'][1]['base_stat']
      defense = data['stats'][2]['base_stat']

      caught_pokemon = Caught_Pokemon(name, abilities, base_experience, sprites, hp, attack, defense)

      db.session.add(caught_pokemon)
      db.session.commit()

      flash(f'Successfully created caught {name}!', 'success')
      return redirect(url_for('main.get_pokemon_info'))
    flash(f'Pokemon not found!', 'danger')
    return redirect(url_for('main.get_pokemon_info'))
