from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

team = db.Table(
    'team',
    db.Column('team_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('pokemon_id', db.Integer, db.ForeignKey('caught__pokemon.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    team = db.relationship(
        'User', secondary=team,
        primaryjoin = (team.columns.team_id == id),
        backref = db.backref('team', lazy='dynamic'),
        lazy='dynamic'
    )

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)

class Caught_Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    abilities = db.Column(db.String, nullable=False)
    base_experience = db.Column(db.Integer, nullable=False)
    sprites = db.Column(db.String, nullable=False)
    hp = db.Column(db.String, nullable=False)
    attack = db.Column(db.String, nullable=False)
    defense = db.Column(db.String, nullable=False)
    team = db.relationship(
        'Caught_Pokemon', secondary=team,
        primaryjoin = (team.columns.pokemon_id == id),
        backref = db.backref('team', lazy='dynamic'),
        lazy='dynamic'
    )

    def __init__(self, name, abilities, base_experience, sprites, hp, attack, defense):
        self.name = name
        self.abilities = abilities
        self.base_experience = base_experience
        self.sprites = sprites
        self.hp = hp
        self.attack = attack
        self.defense = defense