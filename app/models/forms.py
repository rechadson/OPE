from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired

class FornecedorForm(FlaskForm):
    cnpj = IntegerField("cnpj",validators=[DataRequired()])
    fornecedor = StringField("fornecedor",validators=[DataRequired()])
    email = StringField("email",validators=[DataRequired()])
    

class LoginForm(FlaskForm):
    username = StringField("username",validators=[DataRequired()])
    password = PasswordField("password",validators=[DataRequired()])

class ClienteForm(FlaskForm):
    name = StringField("nome",validators=[DataRequired()])
    cpf = StringField("cpf",validators=[DataRequired()])
    endereco = StringField("endereco",validators=[DataRequired()])

class ProdutoForm(FlaskForm):
    codigo = StringField("codigo",validators=[DataRequired()])
    Nome = StringField("Nome",validators=[DataRequired()])
    preco = StringField("preco",validators=[DataRequired()])

class OrcamentoForm(FlaskForm):
    nome_Produto = StringField("nome_Produto",validators=[DataRequired()])
    cpf_cliente = StringField("cpf_cliente",validators=[DataRequired()])
    