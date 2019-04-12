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
    nome = StringField("nome",validators=[DataRequired()])
    cpf = StringField("cpf",validators=[DataRequired()])
    telefone = StringField("telefone", validators=[DataRequired()])
    endereco = StringField("endereco",validators=[DataRequired()])

class ProdutoForm(FlaskForm):
    nome = StringField("nome",validators=[DataRequired()])
    preco = StringField("preco",validators=[DataRequired()])
    fornecedor = IntegerField("fornecedor_id",validators=[DataRequired()])

class OrcamentoForm(FlaskForm):
    codigo_Produto = StringField("codigo_Produto",validators=[DataRequired()])
    cpf_cliente = StringField("cpf_cliente",validators=[DataRequired()])
    