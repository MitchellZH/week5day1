from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    pokemon_name = StringField('Enter Pokemon:', validators=[DataRequired()])
    search_btn = SubmitField('Search')