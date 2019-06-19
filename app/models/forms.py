from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired

class FornecedorForm(FlaskForm):
    cnpj = StringField("cnpj",validators=[DataRequired()])
    fornecedor = StringField("fornecedor",validators=[DataRequired()])
    email = StringField("email",validators=[DataRequired()])
    

class LoginForm(FlaskForm):
    username = StringField("username",validators=[DataRequired()])
    password = PasswordField("password",validators=[DataRequired()])

class ClienteForm(FlaskForm):
    nome = StringField("nome",validators=[DataRequired()])
    cpf = StringField("cpf",validators=[DataRequired()])
    telefone = StringField("telefone", validators=[DataRequired()])
    endereco = StringField("endereco",validators=[DataRequired()])

class ProdutoForm(FlaskForm):
    nome = StringField("nome",validators=[DataRequired()])
    preco = StringField("preco",validators=[DataRequired()])
    

