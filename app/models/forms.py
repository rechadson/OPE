from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("username",validators=[DataRequired()])
    password = PasswordField("password",validators=[DataRequired()])

class Cliente(FlaskForm):
    name = StringField("nome",validators=[DataRequired()])
    cpf = StringField("cpf",validators=[DataRequired()])
    endereco = StringField("endereco",validators=[DataRequired()])

class Produto(FlaskForm):
    codigo = StringField("nome",validators=[DataRequired()])
    Nome = StringField("cpf",validators=[DataRequired()])
    Preco = StringField("endereco",validators=[DataRequired()])