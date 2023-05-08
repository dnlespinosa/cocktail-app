from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class EditProfileForm(FlaskForm):
    """Edit profile form"""

    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class SearchDrinkForm(FlaskForm):
    """Searching for cocktail"""

    drinkname = StringField('Drink Name', validators=[DataRequired()])

class SearchLiquorForm(FlaskForm):
    """Searching for cocktail by liquor"""

    drinkname = StringField('Liquor Name', validators=[DataRequired()])