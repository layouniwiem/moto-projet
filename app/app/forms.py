from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional
from flask_wtf.file import FileAllowed, FileRequired

class LoginForm(FlaskForm):
    username = StringField(
        'Nom d\'utilisateur', 
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Mot de passe', 
        validators=[DataRequired()]
    )
    submit = SubmitField('Se connecter')

class AddMotoForm(FlaskForm):
    marque = StringField('Marque', validators=[DataRequired()])
    modele = StringField('Modèle', validators=[DataRequired()])
    annee = IntegerField('Année', validators=[DataRequired(), NumberRange(min=1900, max=2100)])
    kilometrage = IntegerField('Kilométrage', validators=[DataRequired(), NumberRange(min=0)])
    prix = DecimalField('Prix', validators=[DataRequired(), NumberRange(min=0)])
    description = TextAreaField('Description', validators=[Optional()])
    image = FileField('Image de la moto', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images uniquement !')
    ])
    submit = SubmitField('Ajouter la moto')
