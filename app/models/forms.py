from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("username",validators=[DataRequired()])
    password = PasswordField("password",validators=[DataRequired()])

class Cliente(FlaskForm):
    name = StringField("nome",validators=[DataRequired()])
    cpf = StringField("cpf",validators=[DataRequired()])
    endereco = StringField("endereco",validators=[DataRequired()])

class Produto(FlaskForm):
    codigo = StringField("codigo",validators=[DataRequired()])
    Nome = StringField("Nome",validators=[DataRequired()])
    preco = StringField("preco",validators=[DataRequired()])
class Orcamento(FlaskForm):
    codigo_Produto = StringField("codigo_Produto",validators=[DataRequired()])
    cpf_cliente = StringField("cpf_cliente",validators=[DataRequired()])
    Quantidade = IntegerField("Quantidade",validators=[DataRequired()])